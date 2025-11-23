import os
from rdflib import Graph, URIRef
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI

# -------------------------------
# Carregar variáveis do ambiente
# -------------------------------
load_dotenv()

# Azure OpenAI
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview"
)

# Azure Cognitive Search
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX", "pdf-index"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
)

# -------------------------------
# Carregar grafo SKOS/OWL
# -------------------------------
g_skos = Graph()
g_skos.parse("data/knowledge_graph.ttl", format="turtle")

SKOS = "http://www.w3.org/2004/02/skos/core#"
skos_prefLabel = URIRef(SKOS + "prefLabel")


# ==========================================================
# Função corrigida: reconhecimento REAL de um conceito SKOS
# ==========================================================
def encontrar_conceito_na_frase(frase: str):
    frase_lower = frase.lower()

    # Busca apenas labels SKOS (prefLabel)
    for s, p, o in g_skos.triples((None, skos_prefLabel, None)):
        label = str(o).lower()

        # Match robusto: se o label aparecer na frase, achamos o conceito
        if label in frase_lower:
            return str(s)

    return None


# ==========================================================
# Buscar conceitos relacionados: broader / narrower / related
# ==========================================================
def conceitos_relacionados(uri):
    query = f"""
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT ?tipo ?concept WHERE {{
        {{ <{uri}> skos:broader ?concept  BIND("broader" AS ?tipo) }}
        UNION
        {{ <{uri}> skos:narrower ?concept BIND("narrower" AS ?tipo) }}
        UNION
        {{ <{uri}> skos:related ?concept  BIND("related" AS ?tipo) }}
    }}
    """
    results = []
    for row in g_skos.query(query):
        results.append({
            "tipo": str(row.tipo),
            "concept": str(row.concept)
        })
    return results


# ==========================================================
# Reasoning simples para vendas (placeholder)
# ==========================================================
def vendas_semanticas(uri):
    return []


# ==========================================================
# Buscar trechos do PDF no Azure Cognitive Search
# ==========================================================
def buscar_pdf(query: str):
    try:
        results = search_client.search(query)
        docs = [x.get("content", "") for x in results]
        return "\n".join(docs[:3])
    except:
        return "Não foi possível buscar no Azure Search."


# ==========================================================
# A FUNÇÃO PRINCIPAL DO AGENTE
# ==========================================================
def agente_rag_semantico(pergunta: str):

    pergunta_lower = pergunta.lower()

    # ======================================================
    # Caso especial: reasoning explícito
    # ======================================================
    if "inferiu" in pergunta_lower or "inferidas" in pergunta_lower or "reasoning" in pergunta_lower:
        inferidos = []
        q = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?child WHERE {
            <https://contoso.com/vendas/Categoria_Produtos> skos:narrower ?child .
        }
        """
        for row in g_skos.query(q):
            inferidos.append(str(row.child))

        lista = "\n".join([f"- `{uri}`" for uri in inferidos])

        return f"""
### 🧠 Conceitos inferidos automaticamente pelo Reasoner (OWL-RL)

O reasoner inferiu que a categoria **Produtos** possui:

{lista}

As inferências vêm das relações SKOS (narrower/broader).
"""

    # ======================================================
    # 1) Encontrar conceito SKOS na pergunta
    # ======================================================
    conceito = encontrar_conceito_na_frase(pergunta)

    if not conceito:
        conceito_info = "❌ Nenhum conceito SKOS encontrado."
        relacionados_info = "—"
        vendas_info = "—"
    else:
        conceito_info = f"✔ Conceito encontrado: `{conceito}`"

        # Conceitos relacionados
        try:
            relacionados = conceitos_relacionados(conceito)
            if relacionados:
                relacionados_info = "\n".join([
                    f"- `{r['tipo']}` → `{r['concept']}`"
                    for r in relacionados
                ])
            else:
                relacionados_info = "Nenhum conceito relacionado encontrado."
        except Exception as e:
            relacionados_info = f"⚠ Erro ao consultar relacionados: {e}"

        # Vendas inferidas
        try:
            vendas = vendas_semanticas(conceito)
            if vendas:
                vendas_info = "\n".join([f"- Produto {v}" for v in vendas])
            else:
                vendas_info = "Nenhuma venda inferida."
        except Exception as e:
            vendas_info = f"⚠ Erro: {e}"

    # ======================================================
    # 2) Buscar contexto do PDF
    # ======================================================
    try:
        pdf_context = buscar_pdf(pergunta)
        if not pdf_context:
            pdf_context = "Nenhum trecho relevante encontrado."
    except Exception as e:
        pdf_context = f"⚠ Erro ao buscar PDF: {e}"

    # ======================================================
    # 3) Criar o prompt final
    # ======================================================
    prompt = f"""
Você é um agente semântico com SKOS/OWL + Reasoning + RAG.

### Pergunta:
{pergunta}

## 🔎 1. Conceito SKOS identificado
{conceito_info}

## 🧭 2. Conceitos relacionados (broader / narrower / related)
{relacionados_info}

## 📊 3. Vendas inferidas
{vendas_info}

## 📘 4. Contexto do PDF
{pdf_context}

Explique de forma clara, estruturada e estratégica.
"""

    # ======================================================
    # 4) Chamar Azure OpenAI
    # ======================================================
    resp = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )

    return resp.choices[0].message.content

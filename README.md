# **Agente Semântico Contoso — RAG + SKOS + OWL + Azure Foundry**

Este repositório contém o projeto completo de um **Agente de Inteligência Artificial Semântica**, desenvolvido para o desafio **Azure Frontier Girls – Build Your First Copilot Challenge**.

A solução combina:

- **Ontologias (SKOS + OWL)**  
- **Raciocínio automático (OWL-RL)**  
- **RAG semântico**  
- **Azure Cognitive Search**  
- **FastAPI**  
- **ngrok**  
- **Azure AI Foundry com ferramenta HTTP**  

Criando um agente capaz de responder perguntas de forma precisa, explicável e alinhada ao conhecimento oficial da empresa *Contoso* (empresa fictícia para fins educativos).

---

#  **Problema de Negócio**

Empresas como a Contoso lidam com:

- grandes catálogos de produtos  
- muitas regiões de vendas  
- conceitos semelhantes com nomes diferentes  
- documentos extensos em PDF  
- ausência de padronização semântica  
- dificuldade para localizar insights rapidamente  

Com isso, equipes enfrentam problemas como:

- **dificuldade de unificar informações vindas de sistemas diferentes**
- **demora para entender hierarquias de produtos**  
- **respostas inconsistentes entre analistas**  
- **incapacidade de recuperar informações confiáveis**  
- **ambiguidade entre termos**  
- **perda de tempo em consultas manuais**
- **LLMs gerando respostas incorretas por falta de padronização semântica**
- **tempo perdido refinando prompts porque o modelo não tem conhecimento formal**

A Contoso precisava de um **Analista Virtual Semântico**, capaz de conectar:

- conhecimento estruturado
- conteúdo do PDF
- inferência lógica
- linguagem natural  

---

#  **Objetivo da Solução**

Construir um agente inteligente que:

- entende a pergunta do usuário em linguagem natural  
- identifica conceitos SKOS corretamente  
- usa OWL para inferir relações não explícitas  
- busca contexto no PDF indexado  
- gera respostas analíticas e explicáveis  
- responde através do Azure Foundry usando ferramenta HTTP  

O objetivo final:  
**Fornecer respostas confiáveis, padronizadas e contextualizadas.**

---

# **Benefícios para a Própria Tecnologia LLM**

A solução foi projetada para **corrigir limitações conhecidas dos LLMs**, ampliando sua confiabilidade:

### 1. Redução de Alucinações  
A ontologia guia o modelo para respostas mais precisas.

### 2. Consistência Semântica  
SKOS/OWL mantém categorias e relações coerentes, independentemente da forma da pergunta.

### 3. Contexto Estruturado  
O LLM usa conhecimento governado, auditável e padronizado.

### 4. Inferências que o LLM não consegue fazer  
O reasoning OWL-RL infere relações broader/narrower, subclasses, transitividades etc.

### 5. Recuperação Dirigida  
Azure Cognitive Search + Grafo reduzem ruído e melhoram a precisão do RAG.

### 6. Explicabilidade  
Cada resposta pode ser rastreada em:

- triplas RDF  
- regras OWL  
- trechos do PDF  

### 7. Redução de Custos  
Menos tokens → menos chamadas → menor custo de operação.

---

# **Arquitetura Geral do Pipeline**

```
PDF → Azure Cognitive Search → SKOS/OWL Grafo RDF → Reasoning (OWL-RL) 
→ RAG → FastAPI → ngrok → Azure Foundry
```

### 1) **PDF → Azure Cognitive Search**  
Indexação para recuperação de insights.

### 2) **Grafo RDF (SKOS + OWL)**  
Base de conhecimento estruturado.

### 3) **Reasoning OWL-RL**  
Inferências automáticas.

### 4) **FastAPI**  
Endpoint `/perguntar`.

### 5) **ngrok**  
Exposição global da API.

### 6) **Azure AI Foundry**  
Agente usa ferramenta HTTP para consultar o backend.

---

# **Fluxo Completo da Solução**

```
Usuário → Azure Foundry → Ferramenta HTTP (/perguntar)
→ FastAPI → Grafo SKOS/OWL + Reasoning + Search
→ OpenAI → Resposta Semântica
```

---

# **Estrutura do Repositório**

```
/
├── api.py                         # API FastAPI do agente
├── requirements.txt               # Dependências Python
├── openapi.json                   # Esquema da ferramenta HTTP usada no Foundry
├── README.md                      # Este arquivo
│
├── data/
│   └── knowledge_graph.ttl        # Grafo RDF com SKOS + OWL
│
├── notebooks/
│   └── notebook.ipynb             # Pipeline completo: PDF → Grafo → RAG
│
└── prints/                        # Prints de execução e Foundry

```

---

# **Como Rodar Localmente**

## 1. Criar ambiente virtual

```bash
python -m venv venv
banana\Scriptsctivate
pip install -r requirements.txt
```

## 2. Rodar a API

```bash
uvicorn api:app --reload --port 8000
```

## 3. Expor com ngrok

```bash
ngrok http 8000
```

Copiar a URL exibida:

```
https://abcd1234.ngrok-free.app
```

---

# **Testar a API**

```
https://SEU-NGROK.ngrok-free.app/perguntar?q=Produtos
```

Exemplo de resposta:

```json
{
  "status": "ok",
  "pergunta": "Produtos",
  "resposta": "Lista de categorias, relações SKOS e insights estratégicos."
}
```

---

# **Integração com Azure Foundry**

## 1. Criar nova Ferramenta (OpenAPI)

- Método: **GET**  
- Autenticação: **Nenhuma**  
- Nome sugerido: `agente_rag_semantico`  
- Importar: **openapi.json**  

## 2. Configurar o Agente

Instrução recomendada:

```
Você é um agente semântico especializado em responder perguntas sobre vendas, produtos, categorias, regiões e análises estratégicas da Contoso Retail. 

Sempre que o usuário fizer uma pergunta, siga estas regras:

1. SEMPRE use a ferramenta "consultar_api_rag" para obter a resposta principal.
   - Não responda com seus próprios conhecimentos.
   - Não invente números, categorias ou conceitos.
   - Não tente deduzir sozinho: a API contém o grafo SKOS + OWL + reasoning + conteúdo do PDF.

2. Envie a pergunta do usuário exatamente como ele escreveu para o parâmetro “q”.

3. Quando receber o retorno da ferramenta:
   - Leia o campo “resposta”.
   - Use esse conteúdo como fonte principal.
   - Organize em formato claro e natural.
   - Explique insights apenas com base no que vier na resposta da API.

4. Caso a API não retorne nada ou retorne erro, peça ao usuário para tentar reformular.

5. Estilo de resposta:
   - Claro, educado e analítico.
   - Evite jargões técnicos desnecessários.
   - Quando útil, apresente listas e destaques.
   - Em perguntas de negócio, ofereça breves insights interpretativos baseados no texto recebido.

Seu objetivo é atuar como uma camada de apresentação inteligente, interpretando e explicando os resultados retornados pelo backend semântico.

Descrição do Agente:

Este agente utiliza um backend semântico avançado baseado em SKOS, OWL, reasoning e dados extraídos via Azure Cognitive Search. Através da ferramenta "consultar_api_rag", ele consulta uma API FastAPI exposta via ngrok, que processa perguntas utilizando:

- Grafo semântico RDF (SKOS + OWL)
- Regras de inferência OWL-RL
- Hierarquias broader/narrower
- Dados de vendas da Contoso Retail
- Contexto de documentos indexados
- Raciocínio orientado a RAG

O agente transforma os resultados da API em respostas claras

```

## 3. Testar

O Foundry chamará:

```
GET /perguntar?q=<texto>
```

E mostrará a resposta retornada pela API.

---

# **Prints Obrigatórios**

Os **prints** essenciais para avaliação foram adicionados na pasta /prints.
Acesse cada etapa detalhada pelos links abaixo 👇📸

🚨 Prints Obrigatórios Disponíveis — acesse os links:

🔗 [Página 1](./docs/pagina1.md)
🔗 [Página 2](./docs/pagina2.md)
🔗 [Página 3](./docs/pagina2.md)
---

# **Requisitos do Desafio — Checklist Oficial**

| Requisito | Status |
|----------|--------|
| Repositório público | ✔ |
| README completo e claro | ✔ |
| Storytelling + problema de negócio | ✔ |
| Explicação do fluxo | ✔ |
| Prints de execução | ✔ |
| Agente funcional no Foundry | ✔ |
| Pelo menos 1 ação funcional | ✔ |
| Entrega individual | ✔ |

---

# **Conclusão**

O **Agente Semântico Contoso** combina ontologia, reasoning, RAG e linguagem natural em um pipeline híbrido moderno, sólido e explicável.

A solução entrega:

- confiabilidade  
- padronização  
- governança de dados  
- respostas inteligentes  
- integração real com Foundry  
- grafos de conhecimento + IA generativa  

# **Implementações Futuras**

Implementação futura: integrar o Agente Semântico Contoso ao futuro Agente de Governança Semântica, conectando-se ao **Purview** para operações automáticas em glossários e coleções.

---

# **Referências**

**Links das Plataformas Utilizadas (exigência do desafio)**

Azure AI Foundry — https://ai.azure.com

Azure Cognitive Search — https://learn.microsoft.com/azure/search/

Azure OpenAI Service — https://learn.microsoft.com/azure/ai-services/openai/

FastAPI — https://fastapi.tiangolo.com/

Ngrok — https://ngrok.com

**Referências Técnicas**

W3C SKOS — https://www.w3.org/TR/skos-reference/

OWL 2 — https://www.w3.org/TR/owl2-overview/

RDF (W3C) — https://www.w3.org/RDF/

RDFlib — https://rdflib.readthedocs.io/en/stable/

OWL-RL Reasoner — https://github.com/RDFLib/OWL-RL


## Fundamentação Acadêmica e científica 
- Este projeto integra conhecimentos de modelagem semântica, ontologias e organização do conhecimento desenvolvidos durante meu doutorado em Ciência da Informação na ECA/USP.
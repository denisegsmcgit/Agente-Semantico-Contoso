#!/bin/bash
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000

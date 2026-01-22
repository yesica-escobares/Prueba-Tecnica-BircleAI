# RAG API — FastAPI + LlamaIndex

API REST para **Retrieval-Augmented Generation (RAG)** construida con **FastAPI** y **LlamaIndex**, que permite ingestar documentos, indexarlos en un vector store persistente y responder consultas devolviendo **respuestas con fuentes citadas**.

Este proyecto fue desarrollado como parte de una **prueba técnica**, priorizando claridad de diseño, buenas prácticas de backend y operación.

---

## Features

- Ingesta de documentos (`.txt`, `.pdf`)
- Indexación vectorial persistente (Qdrant local)
- Consultas RAG con:
  - Respuesta generada
  - Fuentes citadas (chunks + metadata)
  - Parámetros de recuperación (`top_k`, filtros)
- Streaming de respuestas vía **Server-Sent Events (SSE)** *(bonus)*
- Seguridad mínima mediante **API Key**
- Rate limiting por IP *(bonus)*
- Endpoints de operación: `/health` y `/stats`
- Logs estructurados en JSON con `request_id`
- Configuración completa por variables de entorno
- Suite mínima de tests automatizados (pytest)

---

## Arquitectura


---

## Configuración

Toda la configuración se realiza mediante variables de entorno.

---

## Modelos

Se utiliza Google Gemini como proveedor de LLM y embeddings, aprovechando su free tier.

- LLM: gemini-2.5-flash
- Embeddings: embedding-001

El sistema está desacoplado del proveedor, por lo que puede adaptarse fácilmente a OpenAI u Ollama.

---

## Ingesta de documentos

### Ingesta automática

Al iniciar la aplicación, se ingesta automáticamente cualquier archivo .txt o .pdf presente en el directorio data/.

### Endpoint manual

POST /ingest

- Protegido por API Key
- Soporta múltiples archivos (multipart/form-data)

Ejemplo:

```bash
curl -X POST http://localhost:8000/ingest \
  -H "X-API-Key: super-secret-api-key" \
  -F "files=@example.pdf"
```

Respuesta:
```json
{
  "ingested": 1,
  "skipped": 0,
  "errors": []
}
``` 

---

## Consulta RAG

Si no se encuentra información relevante, el endpoint responde con HTTP 200 y un mensaje explícito, evitando alucinaciones.

---

## Seguridad

- Autenticación mediante API Key (X-API-Key)
- Rate limiting por IP 
- No se loguea contenido sensible (documentos, prompts, keys)

---

## Logging

- Logs estructurados en formato JSON
- Incluyen request_id para trazabilidad
- Nivel INFO por defecto

Ejemplo:

```json
{
  "request_id": "uuid",
  "method": "POST",
  "path": "/query",
  "status_code": 200,
  "duration_ms": 312.5
}
```

---

## Tests

Suite mínima implementada con pytest:

- /health
- /ingest
- /query

Para ejecutarlo:

```bash
pytest -v
``` 

---

## Ejecución local

1. Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias

```bash
pip install -r requirements.txt
```

3. Ejecutar la API

```bash
uvicorn app.main:app --reload
```
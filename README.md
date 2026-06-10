# Juris Scraper

Async pipeline for collecting and centralizing legal process data from the TJBA (Tribunal de Justiça da Bahia). Accepts a list of CNJ numbers, queries multiple external sources in parallel, normalizes the results into a canonical schema, and persists everything in a relational database.

---

## What it does

Given an array of CNJ numbers, the system:

1. Queries **DataJud** (CNJ's public ElasticSearch API) — returns rich metadata: class, grade, subjects, movements with judging body
2. Queries the **TJBA Consulta Processual API** — returns parties, lawyers, action value, district
3. **Merges** both results following a strict rule: never overwrite a populated field with null
4. Persists via **upsert** — existing records are updated, never duplicated

Everything runs asynchronously with `asyncio.gather` and a semaphore controlling max concurrency.

---

## Stack

| Technology | Why |
|---|---|
| **Python 3.12** | Modern typing with `Mapped` and native type hints |
| **FastAPI** | Native async performance, automatic Swagger docs |
| **SQLAlchemy 2.0 async** | ORM with `AsyncSession` — non-blocking event loop |
| **asyncpg** | Native async PostgreSQL driver |
| **Alembic** | Versioned and reversible migrations |
| **PostgreSQL** | `JSONB` support for storing raw source responses |
| **httpx** | Async HTTP client for external API calls |
| **Docker + Compose** | Reproducible environment with database healthcheck |

---

## Architecture

```
POST /lawsuits/  (array of CNJ numbers)
        │
        ▼
   CollectService
        │
        ├──► DatajudScraper.collect(cnj)               ─┐
        │         └── fetch → normalize                 ├── asyncio.gather
        ├──► ConsultaProcessualScraper.collect(cnj)    ─┘
        │         └── fetch → normalize
        │
        ▼
   merge(data1, data2)
        │
        ▼
   LawsuitRepository.upsert()
        │
        ▼
   PostgreSQL
```

### Design patterns

**Abstract BaseScraper** — defines the `fetch` + `normalize` + `collect` contract. Each source inherits and implements its own parsing logic without touching the pipeline.

**Repository Pattern** — `SqlAlchemyLawsuitRepository` isolates all database access. The service layer doesn't know SQL; the scraper layer doesn't know the database exists.

**Parallel merge with source authority** — both sources run in parallel. The merge respects one rule: the first value to arrive wins, no source overwrites another.

**Smart upsert** — separates `SCALAR_FIELDS` from relationships. Scalar fields only update if the current value is `None`. Child records (parties, movements, subjects) are replaced in batch via cascade.

---

## Database schema

```
tribunals       — court of origin
lawsuits        — process (CNJ as PK)
  ├── subjects      — case subjects (N)
  ├── participants  — parties and lawyers (N)
  ├── movements     — case movements (N)
  ├── petitions     — petitions (N)
  ├── incidents     — incidents (N)
  └── hearings      — hearings (N)
```

All fields are nullable — a process is saved partially on first collection and enriched progressively by each source. The `raw` field stores the original source response as `JSONB` for auditing.

---

## Getting started

### Prerequisites

- Docker and Docker Compose

### Setup

```bash
git clone https://github.com/thiagosampaiog/juris-scraper
cd juris-scraper
cp .env.example .env
docker-compose up --build
```

API available at `http://localhost:8000`  
Swagger docs at `http://localhost:8000/docs`

### Endpoints

```
POST /lawsuits/          — collect one or more processes by CNJ
GET  /lawsuits/          — list processes with pagination
GET  /lawsuits/{cnj}     — process detail with all related records
```

### Example

```bash
curl -X POST http://localhost:8000/lawsuits/ \
  -H "Content-Type: application/json" \
  -d '{"cnjs": ["80041445420258050141", "80007794920188050072"]}'
```

---

## What I would add with more time

**Third source via eSAJ + Discord Bot** — the eSAJ (TJBA's service portal) requires captcha. The plan was to use Playwright to open the browser, capture a captcha screenshot, send it to a Discord channel, and wait for a human response via `asyncio.Event`. This would unlock exclusive eSAJ data: action value, area, petitions, incidents, and hearings.

**Job queue with ARQ + Redis** — each CNJ would become an independent worker with automatic retry, DLQ for persistent failures, and status polling via `GET /jobs/{id}`.

**Per-source rate limiting** — the current semaphore is global. The ideal would be a semaphore per source with configurable delays via `.env` to respect each API's limits.

---

## Author

Thiago Sampaio — [LinkedIn](https://linkedin.com/in/thiago-sampaiog) · [GitHub](https://github.com/thiagosampaiog)
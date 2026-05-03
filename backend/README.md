# Backend (FastAPI)

## Setup

1. Create and activate virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy env file:

```bash
copy .env.example .env
```

If your `.env` already exists, ensure:
`DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/ebook2latex_db`

4. Run migrations:

```bash
alembic upgrade head
```

5. Start API:

```bash
uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/docs`

## Docker (Backend + PostgreSQL)

From project root:

```bash
docker compose up --build
```

Backend container automatically waits for DB and runs `alembic upgrade head` before starting API.

If you installed `psycopg2-binary` before, refresh deps:

```bash
pip uninstall -y psycopg2-binary
pip install -r requirements.txt
```

## Key endpoints

- `POST /api/v1/documents/upload` - Upload PDF and extract formula-like LaTeX lines
- `GET /api/v1/documents/{document_id}/formulas` - List formulas
- `PUT /api/v1/formulas/{formula_id}` - Update one formula
- `POST /api/v1/documents/{document_id}/submit` - Submit edited formulas

## Seed sample data

```bash
python -m scripts.seed
python -m scripts.seed_from_json
```

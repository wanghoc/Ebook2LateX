# Ebook2LateX

Web app to process math ebook PDFs, edit LaTeX with a two-way MathLive editor, and submit formulas to PostgreSQL.

## Stack

- Backend: FastAPI + SQLAlchemy + Alembic
- Frontend: React (Vite) + MathLive
- Database: PostgreSQL
- Orchestration: Docker Compose

## Run with Docker

```bash
docker compose up --build
```

Command above now starts **only backend + database**.

Services:

- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

If you also want frontend in Docker:

```bash
docker compose --profile frontend up --build
```

## Run locally

1. Backend:
   - `cd backend`
   - `pip install -r requirements.txt`
   - `copy .env.example .env`
   - Ensure `.env` has `DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/ebook2latex_db`
   - `alembic upgrade head`
   - `uvicorn app.main:app --reload`
2. Frontend:
   - `cd frontend`
   - `npm install`
   - `copy .env.example .env`
   - `npm run dev`

## Notes for Python 3.14

If you previously installed `psycopg2-binary`, refresh backend deps once:

- `cd backend`
- `pip uninstall -y psycopg2-binary`
- `pip install -r requirements.txt`

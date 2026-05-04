#!/bin/sh
set -e

echo "[backend] Waiting for database..."
python - <<'PY'
import os
import time
from sqlalchemy import create_engine, text

url = os.environ["DATABASE_URL"]
last_error = None

for attempt in range(1, 31):
    try:
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("[backend] Database is ready.")
        break
    except Exception as exc:
        last_error = exc
        print(f"[backend] Attempt {attempt}/30 failed, retrying in 2s...")
        time.sleep(2)
else:
    raise SystemExit(f"[backend] Database is not ready: {last_error}")
PY

echo "[backend] Running migrations..."
alembic upgrade head

echo "[backend] Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

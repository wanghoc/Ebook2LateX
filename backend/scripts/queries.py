from sqlalchemy import func
from pathlib import Path
import sys

# Allow running this file directly: `python scripts/queries.py`.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.database import SessionLocal
from app.models.entities import Document, FormulaEntry, User


def report_documents_by_user() -> None:
    # Aggregate report to see how many documents each user owns.
    db = SessionLocal()
    try:
        rows = (
            db.query(User.full_name, func.count(Document.id))
            .outerjoin(Document, Document.user_id == User.user_id)
            .group_by(User.user_id)
            .all()
        )
        print("--- Documents by user ---")
        for full_name, count in rows:
            print(f"{full_name}: {count}")
    finally:
        db.close()


def search_formula(keyword: str) -> None:
    # Basic full-text like query on latex_content.
    db = SessionLocal()
    try:
        rows = db.query(FormulaEntry).filter(FormulaEntry.latex_content.ilike(f"%{keyword}%")).all()
        print(f"--- Search keyword: {keyword} ---")
        for row in rows:
            print(f"{row.id}: {row.latex_content}")
    finally:
        db.close()


if __name__ == "__main__":
    report_documents_by_user()
    search_formula("sqrt")

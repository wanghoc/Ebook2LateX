import json
import uuid
from pathlib import Path
import sys

# Allow running this file directly: `python scripts/seed_from_json.py`.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.database import SessionLocal
from app.models.entities import Document, FormulaEntry


def seed_from_json() -> None:
    db = SessionLocal()
    try:
        document = db.query(Document).first()
        if document is None:
            print("No document found. Run `python -m scripts.seed` first.")
            return

        # Resolve data file relative to this script so command works from any CWD.
        data_file = Path(__file__).resolve().parent / "data" / "formulas.json"
        with data_file.open("r", encoding="utf-8") as file:
            items = json.load(file)

        for item in items:
            db.add(
                FormulaEntry(
                    id=uuid.uuid4(),
                    document_id=document.id,
                    latex_content=item["latex_content"],
                    order_index=item["order_index"],
                )
            )

        db.commit()
        print("Imported formulas from scripts/data/formulas.json.")
    except Exception as exc:
        db.rollback()
        print(f"Seed from json failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_from_json()

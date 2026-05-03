import uuid
from pathlib import Path
import sys

# Allow running this file directly: `python scripts/seed.py`.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.database import SessionLocal
from app.models.entities import Document, FormulaEntry, User


def seed_data() -> None:
    # Seed one user, one document and one sample formula for quick local demo.
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username_email == "admin@ebook2latex.local").first()
        if existing_user is None:
            existing_user = User(
                user_id=uuid.uuid4(),
                username_email="admin@ebook2latex.local",
                password_hash="hashed_password_here",
                full_name="Ebook2LateX Admin",
                role="Admin",
            )
            db.add(existing_user)
            db.flush()

        document = Document(
            id=uuid.uuid4(),
            user_id=existing_user.user_id,
            file_name="sample_math.pdf",
            file_path_url="uploads/sample_math.pdf",
            status="Completed",
        )
        db.add(document)
        db.flush()

        db.add(
            FormulaEntry(
                id=uuid.uuid4(),
                document_id=document.id,
                latex_content=r"\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
                order_index=1,
            )
        )

        db.commit()
        print("Seed data created successfully.")
    except Exception as exc:
        db.rollback()
        print(f"Seed failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()

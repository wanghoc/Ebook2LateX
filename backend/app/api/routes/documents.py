import shutil
import uuid
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.core.config import settings
from app.models.entities import Document, FormulaEntry
from app.schemas.formula import DocumentSubmitRequest, DocumentSubmitResponse, DocumentUploadResponse, FormulaOut
from app.services.pdf_formula_service import extract_latex_from_pdf

router = APIRouter(prefix="/documents", tags=["documents"])


def _ensure_uploads_dir() -> Path:
    uploads_dir = Path(settings.uploads_dir)
    uploads_dir.mkdir(parents=True, exist_ok=True)
    return uploads_dir


@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db_session),
) -> DocumentUploadResponse:
    # Validate input early to avoid storing unsupported files.
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are supported.")

    uploads_dir = _ensure_uploads_dir()
    safe_name = file.filename.replace(" ", "_")
    stored_name = f"{uuid.uuid4()}_{safe_name}"
    stored_path = uploads_dir / stored_name

    try:
        # Save the uploaded file first, then parse and persist extracted formulas.
        with stored_path.open("wb") as out:
            shutil.copyfileobj(file.file, out)

        document = Document(
            id=uuid.uuid4(),
            file_name=file.filename,
            file_path_url=str(stored_path),
            status="Processed",
        )
        db.add(document)
        db.flush()

        extracted_formulas = extract_latex_from_pdf(stored_path)
        for index, candidate in enumerate(extracted_formulas, start=1):
            db.add(
                FormulaEntry(
                    id=uuid.uuid4(),
                    document_id=document.id,
                    raw_image_path=None,
                    latex_content=candidate.latex_content,
                    order_index=index,
                )
            )

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        file.file.close()

    formulas = (
        db.query(FormulaEntry)
        .filter(FormulaEntry.document_id == document.id)
        .order_by(FormulaEntry.order_index.asc())
        .all()
    )

    return DocumentUploadResponse(
        document_id=document.id,
        file_name=document.file_name,
        formula_count=len(formulas),
        formulas=[
            FormulaOut(
                id=item.id,
                document_id=item.document_id,
                latex_content=item.latex_content,
                order_index=item.order_index,
                confidence_score=extracted_formulas[item.order_index - 1].confidence_score
                if item.order_index - 1 < len(extracted_formulas)
                else None,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in formulas
        ],
    )


@router.get("/{document_id}/formulas", response_model=list[FormulaOut])
def list_document_formulas(
    document_id: UUID,
    db: Session = Depends(get_db_session),
) -> list[FormulaOut]:
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    formulas = (
        db.query(FormulaEntry)
        .filter(FormulaEntry.document_id == document_id)
        .order_by(FormulaEntry.order_index.asc())
        .all()
    )
    return [FormulaOut.model_validate(item) for item in formulas]


@router.post("/{document_id}/submit", response_model=DocumentSubmitResponse)
def submit_document_formulas(
    document_id: UUID,
    payload: DocumentSubmitRequest,
    db: Session = Depends(get_db_session),
) -> DocumentSubmitResponse:
    # Apply all edited formulas in a single DB transaction.
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    formulas = (
        db.query(FormulaEntry)
        .filter(FormulaEntry.document_id == document_id)
        .order_by(FormulaEntry.order_index.asc())
        .all()
    )
    formula_map = {item.id: item for item in formulas}

    for incoming in payload.formulas:
        target = formula_map.get(incoming.id)
        if target is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Formula not found in this document: {incoming.id}",
            )
        target.latex_content = incoming.latex_content

    document.status = "Completed"
    db.commit()

    return DocumentSubmitResponse(
        document_id=document.id,
        updated_count=len(payload.formulas),
        status=document.status,
    )

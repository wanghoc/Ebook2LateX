from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.models.entities import FormulaEntry
from app.schemas.formula import FormulaOut, FormulaUpdateRequest

router = APIRouter(prefix="/formulas", tags=["formulas"])


@router.put("/{formula_id}", response_model=FormulaOut)
def update_formula(
    formula_id: UUID,
    payload: FormulaUpdateRequest,
    db: Session = Depends(get_db_session),
) -> FormulaOut:
    # Single-formula update endpoint used for quick inline edits from frontend.
    formula = db.query(FormulaEntry).filter(FormulaEntry.id == formula_id).first()
    if formula is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formula not found.")

    formula.latex_content = payload.latex_content
    db.commit()
    db.refresh(formula)
    return FormulaOut.model_validate(formula)

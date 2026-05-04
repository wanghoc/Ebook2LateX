from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class FormulaOut(BaseModel):
    id: UUID
    document_id: UUID
    latex_content: str | None
    order_index: int
    confidence_score: float | None = None
    created_at: datetime | None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class DocumentUploadResponse(BaseModel):
    document_id: UUID
    file_name: str
    formula_count: int
    formulas: list[FormulaOut]


class FormulaUpdateRequest(BaseModel):
    latex_content: str = Field(..., min_length=1)


class DocumentSubmitFormula(BaseModel):
    id: UUID
    latex_content: str = Field(..., min_length=1)


class DocumentSubmitRequest(BaseModel):
    formulas: list[DocumentSubmitFormula] = Field(default_factory=list)


class DocumentSubmitResponse(BaseModel):
    document_id: UUID
    updated_count: int
    status: str

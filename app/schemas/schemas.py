from pydantic import BaseModel, field_validator
from typing import Optional
from app.models.models import ParticipantType, SourceType
from datetime import datetime


class CollectInput(BaseModel):
    cnjs: list[str]


@field_validator("cnjs")
@classmethod
def validate_cnjs(cls, value):
    for cnj in value:
        digits_only = cnj.replace(".", "").replace("-", "")
        if not digits_only.isdigit() or len(digits_only) != 20:
            raise ValueError(f"{cnj}: CNJ deve ter 20 dígitos numéricos")
    return value


class TribunalResponse(BaseModel):
    id: int
    name: str
    abbreviation: str

    model_config = {"from_attributes": True}


class SubjectResponse(BaseModel):
    id: int
    name: Optional[str]
    code: Optional[str]

    model_config = {"from_attributes": True}


class ParticipantResponse(BaseModel):
    id: int
    name: Optional[str]
    lawyer_name: Optional[str]
    type_: Optional[ParticipantType]
    cpf_cnpj: Optional[str]

    model_config = {"from_attributes": True}


class MovementResponse(BaseModel):
    id: int
    code: Optional[str]
    description: Optional[str]
    occurred_at: Optional[datetime]

    model_config = {"from_attributes": True}


class PetitionResponse(BaseModel):
    id: int
    type_: Optional[ParticipantType]
    occurred_at: Optional[datetime]

    model_config = {"from_attributes": True}


class IncidentResponse(BaseModel):
    id: int
    description: Optional[str]
    occurred_at: Optional[datetime]

    model_config = {"from_attributes": True}


class HearingResponse(BaseModel):
    id: int
    type_: Optional[ParticipantType]
    occurred_at: Optional[datetime]

    model_config = {"from_attributes": True}


class LawsuitResponse(BaseModel):
    id: int
    class_: Optional[str]
    area: Optional[str]
    court: Optional[str]
    grade: Optional[str]
    subject: Optional[str]
    district: Optional[str]
    control: Optional[str]
    action_value: Optional[float]
    status: Optional[str]
    raw: Optional[str]
    source: Optional[str]
    distributed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    subjects: list[SubjectResponse] = []
    participants: list[ParticipantResponse] = []
    movements: list[MovementResponse] = []
    petitions: list[PetitionResponse] = []
    incidents: list[IncidentResponse] = []
    hearings: list[HearingResponse] = []

    model_config = {"from_attributes": True}

class PaginatedLawsuitsResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[LawsuitResponse]
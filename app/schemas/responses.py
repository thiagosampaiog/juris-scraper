from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, Field

from app.models.models import ParticipantType, SourceType



class TribunalResponse(BaseModel):
    id: int
    name: str
    abbreviation: str

    model_config = {"from_attributes": True}


class SubjectResponse(BaseModel):
    id: int
    name: Optional[str]
    code: Optional[int]

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
    code: Optional[int]
    description: Optional[str]
    occurred_at: Optional[datetime]

    model_config = {"from_attributes": True}


class PetitionResponse(BaseModel):
    id: int
    type_: Optional[str]
    occurred_at: Optional[datetime]

    model_config = {"from_attributes": True}


class IncidentResponse(BaseModel):
    id: int
    description: Optional[str]
    occurred_at: Optional[datetime]

    model_config = {"from_attributes": True}


class HearingResponse(BaseModel):
    id: int
    type_: Optional[str]
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
    action_value: Optional[Decimal]
    status: Optional[str]
    raw: Optional[dict[str, Any]]
    source: Optional[SourceType]
    distributed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    subjects: list[SubjectResponse] = Field(default_factory=list)
    participants: list[ParticipantResponse] = Field(default_factory=list)
    movements: list[MovementResponse] = Field(default_factory=list)
    petitions: list[PetitionResponse] = Field(default_factory=list)
    incidents: list[IncidentResponse] = Field(default_factory=list)
    hearings: list[HearingResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}

class PaginatedLawsuitsResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[LawsuitResponse]
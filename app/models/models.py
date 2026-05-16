import enum
from app.core.database import Base
from typing import Optional
from sqlalchemy import ForeignKey, String, Integer, Numeric, Text, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timezone


class ParticipantType(enum.Enum):
    author = "author"
    defendant = "defendant"
    third_party = "third_party"

class SourceType(enum.Enum):
    consulta_processual = "consulta_processual"
    datajud = "datajud"
    esaj = "esaj"

class Tribunal(Base):
    __tablename__ = "tribunals"
    
    id:              Mapped[int] = mapped_column(Integer, primary_key=True)
    name:            Mapped[str] = mapped_column(String, nullable=False)
    abbreviation:    Mapped[str] = mapped_column(String, nullable=False, unique=True)
    
    lawsuits:        Mapped[list["Lawsuit"]] = relationship(back_populates="tribunal")
    
class Lawsuit(Base):
    __tablename__ = "lawsuits"
    
    id:              Mapped[str]                = mapped_column(String, primary_key=True)
    tribunal_id:     Mapped[int]                = mapped_column(ForeignKey("tribunals.id"), nullable=False)
    
    class_:          Mapped[Optional[str]]      = mapped_column("class", String, nullable=True)
    area:            Mapped[Optional[str]]      = mapped_column(String, nullable=True)
    court:           Mapped[Optional[str]]      = mapped_column(String, nullable=True)
    grade:           Mapped[Optional[str]]      = mapped_column(String(5), nullable=True)
    subject:         Mapped[Optional[str]]        = mapped_column(String, nullable=True)
    district:        Mapped[Optional[str]]        = mapped_column(String, nullable=True)
    control:         Mapped[Optional[str]]       = mapped_column(String, nullable=True)
    action_value:    Mapped[Optional[float]]    = mapped_column(Numeric(15, 2), nullable=True)
    status:          Mapped[Optional[str]]        = mapped_column(String(50), nullable=True)
    raw:             Mapped[Optional[dict]]        = mapped_column(JSONB, nullable=True)
    source:          Mapped[Optional[SourceType]] = mapped_column(Enum(SourceType), nullable=True)
    distributed_at:  Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at:      Mapped[datetime]            = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at:      Mapped[datetime]            = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    tribunal:        Mapped["Tribunal"]          = relationship(back_populates="lawsuits")
    subjects:        Mapped[list["Subject"]]     = relationship(back_populates="lawsuit", cascade="all, delete-orphan")
    participants:    Mapped[list["Participant"]] = relationship(back_populates="lawsuit", cascade="all, delete-orphan")
    movements:       Mapped[list["Movement"]]    = relationship(back_populates="lawsuit", cascade="all, delete-orphan")
    petitions:       Mapped[list["Petition"]]    = relationship(back_populates="lawsuit", cascade="all, delete-orphan")
    incidents:       Mapped[list["Incident"]]    = relationship(back_populates="lawsuit", cascade="all, delete-orphan")
    hearings:        Mapped[list["Hearing"]]      = relationship(back_populates="lawsuit", cascade="all, delete-orphan")

class Subject(Base):
    __tablename__=  'subjects'

    id:              Mapped[int]                  = mapped_column(Integer, primary_key=True)
    lawsuit_id:      Mapped[str]                  = mapped_column(ForeignKey("lawsuits.id"), nullable=False)
    code:            Mapped[Optional[int]]       = mapped_column(Integer, nullable=True)
    name:            Mapped[Optional[str]]       = mapped_column(String, nullable=True)
    
    lawsuit:         Mapped["Lawsuit"]           = relationship(back_populates="subjects")

class Participant(Base):
    __tablename__ = "participants"
    
    id:             Mapped[int]                 = mapped_column(Integer, primary_key=True)
    lawsuit_id:     Mapped[str]                  = mapped_column(ForeignKey("lawsuits.id"), nullable=False)
    
    name:          Mapped[Optional[str]]       = mapped_column(String(200), nullable=True)
    lawyer_name:    Mapped[Optional[str]]       = mapped_column(String(200), nullable=True)
    type_:          Mapped[Optional[ParticipantType]]  = mapped_column("type", Enum(ParticipantType), nullable=True)
    cpf_cnpj:       Mapped[Optional[str]]       = mapped_column(String(20), nullable=True)
    
    lawsuit:       Mapped["Lawsuit"]           = relationship(back_populates="participants")
    
class Movement(Base):
    __tablename__ = "movements"

    id:              Mapped[int]                 = mapped_column(Integer, primary_key=True)
    lawsuit_id:      Mapped[str]                 = mapped_column(ForeignKey("lawsuits.id"), nullable=False)
    
    code:            Mapped[Optional[int]]         = mapped_column(Integer, nullable=True)
    description:     Mapped[Optional[str]]         = mapped_column(Text, nullable=True)
    occurred_at:     Mapped[Optional[datetime]]   = mapped_column(DateTime(timezone=True), nullable=True)
    
    lawsuit :      Mapped["Lawsuit"]              = relationship(back_populates="movements")
    
class Petition(Base):
    __tablename__ = "petitions"
    
    id:               Mapped[int]                  = mapped_column(Integer, primary_key=True)
    lawsuit_id:      Mapped[str]                  = mapped_column(ForeignKey("lawsuits.id"), nullable=False)
    
    type_:           Mapped[Optional[str]]                  = mapped_column("type", String(100), nullable=True)
    occurred_at:      Mapped[Optional[datetime]]             = mapped_column(DateTime(timezone=True), nullable=True)
    
    lawsuit :        Mapped["Lawsuit"]            = relationship(back_populates="petitions")

class Incident(Base):
    __tablename__ = "incidents"
    
    id:               Mapped[int]                    = mapped_column(Integer, primary_key=True)
    lawsuit_id:       Mapped[str]                    = mapped_column(ForeignKey("lawsuits.id"), nullable=False)
    
    description:      Mapped[Optional[str]]          = mapped_column(Text, nullable=True)
    occurred_at:      Mapped[Optional[datetime]]     = mapped_column(DateTime(timezone=True), nullable=True)
    
    lawsuit :         Mapped["Lawsuit"]              = relationship(back_populates="incidents")
    
class Hearing(Base):
    __tablename__ = "hearings"
    
    id:                Mapped[int]                    = mapped_column(Integer, primary_key=True)
    lawsuit_id:        Mapped[str]                    = mapped_column(ForeignKey("lawsuits.id"), nullable=False)
    
    type_:             Mapped[Optional[str]]            = mapped_column("type", String, nullable=True)
    occurred_at:       Mapped[Optional[datetime]]       = mapped_column(DateTime(timezone=True), nullable=True)
    
    lawsuit :         Mapped["Lawsuit"]          = relationship(back_populates="hearings")
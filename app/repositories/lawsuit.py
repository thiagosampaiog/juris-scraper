from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Lawsuit, Movement, Hearing, Incident, Participant, Petition, Subject
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.schemas.responses import PaginatedLawsuitsResponse, LawsuitResponse
from sqlalchemy import func
from app.scrapers.datajud import DatajudScraper


class SqlAlchemyLawsuitRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_cnj(self, cnj: str) -> Lawsuit | None:
        stmt = (
            select(Lawsuit)
            .where(Lawsuit.id == cnj)
            .options(
                selectinload(Lawsuit.subjects),
                selectinload(Lawsuit.participants),
                selectinload(Lawsuit.movements),
                selectinload(Lawsuit.petitions),
                selectinload(Lawsuit.incidents),
                selectinload(Lawsuit.hearings),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def getAll(
        self, limit: int = 20, offset: int = 0
    ) -> PaginatedLawsuitsResponse:
        stmt = (
            select(Lawsuit)
            .options(
                selectinload(Lawsuit.subjects),
                selectinload(Lawsuit.participants),
                selectinload(Lawsuit.movements),
                selectinload(Lawsuit.petitions),
                selectinload(Lawsuit.incidents),
                selectinload(Lawsuit.hearings),
            )
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        count_stmt = select(func.count()).select_from(Lawsuit)
        total = await self.session.scalar(count_stmt) or 0

        return PaginatedLawsuitsResponse(
            total=int(total), limit=limit, offset=offset, items=[LawsuitResponse.model_validate(i) for i in items],
        )
    
    async def upsert(self, cnj: str, data: dict, tribunal_id: int) -> Lawsuit | None:
        SCALAR_FIELDS = {
            "class_", "area", "court", "grade", "subject",
            "district", "control", "action_value", "status",
            "source", "distributed_at", "raw"
        }

        existing = await self.get_by_cnj(cnj)

        if existing is None:
            lawsuit = Lawsuit(
                id=cnj,
                tribunal_id=tribunal_id,
                **{k: data.get(k) for k in SCALAR_FIELDS},
                movements=[
                    Movement(**m) for m in data.get("movements", [])
                ],
                subjects=[
                    Subject(**s) for s in data.get("subjects", [])
                ],
                participants=[
                    Participant(**p) for p in data.get("participants", [])
                ],
                petitions=[
                    Petition(**pet) for pet in data.get("petitions", [])
                ],
                hearings=[
                    Hearing(**h) for h in data.get("hearings", [])
                ],
                incidents=[
                    Incident(**i) for i in data.get("incidents", [])
                ]
            )
            self.session.add(lawsuit)
            await self.session.commit()
            await self.session.refresh(lawsuit)
            return await self.get_by_cnj(cnj)
        else:
            for field in SCALAR_FIELDS:
              value = data.get(field)
              if value is not None:
                setattr(existing, field, value)
            await self.session.commit()
            return existing
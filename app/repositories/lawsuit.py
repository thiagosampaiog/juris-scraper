from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Lawsuit
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.schemas.schemas import PaginatedLawsuitsResponse
from sqlalchemy import func


class SqlAlchemyLawsuitRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_cnj(self, cnj: str) -> Lawsuit:
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
        total = await self.session.scalar(count_stmt)

        return {"total": total, "limit": limit, "offset": offset, "items": items}

    async def upsert(self, cnj: str, data: dict, tribunal_id: int) -> Lawsuit:
        existing = await self.get_by_cnj(cnj)

        if existing is None:
            lawsuit = Lawsuit(
                id=cnj,
                tribunal_id=tribunal_id,
                class_=data.get("class_"),
                area=data.get("area"),
                court=data.get("court"),
                grade=data.get("grade"),
                subject=data.get("subject"),
                district=data.get("district"),
                control=data.get("control"),
                action_value=data.get("action_value"),
                status=data.get("status"),
                source=data.get("source"),
                distributed_at=data.get("distributed_at"),
                raw=data.get("raw"),
            )
            self.session.add(lawsuit)
            await self.session.commit()
            await self.session.refresh(lawsuit)
            return lawsuit
        else:
            for field, value in data.items():
                if value is not None:
                    setattr(existing, field, value)
            await self.session.commit()
            return existing

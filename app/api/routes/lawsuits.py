from app.core.database import DBSession
from fastapi import APIRouter
from app.repositories.lawsuit import SqlAlchemyLawsuitRepository
from app.services.collect import CollectService
from app.schemas.requests import CollectInput
import asyncio
from app.schemas.responses import LawsuitResponse, PaginatedLawsuitsResponse

router = APIRouter(prefix="/lawsuits", tags=["lawsuits"])


@router.get("/{cnj}", response_model=LawsuitResponse)
async def find_by_cnj(cnj: str, session: DBSession):
    repo = SqlAlchemyLawsuitRepository(session)
    return await repo.get_by_cnj(cnj)


@router.get("/", response_model=PaginatedLawsuitsResponse)
async def find_all(session: DBSession, limit: int = 20, offset: int = 0):
    repo = SqlAlchemyLawsuitRepository(session)
    return await repo.getAll(limit=limit, offset=offset)


@router.post("/", response_model=list[LawsuitResponse])
async def collect(session: DBSession, body: CollectInput):
    service = CollectService(session)
    results = await asyncio.gather(*[service.collect(cnj) for cnj in body.cnjs])
    return [result for result in results if result is not None]

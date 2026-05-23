from app.core.database import DBSession
from fastapi import APIRouter
from app.repositories.lawsuit import SqlAlchemyLawsuitRepository
from app.services.collect import CollectService
from app.schemas.requests import CollectInput

router = APIRouter(prefix="/lawsuits", tags=["lawsuits"])


@router.get("/{cnj}")
async def find_by_cnj(cnj: str, session: DBSession):
    repo = SqlAlchemyLawsuitRepository(session)
    return await repo.get_by_cnj(cnj)

@router.get("/")
async def find_all(session: DBSession, limit: int = 20, offset: int = 0):
    repo = SqlAlchemyLawsuitRepository(session)
    return await repo.getAll(limit=limit, offset=offset)

@router.post("/")
async def collect(session: DBSession, body: CollectInput):
        service = CollectService(session)
        results = []
        for cnj in body.cnjs:
            lawsuit = await service.collect(cnj)
            results.append(lawsuit)
        return results
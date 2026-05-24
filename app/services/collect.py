import httpx
from app.scrapers.datajud import DatajudScraper
from app.scrapers.consulta_processual import ConsultaProcessuralScraper
from app.repositories.lawsuit import SqlAlchemyLawsuitRepository
from app.core.database import DBSession
import asyncio


class CollectService:
    def __init__(self, session: DBSession):
        self.session = session

    SEM = asyncio.Semaphore(3)

    async def collect(self, cnj: str):
        async with self.SEM:
            for try_ in range(3):
                try:
                    async with httpx.AsyncClient(timeout=60) as client:
                        scraper1 = DatajudScraper(client)
                        scraper2 = ConsultaProcessuralScraper(client)
                        data1, data2 = await asyncio.gather(
                            scraper1.collect(cnj),
                            scraper2.collect(cnj),
                        )
                    break
                except httpx.ReadTimeout:
                    if try_ == 2:
                        return None
                await asyncio.sleep(2)

        repo = SqlAlchemyLawsuitRepository(self.session)
        if data1 is not None:
            await repo.upsert(cnj, data1, tribunal_id=1)

        if data2 is not None:
            await repo.upsert(cnj, data2, tribunal_id=1)

        return await repo.get_by_cnj(cnj)

import httpx
from app.scrapers.datajud import DatajudScraper
from app.scrapers.consulta_processual import ConsultaProcessuralScraper
from app.repositories.lawsuit import SqlAlchemyLawsuitRepository
from app.core.database import DBSession
import asyncio

class CollectService:
  def __init__(self, session: DBSession):
    self.session = session
  
  async def collect(self, cnj: str):
    response = []
    async with httpx.AsyncClient() as client:
      # Add log and parallelize the asynchronous code
      scraper1 = DatajudScraper(client)
      scraper2 = ConsultaProcessuralScraper(client)
      data1, data2 = await asyncio.gather(
        scraper1.collect(cnj),
        scraper2.collect(cnj),
      )
    repo = SqlAlchemyLawsuitRepository(self.session)
    if data1 is not None:
      print("Starting Datajud upsert...")
      response.append(await repo.upsert(cnj, data1, tribunal_id=1))
    
    if data2 is not None:
      print("Starting Consulta Processual upsert...")
      response.append(await repo.upsert(cnj, data2, tribunal_id=1))
    
    return response
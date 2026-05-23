import httpx
from app.scrapers.datajud import DatajudScraper
from app.repositories.lawsuit import SqlAlchemyLawsuitRepository
from app.core.database import DBSession
import httpx

class CollectService:
  def __init__(self, session: DBSession):
    self.session = session
  
  async def collect(self, cnj: str):
    async with httpx.AsyncClient() as client:
      scraper = DatajudScraper(client)
      data = await scraper.collect(cnj)
    if data is None:
      return None
    
    repo = SqlAlchemyLawsuitRepository(self.session)
    return await repo.upsert(cnj, data, tribunal_id=1)
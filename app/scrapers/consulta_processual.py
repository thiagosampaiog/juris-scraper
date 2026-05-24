from app.scrapers.base import BaseScraper
import httpx
from app.core.config import settings
from app.normalizers.utils import parse_date, parse_datajud_date


class ConsultaProcessuralScraper(BaseScraper):
    consultaProcessualUrl = settings.consulta_processual_api

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def scraper_fetch(self, cnj) -> dict | None:
        raw = await self.client.get(f'{self.consultaProcessualUrl}/numProcessoCnj/{cnj}')
        print("\nT\nT",raw)
        data = raw.json()
        return data[0] if data else None

    def scraper_normalize(self, raw: dict) -> dict:
      return raw
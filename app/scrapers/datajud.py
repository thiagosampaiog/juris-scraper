from app.scrapers.base import BaseScraper
import httpx
from app.core.config import settings


class DatajudScraper(BaseScraper):
    datajudUrl = settings.datajud_api
    datajudKey = f"ApiKey {settings.datajud_api_key}"

    headers = dict(Accept="application/json", Authorization=datajudKey)

    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.client.headers.update(self.headers)

    async def scraper_fetch(self, cnj) -> dict | None:
        body = {"query": {"match": {"numeroProcesso": cnj}}}
        raw = await self.client.post(self.datajudUrl, json=body)
        hits = raw.json().get("hits", {}).get("hits", [])
        return hits[0]["_source"] if hits else None

    def scraper_normalize(self, raw) -> dict:
        return super().scraper_normalize(raw)

from app.scrapers.base import BaseScraper
import httpx
from app.core.config import settings
from app.normalizers.utils import parse_date, parse_datajud_date


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

    def scraper_normalize(self, raw: dict) -> dict:
        return {
            "class_":         raw.get("classe", {}).get("nome"),
            "grade":          raw.get("grau"),
            "subject":        raw.get("assuntos", [{}])[0].get("nome") if raw.get("assuntos") else None,
            "area":           None,
            "court":          raw.get("orgaoJulgador", {}).get("nome"),
            "district":       None,
            "control":        None,
            "action_value":   None,
            "status":         None,
            "source":         "datajud",
            "distributed_at": parse_datajud_date(raw.get("dataAjuizamento")),
            "movements": [
                {
                    "code":        m.get("codigo"),
                    "description": m.get("nome"),
                    "occurred_at": parse_date(m.get("dataHora")),
                }
                for m in raw.get("movimentos", [])
            ],
            "participants": [],
            "subjects": [
                {
                    "code": s.get("codigo"),
                    "name": s.get("nome")
                }
                for s in raw.get("assuntos", [])
            ],
            "incidents": [],
            "hearings": [],
            "petitions": [],
            "raw":   None,
        }
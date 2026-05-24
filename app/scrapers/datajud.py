from app.scrapers.base import BaseScraper
import httpx
from app.core.config import settings
from app.normalizers.utils import parse_date, parse_datajud_date
from app.models.models import SourceType


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
            "class_":         raw.get("classe", {}).get("nome") or None,
            "grade":          raw.get("grau") or None,
            "subject":        raw.get("assuntos", [{}])[0].get("nome") if raw.get("assuntos") else None,
            "area":           None,
            "court":          raw.get("orgaoJulgador", {}).get("nome") or None,
            "district":       None,
            "control":        raw.get('numeroProcesso') or None,
            "action_value":   None,
            "status":         None,
            "source":         SourceType.datajud,
            "distributed_at": parse_datajud_date(raw.get("dataAjuizamento")) or None,
            "movements": [
                {
                    "code":        int(m.get("codMovCnj")) if m.get("codMovCnj") else None,
                    "description": m.get("nome") or None,
                    "occurred_at": parse_date(m.get("dataHora")) or None,
                }
                for m in raw.get("movimentos", [])
            ],
            "participants": [],
            "subjects": [
                {
                    "code": int(s.get("codMovCnj")) if s.get("codMovCnj") else None,
                    "name": s.get("nome") or None
                }
                for s in raw.get("assuntos", [])
            ],
            "incidents": [],
            "hearings": [],
            "petitions": [],
            "raw":   None,
        }
from app.scrapers.base import BaseScraper
import httpx
from app.core.config import settings
from app.normalizers.utils import (
    parse_date,
    parse_datajud_date,
    parse_participant_type,
    parse_br_date,
)
from app.models.models import SourceType
import asyncio


class ConsultaProcessuralScraper(BaseScraper):
    consultaProcessualUrl = settings.consulta_processual_api

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def scraper_fetch(self, cnj) -> dict | None:
        raw1 = await self.client.get(
            f"{self.consultaProcessualUrl}/numProcessoCnj/{cnj}"
        )

        try:
            data1 = raw1.json() if raw1.status_code == 200 else []
        except Exception:
            return None

        if not data1:
            return None

        base = data1[0]
        consultaProcessual_id = base.get("id")

        if consultaProcessual_id:
            raw2 = await self.client.get(
                f"{self.consultaProcessualUrl}/{consultaProcessual_id}/detalhes"
            )
            try:
                data2 = raw2.json() if raw2.status_code == 200 else {}
            except Exception:
                data2 = {}

        if isinstance(data2, dict):
            base.update(data2)

        return base

    def scraper_normalize(self, raw: dict) -> dict:
        valor_causa = raw.get("valorCausa")

        return {
            "class_": raw.get("classe") or None,
            "grade": raw.get("grau") or None,
            "subject": raw.get("assunto") or None,
            "area": None,
            "court": raw.get("distribuicao") or None,
            "district": raw.get("descComarca") or None,
            "control": raw.get("numProcessoCnj") or None,
            "action_value": (
                float(valor_causa) if valor_causa not in (None, "", 0) else None
            ),
            "status": None,
            "source": SourceType.consulta_processual or None,
            "distributed_at": parse_datajud_date(raw.get("dataDistribuicao")) or None,
            "participants": [
                {
                    "name": p.get("nomeParte") or None,
                    "lawyer_name": p.get("nomeAdvogado") or None,
                    "type_": parse_participant_type(p.get("tipoParte")) or None,
                    "cpf_cnpj": p.get("cpfCnpj") or None,
                }
                for p in raw.get("partes", [])
            ],
            "movements": [
                {
                    "code": int(m.get("codMovCnj")) if m.get("codMovCnj") else None,
                    "description": m.get("descricao"),
                    "occurred_at": parse_br_date(m.get("dataMovimento")),
                }
                for m in raw.get("movimentacoes", [])
            ],
            "subjects": [],
            "incidents": [],
            "hearings": [],
            "petitions": [],
            "raw": raw,
        }

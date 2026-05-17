from abc import ABC, abstractmethod


class BaseScraper(ABC):
    @abstractmethod
    async def scraper_fetch(self, cnj: str) -> dict | None:
        pass

    @abstractmethod
    def scraper_normalize(self, raw: dict) -> dict:
        pass

    async def collect(self, cnj: str) -> dict | None:
        raw = await self.scraper_fetch(cnj)
        if raw is None:
            return None
        return self.scraper_normalize(raw)

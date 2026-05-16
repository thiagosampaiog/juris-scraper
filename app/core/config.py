from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, extra="ignore"
    )
    # ===== APP =====
    app_name: str = ""
    app_port: int = 3040
    # ==== DATABASE =====
    database_url: str = "postgresql+asyncpg://juris:juris@localhost:5432/juris_scraper"
    # ==== SCRAPERS ====
    consulta_processual_api: str = (
        "https://consultaprocessualapi.tjba.jus.br/api/processos/"
    )
    datajud_api: str = "https://api-publica.datajud.cnj.jus.br/api_publica_tjba/_search"


settings = Settings()

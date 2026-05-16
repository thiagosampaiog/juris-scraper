from fastapi import FastAPI
from app.core.config import settings
from app.api.routes.lawsuits import router as lawsuits_router

app = FastAPI(
    title=settings.app_name, swagger_ui_parameters={"syntaxhighlights": False}
)
app.include_router(lawsuits_router)


@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "app_port": settings.app_port,
        "database_url": settings.database_url,
    }

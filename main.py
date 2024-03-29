import uvicorn
from fastapi import FastAPI

from src.routers import firing

app = FastAPI(
    title="Jira to Bitrix Webhook",
    contact={"name": "KELONMYOSA", "url": "https://t.me/KELONMYOSA"},
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)

app.include_router(firing.router)

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    uvicorn.run(app, host=host, port=port)

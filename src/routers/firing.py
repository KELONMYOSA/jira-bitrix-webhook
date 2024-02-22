from fastapi import APIRouter, Request

from src.models.firing import FiringTaskData

router = APIRouter(
    prefix="/firing",
    tags=["Firing"],
)


@router.post("/bitrix")
async def from_bitrix_create(data: FiringTaskData):
    return {"status": "ok"}


@router.post("/jira")
async def from_jira_process(request: Request):
    r = await request.json()
    issue = r["issue"]
    key = issue["key"]
    status = issue["fields"]["status"]["name"]

    return {"status": "ok"}

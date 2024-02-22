from fastapi import APIRouter, Request

from src.db.dao import Database
from src.models.firing import FiringTaskData

router = APIRouter(
    prefix="/firing",
    tags=["Firing"],
)


@router.post("/bitrix")
async def from_bitrix_create(data: FiringTaskData):
    with Database() as db:
        db.set_firing_tasks(data)

    return {"status": "success"}


@router.post("/jira")
async def from_jira_process(request: Request):
    r = await request.json()
    issue = r["issue"]
    key = issue["key"]
    status = issue["fields"]["status"]["name"]

    with Database() as db:
        if not db.jira_firing_task_exists(key):
            return {"status": "error", "message": "Jira task key does not exist"}

        db.update_firing_jira_status(key, status)
        db.connection.commit()

        bitrix_task_id = db.get_firing_bitrix_id_by_jira_key(key)

        if db.all_firing_jira_tasks_solved(bitrix_task_id):
            await db.set_firing_bitrix_task_solved(bitrix_task_id)

    return {"status": "success"}

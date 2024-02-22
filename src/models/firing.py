from pydantic import BaseModel


class FiringTaskData(BaseModel):
    bitrix_task_id: int
    jira_task_keys: list[str]

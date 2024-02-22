from pydantic import BaseModel


class FiringTaskData(BaseModel):
    bitrix_task_key: str
    jira_task_keys: list[str]

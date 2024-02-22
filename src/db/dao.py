import sqlite3

from src.models.firing import FiringTaskData
from src.utils.bitrix_requests import solve_bitrix_task


class Database:
    __DB_PATH = "src/db/database.sqlite"

    # Устанавливаем соединение с базой данных
    def __init__(self, db_location: str | None = None):
        if db_location is not None:
            self.connection = sqlite3.connect(db_location)
        else:
            self.connection = sqlite3.connect(self.__DB_PATH)
        self.cur = self.connection.cursor()

    def __enter__(self):
        return self

    # Сохраняем изменения и закрываем соединение
    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

    # Записываем id задачи из Bitrix и ключи задач из Jira
    def set_firing_tasks(self, data: FiringTaskData):
        self.cur.execute("INSERT INTO firing_bitrix_tasks (bitrix_task_id) VALUES (?)", (data.bitrix_task_id,))
        for jira_key in data.jira_task_keys:
            self.cur.execute(
                "INSERT INTO firing_jira_tasks (bitrix_task_id, jira_task_key, status) VALUES (?, ?, ?)",
                (data.bitrix_task_id, jira_key, "Pending"),
            )

    # Проверяем, есть ли такая задача Jira
    def jira_firing_task_exists(self, jira_key: str) -> bool:
        return self.cur.execute(
            "SELECT EXISTS(SELECT 1 FROM firing_jira_tasks WHERE jira_task_key = ?)", (jira_key,)
        ).fetchone()[0]

    # Обновляем статус задачи Jira
    def update_firing_jira_status(self, jira_key: str, status: str):
        self.cur.execute("UPDATE firing_jira_tasks SET status = ? WHERE jira_task_key = ?", (status, jira_key))

    # Получаем id задачи в Bitrix по ключу задачи в Jira
    def get_firing_bitrix_id_by_jira_key(self, jira_key: str) -> int:
        return self.cur.execute(
            "SELECT bitrix_task_id FROM firing_jira_tasks WHERE jira_task_key = ?", (jira_key,)
        ).fetchone()[0]

    # Проверяем, все ли задачи из Jira решены
    def all_firing_jira_tasks_solved(self, bitrix_task_id: int) -> bool:
        unresolved = self.cur.execute(
            "SELECT COUNT(*) FROM firing_jira_tasks WHERE bitrix_task_id = ? AND status != 'Решено'",
            (bitrix_task_id,),
        ).fetchone()[0]
        return unresolved == 0

    # Помечаем задачу в Bitrix решенной
    async def set_firing_bitrix_task_solved(self, bitrix_task_id: int):
        if await solve_bitrix_task(bitrix_task_id):
            self.cur.execute("UPDATE firing_bitrix_tasks SET processed = 1 WHERE bitrix_task_id= ?", (bitrix_task_id,))

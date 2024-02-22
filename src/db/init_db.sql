CREATE TABLE firing_bitrix_tasks (
    bitrix_task_id INTEGER PRIMARY KEY,
    processed INTEGER DEFAULT 0
);

CREATE TABLE firing_jira_tasks (
    jira_task_key TEXT PRIMARY KEY,
    bitrix_task_id INTEGER,
    status TEXT,
    FOREIGN KEY(bitrix_task_id) REFERENCES firing_bitrix_tasks(bitrix_task_id) ON DELETE CASCADE
);
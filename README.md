# Jira to Bitrix webhook

## Как запустить:

### 1. Клонировать репозиторий

```bash
git clone https://github.com/KELONMYOSA/jira-bitrix-webhook.git
```

### 2. Создать .env файл

#### .env example

```
BITRIX_WEBHOOK=https://bitrix.company.com/webhook
JIRA_URL=https://jira.atlassian.net
```

### 3. Создать SQLite базу данных из SQL файла

```bash
sqlite3 src/db/database.sqlite < src/db/init_db.sql
```

### 4. Запустить docker-compose

```bash
docker compose up -d
```
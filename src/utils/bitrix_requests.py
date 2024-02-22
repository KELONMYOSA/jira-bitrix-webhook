import aiohttp

from src.config import settings


async def solve_bitrix_task(task_id: int) -> bool:
    url = f"{settings.BITRIX_WEBHOOK}/task.item.complete.json?taskId={task_id}"
    async with aiohttp.ClientSession() as session:  # noqa: SIM117
        async with session.get(url) as response:
            return response.status == 200  # noqa: PLR2004

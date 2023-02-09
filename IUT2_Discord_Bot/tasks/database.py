from lightbulb.ext import tasks
from IUT2_Discord_Bot.data.manipulate_db import update_db


@tasks.task(h=1, auto_start=True, wait_before_execution=True)
async def update_db_task():
    update_db()

from lightbulb.ext import tasks
from IUT2_Discord_Bot.data.manipulate_db import update_db


@tasks.task(h=12, auto_start=True, wait_before_execution=False)
async def update_db_every_12_hours():
    update_db()

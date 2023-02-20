import hikari
import lightbulb

from IUT2_Discord_Bot.data.manipulate_db import update_db


admin_plugin = lightbulb.Plugin("AdminPlugin", "Commandes servant à de l'administration")


@admin_plugin.command
@lightbulb.app_command_permissions(hikari.Permissions.ADMINISTRATOR)
@lightbulb.command("update_database", "Lancer la mise à jour de l'emploi du temps dans la base de données", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def update_database(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond("Updating database...")
    update_db()
    await ctx.respond("Update finished!")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(admin_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(bot.get_plugin("admin_plugin"))

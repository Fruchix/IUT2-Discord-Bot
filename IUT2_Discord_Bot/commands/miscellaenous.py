import hikari
import lightbulb


@lightbulb.add_checks(lightbulb.checks.has_roles(1048357379911192657, 1048357830509465700, mode=any))
@lightbulb.command("ratio", "")
@lightbulb.implements(lightbulb.commands.MessageCommand)
async def ratio(ctx: lightbulb.MessageContext):
    message = ctx.options.target

    for i in ["🇷", "🇦", "🇹", "🇮", "🇴"]:
        await message.add_reaction(i)

    await ctx.respond(f"Succesfully ratioed <@{message.author.id}>", flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: lightbulb.BotApp) -> None:
    bot.command(ratio)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_message_command("ratio"))

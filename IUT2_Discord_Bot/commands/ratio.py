import hikari
import lightbulb
import miru


class SeeMessage(miru.Button):

    async def callback(self, ctx: miru.Context) -> None:
        await ctx.message.edit(components=self.view.build())
        return


@lightbulb.add_checks(lightbulb.checks.has_roles(1048357379911192657, 1048357830509465700, mode=any))
@lightbulb.command("ratio", "")
@lightbulb.implements(lightbulb.commands.MessageCommand)
async def ratio(ctx: lightbulb.MessageContext):
    message = ctx.options.target

    for i in ["🇷", "🇦", "🇹", "🇮", "🇴"]:
        await message.add_reaction(i)

    view = miru.View(timeout=60)
    view.add_item(SeeMessage(style=hikari.ButtonStyle.LINK,
                             label="See message",
                             url=ctx.options.target.make_link(ctx.get_guild())))
    resp = await ctx.respond(f"Succesfully ratioed <@{message.author.id}>",
                             flags=hikari.MessageFlag.EPHEMERAL,
                             components=view.build())
    message = await resp.message()
    view.start(message=message)


def load(bot: lightbulb.BotApp) -> None:
    bot.command(ratio)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_message_command("ratio"))

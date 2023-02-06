import hikari
import lightbulb


@lightbulb.command("embed_test", "Testing embeds")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def embed_test(ctx : lightbulb.context.SlashContext) -> None :

    myEmbed = hikari.Embed(title="Test Embed", color=hikari.Color.of((33, 186, 217)))
    myEmbed.set_image("IUT2_Discord_Bot/resources/images/agenda.png")\
        .set_author(name=f"{ctx.author}", icon=ctx.author.avatar_url)\
        .set_footer(text=f"{ctx.author}", icon=ctx.author.avatar_url)

    await ctx.respond(myEmbed)


def load(bot: lightbulb.BotApp) -> None:
    bot.command(embed_test)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("embed_test"))

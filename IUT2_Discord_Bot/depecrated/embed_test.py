import hikari
import lightbulb
from miru.ext import nav


@lightbulb.command("embed_test", "Testing embeds")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def embed_test(ctx : lightbulb.context.SlashContext) -> None:

    myEmbed = hikari.Embed(title="Test Embed", color=hikari.Color.of((33, 186, 217)))
    myEmbed.set_image("IUT2_Discord_Bot/resources/images/agenda.png")\
        .add_field(name="Source", value="📌 Stolen from [ADE](https://redirect.univ-grenoble-alpes.fr/ADE_ETUDIANTS_ETC)")\
        .set_author(name=f"{ctx.author}", icon=ctx.author.avatar_url)\
        .set_footer(text=f"{ctx.author}", icon=ctx.author.avatar_url)

    myEmbed.description = "📌 Stolen from [ADE](https://redirect.univ-grenoble-alpes.fr/ADE_ETUDIANTS_ETC)"

    await ctx.respond(myEmbed)


@lightbulb.command("nav_test", "Testing navigators")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def nav_test(ctx: lightbulb.SlashContext) -> None:
    pages = ["Page 1", "Page 2"]
    navigator = nav.NavigatorView(pages=pages)
    await navigator.send(ctx.channel_id)
    await ctx.respond("Navigator sent", flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: lightbulb.BotApp) -> None:
    bot.command(embed_test)
    bot.command(nav_test)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("embed_test"))
    bot.remove_command(bot.get_slash_command("nav_test"))

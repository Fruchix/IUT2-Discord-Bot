import hikari
import lightbulb

@lightbulb.command("embed_test", "Testing embeds")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def embed_test(ctx : lightbulb.context.SlashContext) -> None :

    myEmbed = hikari.Embed(title="Test Embed", color=hikari.Color.of((33, 186, 217)))
    myEmbed.set_image("IUT2_Discord_Bot/resources/images/agenda.png")

    await ctx.respond(myEmbed)
    return

def load(bot: lightbulb.BotApp) -> None:
    bot.command(embed_test)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("embed_test"))
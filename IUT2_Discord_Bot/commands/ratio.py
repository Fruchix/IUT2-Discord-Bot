import hikari
import lightbulb
import miru


class SeeMessage(miru.Button):

    async def callback(self, ctx: miru.Context) -> None:
        await ctx.message.edit(components=self.view.build())
        return


@lightbulb.command("ratio", "")
@lightbulb.implements(lightbulb.commands.MessageCommand)
async def ratio(ctx: lightbulb.MessageContext):
    # récupération du destinataire du message
    message = ctx.options.target
    # ajout des réactions
    for i in ["🇷", "🇦", "🇹", "🇮", "🇴"]:
        await message.add_reaction(i)

    # création de la vue
    view = miru.View(timeout=60)
    # ajout du bouton "See message" à la vue
    view.add_item(SeeMessage(style=hikari.ButtonStyle.LINK,
                             label="See message",
                             url=ctx.options.target.make_link(ctx.get_guild())))
    # création de la réponse, contenant la vue, visible uniquement par l'utilisateur de la commande
    resp = await ctx.respond(f"Succesfully ratioed <@{message.author.id}>",
                             flags=hikari.MessageFlag.EPHEMERAL,
                             components=view.build())
    # création du message à partir de la réponse
    message = await resp.message()
    # démarrage de la vue
    view.start(message=message)


def load(bot: lightbulb.BotApp) -> None:
    bot.command(ratio)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_message_command("ratio"))

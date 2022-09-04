import hikari
import lightbulb

from guilds.RoleViews import get_role_view
from utils.json_utils import append_element_json_array


@lightbulb.add_checks(lightbulb.checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option("channel","Identifiant du channel où envoyer le menu.", type=hikari.GuildChannel, required=True)
@lightbulb.option("titre", "Titre du menu", type=str, required=True)
@lightbulb.command("selecteur_role", "Créé un menu où les utilisateurs peuvent choisir leur role.", guilds=[994181854058000416, 890968871845122108])
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def selecteur_role(ctx: lightbulb.context.SlashContext):

    try:
        view = get_role_view(guild_id=ctx.guild_id)
    except ValueError:
        await ctx.respond("Ce serveur n'a pas de sélecteur de rôle dédié.", delete_after=10)
        return

    await ctx.respond(f"Sélecteur de rôles créé dans le salon <#{ctx.options.channel.id}>", delete_after=10)

    my_embed = hikari.Embed(title=ctx.options.titre,
                            color=hikari.Color.of((33, 186, 217)))
    message = await ctx.bot.rest.create_message(channel=ctx.options.channel, components=view.build(), embed=my_embed)
    view.start(message)

    selector = {
        'id': message.id,
        'channel_id': message.channel_id,
        'guild_id': ctx.guild_id
    }

    append_element_json_array(selector, "selectors", "guilds/selectors.json")

    return


def load(bot: lightbulb.BotApp) -> None:
    bot.command(selecteur_role)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command((bot.get_slash_command("selecteur_role")))
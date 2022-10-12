import datetime
import hikari
import lightbulb

from IUT2_Discord_Bot.edt.get_agenda import generate_agenda, select_semaine
from IUT2_Discord_Bot.edt.edt_utils import auto_select_edt, liste_groupes, id_edt_groupe


@lightbulb.option("groupe", "Le groupe dont il faut récupérer l'emploi du temps", choices=liste_groupes, type=str, default="", required=False)
@lightbulb.option("semaine", "La semaine souhaitée (0 = semaine actuelle, 1 = semaine suivante, -1 = semaine précédente, ...)", type=int, default=0, required=False)
@lightbulb.command("edt", "Afficher un emploi du temps")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def edt(ctx: lightbulb.context.SlashContext) -> None:

    # si un groupe de TP a été passé en paramètre,
    # alors on récupère l'identifiant de l'edt correspondant dans le dictionnaire id_edt_groupe,
    # sinon on auto-sélectionne l'edt via les rôles de l'utilisateur
    if ctx.options.groupe != "":
        id_groupe_tp = id_edt_groupe[ctx.options.groupe]
    else:
        # si la commande est entrée dans des messages privés
        # alors envoi d'un message d'erreur et fin de la fonction
        # sinon sélection automatique de l'edt via les rôles de l'utilisateur
        if ctx.guild_id is None:
            await ctx.respond("Veuillez préciser le groupe souhaité.")
            return
        else:
            try:
                id_groupe_tp = auto_select_edt(ctx.member.get_roles())
            except ValueError:
                await ctx.respond("Vous n'avez pas de rôle de groupe : veuillez préciser le groupe souhaité.")
                return

    # vérification qu'un rôle a été trouvé
    if id_groupe_tp is None:
        await ctx.respond("Aucun groupe TP trouvé dans vos rôles." )
        return

    # génération du fichier agenda.png
    generate_agenda(id_groupe_tp, ctx.options.semaine)

    # envoi du fichier agenda.png

    await ctx.respond(
        hikari.Embed(
            title="Emploi du temps",
            color=hikari.Color.of((33, 186, 217))
        )
        .add_field("Groupe", " ".join(g for g in id_edt_groupe.keys() if id_edt_groupe[g] == id_groupe_tp), inline=True)
        .add_field("Semaine", "Du " + str(select_semaine(ctx.options.semaine).strftime("%d-%m-%Y")) + " au " + str((select_semaine((ctx.options.semaine)) + datetime.timedelta(4)).strftime("%d-%m-%Y")), inline=True)
        .set_image("IUT2_Discord_Bot/edt/agenda.png")
    )
    return


@lightbulb.command("calendrier", "Afficher le calendrier de l'année.")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def calendrier(ctx: lightbulb.context.SlashContext):

    # envoyer le calendrier
    await ctx.respond(
        hikari.Embed(
            title="Calendrier 2022/2023",
            color=hikari.Color.of((33, 186, 217))
        )
        .set_image("IUT2_Discord_Bot/resources/calendrier-2022-2023.png")
    )
    return



def load(bot: lightbulb.BotApp) -> None:
    bot.command(edt)
    bot.command(calendrier)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("edt"))
    bot.remove_command(bot.get_slash_command("calendrier"))
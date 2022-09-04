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

    ##################################################
    # génération du fichier agenda.png via la fonction select_agenda(...) de get_edt
    #    await ctx.respond("Groupe demandé : " + groupe_tp + " Semaine demandée : " + str(ctx.options.semaine))

    generate_agenda(id_groupe_tp, ctx.options.semaine)

    ##################################################
    # envoi du fichier agenda.png

    await ctx.respond(
        hikari.Embed(
            title="Emploi du temps",
            color=hikari.Color.of((33, 186, 217))
        )
        .add_field("Groupe", " ".join(g for g in id_edt_groupe.keys() if id_edt_groupe[g] == id_groupe_tp), inline=True)
        .add_field("Semaine", "Du " + str(select_semaine(ctx.options.semaine).strftime("%d-%m-%Y")) + " au " + str((select_semaine((ctx.options.semaine)) + datetime.timedelta(4)).strftime("%d-%m-%Y")), inline=True)
        .set_image("edt/agenda.png")
    )
    return


@lightbulb.option("promotion", "La promotion dont il faut afficher le calendrier.", choices=["1A", "2A", "LP"], default="", required=False)
@lightbulb.command("calendar", "Afficher le calendrier de l'année.")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def calendar(ctx: lightbulb.context.SlashContext):

    # si aucun paramètre de promotion n'a été donné et que la commande n'est pas effectuée dans un serveur
    # alors renvoit message erreur
    # sinon autodétection du calendrier à envoyer en fonction du serveur
    if ctx.options.promotion == "" and ctx.guild_id is None:
        await ctx.respond("Veuillez préciser la promotion souhaitée.")
        return
    elif ctx.options.promotion == "":
        if ctx.guild_id == 994181854058000416:
            promotion = "1A"
        elif ctx.guild_id == 890968871845122108:
            promotion = "2A"
        else:
            await ctx.respond("Veuillez préciser la promotion souhaitée.")
            return
    else:
        promotion = ctx.options.promotion

    try:
        await ctx.respond(
            hikari.Embed(
                title="Calendrier",
                color=hikari.Color.of((33, 186, 217))
            )
            .set_image(f"resources/calendrier-2022-2023-{promotion}.png")
        )
        return
    except FileNotFoundError:
        await ctx.respond("Le fichier recherché n'est pas disponible.")
        return


def load(bot: lightbulb.BotApp) -> None:
    bot.command(edt)
    bot.command(calendar)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("edt"))
    bot.remove_command(bot.get_slash_command("calendar"))
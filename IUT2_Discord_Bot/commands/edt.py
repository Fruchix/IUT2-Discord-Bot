import datetime
import hikari
import lightbulb

from IUT2_Discord_Bot.edt.draw_agenda import draw_agenda
from IUT2_Discord_Bot.edt.edt_utils import auto_select_edt, liste_groupes, id_edt_groupe, select_semaine
from IUT2_Discord_Bot.data.manipulate_db import read_liste_salles_libres


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
            id_groupe_tp = auto_select_edt(ctx.member.get_roles())

            if id_groupe_tp == -1:
                await ctx.respond("Vous n'avez pas de rôle de groupe : veuillez préciser le groupe souhaité.")
                return

    # vérification qu'un rôle a été trouvé
    if id_groupe_tp is None:
        await ctx.respond("Aucun groupe TP trouvé dans vos rôles." )
        return

    # pré-génération de l'embed
    embed_edt = hikari.Embed(
        color=hikari.Color.of((33, 186, 217))
    )\
        .add_field("Groupe", " ".join(g for g in id_edt_groupe.keys() if id_edt_groupe[g] == id_groupe_tp), inline=True)\
        .add_field("Semaine", "Du " + str(select_semaine(ctx.options.semaine).strftime("%d-%m-%Y")) + " au " +
                   str((select_semaine(ctx.options.semaine) + datetime.timedelta(4)).strftime("%d-%m-%Y")), inline=True)

    try:
        # génération du fichier agenda.png
        draw_agenda(id_groupe_tp, ctx.options.semaine)

        embed_edt.title = "Emploi du temps"
        embed_edt.set_image("IUT2_Discord_Bot/resources/images/agenda.png")
    except ValueError:
        embed_edt.title = "Aucun emploi du temps trouvé"

    await ctx.respond(embed_edt)


@lightbulb.option("duree_en_h", "La durée pendant laquelle les salles doivent être disponibles (en heures)", type=float)
@lightbulb.option("heure", "Heure où chercher, au format \"14:26\"", type=str)
@lightbulb.option("jour", "Jour où chercher", choices=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"])
@lightbulb.command("salles_libres", "Afficher les salles libres à un certain créneau")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def salles_libres(ctx: lightbulb.context.SlashContext):
    jours = {
        "Lundi": 0,
        "Mardi": 1,
        "Mercredi": 2,
        "Jeudi": 3,
        "Vendredi": 4
    }

    date = select_semaine(0) + datetime.timedelta(jours[ctx.options.jour])

    salles = read_liste_salles_libres(
        datetime.datetime.strptime(str(date) + "T" + ctx.options.heure + ":00+01:00", "%Y-%m-%dT%H:%M:%S%z"), datetime.timedelta(hours=float(ctx.options.duree_en_h)))

    my_embed = hikari.Embed(
        title="Salles libres",
        color=hikari.Color.of((33, 186, 217))
    )

    etages = {
        "3": "Etage 3",
        "2": "Etage 2",
        "1": "Etage 1",
        "0": "Rez de chaussée",
        "S": "Sous-sol"
    }

    for key, value in etages.items():
        liste_salles = "\n".join([s[0] for s in salles if s[1] == key])

        my_embed.add_field(value, liste_salles if liste_salles else "Aucune salle libre")

    await ctx.respond(my_embed)


@lightbulb.command("calendrier", "Afficher le calendrier de l'année.")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def calendrier(ctx: lightbulb.context.SlashContext):

    # envoyer le calendrier
    await ctx.respond(
        hikari.Embed(
            title="Calendrier 2022/2023",
            color=hikari.Color.of((33, 186, 217))
        )
        .set_image("IUT2_Discord_Bot/resources/images/calendrier-2022-2023.png")
    )
    return


def load(bot: lightbulb.BotApp) -> None:
    bot.command(edt)
    bot.command(calendrier)
    bot.command(salles_libres)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("edt"))
    bot.remove_command(bot.get_slash_command("calendrier"))
    bot.remove_command(bot.get_slash_command("salles_libres"))

import hikari
import lightbulb
import requests


@lightbulb.option("option", "free = 5 machines les moins occupées | up = toutes les machines allumées | "
                            "all = toutes les machines",
                  choices=["free", "up", "all"], required=False, default="free")
@lightbulb.command("etat_machines", "Renvoie l'état des stations Linux de l'IUT2.")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def etat_machines(ctx: lightbulb.context.SlashContext):
    # récupération de la page web l'état des machines et stockage du texte de cette page dans la variable text_page
    text_page = requests.get(
        "https://www-info.iut2.univ-grenoble-alpes.fr/intranet/informations/cellule-info/etat-stations.php").text

    etat = "État des stations linux le " + text_page.split("État le ")[1].split("<pre>")[0]

    # récupération stations linux dans une liste : chaque ligne devient un élément
    list_stations_prov = text_page.split("<pre>")[1].split("</pre>")[0].splitlines()[3:-1]

    # récupération des noms machines, de leur état et nombre d'utilisateurs dans une liste
    # (à partir de la liste des stations)
    liste_machines = []
    for machine in list_stations_prov:
        # récupération du nom de la machine (numéro)
        num_machine = machine[:12]
        # récupération de l'état de la machine ("up" ou "down")
        etat_machine = machine[12:17].strip()
        if etat_machine == "up":
            nb_users = int(machine[30:35].strip())
            liste_machines.append([num_machine, etat_machine, nb_users])
        elif ctx.options.option == "all":
            liste_machines.append([num_machine, etat_machine, 0])

    # si aucune machine n'est allumée, retour message
    if not ("up" in (state for machine, state, users in liste_machines)):
        await ctx.respond("Toutes les machines sont éteintes.")
        return

    def value_field(salle: int) -> str:
        return "\n".join(
                    "`" + machine[0] + " " + machine[1] + (" " + str(machine[2]) + (
                        " user " if machine[2] == 1 else " users") if machine[1] == "up" else "      ") + "`" for
                    machine in liste_machines if machine[0][7:9] == str(salle))

    embed_machine = hikari.Embed(
        title=etat,
        color=hikari.Color.of((255, 87, 51))
    )

    embed_machine.description = "📌 Stolen from [Intranet Info IUT2](https://www-info.iut2.univ-grenoble-alpes.fr/intranet/informations/cellule-info/etat-stations.php)"

    if ctx.options.option != "free":
        await ctx.respond(
            embed_machine
            .add_field("`Salle 25`", value_field(25), inline=True)
            .add_field("`Salle 27`", value_field(27), inline=True)
            .add_field("`Salle 33`", value_field(33), inline=True)
            .add_field("`Salle 35`", value_field(35), inline=True)
            .add_field("`Salle 37`", value_field(37), inline=True)
            .add_field("`Salle 39`", value_field(39), inline=True)
        )
    else:
        await ctx.respond(
            embed_machine
            .add_field("Machines les moins occupées",
                       "\n".join("`" + machine[0] + " " + machine[1] + " " + str(machine[2])
                                 + (" user" if machine[2] == 1 else " users") + "`" for
                                 machine in sorted(liste_machines, key=lambda x: x[2])[:5])
                       )
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.command(etat_machines)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("etat_machines"))

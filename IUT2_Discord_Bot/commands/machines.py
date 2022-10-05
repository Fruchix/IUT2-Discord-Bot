import hikari
import lightbulb
import requests


@lightbulb.option("option", "free = 5 machines les moins occupées | up = toutes les machines allumées | "
                            "all = toutes les machines",
                  choices=["free", "up", "all"], required=False, default="free")
@lightbulb.command("etat_machines", "Renvoie l'état des stations Linux de l'IUT2.")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def etat_machines(ctx: lightbulb.context.SlashContext):
    print(ctx.options.option)

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

    if ctx.options.option != "free":
        await ctx.respond(hikari.Embed()
                          .add_field("Machines",
                                     "`" + "\n".join(
                                         machine[0] + " " + machine[1] + " " + str(machine[2]) + (
                                             " user" if machine[2] == 1 else " users") for
                                         machine in liste_machines if machine[0][7:9] == "25") + "`", inline=True)
                          .add_field("Machines",
                                     "`" + "\n".join(
                                         machine[0] + " " + machine[1] + " " + str(machine[2]) + (
                                             " user" if machine[2] == 1 else " users") for
                                         machine in liste_machines if machine[0][7:9] == "27") + "`", inline=True)
                          .add_field("Machines",
                                     "`" + "\n".join(
                                         machine[0] + " " + machine[1] + " " + str(machine[2]) + (
                                             " user " if machine[2] == 1 else " users") for
                                         machine in liste_machines if machine[0][7:9] == "33") + "`", inline=True)
                          .add_field("Machines",
                                     "`" + "\n".join(
                                         machine[0] + "\t" + machine[1] + "\t" + str(machine[2]) + (
                                             " user" if machine[2] == 1 else " users") for
                                         machine in liste_machines if machine[0][7:9] == "35") + "`", inline=True)
                          .add_field("Machines",
                                     "`" + "\n".join(
                                         machine[0] + "\t" + machine[1] + "\t" + str(machine[2]) + (
                                             " user" if machine[2] == 1 else " users") for
                                         machine in liste_machines if machine[0][7:9] == "37") + "`", inline=True)
                          .add_field("Machines",
                                     "`" + "\n".join(
                                         machine[0] + "\t" + machine[1] + "\t" + str(machine[2]) + (
                                             " user" if machine[2] == 1 else " users") for
                                         machine in liste_machines if machine[0][7:9] == "39"), inline=True)
                          )
    await ctx.respond("isbdqsd")


def load(bot: lightbulb.BotApp) -> None:
    bot.command(etat_machines)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("etat_machines"))

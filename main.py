import discord
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv

import edt_utils.get_edt as ge


# récupération des variables contenues dans le fichier config
load_dotenv(dotenv_path="config")

bot = commands.Bot(command_prefix="!")
bot.load_extension("Time")

@bot.event
async def on_ready():
    print("Bot opérationnel.")


@bot.event
async def on_message(message: discord.Message):
    if str(message.content).lower() == "un hôtel ?" or str(message.content).lower() == "un hotel ?":
        await message.add_reaction("🇹")
        await message.add_reaction("🇷")
        await message.add_reaction("🇮")
        await message.add_reaction("🇻")
        await message.add_reaction("🇦")
        await message.add_reaction("🇬")
        await message.add_reaction("🇴")

    await bot.process_commands(message)

@bot.command(name='edt_prov')
async def send_edt_picture(ctx, sem_decal: int = 0, groupe_tp: str = ""):
    """Envoyer une image d'un agenda.
    Sélection de l'agenda du groupe voulu selon le rôle de la personne ou du paramètre donné.
    Sélection de la semaine voulue en prenant par défaut la semaine de travail dans laquelle on est/celle qui arrive si on est en week-end,
     possibilité de décaler cette semaine choisie via le paramètre sem_decal

    :param ctx: le contexte de la commande
    :param sem_decal: le nombre de semaine de décalage
    :param groupe_tp: le groupe de l'étudiant
    """
    # passage du nom du groupe TP en uppercase pour le rendre insensible à la casse
    groupe_tp = groupe_tp.upper()

    # vérification du salon où la commande est envoyée : si ce n'est pas dans un serveur alors il ne peut y avoir de rôles
    if ctx.guild is None and groupe_tp == "":
        await ctx.channel.send("Veuillez préciser le rôle et la semaine voulue.")
        return

    # sélection du groupe de l'étudiant
    try:
        if groupe_tp != "":
            ge.select_agenda(groupe_tp, sem_decal)
        else:
            # sélection du groupe de l'étudiant via la fonction select_role(...)
            role_user = select_role(ctx.author.roles)

            # génération du fichier agenda.png via la fonction select_agenda(...) de get_edt
            ge.select_agenda(role_user, sem_decal)

    except KeyError:
        await ctx.channel.send("Nom de groupe invalide.")
        return

    with open('edt_utils/agenda.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.channel.send(file=picture)


def select_role(liste_roles):
    """Sélection du nom du groupe d'un étudiant. Parcours de sa liste de roles et retour du premier groupe qui convient.
    Normalement, un étudiant ne fait partie que d'un seul groupe de TP, il ne doit donc pas y avoir de problème.

    :param liste_roles: la liste des rôles de l'étudiant
    :rtype: str
    :return: le nom du groupe
    """
    for role in liste_roles:
        if role.name.find("A1") != -1:
            return "A1"
        if role.name.find("A2") != -1:
            return "A2"
        if role.name.find("B1") != -1:
            return "B1"
        if role.name.find("B2") != -1:
            return "B2"
        if role.name.find("C1") != -1:
            return "C1"
        if role.name.find("C2") != -1:
            return "C2"
        if role.name.find("D1") != -1:
            return "D1"
        if role.name.find("D2") != -1:
            return "D2"
        if role.name.find("S0") != -1:
            return "S0"

@bot.command(name="systemload")
async def iut_system_load(ctx, option: str = "all", nb_machines_min: int = 1):
    """Afficher l'état des machines de l'iut.

    :param ctx:
    :param option:  "all" (défaut) : affiche l'entièreté de la liste des machines par défaut
                    "up" : affiche uniquement les machines en ligne
                    "free" : affiche les nb_machines_min machines ayant le moins d'utilisateurs
    :param nb_machines_min: le nombre de machines ayant le moins d'utilisateurs à afficher (entre 1 et 5)
    :return:
    """
    # récupération de la page web où se trouve l'état des machines et stockage du texte de cette page dans la variable t_page_etat
    t_page_etat = requests.get("https://www-info.iut2.univ-grenoble-alpes.fr/intranet/informations/cellule-info/etat-stations.php").text

    etat = "État des stations linux le " + t_page_etat.split("État le ")[1].split("<pre>")[0]

    # récupération de la partie contenant les stations dans une liste : chaque ligne devient un élément (sous forme de chaine de caractères)
    list_stations_prov = t_page_etat.split("<pre>")[1].split("</pre>")[0].splitlines()[3:-1]

    # récupération des noms machines, de leur état et nombre d'utilisateurs dans une liste (à partir de la liste des stations)
    liste_machines = []
    for machine in list_stations_prov:
        # récupération du nom de la machine (numéro)
        num_machine = machine[:12]
        # récupération de l'état de la machine ("up" ou "down")
        etat_machine = machine[12:17].strip()

        if (etat_machine == "up"):
            nb_users = int(machine[30:35].strip())
            users_string = "user" if nb_users == 1 else "users"
            liste_machines.append([num_machine, etat_machine, nb_users, users_string])
        elif option != "up":
            liste_machines.append([num_machine, etat_machine])


    if option == "all" or option == "up":
        string1 = "\n".join(machine[0] + "  " + machine[1] if machine[1] == "down" else machine[0] + "  " + machine[1] + "  " + str(machine[2]) + " " + machine[3] for machine in liste_machines[0:len(liste_machines) // 4])
        string2 = "\n".join(machine[0] + "  " + machine[1] if machine[1] == "down" else machine[0] + "  " + machine[1] + "  " + str(machine[2]) + " " + machine[3] for machine in liste_machines[len(liste_machines) // 4:len(liste_machines) // 2])
        string3 = "\n".join(machine[0] + "  " + machine[1] if machine[1] == "down" else machine[0] + "  " + machine[1] + "  " + str(machine[2]) + " " + machine[3] for machine in liste_machines[len(liste_machines) // 2:len(liste_machines) // 4 * 3])
        string4 = "\n".join(machine[0] + "  " + machine[1] if machine[1] == "down" else machine[0] + "  " + machine[1] + "  " + str(machine[2]) + " " + machine[3] for machine in liste_machines[len(liste_machines) // 4 * 3:len(liste_machines)])

        await ctx.channel.send(etat)
        await ctx.channel.send(string1)
        await ctx.channel.send(string2)
        await ctx.channel.send(string3)
        await ctx.channel.send(string4)
    elif option == "free":

        # bornage du nombre de machines à afficher entre 1 et 5
        if nb_machines_min > 5:
            nb_machines_min = 5
        elif nb_machines_min < 1:
            nb_machines_min = 1

        liste_min_users_machines = []
        for i in range(nb_machines_min):

            min_users_machine = ["", "up", 999]
            for machine in liste_machines:
                if machine[1] == "up":
                    min_users_machine = machine if machine[2] < min_users_machine[2] else min_users_machine
                    liste_machines.remove(machine)

            if min_users_machine[2] != 999:
                liste_min_users_machines.append(min_users_machine)

        if liste_min_users_machines:
            string1 = "Machines ayant le moins d'utilisateurs : \n" + "\n".join(machine[0] + "  " + str(machine[2]) + " " + machine[3] for machine in liste_min_users_machines)
        else:
            string1 = "Toutes les machines sont éteintes."
        await ctx.channel.send(string1)
bot.run(os.getenv("TOKEN"))
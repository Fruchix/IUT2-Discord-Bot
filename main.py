import discord
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv

import edt_utils.get_edt as ge


# récupération des variables contenues dans le fichier config
load_dotenv(dotenv_path="config")

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Bot opérationnel.")


@bot.event
async def on_message(message: discord.Message):
    if message.content == "Un hôtel ?" or message.content == "Un hotel ?":
        await message.add_reaction("🇹")
        await message.add_reaction("🇷")
        await message.add_reaction("🇮")
        await message.add_reaction("🇻")
        await message.add_reaction("🇦")
        await message.add_reaction("🇬")
        await message.add_reaction("🇴")

    await bot.process_commands(message)

@bot.command(name='edt')
async def send_edt_picture(ctx, sem_decal: int = 0, groupe_tp: str = ""):
    """Envoyer une image d'un agenda.
    Sélection de l'agenda du groupe voulu selon le rôle de la personne ou du paramètre donné.
    Sélection de la semaine voulue en prenant par défaut la semaine de travail dans laquelle on est/celle qui arrive si on est en week-end,
     possibilité de décaler cette semaine choisie via le paramètre sem_decal

    :param ctx: le contexte de la commande
    :param sem_decal: le nombre de semaine de décalage
    :param groupe_tp: le groupe de l'étudiant
    """
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
async def iut_system_load(ctx):
    data = requests.get("https://www-info.iut2.univ-grenoble-alpes.fr/intranet/informations/cellule-info/etat-stations.php")
    text = data.text

    etat = "État des stations linux le " + text.split("État le ")[1].split("<pre>")[0]

    listStations = text.split("<pre>")[1].split("</pre>")[0].splitlines()[1:]
    listStationsRecoupee = []

    for ligne in listStations:
        if ligne[40] == ",":
            listStationsRecoupee.append(ligne[:16] + "  " + ligne[33:40])
        else:
            listStationsRecoupee.append(ligne[:16] + "  " + ligne[33:39])

    string1 = "\n".join(ligne for ligne in listStationsRecoupee[0:len(listStationsRecoupee)//4])
    string2 = "\n".join(ligne for ligne in listStationsRecoupee[len(listStationsRecoupee) // 4:len(listStationsRecoupee) // 2])
    string3 = "\n".join(ligne for ligne in listStationsRecoupee[len(listStationsRecoupee) // 2:len(listStationsRecoupee) // 4 * 3])
    string4 = "\n".join(ligne for ligne in listStationsRecoupee[len(listStationsRecoupee) // 4 * 3:len(listStationsRecoupee)])

    await ctx.channel.send(etat)
    await ctx.channel.send(string1)
    await ctx.channel.send(string2)
    await ctx.channel.send(string3)
    await ctx.channel.send(string4)

bot.run(os.getenv("TOKEN"))
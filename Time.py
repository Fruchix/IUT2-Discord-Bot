import discord
from discord.ext import commands
import edt_utils.get_edt as ge

class Time(commands.Cog) :
    """Mets à disposition les commandes relatives à l'emploi du temps."""

    # attributs
    liste_groupes = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2", "S0"]      # groupes existants

    # constructeur
    def __init__(self, bot):
        self.bot = bot

    class MauvaisGroupe(Exception):
        """Exception pour nom de groupe non existant."""
        pass

    # méthodes de service
    def select_role(self, liste_roles):
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

    @commands.command()
    async def edt(self, ctx, arg_1=None, arg_2=None):
        """Envoyer l'image d'un agenda.

        :param arg_1: le nombre de semaines décalées ou le groupe_tp
        :param arg_2: le nombre de semaines décalées ou le groupe_tp
        :return: envoi de l'emploi du temps du groupe de tp pour la semaine en question
        """

        ##################################################
        # sélection du groupe de tp et de la semaine voulue

        # initialisation des variables contenant le groupe tp et le décalage de semaines à partir de la semaine actuelle
        groupe_tp = ""
        sem_decal = 0

        # si un premier argument a été renseigné, on cherche à savoir si cet argument est un groupe_tp ou une sem_decal
        if arg_1 != None:
            # essai de conversion du paramètre en entier,
            # si cela marche alors l'argument est une sem_decal,
            # sinon c'est un groupe_tp
            try:
                sem_decal = int(arg_1)
            except ValueError:
                groupe_tp = str(arg_1).upper()

        # si un deuxième argument est renseigné, on cherche à savoir si cet argument est un groupe_tp ou une sem_decal
        if arg_2 != None:
            # essai de conversion du paramètre en entier,
            # si cela marche alors l'argument est une sem_decal,
            # sinon c'est un groupe_tp
            try:
                sem_decal = int(arg_2)
            except ValueError:
                groupe_tp = str(arg_2).upper()

        # vérification de l'existence de la valeur du paramètre groupe_tp,
        # si le groupe n'existe pas alors envoi d'un message d'erreur et fin de la fonction
        if groupe_tp != "" and groupe_tp not in self.liste_groupes:
            await ctx.channel.send("Nom de groupe invalide.")
            return

        # si le groupe_tp n'a pas été passé en paramètre alors définition de celui ci
        if groupe_tp == "":
            # si la commande est entrée dans des messages privés
            # alors envoi d'un message d'erreur et fin de la fonction
            # sinon sélection automatique du rôle parmis les rôles de l'utilisateur via la méthode select_role(...) de cette classe
            if ctx.guild is None:
                await ctx.channel.send("Veuillez préciser le rôle et la semaine voulue.")
                return
            else :
                groupe_tp = self.select_role(ctx.author.roles)


        ##################################################
        # génération du fichier agenda.png via la fonction select_agenda(...) de get_edt
        ge.select_agenda(groupe_tp, sem_decal)

        ##################################################
        # envoi du fichier agenda.png
        with open('edt_utils/agenda.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture)


def setup(bot):
    return bot.add_cog(Time(bot))
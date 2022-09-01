import datetime

from ics import Calendar
import requests
import IUT2_Discord_Bot.edt.draw_edt as de


def load_edt(resources, first_date):
    """Récupérer un emploi du temps ADE (d'une semaine) sous format iCal et récupérer ses évènements dans une liste.

    :param resources: le numéro de l'argument resources, correspond à l'emploi du temps désiré.
    :type resources: integer
    :param first_date: le jour de début de semaine
    :type first_date: datetime.time

    :returns: une liste de listes. Chaque sous liste caractérise un évènement (un cours dans la semaine).
    Forme des sous listes : [date, heure_début, durée, salle, type_de_cours, numéro_ressource, nom_ressource, nom_prof, groupes participants]

    """
    # dictionnaire des paramètres de la requête récupérant le calendrier iCal. On utilise les paramètres de la fonction
    param_requete = {
        "resources" : resources,
        "firstDate" : first_date,
        "lastDate" : first_date + datetime.timedelta(4)
    }

    # requête récupérant le calendrier iCal, passage du dictionnaire param_requete en paramètres de l'URL
    r = requests.get("https://ade-uga-ro-vs.grenet.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?projectId=5&calType=ical", params=param_requete)
    # récupération du contenu du calendrier iCal
    edt_from_ical = Calendar(r.text)

    # initialisation d'une liste qui contiendra les cours de la semaine
    liste_cours = []

    # Parcours des évènements de l'objet calendrier edtCal.
    # Pour chaque évènement, ajout d'une liste à la liste des cours (évènements) listeCours.
    #
    # Format de la liste : [date, heure_début, durée, salle, type_de_cours, numéro_ressource, nom_ressource, nom_prof, [groupes participants]]
    #        type_de_cours : TP/TD/CM
    #        [groupes participants] : les noms des groupes présent à ce cours (ex: INFO2A1, INFO2D2)
    for event in list(edt_from_ical.events):

        # si la matière est une AA, il n'y a pas de prof ni de nom de matière, on remplace ces champs par une string vide
        # sinon, on récupère le nom de la ressource et le nom du prof
        if event.name.split(" ")[1] == 'AA':
            nom_ressource = ""
            nom_prof = ""
        else:
            nom_ressource = event.description.splitlines()[-3:-2][0]
            nom_prof = event.description.splitlines()[-2:-1][0]


        # l'ordre du nom de la ressource et du prof est parfois inversé dans l'agenda iCal, on fait donc une vérification
        # on compare donc le début de la string actuelle de nom_prof avec le numéro de ressource : on permute si cela correspond
        if nom_prof.startswith(str(event.name.split(" ")[0])[:4]):
            # permutation des valeurs de nom_ressource et nom_prof
            temp_string = nom_ressource
            nom_ressource = nom_prof
            nom_prof = temp_string


        # création de la liste contenant les éléments d'un cours
        # l'heure est initialement à UTC+0, donc modification à UTC+1
        new_cours = [event.begin.date(),
                    event.begin.to('Europe/Paris').time(),
                    event.duration,
                    event.location,
                    event.name.split(" ")[1],
                    event.name.split(" ")[0],
                    nom_ressource,
                    nom_prof,
                    event.description.splitlines()[2:-3]]


        #ajout de cette liste à la liste à la liste de cours (évènements)
        liste_cours.append(new_cours)

    return liste_cours


def affiche_liste_cours(liste):
    """Afficher les cours d'une liste de cours dans le terminal.

    :param liste: une liste de listes, où les sous-listes caractérisent des cours
    Les éléments caractérisant un cours sont affichés sur une même ligne.
    """
    for cours in liste:
        for element in cours:
            print(element, end='')
            print("    ", end="")


def select_current_semaine() -> datetime.date:
    """Sélectionner le premier jour de la semaine de travail dans laquelle on se trouve. Si on est en week-end, récupération du premier jour de la semaine suivante.

    :return: le premier d'une semaine de travail
    """
    # récupération du premier jour de la semaine actuelle
    deb_sem = datetime.date.today() - datetime.timedelta(datetime.date.today().weekday())

    # si l'on est en week-end, ajout de 7 jours
    if datetime.date.today().weekday() > 4:
        deb_sem = deb_sem + datetime.timedelta(7)

    return deb_sem

def select_semaine(nb_sem_decale: int) -> datetime.date:
    """Sélectionner la semaine voulue à partir de la semaine de travail actuelle. On décalle de nb_sem_decale semaines la semaine sélectionnée.

    :param nb_sem_decale: le nombre de semaines de décallage
    :return: la semaine voulue
    """
    sem_select = select_current_semaine() + datetime.timedelta(7 * nb_sem_decale)

    return sem_select

def get_agenda(id_groupe, nb_sem_decale: int):
    """Générer l'image de l'agenda et la sauver.
    L'image est créée pour le groupe nom_groupe à la semaine courante + nb_sem_decale

    :param id_groupe: le nom du groupe
    :param nb_sem_decale: le décalage de semaine
    :return:
    """
    # récupération des données de l'agenda iCal de ADE
    data = load_edt(id_groupe, select_semaine(nb_sem_decale))

    # détermination de l'heure de début du dernier cours
    cours_max = data[0][1]
    # parcours complet des cours et comparaisons des heures de début de cours
    for cours in data:
        if cours[1] > cours_max:
            cours_max = cours[1]

    # adapter la hauteur de la page à l'heure de début du dernier cours
    if cours_max > datetime.time(17, 0, 0, 0):
        y_max = 1700
    elif cours_max > datetime.time(16, 0, 0, 0):
        y_max = 1450
    else:
        y_max = 1200


    # initialisation de l'agenda
    current_agenda = de.initialize_agenda(1200, y_max, data)

    # dessin des cours
    de.draw_liste_cours(current_agenda, data)

    # sauvegarde de l'image
    current_agenda.save("edt/agenda.png")


# opérations de tests utilisés au long du développement de ce fichier
# ma_liste = load_edt(id_edt_groupe['A2'],select_semaine(-11))
# affiche_liste_cours(ma_liste)

# select_agenda("A2", 0)

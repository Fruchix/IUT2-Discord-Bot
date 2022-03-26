from ics import Calendar
import requests

# dictionnaire contenant les groupes de S2 et leur identifiant de "resources" dans l'url de ADE
# chaque identifiant désigne un emploi du temps
id_edt_groupe = {
    'A1' : 41821,
    'A2' : 41822,
    'B1' : 41824,
    'B2' : 41825,
    'C1' : 41827,
    'C2' : 41828,
    'D1' : 41830,
    'D2' : 41831
}


def load_edt(resources, first_date, last_date):
    """Récupérer un emploi du temps ADE sous format iCal et récupérer ses évènements dans une liste.

    :param resources: le numéro de l'argument resources, correspond à l'emploi du temps désiré.
    :type resources: integer
    :param first_date: le jour de début de semaine
    :type first_date: str
    :param last_date: le jour de fin de semaine (semaine de 5 jours de travail)
    :type last_date: str

    :returns: une liste de listes. Chaque sous liste caractérise un évènement (un cours dans la semaine).
    Forme des sous listes : [date, heure_début, durée, salle, type_de_cours, numéro_ressource, nom_ressource, nom_prof, groupes participants]

    """
    # dictionnaire des paramètres de la requête récupérant le calendrier iCal. On utilise les paramètres de la fonction
    param_requete = {
        "resources" : resources,
        "firstDate" : first_date,
        "lastDate" : last_date
    }

    # requête récupérant le calendrier iCal, passage du dictionnaire param_requete en paramètres de l'URL
    r = requests.get("https://ade-uga.grenet.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?projectId=1&calType=ical", params=param_requete)
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
        print()


# opérations de tests utilisés au long du développement de ce fichier
# ma_liste = load_edt(id_edt_groupe['A2'],"2022-03-21","2022-03-25")
# affiche_liste_cours(ma_liste)
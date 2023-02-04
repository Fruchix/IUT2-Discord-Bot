import requests
import datetime
import ics

from IUT2_Discord_Bot.edt.edt_utils import select_semaine, ical_to_list
from IUT2_Discord_Bot.edt.draw_agenda import draw_edt
from IUT2_Discord_Bot.data.manipulate_db import insert_liste_cours, read_liste_cours


def load_edt(resource: int, first_date: datetime.date):
    """Récupérer un emploi du temps ADE (d'une semaine) sous format iCal.

    :param resource: l'identifiant "resources" d'ADE
    :param first_date: le jour de début de semaine
    """

    # dictionnaire des paramètres de la requête récupérant le calendrier iCal. On utilise les paramètres de la fonction
    param_requete = {
        "resources": resource,
        "firstDate": first_date,
        "lastDate": first_date + datetime.timedelta(4)
    }

    # requête récupérant le calendrier iCal, passage du dictionnaire param_requete en paramètres de l'URL
    r = requests.get(
        "https://ade-uga-ro-vs.grenet.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?projectId=5&calType=ical",
        params=param_requete)

    # renvoit du calendrier iCal
    return ics.icalendar.Calendar(r.text)


def generate_agenda(resource: int, sem_decal: int) -> None:
    """
    Générer l'image d'un agenda et la sauver.

    :param resource: l'identifiant "resources" d'ADE
    :param sem_decal: le décalage de semaine à partir de celle actuelle
    """

    # ical_agenda = load_edt(resource, select_semaine(sem_decal))

    # liste_cours = ical_to_list(ical_agenda)


    # for cours in liste_cours:
    #    cours["id_edt"] = resource

    # insert_liste_cours(liste_cours=liste_cours)

    liste_cours = read_liste_cours(id_edt=resource)

    current_agenda = draw_edt(liste_cours=liste_cours)

    current_agenda.save("IUT2_Discord_Bot/resources/images/agenda.png")


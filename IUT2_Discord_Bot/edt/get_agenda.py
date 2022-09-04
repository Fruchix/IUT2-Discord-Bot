import requests
import datetime
import ics

from edt.edt_utils import select_semaine
from edt.draw_agenda import draw_edt


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


def generate_agenda(resource: int, sem_decal: int):
    """
    Générer l'image d'un agenda et la sauver.

    :param resource: l'identifiant "resources" d'ADE
    :param sem_decal: le décalage de semaine à partir de celle actuelle
    """

    ical_agenda = load_edt(resource, select_semaine(sem_decal))

    current_agenda = draw_edt(ical=ical_agenda)

    current_agenda.save("edt/agenda.png")


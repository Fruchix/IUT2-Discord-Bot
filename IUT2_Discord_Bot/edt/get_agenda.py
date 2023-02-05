import requests
import datetime
import ics


def load_ical(resource: int, first_date: datetime.date) -> ics.icalendar.Calendar:
    """Récupérer un emploi du temps ADE (d'une semaine) sous format iCal.
    Insère la liste des cours obtenus dans la base de données.

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

    ical_agenda = ics.icalendar.Calendar(r.text)

    # renvoit du calendrier iCal
    return ical_agenda

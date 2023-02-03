import sqlite3
import datetime
import ics
import requests
from IUT2_Discord_Bot.edt.edt_utils import select_semaine

# Connection object on the database
con = sqlite3.connect("../resources/edt.db")

# cursor object
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS salles_prov(nom, etage, batiment)")

data = []
for i in range(10):
    parametres = {
        "resources": 44676,
        "firstDate": select_semaine(-i),
        "lastDate": select_semaine(-i) + datetime.timedelta(4)
    }
    ical = ics.icalendar.Calendar(requests.get(
        "https://ade-uga-ro-vs.grenet.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?projectId=5&calType=ical",
        params=parametres
    ).text)

    # print("\n".join(["\n".join(str(event.location).split(",")) for event in ical.events]))

    etage_amphi = {
        'Amphi 1': 2,
        'Amphi 2': 1,
        'Amphi 3': 2
    }

    for cours in ical.events:
        for salle in cours.location.split(","):
            if not salle:
                break

            if salle[0:4] != "IUT2":
                break

            batiment = salle.split("-")[1]
            if batiment != "DG":
                break

            etage = salle.split("-")[2][0] if salle.split("-")[2][0] != 'A' else etage_amphi[salle.split("-")[2]]
            data.append((salle, etage, batiment))


cur.executemany("INSERT INTO salles_prov VALUES(?, ?, ?)", data)
con.commit()

cur.execute("CREATE TABLE IF NOT EXISTS salles_iut2(nom, etage, batiment, PRIMARY KEY(nom))")
cur.execute("INSERT INTO salles_iut2 SELECT DISTINCT * FROM salles_prov ORDER BY nom")
con.commit()

cur.execute("CREATE TABLE IF NOT EXISTS cours()")

con.close()

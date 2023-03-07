import sqlite3
import os
import ics
import requests
from datetime import datetime, timedelta, timezone

from IUT2_Discord_Bot.edt.edt_utils import id_edt_groupe, select_semaine, ical_to_list
from IUT2_Discord_Bot.edt.get_agenda import load_ical


def insert_ical(resource: int, ical_agenda: ics.icalendar.Calendar) -> bool:
    """Insérer un emploi du temps dans la base de données
    """

    if resource in id_edt_groupe.values():
        # transformation des données du fichier Ical en liste de dictionnaires, et ajout de l'identifiant de l'edt
        liste_cours = ical_to_list(ical_agenda)
        for cours in liste_cours:
            cours["id_edt"] = resource

        # insertion des cours dans la base de données
        return insert_liste_cours(liste_cours=liste_cours)
    else:
        liste_salles_occupees = ical_to_list(ical_agenda, short_format=True)
        return insert_liste_salles_occupees(liste_salles_occupees=liste_salles_occupees)


def insert_liste_cours(liste_cours: list[dict]) -> bool:
    """Insérer une liste de cours dans la base de données edt.db
    Chaque cours doit être représenté par un dictionnaire de la forme :

    {
        "id_edt": int,
        "titre": string,
        "profs": [str, str, ...],
        "groupes": [str, str, ..],
        "salles": [str, str, ...],
        "date_debut": datetime.datetime,
        "date_fin": datetime.datetime,
        "duree_event": datetime.timedelta
    }
    """

    # créer une liste de tuples à insérer en base de données
    data = [(
        cours["id_edt"],
        cours["titre"],
        ";".join(cours["profs"]),
        ";".join(cours["groupes"]),
        ";".join(cours["salles"]),
        str(cours["date_debut"]),
        str(cours["date_fin"]),
        str(cours["duree_event"])) for cours in liste_cours
    ]

    # se connecter à la base de données
    con = sqlite3.connect("IUT2_Discord_Bot/resources/edt.db")
    cursor = con.cursor()

    try:
        # insérer les données
        cursor.executemany("INSERT INTO cours values (?, ?, ?, ?, ?, ?, ?, ?)", data)
        con.commit()

        con.close()
        return True
    except:
        con.close()
        return False


def insert_liste_salles_occupees(liste_salles_occupees: list[dict]) -> bool:
    """Insérer une liste de cours dans la base de données edt.db
    Ces cours ne servent qu'à savoir si une salle est libre, donc le nombre d'informations est réduit.
    On ne peut pas se servir de ce type de cours pour dessiner un emploi du temps.

    Chaque cours doit être représenté par un dictionnaire de la forme :
    {
        "id_edt": int,
        "salles": [str, str, ...],
        "date_debut": datetime.datetime,
        "date_fin": datetime.datetime
    }
    """

    # créer une liste de tuples à insérer en base de données
    data = [(
        ";".join(cours["salles"]),
        str(cours["date_debut"]),
        str(cours["date_fin"])) for cours in liste_salles_occupees
    ]

    # se connecter à la base de données
    con = sqlite3.connect("IUT2_Discord_Bot/resources/edt.db")
    cursor = con.cursor()

    try:
        # insérer les données
        cursor.executemany("INSERT INTO salles_occupees values (?, ?, ?)", data)
        con.commit()

        con.close()
        return True
    except:
        con.close()
        return False


def read_liste_cours(id_edt: int, semaine_decal: int) -> list[dict]:
    """Lire une liste de cours dans la base de données edt.db
    Les cours sont identifiés par leur identifiant d'emploi du temps et la semaine demandée.

    Chaque cours doit être représenté par un dictionnaire de la forme :

    {
        "id_edt": int,
        "titre": string,
        "profs": [str, str, ...],
        "groupes": [str, str, ..],
        "salles": [str, str, ...],
        "date_debut": datetime.datetime,
        "date_fin": datetime.datetime,
        "duree_event": datetime.timedelta
    }
    """
    connect = sqlite3.connect("IUT2_Discord_Bot/resources/edt.db")
    cursor = connect.cursor()

    debut_semaine = select_semaine(nb_sem_decale=semaine_decal)
    fin_semaine = debut_semaine + timedelta(4)

    res = cursor.execute("SELECT * FROM cours where id_edt = ? and date(date_debut) >= ? and date(date_debut) <= ?",
                         [id_edt, str(debut_semaine), str(fin_semaine)])

    liste_cours = []
    for cours in res.fetchall():
        duree = datetime.strptime(cours[7], "%H:%M:%S")

        liste_cours.append({
            "titre": cours[1],
            "profs": cours[2].split(";"),
            "groupes": cours[3].split(";"),
            "salles": cours[4].split(";"),
            "date_debut": datetime.strptime(cours[5], "%Y-%m-%dT%H:%M:%S%z").astimezone(tz=timezone(timedelta(hours=1))),
            "date_fin": datetime.strptime(cours[6], "%Y-%m-%dT%H:%M:%S%z").astimezone(tz=timezone(timedelta(hours=1))),
            "duree_event": timedelta(hours=duree.hour, minutes=duree.minute, seconds=duree.second)
        })

    return liste_cours


def read_liste_salles_libres(heure_debut: datetime, temps_libre: timedelta) -> list:
    # Connection object on the database
    connect = sqlite3.connect("IUT2_Discord_Bot/resources/edt.db")

    # cursor object
    cursor = connect.cursor()

    # récupération des salles occupées sur le créneau demandé
    data = [
        heure_debut,
        heure_debut,
        heure_debut + temps_libre,
        heure_debut + temps_libre,
        heure_debut,
        heure_debut + temps_libre,
    ]

    # res = cursor.execute("SELECT DISTINCT salles FROM salles_occupees WHERE "
    #                      "(datetime(?) BETWEEN datetime(date_debut) AND datetime(date_fin)"
    #                      "OR datetime(?) BETWEEN datetime(date_debut) AND datetime(date_fin))"
    #                      "AND salles != ''", data)

    res = cursor.execute("SELECT DISTINCT salles FROM salles_occupees WHERE "
                         "(datetime(?) >= datetime(date_debut) AND datetime(?) < datetime(date_fin)"        # si l'heure de début est pendant un cours
                         "OR datetime(?) > datetime(date_debut) AND datetime(?) <= datetime(date_fin)"      # si l'heure de fin est pendant un cours
                         "OR datetime(?) <= datetime(date_debut) AND datetime(?) >= datetime(date_fin))"     # si l'heure de début est avant un cours et l'heure de fin après un cours
                         "AND salles != ''", data)

    liste_salles_occupees = []
    for salle in res.fetchall():
        for s in salle[0].split(";"):
            liste_salles_occupees.append(s)

    # récupération des salles de l'iut2
    res = cursor.execute("SELECT * from salles_iut2")

    liste_salles_iut2 = []
    for salle in res.fetchall():
        liste_salles_iut2.append([salle[0], salle[1], salle[2]])

    return [salle for salle in liste_salles_iut2 if salle[0] not in liste_salles_occupees]


def create_db():
    print("Creating database...")
    # Connection object on the database
    con = sqlite3.connect("IUT2_Discord_Bot/resources/edt.db")

    # cursor object
    cur = con.cursor()

    # drop all tables
    cur.execute("DROP TABLE IF EXISTS salles_prov")
    cur.execute("DROP TABLE IF EXISTS salles_iut2")
    cur.execute("DROP TABLE IF EXISTS cours")
    cur.execute("DROP TABLE IF EXISTS salles_occupees")

    print("Populating database...")
    # create new table and insert data
    cur.execute("CREATE TABLE salles_prov(nom, etage, batiment)")

    data = []
    for i in range(10):
        parametres = {
            "resources": 44676,
            "firstDate": select_semaine(-i),
            "lastDate": select_semaine(-i) + timedelta(4)
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

    cur.execute("CREATE TABLE salles_iut2(nom, etage, batiment, PRIMARY KEY(nom))")
    cur.execute("INSERT INTO salles_iut2 SELECT DISTINCT * FROM salles_prov ORDER BY nom")
    cur.execute("DROP TABLE salles_prov")
    con.commit()

    cur.execute(
        "CREATE TABLE cours(id_edt, titre, profs, groupes, salles, date_debut, date_fin, duree_event,"
        " PRIMARY KEY(id_edt, date_debut, date_fin))"
    ).execute(
        "CREATE TABLE salles_occupees(salles, date_debut, date_fin)"
    )
    con.commit()

    con.close()
    print("Database ready to use.")


def update_db():
    print("Updating database...")
    if not os.path.exists("IUT2_Discord_Bot/resources/edt.db"):
        create_db()

    connect = sqlite3.connect("IUT2_Discord_Bot/resources/edt.db")
    cursor = connect.cursor()

    for id_resource in id_edt_groupe.values():

        try:
            load_ical(id_resource, select_semaine(0))
        except:
            continue

        cursor.execute("DELETE FROM cours WHERE id_edt = ?", [id_resource])
        connect.commit()
        for semaine in range(-10, 10):
            insert_ical(resource=id_resource, ical_agenda=load_ical(id_resource, select_semaine(semaine)))

    cursor.execute("DELETE FROM salles_occupees")
    connect.commit()
    connect.close()

    resource_tout_iut = 44676
    try:
        insert_ical(resource=resource_tout_iut, ical_agenda=load_ical(resource_tout_iut, select_semaine(0)))
        print("Successfully updated salles_occupees")
    except:
        print("Update failed on salles_occupees")
    print("Update finished !")

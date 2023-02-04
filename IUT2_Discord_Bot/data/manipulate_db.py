import sqlite3
from datetime import datetime, timedelta, timezone
from IUT2_Discord_Bot.edt.edt_utils import select_semaine


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


def read_liste_cours(id_edt: int) -> list[dict]:
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

    debut_semaine = select_semaine(0)
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

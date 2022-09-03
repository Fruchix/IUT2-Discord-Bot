import datetime

# dictionnaires contenant les groupes et leur identifiant de "resources" dans l'url de ADE
# chaque identifiant désigne un emploi du temps
id_edt_groupe = {
    'BUT1 A1': 40435,
    'BUT1 A2': 40436,
    'BUT1 B1': 40437,
    'BUT1 B2': 40438,
    'BUT1 C1': 40439,
    'BUT1 C2': 40440,
    'BUT1 D1': 40441,
    'BUT1 D2': 40442,
    'BUT1 E1': 22510,
    'BUT1 E2': 22508,
    'BUT1 S0A1': 41200,
    'BUT1 S0A2': 41201,
    'BUT2 A11': 40450,
    'BUT2 A12': 40451,
    'BUT2 A21': 40452,
    'BUT2 A22': 40453,
    'BUT2 A31': 40454,
    'BUT2 A32': 40455,
    'BUT2 B11': 40456,
    'BUT2 B12': 40457,
    'LP ASSR': 40681,
    'LP AW': 40270,
    'LP BIG DATA': 41571,
    'LP SIMO': 41451
}
# dictionnaire des identifiants des rôles associés à des identifiants d'emploi du temps de groupe TP
id_edt_role = {
    994193894038327306: id_edt_groupe['BUT1 A1'],
    994193958924202025: id_edt_groupe['BUT1 A2'],
    994194055443517470: id_edt_groupe['BUT1 B1'],
    994194085009182730: id_edt_groupe['BUT1 B2'],
    994194108748931183: id_edt_groupe['BUT1 C1'],
    994194139954544661: id_edt_groupe['BUT1 C2'],
    994196538022711307: id_edt_groupe['BUT1 D1'],
    994196567252795503: id_edt_groupe['BUT1 D2'],
    1014167472867397722: id_edt_groupe['BUT1 E1'],
    1014167522364366949: id_edt_groupe['BUT1 E2'],

    1005431453800218664: id_edt_groupe['BUT2 A11'],
    1005431520384794636: id_edt_groupe['BUT2 A12'],
    1005431589787934744: id_edt_groupe['BUT2 A21'],
    1005431617038327808: id_edt_groupe['BUT2 A22'],
    1005431639050047508: id_edt_groupe['BUT2 A31'],
    1005431663569940570: id_edt_groupe['BUT2 A32'],
    1005431187961036800: id_edt_groupe['BUT2 B11'],
    1005431249885732924: id_edt_groupe['BUT2 B12']
}
# liste des groupes existants
liste_groupes = list(id_edt_groupe.keys())


def auto_select_edt(liste_roles):
    """Sélection de l'identifiant de l'edt ADE de l'utilisateur. Renvoit l'id de l'edt correspondant au rôle de TP de l'utilisateur.
    Normalement, un étudiant ne fait partie que d'un seul groupe de TP, il ne doit donc pas y avoir de problème.

    :param liste_roles: la liste des rôles de l'étudiant
    :return: l'identifiant de l'edt
    """
    for role in liste_roles:
        if role.id in list(id_edt_role.keys()):
            return id_edt_role[role.id]
    # si aucun rôle de l'utilisateur n'est dans la liste de rôles associés à des emplois du temps
    raise ValueError


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

import datetime

from PIL import Image, ImageDraw, ImageFont

global COURS_TEXT_COLOR
COURS_TEXT_COLOR = (54, 57, 62)

global CADRE_COLOR
CADRE_COLOR = (30, 33, 36)

global BG_AGENDA_COLOR
BG_AGENDA_COLOR = (255, 255, 255)

global BG_COURS_COLOR
BG_COURS_COLOR = (0, 180, 216, 200)
# (191, 210, 0)
# (0, 145, 173)
# (48, 199, 40, 200)


def initialize_agenda(size_x, size_y, liste_cours):
    """Initialiser une nouvelle image de taille size_x par size_y représentant l'agenda liste_cours.

    :param size_x: largeur voulue
    :param size_y: hauteur voulue
    :param liste_cours : la liste de cours à afficher dans l'agenda
    :return: l'image initialisée
    """
    # initialisation image
    agenda_picture = Image.new("RGB", (size_x, size_y), color=BG_AGENDA_COLOR)
    # déclaration d'un objet de dessin
    d = ImageDraw.Draw(agenda_picture,"RGB")

    # initialisation police
    myFont = ImageFont.truetype("edt/fonts/IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Medium.ttf", 20)

    # cadre : ligne verticale à gauche et ligne horizontale en haut
    d.line([75, 50, size_x, 50], fill=CADRE_COLOR, width=2)
    d.line([75, 50, 75, size_y], fill=CADRE_COLOR, width=2)

    # colonnes entre chaque jours
    for x_column in range(75, size_x, 225):
        d.line([x_column, 25, x_column, size_y], fill=CADRE_COLOR, width=2)

    # lignes horizontales de la pause pour manger 12:00 - 13:00
    d.line((75, 550, size_x, 550), fill=CADRE_COLOR, width=2)
    d.line((75, 675, size_x, 675), fill=CADRE_COLOR, width=2)

    heure = 8 # compteur de l'heure de la journée
    # affichage des heures
    for y_hour in range(35, size_y, 125):
        # pour un meilleur affichage, si l'heure est inférieure à 2 chiffres, on rajoute un "0" devant
        if heure < 10:
            string_heure = "0" + str(heure)
        else:
            string_heure = str(heure)
        # dessin de l'heure
        d.text((5, y_hour), string_heure + "h00", fill=CADRE_COLOR, font=myFont)
        # incrémentation de l'heure
        heure += 1

    # tirets horizontaux devant les heures
    for y_hour in range(50, size_y, 125):
        d.line((70, y_hour, 75, y_hour), fill=CADRE_COLOR, width=2)


    # calcul du premier jour de la semaine
    # on récupère la date du premier cours dans liste_cours et on soustrait alors la valeur du jour au numéro du jour
    # la valeur du jour vaut 0 à 6 respectivement de lundi à dimanche
    premier_jour = liste_cours[0][0] - datetime.timedelta(liste_cours[0][0].weekday())

    liste_jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]   # liste contenant les jours de la semaine
    liste_jours_indexe = 0  # indexe permettant de parcourir la liste des jours de la semaine

    # affichage des noms des jours de la semaine
    for x_jour in range(80, size_x, 225):
        d.text((x_jour, 22), liste_jours[liste_jours_indexe] + " " + str((premier_jour + datetime.timedelta(liste_jours_indexe)).day) + "/" + str((premier_jour + datetime.timedelta(liste_jours_indexe)).month), fill=CADRE_COLOR, font=myFont)
        liste_jours_indexe += 1

    return agenda_picture



def draw_cours(agenda_picture, cours):
    """Dessiner un cours sur l'image de l'agenda.

    :param agenda_picture: l'image de l'agenda  sur laquelle dessiner
    :param cours: le cours à dessiner
    """
    # déclaration d'un objet de dessin
    d = ImageDraw.Draw(agenda_picture, "RGBA")

    # initialisation police
    myFont = ImageFont.truetype("edt/fonts/IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Medium.ttf", 24)


    # détermination des coordonnées du cours grâce à la valeur du jour de la semaine, de l'heure du cours et de la durée

    # pour déterminer x0, on multiplie la valeur du jour de la semaine par la largeur d'une colonne (225px), et on rajoute la marge de gauche (75px)
    # exemple : si lundi, alors x0 = 0 * 225 + 75 = 75 ; si mardi, alors x0 = 1 * 225 + 75 = 300 ; etc
    x0 = cours[0].weekday() * 225 + 75

    # pour déterminer y0, on convertit l'heure et les minutes en flottant, auxquel on soustrait 8h, qu'on multiplie par la hauteur d'une cellule (125px), et on rajoute la marge supérieur (50px)
    # exemple : si heure vaut 08:00:00, alors y0 = (8 + 0/60 - 8) * 125 + 50 = 0 * 125 + 50 = 50 ; si heure vaut 13:30:00, alors y0 = (13 + 30/60 - 8) * 125 + 50 = 5.5 * 125 + 50 = 737.5
    y0 = (cours[1].hour + cours[1].minute/60 - 8) * 125 + 50

    # pour déterminer x1, on ajoute à x0 la largeur d'une colonne (225px) + 1px, ce pixel servant à maintenir l'esthétique de l'agenda (sinon, décalage des lignes verticales de 1 px)
    x1 = x0 + 226

    # pour déterminer y1, on ajoute à y0 la durée du cours en heure multipliée par la hauteur d'une cellule (125px) + 1px d'esthétisme
    # on extrait la durée du cours à partir d'un objet de format datetime.timestamp, grâce à la méthode .seconds, qui renvoit la durée en secondes
    # on convertit cette valeur en heure en divisant par 3600
    y1 = y0 + (cours[2].seconds/3600) * 125 +1


    # dessin d'un rectangle aux coordonnées du cours
    d.rectangle((x0, y0, x1, y1), fill=BG_COURS_COLOR, outline=CADRE_COLOR, width=2)


    # extraction du nom de la ressource (il contient en première position le numéro de la ressource, qui ne nous intéresse pas)
    nom_ressource = ""
    for text in str(cours[6]).split(" ")[1:]:
        nom_ressource += text + " "

    # extraction de la salle (nom trop long, simplification ; exemple : IUT2-DG-015 -> DG-015)
    salle = ""
    for lieu in str(cours[3]).split(","):
        salle += lieu.split("-")[-2] + " " + lieu.split("-")[-1] + "\n"
    # suppression du dernier retour à la ligne
    salle = salle[:-1]

    # extraction des noms des groupes de TP présents à ce cours
    if len(cours[-1]) > 6:
        groupes = "\nPromo"
    else:
        groupes = "\n"
        for nom_groupe in cours[-1]:
            groupes += nom_groupe[-2:] + " "

    # dessin des informations du cours (Ressource, Nom de la ressource, salle, type de cours)
    d.multiline_text(((x0+x1)/2, (y0+y1)/2), cours[5] + " " + cours[4] + "\n" + nom_ressource.capitalize() + "\n" + salle + groupes, fill=COURS_TEXT_COLOR, font=myFont, anchor="mm", align="center", spacing=10)


def draw_liste_cours(agenda_picture, liste_cours):
    """Dessiner la liste des cours sur l'image de l'agenda.

    :param agenda_picture: l'image de l'agenda sur laquelle dessiner
    :param liste_cours: la liste des cours à dessiner
    """
    # parcours complet de la liste des cours et dessin des cours via la méthode draw_cours(...)
    for cours in liste_cours:
        draw_cours(agenda_picture, cours)
import ics
import datetime
from PIL import Image, ImageDraw, ImageFont

COURS_TEXT_COLOR = (54, 57, 62)

CADRE_COLOR = (30, 33, 36)

BG_AGENDA_COLOR = (255, 255, 255)

BG_COURS_COLOR = (55, 196, 224)
# (191, 210, 0)
# (0, 145, 173)
# (48, 199, 40, 200)


def draw_event(agenda_picture, event: ics.icalendar.Event) -> None:
    """Dessiner un évènement (un cours) sur l'image de l'agenda.

    :param agenda_picture: l'image de l'agenda  sur laquelle dessiner
    :param event: l'évènement à dessiner
    """
    # récupération des données importantes à dessiner sur l'agenda
    titre = event.name
    profs = [p for p in event.description.split("\n") if
             not p.__contains__("INFO") and p != '' and not p.__contains__("Exporté")][1:]
    groupes = [g[5:] if g.__contains__("INFO1") or g.__contains__("INFO2") else g for g in event.description.split("\n")
               if g != '' and not g.__contains__("Exporté") and g not in profs][1:]
    salles = [s[5:] if s.__contains__("IUT2-") else s for s in
              event.location.split(",") if s != '']
    date_debut = event.begin
    duree_event = event.duration

    print("Description : " + str(event.description))
    print("Profs : " + str(profs))
    print("Groupes : " + str(groupes))

    # déclaration d'un objet de dessin
    d = ImageDraw.Draw(agenda_picture, "RGB")

    # initialisation police
    title_font = ImageFont.truetype("resources/fonts/IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Medium.ttf", 18)
    text_font = ImageFont.truetype("resources/fonts/IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Medium.ttf", 15)

    # détermination des coordonnées du cours grâce à la valeur du jour de la semaine, de l'heure du cours et de la durée

    # x0 : produit de la valeur du jour de la semaine et de la largeur d'une colonne (225px) + marge de gauche (75px)
    # exemple : si lundi, alors x0 = 0 * 225 + 75 = 75 ; si mardi, alors x0 = 1 * 225 + 75 = 300 ; etc
    x0 = date_debut.weekday() * 225 + 75

    # recalage des heures de début de cours à partir de 0 pour déterminer y0 ->
    # y0 : produit heure et hauteur d'une cellule (125px) + marge supérieur (50px)
    y0 = (date_debut.to('Europe/Paris').datetime.hour + date_debut.to('Europe/Paris').datetime.minute / 60 - 8) * 125 + 50

    # x1 : x0 + largeur colonne + 1 pixel d'esthétisme
    x1 = x0 + 226

    # y1 : y0 + la durée du cours en heure multipliée par la hauteur d'une cellule (125px) + 1px d'esthétisme
    y1 = y0 + (duree_event.seconds / 3600) * 125 + 1

    # dessin d'un rectangle aux coordonnées du cours
    d.rectangle((x0, y0, x1, y1), fill=BG_COURS_COLOR, outline=CADRE_COLOR, width=2)

    # dessin du titre tout en haut de la case
    d.text(xy=((x0+x1)/2, y0 + 0.28 * (y1 - y0)),
           text=titre,
           fill=COURS_TEXT_COLOR,
           font=title_font,
           anchor="mm"
           )

    # salles et profs sont à eux deux alignés au centre, si un des deux est vide alors on l'aligne tout court au centre
    decal_centre = 12 if salles != [] and profs != [] else 0

    # dessin des salles du cours
    # si plus de deux salles, alors affichage sur plusieurs lignes
    # sinon affichage sur une seule ligne
    if len(salles) > 2:
        d.text(xy=((x0 + x1) / 2, (y0 + y1) / 2 - decal_centre),
               text=("\n".join(salles[i] + ", " + salles[i+1] + ", " + salles[i+2]
                               for i in range(0, len(salles[:6])-2, 3))) + ", ..." if len(salles) > 6
               else ("\n".join(salles[i] + ", " + salles[i+1] + ", " + salles[i+2]
                               for i in range(0, len(salles)-2, 3))),
               fill=COURS_TEXT_COLOR,
               font=text_font,
               anchor="mm",
               align="center"
               )
    else:
        d.text(xy=((x0 + x1) / 2, (y0 + y1) / 2 - decal_centre),
               text=(", ".join(salles) if salles != [] else "")[:20],
               fill=COURS_TEXT_COLOR,
               font=title_font,
               anchor="mm",
               align="center"
               )

    # dessin des noms des profs du cours
    # s'il y a plus de 2 profs on ne les affiche pas
    d.text(xy=((x0 + x1) / 2, (y0 + y1) / 2 + decal_centre * len(profs)),
           text=("\n".join(prof[:24] + "..." if len(prof) > 24 else prof for prof in profs)
                 if profs != [] and len(profs) < 3 else ""),
           fill=COURS_TEXT_COLOR,
           font=text_font,
           anchor="mm",
           align="center"
           )

    # dessin des groupes du cours
    # si il y a plus de 4 groupes et que l'évènement dure plus d'1H alors affichage en grand  d'au maximum 8 groupes
    # sinon si l'évènement dure plus d'1H, alors affichage en grand de tous les groupes,
    # sinon affichage des groupes en petit (case trop petite)
    if len(groupes) > 4 and duree_event.seconds / 3600 > 1:
        d.text(xy=((x0 + x1) / 2, y1 - 0.15 * (y1-y0)),
               text=("\n".join(groupes[i] + ", " + groupes[i + 1] + ", " + groupes[i + 2] + ", " + groupes[i + 3]
                               for i in range(0, len(groupes[:8]) - 2, 4))) + ", ..." if len(groupes) > 8
               else ("\n".join(groupes[i] + ", " + groupes[i + 1] + ", " + groupes[i + 2] + ", " + groupes[i + 3]
                               for i in range(0, len(groupes) - 3, 4))),
               fill=COURS_TEXT_COLOR,
               font=text_font,
               anchor="mm",
               align="center"
               )
    elif duree_event.seconds / 3600 > 1:
        d.text(xy=((x0 + x1) / 2, y1 - 0.2 * (y1 - y0)),
               text=(", ".join(groupes) if groupes != [] else "")[:20],
               fill=COURS_TEXT_COLOR,
               font=title_font,
               anchor="mm",
               align="center"
               )
    else:
        d.text(xy=((x0 + x1) / 2, y1 - 0.1 * (y1-y0)),
               text=(", ".join(groupes) if groupes != [] else "")[:20],
               fill=COURS_TEXT_COLOR,
               font=text_font,
               anchor="mm",
               align="center"
               )


def draw_edt(ical: ics.icalendar.Calendar) -> Image:
    """
    Génère une image de l'emploi du temps ical fournit.
    Cet edt doit s'étendre sur une semaine de cours entière.

    :param ical:le calendrier au format ical
    :return: None
    """

    # détermination de l'heure de fin maximale d'un cours de cette semaine
    heure_fin_cours_max = max([e.end.to("Europe/Paris").datetime.hour +
                               e.end.to("Europe/Paris").datetime.minute / 60
                               for e in ical.events])

    # définition de la taille de l'image : plus l'heure de fin maximale d'un cours est grande plus l'image l'est aussi
    size_x = 1200
    size_y = int(125 * (heure_fin_cours_max - 8) + 75)

    # initialisation image
    agenda_picture = Image.new("RGB", (size_x, size_y), color=BG_AGENDA_COLOR)
    # déclaration d'un objet de dessin
    d = ImageDraw.Draw(agenda_picture, "RGB")

    # initialisation police
    myFont = ImageFont.truetype("resources/fonts/IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Medium.ttf", 20)

    # cadre : ligne verticale à gauche et ligne horizontale en haut
    d.line([75, 50, size_x, 50], fill=CADRE_COLOR, width=2)
    d.line([75, 50, 75, size_y], fill=CADRE_COLOR, width=2)

    # colonnes entre chaque jours
    for x_column in range(75, size_x, 225):
        d.line([x_column, 25, x_column, size_y], fill=CADRE_COLOR, width=2)

    # lignes horizontales de la pause pour manger 12:00 - 13:00
    d.line((75, 550, size_x, 550), fill=CADRE_COLOR, width=2)
    d.line((75, 675, size_x, 675), fill=CADRE_COLOR, width=2)

    # affichage des heures
    heure = 8  # compteur de l'heure de la journée
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

    # tirets horizontaux après les heures
    for y_hour in range(50, size_y, 125):
        d.line((70, y_hour, 75, y_hour), fill=CADRE_COLOR, width=2)

    # calcul du premier jour de la semaine
    # on récupère la date du premier cours dans liste_cours et on soustrait alors la valeur du jour au numéro du jour
    # la valeur du jour vaut 0 à 6 respectivement de lundi à dimanche
    premier_jour = [event for event in ical.events][0].begin - datetime.timedelta([event for event in ical.events][0].begin.weekday())

    liste_jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]  # liste contenant les jours de la semaine

    # affichage des noms des jours de la semaine
    for idx, jour in enumerate(liste_jours):
        d.text((80 + idx * 225, 22),
               jour + " " + str((premier_jour + datetime.timedelta(idx)).day) +
               "/" + str((premier_jour + datetime.timedelta(idx)).month),
               fill=CADRE_COLOR,
               font=myFont
               )

    for event in ical.events:
        draw_event(agenda_picture=agenda_picture, event=event)

    return agenda_picture

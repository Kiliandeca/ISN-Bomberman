
# Ce jeu a etait realiser dans le cadre du projet d ISN de Julien Falson et Kilian Decaderincourt au Lycee Lucie Aubrac de Bollene
# Pour toute informations ou question vous pouvez me contacter a l'adresse kilian@decaderincourt.fr

from tkinter import *   # Utilise pour interface graphique
import random           # Utilise pour le loot de bonus

fen = Tk()
fen.wm_title("Bomber man")


menu = True
position = 0

menu0 = PhotoImage(file="menu0.gif")
menu1 = PhotoImage(file="menu1.gif")
menu2 = PhotoImage(file="menu2.gif")
aide = PhotoImage(file="aide.gif")
joueur1gagne = PhotoImage(file="joueur1gagne.gif")
joueur2gagne = PhotoImage(file="joueur2gagne.gif")


def initmenu():

    global canva

    canva = Canvas(fen, width=388, height=448, bg="ivory")
    canva.pack()

    canva.focus_set()
    canva.bind("<Key>", clavier)

    affichermenu()


def affichermenu():

    canva.delete("all")

    if position == 0:
        canva.create_image(0, 0, image= menu0, anchor=NW)
    if position == 1:
        canva.create_image(0, 0, image= menu1, anchor=NW)
    if position == 2:
        canva.create_image(0, 0, image= menu2, anchor=NW)
    if position == 3:
        canva.create_image(0, 0, image= aide, anchor=NW)
    if position == 4:
        canva.create_image(0, 0, image= joueur1gagne, anchor=NW)
    if position == 5:
        canva.create_image(0, 0, image= joueur2gagne, anchor=NW)


def clavier(touche):

    touchestr = touche.keysym

    global menu

    if menu:
        global position

        if touchestr == "Up" or touchestr == "z":
            if 0 < position < 3:
                position -= 1
                affichermenu()

        if touchestr == "Down" or touchestr == "s":
            if position < 2:
                position += 1
                affichermenu()

        if touchestr == "Return":
            if position == 0:
                canva.destroy()
                menu = False
                iniaffichage()

            if position == 3 or position == 4 or position == 5:
                position = 0
                affichermenu()

            if position == 1:
                position = 3
                affichermenu()

            if position == 2:
                fen.destroy()




    else:

        # Direction 0 = deplacement vers le haut
        # Direction 1 = deplacement vers la droite
        # Direction 2 = deplacement vers le bas
        # Direction 3 = deplacement vers la gauche

        if touchestr == "z":
            j1.mouvement(0)

        if touchestr == "d":
            j1.mouvement(1)

        if touchestr == "s":
            j1.mouvement(2)

        if touchestr == "q":
            j1.mouvement(3)

        if touchestr == "o":
            j2.mouvement(0)

        if touchestr == "m":
            j2.mouvement(1)

        if touchestr == "l":
            j2.mouvement(2)

        if touchestr == "k":
            j2.mouvement(3)

        if touchestr == "a" and carte[j1.y][j1.x] == "v" and j1.nbombes > 0:
            # Comme il pose une bombe on retire son nombre de bombe posable de 1
            j1.nbombes -= 1
            # On initialise le decompte du joueur 1
            carte[j1.y][j1.x] = 20
            # On precise que le joueur pour la suite
            joueur = 1

        if touchestr == "i" and carte[j2.y][j2.x] == "v" and j2.nbombes > 0:
            j2.nbombes -= 1
            # On initialise le decomtpe du joueur 2
            carte[j2.y][j2.x] = 120
            joueur = 2

        if touchestr == "Escape":
            menu = True
            print("debug1")
            canva.destroy()
            affichagevie.destroy()
            affichageportee.destroy()
            affichagenbombes.destroy()

            initmenu()


        # Si le joueur marche sur un bonus on augmente ses caracteristique pour cette objet

        if carte[j1.y][j1.x] == "bp":
            j1.portee += 1
            carte[j1.y][j1.x] = "v"

        if carte[j2.y][j2.x] == "bp":
            j2.portee += 1
            carte[j2.y][j2.x] = "v"

        if carte[j1.y][j1.x] == "bv":
            j1.vie += 1
            carte[j1.y][j1.x] = "v"

        if carte[j2.y][j2.x] == "bv":
            j2.vie += 1
            carte[j2.y][j2.x] = "v"

        if carte[j1.y][j1.x] == "bb":
            j1.nbombes += 1
            carte[j1.y][j1.x] = "v"

        if carte[j2.y][j2.x] == "bb":
            j2.nbombes += 1
            carte[j2.y][j2.x] = "v"

        # on actualise la position des joueurs, cela permet une meilleur fluidite car on n'attend pas le prochain tour de la boucle qui peut allez jusqu'a 100ms


class Joueur:

        # Initialisation du joueur au debut de la partie
        # Celui-ci a plusieurs atributs qui lui son propre: sa position (x et y) sa vie, la portee de ses bombes et enfin le nombre de bombes qu'il peut poser

        def __init__(self, x, y, vie, portee, nbombes):
            self.x = x
            self.y = y
            self.vie = vie
            self.portee = portee
            self.nbombes = nbombes
            self.direction = 0

        # Permet de faire un mouvement au joueur

        def mouvement(self, direction):

            # Direction 0 = deplacement vers le haut
            # Direction 1 = deplacement vers la droite
            # Direction 2 = deplacement vers le bas
            # Direction 3 = deplacement vers la gauche

            # On utilise la varialbe temp pour l'optimisation afin de ne pas explorer la list plusieurs fois pour le meme resultat
            # temp correspond a la futur position theorique du joueur et on verifie si celle-ci n'est pas un bloc non traversable
            # "d" et "m" represente respectivement sur la carte les blocs destructibles et les murs indestructible
            # Si la position theorique demande est correct alors la position du joueur est mise a jour

            self.direction = direction

            if direction == 0 and self.y > 0:

                temp = carte[self.y - 1][self.x]

                if temp != "d" and temp != "m" and type(temp) != int:
                    self.y -= 1

            if direction == 1 and self.x < dimensionxcarte:

                temp = carte[self.y][self.x + 1]

                if temp != "d" and temp != "m" and type(temp) != int:
                    self.x += 1

            if direction == 2 and self.x < dimensionycarte:

                temp = carte[self.y + 1][self.x]

                if temp != "d" and temp != "m" and type(temp) != int:
                    self.y += 1

            if direction == 3 and self.x > 0:

                temp = carte[self.y][self.x - 1]

                if temp != "d" and temp != "m" and type(temp) != int:
                    self.x -= 1


def iniaffichage():

    global carte

    carte = [
    ["m", "m", "m", "m", "m", "m", "m", "m", "m", "m", "m", "m", "m"],
    ["m", "v", "v", "d", "d", "d", "d", "d", "d", "d", "d", "d", "m"],
    ["m", "v", "m", "d", "m", "d", "m", "d", "m", "d", "m", "d", "m"],
    ["m", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "m"],
    ["m", "d", "m", "d", "m", "d", "m", "d", "m", "d", "m", "d", "m"],
    ["m", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "m"],
    ["m", "d", "m", "d", "m", "d", "m", "d", "m", "d", "m", "d", "m"],
    ["m", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "m"],
    ["m", "d", "m", "d", "m", "d", "m", "d", "m", "d", "m", "d", "m"],
    ["m", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "m"],
    ["m", "d", "m", "d", "m", "d", "m", "d", "m", "d", "m", "v", "m"],
    ["m", "d", "d", "d", "d", "d", "d", "d", "d", "d", "v", "v", "m"],
    ["m", "m", "m", "m", "m", "m", "m", "m", "m", "m", "m", "m", "m"]]

    global dimensionxcarte, dimensionycarte

    # On enregistre les dimensions de la carte pour pouvoir s'en servir apres
    dimensionxcarte = len(carte[0])
    dimensionycarte = len(carte)

    global j1, j2

    # On creer les deux joueurs avec leurs coordonees et leurs caracteristiques (vie, portee et nombre de bombes)
    j1 = Joueur(1, 1, 3, 1, 1)
    j2 = Joueur(11, 11, 3, 1, 1)

    global blocdur, blocmou, bombe1, bombe2, bombe3, vide, persoA0, persoA1, persoA2, persoA3, persoB0, persoB1, persoB2, persoB3

    blocdur = PhotoImage(file="blocdur.gif")
    blocmou = PhotoImage(file="blocmou.gif")
    bombe1 = PhotoImage(file="bombe1.gif")
    bombe2 = PhotoImage(file="bombe2.gif")
    vide = PhotoImage(file="vide.gif")
    persoA0 = PhotoImage(file="persoA0.gif")
    persoA1 = PhotoImage(file="persoA1.gif")
    persoA2 = PhotoImage(file="persoA2.gif")
    persoA3 = PhotoImage(file="persoA3.gif")
    persoB0 = PhotoImage(file="persoB0.gif")
    persoB1 = PhotoImage(file="persoB1.gif")
    persoB2 = PhotoImage(file="persoB2.gif")
    persoB3 = PhotoImage(file="persoB3.gif")

    # Initialisation de tout les element de la fenetre pour la premiere fois
    # Les label qui affichent la vie, la portee des bombes du joueur et le nombre max de bombe presentes sur la carte

    global affichagevie, affichageportee, affichagenbombes

    affichagevie = Label(fen, text=('vie rouge: ' + str(j1.vie)+"        vie vert: " + str(j2.vie)))
    affichagevie.pack()

    affichageportee = Label(fen, text=('portee rouge: ' + str(j1.portee)+"        portee vert: " + str(j2.portee)))
    affichageportee.pack()

    affichagenbombes = Label(fen, text=('bombes rouge: ' + str(j1.nbombes)+"        bombes vert: " + str(j2.nbombes)))
    affichagenbombes.pack()

    # On initialise le canva sur lequel la carte sera dessine apres

    global canva

    canva = Canvas(fen, width=30*dimensionxcarte, height=30*dimensionycarte, bg="green")
    canva.pack()

    canva.focus_set()
    canva.bind("<Key>", clavier)

    # On lance l'affichage qui se reactualise en boucle toutes les 100ms
    affichercarte()


def affichercarte():

    global menu

    if not menu:
        # Cette fonction permet d'afficher la carte
        # On commence par suprimer tout ce qui se trouve sur le canva a chaque fois que l'on appele la methode

        canva.delete("all")

        # On met a jour les label d'indication

        affichagevie.config(text=('vie rouge: '+ str(j1.vie)+"        vie vert: "+ str(j2.vie)))
        affichageportee.config(text='portee rouge: '+ str(j1.portee)+"        portee vert: "+ str(j2.portee))
        affichagenbombes.config(text='nbombes rouge: '+ str(j1.nbombes)+"        nbombes vert: "+ str(j2.nbombes))

        # On marque la position de chaque joueur par un carre de differente couleur

        # On scan toute la liste afin d'ensuite representer chaque bloc

        for y in range(len(carte)):

            for x in range(len(carte[y])):

                # On utilise la variable case a des fin d'optimisation car on utilise souvent carte[y][x]

                case = carte[y][x]

                # les bombes sont represente dans la list par des nombres
                # le nombre represente le decompte avant l'explosion

                if type(case) == int:

                    # A chaque fois que la methode est appeler on diminue le decompte

                    if (0 < case < 3) or (100 < case < 103):
                        carte[y][x] = case-1

                        # Si la case est une bombe on affiche l'image pour la representer

                        canva.create_image(x*30, y*30, image=bombe2, anchor=NW)

                    if (3 <= case <= 20) or (103 <= case <= 120):
                        carte[y][x] = case-1

                        # Si la case est une bombe on affiche l'image pour la representer

                        canva.create_image(x*30, y*30, image=bombe1, anchor=NW)

                    # Comme les deux joueurs on des portees differentes pour leurs bombes il fallait les differencier
                    # le joueur 1 a son decompte qui va de 10 a 0 tandis que le joueur 2 a son decompte qui va de 110 a 100

                    if case == 0:
                        # Comme la bombe a exploser le joueur peut la reposer
                        j1.nbombes += 1
                        # La case est maintenant vide
                        carte[y][x] = "v"
                        # On appele la methode explosion en donnant comme info la position de la bombe et le joueur auquel elle appartient
                        explosion(x, y, 1)

                    if case == 100:
                        j2.nbombes += 1
                        carte[y][x] = "v"
                        explosion(x, y, 2)

                if case == "v":

                    canva.create_image(x*30, y*30, image=vide, anchor= NW)

                if case == "m":     # Mur indestructible

                    canva.create_image(x*30, y*30, image= blocdur, anchor= NW)

                if case == "d":     # Mur destructible

                    canva.create_image(x*30, y*30, image= blocmou, anchor= NW)

                if case == "bp":    # Bonus portee des bombes
                    canva.create_rectangle(x*30+5, y*30+5, x*30+30-5, y*30+30-5, fill="yellow")

                if case == "bv":    # Bonus vie
                    canva.create_rectangle(x*30+5, y*30+5, x*30+30-5, y*30+30-5, fill="red")

                if case == "bb":    # Bonus bombe max
                    canva.create_rectangle(x*30+5, y*30+5, x*30+30-5, y*30+30-5, fill="blue")

                direction = j1.direction

                if direction == 0 and not menu:
                    canva.create_image(j1.x*30, j1.y*30, image=persoA0, anchor= NW)
                elif direction == 1:
                    canva.create_image(j1.x*30, j1.y*30, image=persoA1, anchor= NW)
                elif direction == 2:
                    canva.create_image(j1.x*30, j1.y*30, image=persoA2, anchor= NW)
                elif direction == 3:
                    canva.create_image(j1.x*30, j1.y*30, image=persoA3, anchor= NW)

                direction = j2.direction

                if direction == 0 and not menu:
                    canva.create_image(j2.x*30, j2.y*30, image=persoB0, anchor= NW)
                elif direction == 1:
                    canva.create_image(j2.x*30, j2.y*30, image=persoB1, anchor= NW)
                elif direction == 2:
                    canva.create_image(j2.x*30, j2.y*30, image=persoB2, anchor= NW)
                elif direction == 3:
                    canva.create_image(j2.x*30, j2.y*30, image=persoB3, anchor= NW)


        # Si un des joueurs n'a plus de vie la partie s'arrete en lancant la methode mort

        if j1.vie == 0 or j2.vie == 0:
            mort()


        # Ceci est une des mecanique principal sur laquel le jeu se base, toute les 100 ms il actualise la carte en appelant la methode

        if not menu:

            fen.after(100, affichercarte)


def explosion(xbombe, ybombe, joueur):

    # Cette methode sert pour les explosions

    portee = 0

    # On commance par attribue la portee correspondante a la bombe

    if joueur == 1:
        portee = j1.portee

    if joueur == 2:
        portee = j2.portee

    # On verifie si un joueur est present sur la bombe et si c'est le cas il perd 1 point de vie

    if xbombe == j1.x and ybombe == j1.y:
        j1.vie -= 1

    if xbombe == j2.x and ybombe == j2.y:
        j2.vie -= 1

    # Explosion vers le bas

    for a in range(1, portee+1):

        if ybombe+a < dimensionycarte:

            if carte[ybombe+a][xbombe] == "d":
                loot(xbombe, ybombe+a)

            if ybombe+a == j1.y and xbombe == j1.x:
                j1.vie -= 1

            if ybombe+a == j2.y and xbombe == j2.x:
                j2.vie -= 1

            if carte[ybombe+a][xbombe] == "m":
                break

    # Explosion vers le haut

    for a in range(1, portee+1):

        if ybombe-a >= 0:

            if carte[ybombe-a][xbombe] == "d":
                loot(xbombe, ybombe-a)

            if ybombe-a == j1.y and xbombe == j1.x:
                j1.vie -= 1

            if ybombe-a == j2.y and xbombe == j2.x:
                j2.vie -= 1

            if carte[ybombe-a][xbombe] == "m":
                break

    # Explosion vers la droite

    for a in range(1, portee+1):

        if xbombe+a < dimensionxcarte:

            if carte[ybombe][xbombe+a] == "d":
                loot(xbombe+a, ybombe)

            if ybombe == j1.y and xbombe+a == j1.x:
                j1.vie -= 1

            if ybombe == j2.y and xbombe+a == j2.x:
                j2.vie -= 1

            if carte[ybombe][xbombe+a] == "m":
                break

    # Explosion vers la gauche

    for a in range(1, portee+1):

        if xbombe-a >= 0:

            if carte[ybombe][xbombe-a] == "d":
                loot(xbombe-a, ybombe)

            if ybombe == j1.y and xbombe-a == j1.x:
                j1.vie -= 1

            if ybombe == j2.y and xbombe-a == j2.x:
                j2.vie -= 1

            if carte[ybombe][xbombe-a] == "m":
                break


def loot(xcasedetruite, ycasedetruite):

    # Cette methode sert pour les bonus obtenus lors de la destruction de blocs

    alea = random.randint(1, 101)

    # 0.05 chance d avoir un bonus de portee

    if alea < 5:
        carte[ycasedetruite][xcasedetruite] = "bp"

    # 0.05 chance d avoir un bonus de vie

    elif alea < 10:
        carte[ycasedetruite][xcasedetruite] = "bv"

    # 0.1 chance d avoir un bonus de bombe

    elif alea < 25:
        carte[ycasedetruite][xcasedetruite] = "bb"

    else:
        carte[ycasedetruite][xcasedetruite] = "v"


def mort():

    global position, menu, canva

    menu = True

    if j1.vie == 0:
        print("mort joueur 1")
        position = 5

    if j2.vie == 0:
        print("mort joueur 2")
        position = 4

    canva.destroy()
    affichagevie.destroy()
    affichageportee.destroy()
    affichagenbombes.destroy()

    fen.after(100, initmenu)

initmenu()
fen.mainloop()

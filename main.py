# Code crée par Édouard Fortin-Lefrancois
# Tp3: Jeu de monstre

import arcade
import random
import os

# Titre et Size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Jeu de monstre"


class Monstre():
    """Classe qui crée des objects monstres avec une force et une image"""

    def __init__(self):
        # Pour joeur avec deux dé: self.force = random.randint(1, 11)
        self.force = random.randint(1, 5)
        # Prend une image aléatoire du fichier Monstres
        imgpath = "Images/Monstres"
        files = os.listdir(imgpath)
        self.imagePath = random.choice(files)


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.PURPLE_NAVY)

        self.doorlist = None
        self.enemyList = None
        self.monstre = None

        self.attackbutton = None
        self.runButton = None

        self.winText = None
        self.loseText = None

        self.background = None

        self.helpButton = None
        self.helpText = None

        self.exitButton = None
        self.exitText = None

        self.mouseX = 0
        self.mouseY = 0

        self.vie = 20
        self.victoires = 0

    def setup(self):
        """ Fonction qui initialise le jeu."""
        self.doorlist = arcade.SpriteList()
        self.enemyList = arcade.SpriteList()
        self.combat()
        self.background = arcade.load_texture("Images/Background.png")

        # Sprite du bouton Aide
        self.helpButton = arcade.Sprite("Images/Help_Button.png", 0.25)
        self.helpButton.center_x = 25
        self.helpButton.center_y = 740

        # Sprite du bouton Quitter
        self.exitButton = arcade.Sprite("Images/Exit_Button.png", 0.25)
        self.exitButton.center_x = 1000
        self.exitButton.center_y = 740

    def on_draw(self):
        """ Fonction qui render les images"""
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        # Les boutons help et exit sont toujours présent
        self.helpButton.draw()
        self.exitButton.draw()

        # Si le joeur n'est pas mort, en train de lire le text help ou en train de quitter, on peu dessiner le reste des images
        if not self.helpText and not self.exitText and self.vie > 0:
            # Dessine le nb de victoires et le nb de points de vie
            arcade.draw_text("Victoires:" + str(self.victoires), 100, 400, arcade.color.BLACK, 25)
            arcade.draw_text("PV:" + str(self.vie), 490, 720, arcade.color.BLACK, 25)

            # Si le monstre est présent, le joeur est en combat: On dessine la spritelist du monstre et les boutons attaque/fuir
            if self.monstre:
                self.enemyList.draw()
                arcade.draw_text("Force du\nMonstre:" + str(self.monstre.force), 825, 375, arcade.color.BLACK, 20,
                                 multiline=True, width=300)

                # Effect qui agrandi et raptise les boutons lorsque le curseur est dessus
                for i in self.attackbutton, self.runButton:
                    if i.collides_with_point((self.mouseX, self.mouseY)) and i.scale <= 0.26:
                        i.scale += 0.002

                    if not i.collides_with_point((self.mouseX, self.mouseY)) and i.scale > 0.25:
                        i.scale -= 0.002

                # Dessine les boutons attaque et run
                self.attackbutton.draw()
                self.runButton.draw()
                arcade.draw_text("Attaquer", 685, 40, arcade.color.BLACK, 15)
                arcade.draw_text("Fuir", 300, 40, arcade.color.BLACK, 15)

            # Dessine le text présent lorsque le joeur gagne
            if self.winText:
                arcade.draw_text(self.winText, 400, 500, arcade.color.BLACK, 20, multiline=True, width=1000)

            # Dessine le text présent lorsque le joeur perd
            if self.loseText:
                arcade.draw_text(self.loseText, 425, 600, arcade.color.BLACK, 20, multiline=True, width=1000)

            # Dessine les portes
            self.doorlist.draw()

        # Dessine le text d'aide si le joeur n'est pas mort ou en train de quitter
        if self.helpText and not self.exitText and self.vie > 0:
            arcade.draw_text(self.helpText, 225, 600, arcade.color.BLACK, 20, multiline=True, width=600)

        # Dessine le text losrque le joeur quitte
        if self.exitText:
            arcade.draw_text(self.exitText, 325, 400, arcade.color.BLACK, 20, multiline=True, width=600)

        # Dessine l'écran de mort
        if self.vie <= 0 and not self.exitText:
            arcade.draw_text("Vous êtes mort !\nVictoires: " + str(self.victoires), 325, 400, arcade.color.BLACK, 20,
                             multiline=True, width=600)

    def combat(self):
        """ Fonction qui est en charge des sprites reliés combat avec les monstres"""
        self.doorlist.clear()
        self.winText = None

        # Crée un nouveau monstre et un sprite de ce monstre
        self.monstre = Monstre()
        monstreSprite = arcade.Sprite("Images/Monstres/"+str(self.monstre.imagePath), 0.8)
        monstreSprite.center_x = 520
        monstreSprite.center_y = 375
        self.enemyList.append(monstreSprite)

        # Montrer le bouton d'attaque
        self.attackbutton = arcade.Sprite("Images/Bouton_Attaque.png", 0.25)
        self.attackbutton.center_x = 720
        self.attackbutton.center_y = 125

        # Montrer le bouton pour fuir
        self.runButton = arcade.Sprite("Images/Running_Button.png", 0.25)
        self.runButton.center_x = 320
        self.runButton.center_y = 125

    def porte(self):
        """Fonction qui en charge de créer les sprites de portes et d'enlever les boutons reliés au combat"""
        # Efface le monstre, le bouton attaque et le bouton fuir
        self.enemyList.clear()
        self.attackbutton = None
        self.runButton = None
        self.monstre = None

        # Crée deux sprites pour les portes
        for i in range(2):
            doorSprite = arcade.Sprite("Images/door.png", 0.8)
            if i == 0:
                doorSprite.center_x = 340
                doorSprite.center_y = 350

            if i == 1:
                doorSprite.center_x = 700
                doorSprite.center_y = 350
            self.doorlist.append(doorSprite)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """Fonction qui est en charge du fonctionnement des interactions avec le curseur (boutons, portes, ect)"""
        # Logique du combat quand le joeur appuye sur le bouton pour attaquer
        if self.attackbutton and self.attackbutton.collides_with_point((x, y)):
            self.loseText = None
            # La force d'attaque du joeur est un nombre aléatoire entre 1-6.
            # Pour jouer avec 2 dés: attaque = random.randint(1, 6) + random.randint(1, 6)
            attaque = random.randint(1, 6)
            # Si l'attaque du joeur est plus grande que la force du monstre, le joeur gagne
            # On ajoute + 1 aux victoires, on aujoute la force du monstre aux pv et on active la fonction Porte
            if attaque > self.monstre.force:
                self.winText = "Vous avez battu\nvotre adversaire\navec une puissance\nde " + str(attaque)
                self.victoires += 1
                self.vie += self.monstre.force
                self.porte()
            # Sinon, le joeur perd. On soustrait la force du monstre de ses PV et on n'active pas la fonction Porte
            else:
                self.loseText = "Vous avez roulé " + str(attaque) + "\nVous perdez -" + str(self.monstre.force) + "PV"
                self.vie -= self.monstre.force

        # Si le joeur appuye sur le bouton fuir, il pert 1 PV et on active la fonction Porte
        if self.runButton and self.runButton.collides_with_point((x, y)):
            self.vie -= 1
            self.porte()

        # Si le joeur appuye sur les portes, on recommence un combat
        if self.doorlist and arcade.get_sprites_at_point((x, y), self.doorlist):
            self.combat()

        # Si le joeur appuye sur le bouton aide et le text est déja présent, on le ferme.
        if self.helpButton and self.helpButton.collides_with_point((x, y)):
            if self.helpText:
                self.helpText = None
            else:
                # Sinon, on affiche le text d'aide
                self.helpText = "Pour réussir un combat, il faut que la valeur du dé lancé soit supérieure à la force de l’adversaire.  Dans ce cas, le niveau de vie de l’usager est augmenté de la force de l’adversaire.Une défaite a lieu lorsque la valeur du dé lancé par l’usager est inférieure ou égale à la force de l’adversaire.  Dans ce cas, le niveau de vie de l’usager est diminué de la force de l'adversaire. La partie se termine lorsque les points de vie de l’usager tombent sous 0.L’usager peut combattre ou éviter chaque adversaire, dans le cas de l’évitement, il y a une pénalité de 1 point de vie."

        # si le joeur appuye sur l'écran pendant que le text d'au revoir est présent, on ferme le jeu
        if self.exitText:
            arcade.exit()

        # si le joeur appuye sur le bouton pour quitter, on affiche le text d'au revoir
        if self.exitButton and self.exitButton.collides_with_point((x, y)):
            self.exitText = "                Au revoir !\n (clicker n'importe ou pour quitter)"

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """Fonction qui donne les coordonnés de la sourir a chaque fois que le joeur la bouge"""
        self.mouseX = x
        self.mouseY = y

#Crée une instance du jeu
window = MyGame()
window.setup()
arcade.run()

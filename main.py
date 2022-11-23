import arcade
import random

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Jeu de monstre"

class Monstre():
    def __init__(self):
        self.force = random.randint(1,5)
        self.imagePath = "Images/angry_cate.PNG"

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.PURPLE_NAVY)

        self.doorlist = None
        self.enemyList = None

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
        """ Set up the game here. Call this function to restart the game. """
        self.doorlist = arcade.SpriteList()
        self.enemyList = arcade.SpriteList()
        self.combat()
        self.background = arcade.load_texture("Images/Background.png")

        self.helpButton = arcade.Sprite("Images/Help_Button.png", 0.25)
        self.helpButton.center_x = 25
        self.helpButton.center_y = 740

        self.exitButton = arcade.Sprite("Images/Exit_Button.png", 0.25)
        self.exitButton.center_x = 1000
        self.exitButton.center_y = 740

    def on_draw(self):
        """ Fonction qui render les images"""
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        self.helpButton.draw()
        self.exitButton.draw()

        if not self.helpText and not self.exitText and self.vie > 0:
            arcade.draw_text("Victoires:" + str(self.victoires), 100, 400, arcade.color.BLACK, 25)
            arcade.draw_text("PV:" + str(self.vie), 490,720, arcade.color.BLACK, 25)

            if self.monstre:
                self.enemyList.draw()
                arcade.draw_text("Force du\nMonstre:" + str(self.monstre.force),825, 375, arcade.color.BLACK, 20, multiline=True, width=300)

            #Effect qui agrandi et raptise les boutons lorsque le curseur est dessus
                for i in self.attackbutton, self.runButton:
                    if i.collides_with_point((self.mouseX, self.mouseY)) and i.scale <= 0.26:
                        i.scale += 0.002

                    if not i.collides_with_point((self.mouseX, self.mouseY)) and i.scale > 0.25:
                        i.scale -= 0.002

                self.attackbutton.draw()
                self.runButton.draw()
                arcade.draw_text("Attaquer", 685, 40, arcade.color.BLACK, 15)
                arcade.draw_text("Fuir", 300, 40, arcade.color.BLACK, 15)

            if self.winText:
                arcade.draw_text(self.winText, 400, 500, arcade.color.BLACK, 20, multiline=True, width=1000)

            if self.loseText:
                arcade.draw_text(self.loseText, 425, 600, arcade.color.BLACK, 20, multiline=True, width=1000)

            if not self.helpText and not self.exitText:
                self.doorlist.draw()

        if self.helpText and not self.exitText and self.vie > 0:
            arcade.draw_text(self.helpText, 225, 600, arcade.color.BLACK, 20, multiline=True, width=600)

        if self.exitText:
            arcade.draw_text(self.exitText, 325, 400, arcade.color.BLACK, 20, multiline=True, width=600)

        if self.vie <= 0 and not self.exitText:
            arcade.draw_text("Vous êtes mort !\nVictoires: " + str(self.victoires), 325, 400, arcade.color.BLACK, 20, multiline=True, width=600)


    def combat(self):
        """ Fonction qui est en charge des sprites reliés combat avec les monstres"""
        self.doorlist.clear()
        self.winText = None

        self.monstre = Monstre()
        monstreSprite = arcade.Sprite(self.monstre.imagePath, 0.8)
        monstreSprite.center_x = 520
        monstreSprite.center_y = 375
        self.enemyList.append(monstreSprite)

        self.attackbutton = arcade.Sprite("Images/Bouton_Attaque.png", 0.25)
        self.attackbutton.center_x = 720
        self.attackbutton.center_y = 125

        self.runButton = arcade.Sprite("Images/Running_Button.png", 0.25)
        self.runButton.center_x = 320
        self.runButton.center_y = 125

    def porte(self):
        self.enemyList.clear()
        self.attackbutton = None
        self.runButton = None
        self.monstre = None

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
        """Fonction qui est en charge du fonctionnement des interactions avec le curseur (boutons, portes)"""
        if self.attackbutton and self.attackbutton.collides_with_point((x,y)):
            self.loseText = None
            attaque = random.randint(1,6)
            if attaque > self.monstre.force:
                self.winText = "Vous avez battu\nvotre adversaire\navec une puissance\nde " + str(attaque)
                self.victoires += 1
                self.vie += self.monstre.force
                self.porte()
            else:
                print("LOOSE")
                self.loseText = "Vous avez roulé " + str(attaque) + "\nVous perdez -" + str(self.monstre.force) + "PV"
                self.vie -= self.monstre.force

        if self.runButton and self.runButton.collides_with_point((x,y)):
            self.vie -= 1
            self.porte()

        if self.doorlist and arcade.get_sprites_at_point((x,y), self.doorlist):
            self.combat()

        if self.helpButton and self.helpButton.collides_with_point((x,y)):
            if self.helpText:
                self.helpText = None
            else:
                self.helpText = "Pour réussir un combat, il faut que la valeur du dé lancé soit supérieure à la force de l’adversaire.  Dans ce cas, le niveau de vie de l’usager est augmenté de la force de l’adversaire.Une défaite a lieu lorsque la valeur du dé lancé par l’usager est inférieure ou égale à la force de l’adversaire.  Dans ce cas, le niveau de vie de l’usager est diminué de la force de l'adversaire. La partie se termine lorsque les points de vie de l’usager tombent sous 0.L’usager peut combattre ou éviter chaque adversaire, dans le cas de l’évitement, il y a une pénalité de 1 point de vie."

        if self.exitText:
            arcade.exit()

        if self.exitButton and self.exitButton.collides_with_point((x,y)):
            self.exitText = "                Au revoir !\n (clicker n'importe ou pour quitter)"

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouseX = x
        self.mouseY = y

window = MyGame()
window.setup()
arcade.run()
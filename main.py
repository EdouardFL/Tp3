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
        self.helpButton = None
        self.background = None

        self.mouseX = 0
        self.mouseY = 0

        self.GameState = None

        self.vie = 20

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.doorlist = arcade.SpriteList()
        self.enemyList = arcade.SpriteList()
        self.combat()
        self.background = arcade.load_texture("Images/Background.png")

        self.helpButton = arcade.Sprite("Images/Help_Button.png", 0.25)
        self.helpButton.center_x = 1000
        self.helpButton.center_y = 725

    def on_draw(self):
        """ Fonction qui render les images"""
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        self.enemyList.draw()
        self.doorlist.draw()

        arcade.draw_text("PV:" + str(self.vie), 490,720, arcade.color.BLACK, 25)

        if self.monstre:
            arcade.draw_text("Force du\nMonstre:" + str(self.monstre.force),825, 375, arcade.color.BLACK, 20, multiline=True, width=300)

        #Effect qui agrandi et raptise les boutons lorsque le curseur est dessus
            for i in self.attackbutton, self.runButton, self.helpButton:
                if i.collides_with_point((self.mouseX, self.mouseY)) and i.scale <= 0.26:
                    i.scale += 0.002

                if not i.collides_with_point((self.mouseX, self.mouseY)) and i.scale > 0.25:
                    i.scale -= 0.002

            self.attackbutton.draw()
            self.runButton.draw()
            self.helpButton.draw()
            arcade.draw_text("Attaquer", 685, 40, arcade.color.BLACK, 15)
            arcade.draw_text("Fuir", 300, 40, arcade.color.BLACK, 15)

        if self.winText:
            arcade.draw_text(self.winText, 400, 500, arcade.color.BLACK, 20, multiline=True, width=1000)
        if self.loseText:
            arcade.draw_text(self.loseText, 425, 600, arcade.color.BLACK, 20, multiline=True, width=1000)

    def combat(self):
        """ Fonction qui est en charge des sprites reliés combat avec les monstres"""
        self.doorlist.clear()
        self.winText = None

        self.monstre = Monstre()
        monstreSprite = arcade.Sprite(self.monstre.imagePath)
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
            doorSprite = arcade.Sprite("Images/door.png")
            if i == 0:
                doorSprite.center_x = 320
                doorSprite.center_y = 325

            if i == 1:
                doorSprite.center_x = 720
                doorSprite.center_y = 325
            self.doorlist.append(doorSprite)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """Fonction qui est en charge du fonctionnement des interactions avec le curseur (boutons, portes)"""
        if self.attackbutton and self.attackbutton.collides_with_point((x,y)):
            self.loseText = None
            attaque = random.randint(1,6)
            if attaque > self.monstre.force:
                self.winText = "Vous avez battu\nvotre adversaire\navec une puissance\nde " + str(attaque)
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

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouseX = x
        self.mouseY = y


window = MyGame()
window.setup()
arcade.run()
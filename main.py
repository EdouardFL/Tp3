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
        arcade.set_background_color(arcade.color.AMAZON)

        self.doorlist = None
        self.enemyList = None
        self.attackbutton = None
        self.runButton = None

        self.mouseX = 0
        self.mouseY = 0

        self.GameState = None

        self.vie = 20

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.doorlist = arcade.SpriteList()
        self.enemyList = arcade.SpriteList()
        self.combat()

    def on_draw(self):
        """ Fonction qui render les images"""
        arcade.start_render()
        self.enemyList.draw()
        self.doorlist.draw()

        arcade.draw_text("PV:" + str(self.vie), 500,720, arcade.color.BLACK, 25)

        if self.monstre:
            arcade.draw_text("Force du\nMonstre:" + str(self.monstre.force),825, 375, arcade.color.BLACK, 20, multiline=True, width=300)

        #Effect qui agrandi et raptise les boutons lorsque le curseur est dessus
        if self.attackbutton and self.runButton:
            for i in self.attackbutton, self.runButton:
                if i.collides_with_point((self.mouseX, self.mouseY)) and i.scale <= 0.11:
                    i.scale += 0.002

                if not i.collides_with_point((self.mouseX, self.mouseY)) and i.scale > 0.1:
                    i.scale -= 0.002

            self.attackbutton.draw()
            self.runButton.draw()

    def combat(self):
        """ Fonction qui est en charge des sprites reliés combat avec les monstres"""
        self.doorlist.clear()

        self.monstre = Monstre()
        monstreSprite = arcade.Sprite(self.monstre.imagePath)
        monstreSprite.center_x = 520
        monstreSprite.center_y = 375
        self.enemyList.append(monstreSprite)

        self.attackbutton = arcade.Sprite("Images/white_die.png", 0.1)
        self.attackbutton.center_x = 520
        self.attackbutton.center_y = 125

        self.runButton = arcade.Sprite("Images/guy_running.png", 0.1)
        self.runButton.center_x = 220
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
                doorSprite.center_y = 375
            if i == 1:
                doorSprite.center_x = 720
                doorSprite.center_y = 375
            self.doorlist.append(doorSprite)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """Fonction qui est en charge du fonctionnement des interactions avec le curseur (boutons, portes)"""

        if self.attackbutton and self.attackbutton.collides_with_point((x,y)):
            attaque = random.randint(0,6)
            if attaque > self.monstre.force:
                print("WIN")
                self.porte()
            else:
                print("LOOSE")
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
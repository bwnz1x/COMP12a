import arcade
from pyglet.math import Vec2

#CONSTANTS
ScreenWidth = 900
ScreenHeight = 720
PlayerSpeed = 5
tile_size = 32


class Game(arcade.Window):
    def __init__(self):
        super().__init__(ScreenWidth, ScreenHeight, "Game Window")
        arcade.set_background_color(arcade.color.GREEN)
        self.set_mouse_visible(False)

        self.player_list = None
        self.player_sprite = None
        self.wall_list = None
        self.title_list

        self.camera_sprites = arcade.Camera(ScreenWidth, ScreenHeight)
        self.camera_gui = arcade.Camera(ScreenWidth, ScreenHeight)

    def setup(self):
        """LOAD MAPS AND SPRITES"""
        map = arcade.load_tilemap("", tile_size=tile_size)

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.title_list = arcade.SpriteList()

        # Load player sprite
        self.player_sprite = arcade.Sprite("tileset/sprite.png", scale=1)
        self.player_sprite.center_x = ScreenWidth // 2
        self.player_sprite.center_y = ScreenHeight // 2
        self.player_list.append(self.player_sprite)

        

class monster_melee(hp, atk, atk_speed):
    def __init__(self, hp, atk, atk_speed):
        self.hp = hp
        self.atk = atk
        self.atk_speed = atk_speed

    def attack(self):
        """ 
        Find where the player with LOS, walk towards them, and attack.
        Attack by getting the player within range and dealing damage after a delay. If the player is not within range, walk towards them.

        """
        # get player position
        # get enemy self position
        
        pass

    
class monster_ranged(hp, atk, projectile_speed):
    """Find player with LOS, attack after a few seconds."""
    def __init__(self, hp, atk, projectile_speed):
        self.hp = hp
        self.atk = atk
        self.projectile_speed = projectile_speed

    def attack(self):
        """ 
        Find where the player with LOS, attack after a few seconds.
        Attack by shooting a projectile towards the player.
        """
        pass

class monster_boss(hp, atk):
    



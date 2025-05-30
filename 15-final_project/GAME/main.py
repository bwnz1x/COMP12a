import arcade

#CONSTANTS
ScreenWidth = 900
ScreenHeight = 720
PlayerSpeed = 5



class Game(arcade.Window):
    def __init__(self):
        super().__init__(ScreenWidth, ScreenHeight, "Game Window")
        arcade.set_background_color(arcade.color.BLACK)
        self.set_mouse_visible(False)

    def setup(self):
        """LOAD MAPS AND SPRITES"""
        pass    


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
    



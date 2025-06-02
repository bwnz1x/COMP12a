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
        self.title_list = None
        self.title_map = None

        self.camera_sprites = arcade.Camera(ScreenWidth, ScreenHeight)
        self.camera_gui = arcade.Camera(ScreenWidth, ScreenHeight)

        # Add a set to track pressed keys
        self.pressed_keys = set()

    def setup(self):
        """LOAD MAPS AND SPRITES"""

        # Load the tile map first
        self.title_map = arcade.load_tilemap("tileset/TESTWALL_RAYCAST.json")

        # Then access its sprite lists
        self.wall_list = self.title_map.sprite_lists["Walls"]

        self.player_list = arcade.SpriteList()

        # Load player sprite
        self.player_sprite = arcade.Sprite("tileset/character.png", scale=1)
        self.player_sprite.center_x = ScreenWidth // 2
        self.player_sprite.center_y = ScreenHeight // 2
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """DRAW EVERYTHING"""
        self.clear()
        self.camera_sprites.use()
        self.wall_list.draw()
        self.player_list.draw()

        # Draw GUI
        self.camera_gui.use()
        arcade.draw_text("Player Position: " + str(self.player_sprite.position), 10, 10, arcade.color.WHITE, 12)
    def on_update(self, delta_time):
        """UPDATE EVERYTHING"""
        self.player_list.update()
        self.player_sprite.update()

        # Handle player movement
        self.handle_player_movement()
        

    def on_key_press(self, key, modifiers):
        """Called when a key is pressed."""
        self.pressed_keys.add(key)

    def on_key_release(self, key, modifiers):
        """Called when a key is released."""
        self.pressed_keys.discard(key)

    def handle_player_movement(self):
        """Handle player movement based on key presses."""
        if arcade.key.LEFT in self.pressed_keys:
            self.player_sprite.change_x = -PlayerSpeed
        elif arcade.key.RIGHT in self.pressed_keys:
            self.player_sprite.change_x = PlayerSpeed
        else:
            self.player_sprite.change_x = 0

        if arcade.key.UP in self.pressed_keys:
            self.player_sprite.change_y = PlayerSpeed
        elif arcade.key.DOWN in self.pressed_keys:
            self.player_sprite.change_y = -PlayerSpeed
        else:
            self.player_sprite.change_y = 0


# # class monster_melee(hp, atk, atk_speed):
#     def __init__(self, hp, atk, atk_speed):
#         self.hp = hp
#         self.atk = atk
#         self.atk_speed = atk_speed

#     def attack(self):
#         """ 
#         Find where the player with LOS, walk towards them, and attack.
#         Attack by getting the player within range and dealing damage after a delay. If the player is not within range, walk towards them.

#         """
#         # get player position
#         # get enemy self position
        
#         pass

    
# # class monster_ranged(hp, atk, projectile_speed):
#     """Find player with LOS, attack after a few seconds."""
#     def __init__(self, hp, atk, projectile_speed):
#         self.hp = hp
#         self.atk = atk
#         self.projectile_speed = projectile_speed

#     def attack(self):
#         """ 
#         Find where the player with LOS, attack after a few seconds.
#         Attack by shooting a projectile towards the player.
#         """
#         pass

# # class monster_boss(hp, atk):
    


def main():
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
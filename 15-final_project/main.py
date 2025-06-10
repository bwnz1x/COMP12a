# import libraries
import arcade
from pyglet.math import Vec2
import math

#CONSTANTS
ScreenWidth = 1280
ScreenHeight = 720
tile_size = 32
CameraSpeed = 0.1

# class for processing player sprite
class Player(arcade.Sprite):
    def __init__(self, image, scale, hp, atk, spd, window):
        super().__init__(image, scale)
        self.hp = hp
        self.atk = atk
        self.spd = spd
        self.window = window  # Store a reference to the Game instance

        # Ammo attributes
        self.ammo = 10  # Current ammo
        self.max_ammo = 10  # Maximum ammo capacity
        self.reload_time = 2.0  # Time to reload in seconds
        self.reloading = False  # Boolean to track if reloading is in progress

    def player_gun(self, target_x, target_y):
        """Player main weapon, a gun that shoots bullets."""
        if self.reloading:
            return  # Cannot shoot while reloading

        if self.ammo > 0:
            # Calculate direction to the target
            direction = Vec2(target_x - self.center_x, target_y - self.center_y).normalize()
            # Create a new projectile
            projectile = Projectile("tileset/playerprojectile.png", scale=1, speed=10, direction=(direction.x, direction.y))
            projectile.center_x = self.center_x
            projectile.center_y = self.center_y
            # Add the projectile to the game's projectile list
            self.window.projectile_list.append(projectile)
            self.ammo -= 1  # Decrease ammo count
        

    def reload(self):
        """Reload the player's weapon."""
        if not self.reloading:
            self.reloading = True
            arcade.schedule(self.finish_reload, self.reload_time)

    def finish_reload(self, delta_time):
        """Finish reloading and reset ammo."""
        self.ammo = self.max_ammo
        self.reloading = False
        arcade.unschedule(self.finish_reload)

    def player_melee(self):
        """If there is an enemy in range, attack with melee weapon."""
        # check if there is an enemy in range
        # if arcade.check_for_collision_with_list(self, self.enemy_list):
        pass
    def player_gernade(self):
        """Press a key to throw a grenade."""
        pass

class Projectile(arcade.Sprite):
    def __init__(self, image, scale, speed, direction):
        super().__init__(image, scale)
        self.speed = speed
        self.change_x = direction[0] * speed
        self.change_y = direction[1] * speed

class Game(arcade.Window):
    def __init__(self):
        # Dynamically get the monitor's resolution
        global ScreenWidth, ScreenHeight
        ScreenWidth, ScreenHeight = arcade.get_display_size()
        super().__init__(ScreenWidth, ScreenHeight - 100, "Game Window")
        arcade.set_background_color(arcade.color.DARK_GREEN)


        self.player_list = None
        self.enemy_list = None
        self.player_sprite = None
        self.wall_list = None
        self.title_list = None
        self.title_map = None

        self.camera_sprites = arcade.Camera(ScreenWidth, ScreenHeight)
        self.camera_gui = arcade.Camera(ScreenWidth, ScreenHeight)

        # Add a set to track pressed keys
        self.pressed_keys = set()
        self.paused = False  # Track pause state
        self.projectile_list = arcade.SpriteList()  # List to manage projectiles

    def setup(self):
        """LOAD MAPS AND SPRITES"""

        # Load the tile map first
        self.title_map = arcade.load_tilemap("tileset/map1.json")

        # Then access its sprite lists
        self.wall_list = self.title_map.sprite_lists["Walls"]
        self.floor_list = self.title_map.sprite_lists["Floor"]

        self.player_list = arcade.SpriteList()

        # Load player sprite
        self.player_sprite = Player("tileset/character.png", scale=1.5, hp=100, atk=10, spd=2, window=self)
        self.player_sprite.center_x = 60
        self.player_sprite.center_y = 350
        self.player_list.append(self.player_sprite)

        # test enemy sprite
        # Dynamically set spawn points for the monster
        spawn_x, spawn_y = 300, 400  # Example spawn location
        self.enemy1_sprite = monster_melee("tileset/enemy1.png", scale=1, hp=100, atk=10, atk_speed=3, spawn_x=spawn_x, spawn_y=spawn_y)
        self.player_list.append(self.enemy1_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_draw(self):
        """DRAW EVERYTHING"""
        self.clear()
        self.camera_sprites.use()
        self.wall_list.draw()
        self.floor_list.draw()
        self.player_list.draw()
        self.enemy1_sprite.draw()
        self.projectile_list.draw()  # Draw projectiles

        # Draw GUI
        self.camera_gui.use()
        arcade.draw_text("Player Position: " + str(self.player_sprite.position), 10, 10, arcade.color.WHITE, 12)
        arcade.draw_text(f"Player HP: {self.player_sprite.hp}", 10, 50, arcade.color.WHITE, 12)
        arcade.draw_text(f"Ammo: {self.player_sprite.ammo}/{self.player_sprite.max_ammo}", 10, 70, arcade.color.WHITE, 12)
        if self.player_sprite.ammo == 0 and not self.player_sprite.reloading:
            arcade.draw_text("Out of Ammo! Press R to Reload", 10, 100, arcade.color.RED, 12)
        if self.player_sprite.reloading:
            arcade.draw_text("Reloading...", 10, 90, arcade.color.RED, 12)

        # Draw pause menu if paused
        if self.paused:
            # Draw a semi-transparent overlay
            arcade.draw_rectangle_filled(
                ScreenWidth // 2, ScreenHeight // 2,
                ScreenWidth, ScreenHeight,
                (0, 0, 0, 150)
            )
            arcade.draw_text("PAUSED", ScreenWidth // 2 - 50, ScreenHeight // 2, arcade.color.WHITE, 24)
            arcade.draw_text("Press ESC to Resume", ScreenWidth // 2 - 100, ScreenHeight // 2 - 40, arcade.color.WHITE, 18)

    def on_update(self, delta_time):
        """UPDATE EVERYTHING"""
        if self.paused:
            return  # Skip updates when paused

        self.player_list.update()
        self.player_sprite.update()
        self.projectile_list.update()  # Update projectiles

        # Remove projectiles that go off-screen
        for projectile in self.projectile_list:
            if (projectile.center_x < 0 or projectile.center_x > ScreenWidth or
                projectile.center_y < 0 or projectile.center_y > ScreenHeight):
                projectile.remove_from_sprite_lists()

        # Call the monster's attack method
        self.enemy1_sprite.check_line_of_sight(self.player_sprite, self.wall_list)

        # Handle player movement
        self.handle_player_movement()

        # Update the camera to follow the player
        self.physics_engine.update()
        self.scroll_to_player()

    def on_mouse_press(self, x, y, button, modifiers):
        """Called when the mouse is pressed."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player_sprite.player_gun(x, y)

    def scroll_to_player(self):
        position = Vec2(self.player_sprite.center_x - self.width / 2,
                        self.player_sprite.center_y - self.height / 2)
        self.camera_sprites.move_to(position, CameraSpeed)
# movement here
    def on_key_press(self, key, modifiers):
        """Called when a key is pressed."""
        if key == arcade.key.ESCAPE:
            self.paused = not self.paused  # Toggle pause state
        elif key == arcade.key.R:
            self.player_sprite.reload()  # Trigger reload
        else:
            self.pressed_keys.add(key)

    def on_key_release(self, key, modifiers):
        """Called when a key is released."""
        self.pressed_keys.discard(key)

    def handle_player_movement(self):
        """Handle player movement based on key presses."""
        if arcade.key.LEFT in self.pressed_keys:
            self.player_sprite.change_x = self.player_sprite.spd * -1
        elif arcade.key.RIGHT in self.pressed_keys:
            self.player_sprite.change_x = self.player_sprite.spd
        else:
            self.player_sprite.change_x = 0

        if arcade.key.UP in self.pressed_keys:
            self.player_sprite.change_y = self.player_sprite.spd
        elif arcade.key.DOWN in self.pressed_keys:
            self.player_sprite.change_y = self.player_sprite.spd * -1
        else:
            self.player_sprite.change_y = 0


class monster_melee(arcade.Sprite):
    def __init__(self, image, scale, hp, atk, atk_speed, spawn_x, spawn_y):
        super().__init__(image, scale)
        self.hp = hp
        self.atk = atk
        self.atk_speed = atk_speed
        self.center_x = spawn_x
        self.center_y = spawn_y

    def check_line_of_sight(self, player_sprite, wall_list):
        los_check = arcade.has_line_of_sight(
            (self.center_x, self.center_y),
            (player_sprite.center_x, player_sprite.center_y),
            wall_list
        )
        if los_check:
            self.attack(player_sprite)  # Pass player_sprite to attack
        else:
            # Stop the monster's movement when LOS is lost
            self.change_x = 0
            self.change_y = 0

    def attack(self, player_sprite):
        """
        Find where the player is, walk towards them, and attack.
        """
        # Walk towards the player
        direction = Vec2(
            player_sprite.center_x - self.center_x,
            player_sprite.center_y - self.center_y).normalize()
        self.change_x = direction.x * self.atk_speed
        self.change_y = direction.y * self.atk_speed

        # Check if within attack range
        distance = math.sqrt(
            (self.center_x - player_sprite.center_x) ** 2 +
            (self.center_y - player_sprite.center_y) ** 2)
        if distance <= 15:
            # Attack the player
            player_sprite.hp -= self.atk
    
    def death(self):
        """Handle monster death"""
        if self.hp <= 0:
            self.remove_from_sprite_lists()





    
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
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
class Player(arcade.AnimatedTimeBasedSprite):
    def __init__(self, image, scale, hp, atk, spd, window):
        super().__init__()
        self.hp = hp
        self.atk = atk
        self.spd = spd
        self.window = window  # Store a reference to the Game instance

        # Ammo attributes
        self.ammo = 50  # Current ammo
        self.max_ammo = 50  # Maximum ammo capacity
        self.reload_time = 2.0  # Time to reload in seconds
        self.reloading = False  # Boolean to track if reloading is in progress

        self.invincible = False  # Boolean to track if the player is invincible
        self.scale = scale
        self.load_idle_frames()

    def load_idle_frames(self):
        self.frames.clear()
        texture = arcade.load_texture("tileset/sprite.png", 0, 0, 32, 32)
        anim = arcade.AnimationKeyframe(0, 250, texture)
        self.frames.append(anim)
        self.texture = texture  # Ensure texture is set for collisions
        self.cur_frame_idx = 0  # Reset frame index

    def set_direction_frames(self, direction):
        self.frames.clear()
        if direction == "up":
            y = 32
        elif direction == "down":
            y = 0
        elif direction == "left":
            y = 64
        elif direction == "right":
            y = 96
        else:
            y = 0
        for i in range(4):
            texture = arcade.load_texture("tileset/sprite.png", i * 32, y, 32, 32)
            anim = arcade.AnimationKeyframe(i, 150, texture)
            self.frames.append(anim)
        if self.frames:
            self.texture = self.frames[0].texture  # Ensure texture is set for collisions
        self.cur_frame_idx = 0  # Reset frame index

    def player_gun(self, target_x, target_y):
        """Player main weapon, a gun that shoots bullets."""
        if self.reloading:
            return  # Cannot shoot while reloading

        if self.ammo > 0:
            # Transform mouse coordinates to world coordinates relative to the camera
            camera_x, camera_y = self.window.camera_sprites.position
            world_mouse_x = target_x + camera_x
            world_mouse_y = target_y + camera_y

            # Calculate the angle to the target 
            dx = world_mouse_x - self.center_x
            dy = world_mouse_y - self.center_y
            angle = math.atan2(dy, dx)

            # Calculate direction vector from the angle
            direction_x = math.cos(angle)
            direction_y = math.sin(angle)

            # Create a new projectile
            projectile = Projectile("tileset/playerprojectile.png", scale=1, speed=10, direction=(direction_x, direction_y))
            projectile.center_x = self.center_x
            projectile.center_y = self.center_y

            # Rotate the projectile to match its direction
            projectile.angle = math.degrees(angle)

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

    def remove_invincibility(self, delta_time):
        """Remove the player's invincibility state."""
        self.invincible = False

    def update_animation(self, delta_time: float = 1/60):
        if self.frames:
            super().update_animation(delta_time)
        else:
            self.load_idle_frames()

class Projectile(arcade.Sprite):
    def __init__(self, image, scale, speed, direction):
        super().__init__(image, scale)
        self.speed = speed
        self.change_x = direction[0] * speed
        self.change_y = direction[1] * speed

class Game(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_list = None
        self.enemy_list = None
        self.player_sprite = None
        self.wall_list = None
        self.title_list = None
        self.title_map = None

        # Add a set to track pressed keys
        self.pressed_keys = set()
        self.paused = False  # Track pause state
        self.projectile_list = arcade.SpriteList()  # List to manage projectiles
        self.health_refill_list = arcade.SpriteList()  # List to manage health refills

        # Dash ability variables
        self.dash_cooldown = 0.0
        self.dash_cooldown_max = 5.0
        self.dash_distance = 120  # How far the dash moves the player
        self.dash_speed = 20  # Dash speed multiplier
        self.dashing = False
        self.dash_direction = (0, 0)
        self.dash_time = 0.15  # Dash duration in seconds
        self.dash_timer = 0.0

        # Track if boss has been spawned
        self.boss_spawned = False
        self.boss_sprite = None

        # Game over and win state
        self.game_over = False
        self.game_win = False
        self.restart_requested = False

        self.money = 500  # Start with 500 money

    def setup(self):
        """LOAD MAPS AND SPRITES"""

        # Load the tile map first with spatial hashing enabled
        self.title_map = arcade.load_tilemap("tileset/map1.json", use_spatial_hash=True)

        # Then access its sprite lists
        self.wall_list = self.title_map.sprite_lists["Walls"]
        self.floor_list = self.title_map.sprite_lists["Floor"]

        self.player_list = arcade.SpriteList()
        # Use the animated player sprite
        self.player_sprite = Player("tileset/sprite.png", scale=1.3, hp=100, atk=10, spd=3, window=self)
        self.player_sprite.center_x = 90
        self.player_sprite.center_y = 350
        self.player_list.append(self.player_sprite)

        # test enemy sprite
        # Dynamically set spawn points for the monster
        spawn_x, spawn_y = 300, 400  # Example spawn location
        self.enemy1_sprite = monster_melee("tileset/enemy1.png", scale=1, hp=100, atk=10, atk_speed=1, spawn_x=spawn_x, spawn_y=spawn_y)
        self.player_list.append(self.enemy1_sprite)

        # Initialize the enemy list
        self.enemy_list = arcade.SpriteList()

        # Add the test enemy sprite to the enemy list
        self.enemy_list.append(self.enemy1_sprite)

        # Health refill sprite list
        self.health_refill_list = arcade.SpriteList()
        # Example: Place a health refill at (400, 400)
        health_refill = arcade.Sprite("tileset/Health1.png", scale=1)
        health_refill.center_x = 400
        health_refill.center_y = 400
        self.health_refill_list.append(health_refill)
        
        # Portal sprite list (empty at start, will spawn after boss dies)
        self.portal_list = arcade.SpriteList()
        
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_show_view(self):
        arcade.set_background_color((45, 188, 227))
        # Recreate cameras for this view
        self.camera_sprites = arcade.Camera(ScreenWidth, ScreenHeight)
        self.camera_gui = arcade.Camera(ScreenWidth, ScreenHeight)

    def on_draw(self):
        """DRAW EVERYTHING"""
        self.clear()
        self.camera_sprites.use()
        self.floor_list.draw()
        self.wall_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()  # Draw all enemies
        self.projectile_list.draw()  # Draw projectiles
        self.health_refill_list.draw()  # Draw health refills
        self.portal_list.draw()  # Draw portals

        # Draw GUI
        self.camera_gui.use()
        arcade.draw_text("Player Position: " + str(self.player_sprite.position), 10, 10, arcade.color.WHITE, 12)
        # arcade.draw_text(f"Player HP: {self.player_sprite.hp}", 10, 50, arcade.color.WHITE, 12)
        # arcade.draw_text(f"Ammo: {self.player_sprite.ammo}/{self.player_sprite.max_ammo}", 10, 70, arcade.color.WHITE, 12)
        if self.player_sprite.ammo == 0 and not self.player_sprite.reloading:
            arcade.draw_text("Out of Ammo! Press R to Reload", 10, 100, arcade.color.RED, 12)
        if self.player_sprite.reloading:
            arcade.draw_text("Reloading...", 10, 90, arcade.color.RED, 12)
        # Draw money counter on HUD
        arcade.draw_text(f"Money: {self.money}", 10, 150, arcade.color.GOLD, 18)

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

        # Draw health bars for enemies
        camera_x, camera_y = self.camera_sprites.position
        for enemy in self.player_list:
            if isinstance(enemy, monster_melee):
                enemy.draw_health_bar(camera_x, camera_y)

        # Draw health bars for bosses (ensure always visible and updated)
        camera_x, camera_y = self.camera_sprites.position
        for enemy in self.enemy_list:
            if isinstance(enemy, monster_boss):
                enemy.draw_health_bar(camera_x, camera_y)

        # Draw debug HUD for projectiles
        for i, projectile in enumerate(self.projectile_list):
            arcade.draw_text(
                f"Projectile {i}: ({projectile.center_x:.1f}, {projectile.center_y:.1f})",
                10, 120 + i * 20,  # Offset each line vertically
                arcade.color.YELLOW, 12
            )

        # HP, Dash, and Ammo bars cluster (shifted up and left)
        hud_x = 75
        hud_y = 250  # 50 (original) + 200 (shift up)
        bar_width = 150
        bar_height = 20
        # HP bar
        arcade.draw_rectangle_filled(hud_x, hud_y, bar_width, bar_height, arcade.color.RED)
        health_percentage = max(self.player_sprite.hp / 100, 0)
        health_bar_width = bar_width * health_percentage
        arcade.draw_rectangle_filled(hud_x - (bar_width - health_bar_width) / 2, hud_y, health_bar_width, bar_height, arcade.color.GREEN)
        arcade.draw_rectangle_outline(hud_x, hud_y, bar_width, bar_height, arcade.color.BLACK, 2)
        arcade.draw_text(f"{self.player_sprite.hp}/100", hud_x, hud_y - 10, arcade.color.WHITE, 14, anchor_x="center")
        # Dash bar just below
        dash_color = arcade.color.GREEN if self.dash_cooldown == 0 else arcade.color.GRAY
        dash_text = "Ready" if self.dash_cooldown == 0 else f"{self.dash_cooldown:.1f}s"
        arcade.draw_rectangle_filled(hud_x, hud_y - 25, bar_width, bar_height, dash_color)
        arcade.draw_rectangle_outline(hud_x, hud_y - 25, bar_width, bar_height, arcade.color.BLACK, 2)
        arcade.draw_text(f"Dash: {dash_text}", hud_x, hud_y - 35, arcade.color.WHITE, 14, anchor_x="center")
        # Ammo bar just below dash bar
        ammo_percentage = max(self.player_sprite.ammo / self.player_sprite.max_ammo, 0)
        ammo_bar_width = bar_width * ammo_percentage
        arcade.draw_rectangle_filled(hud_x - (bar_width - ammo_bar_width) / 2, hud_y - 50, ammo_bar_width, bar_height, arcade.color.BLUE)
        arcade.draw_rectangle_filled(hud_x, hud_y - 50, bar_width, bar_height, arcade.color.DARK_BLUE, 0.2)
        arcade.draw_rectangle_outline(hud_x, hud_y - 50, bar_width, bar_height, arcade.color.BLACK, 2)
        arcade.draw_text(f"Ammo: {self.player_sprite.ammo}/{self.player_sprite.max_ammo}", hud_x, hud_y - 60, arcade.color.WHITE, 14, anchor_x="center")

        # Game over screen
        if self.game_over:
            # Draw a semi-transparent black rectangle covering the screen
            arcade.draw_rectangle_filled(
                ScreenWidth // 2, ScreenHeight // 2,
                ScreenWidth, ScreenHeight,
                (0, 0, 0, 200)
            )
            arcade.draw_text("GAME OVER", ScreenWidth // 2, ScreenHeight // 2 + 20, arcade.color.RED, 40, anchor_x="center")
            arcade.draw_text("Press ESC to Quit", ScreenWidth // 2, ScreenHeight // 2 - 40, arcade.color.WHITE, 20, anchor_x="center")

        # Win screen
        if hasattr(self, 'game_win') and self.game_win:
            arcade.draw_rectangle_filled(
                ScreenWidth // 2, ScreenHeight // 2,
                ScreenWidth, ScreenHeight,
                (0, 0, 0, 200)  # Gray and translucent, matches pause/lose
            )
            arcade.draw_text("YOU WIN!", ScreenWidth // 2, ScreenHeight // 2 + 20, arcade.color.GREEN, 40, anchor_x="center")
            arcade.draw_text("Press ESC to Quit", ScreenWidth // 2, ScreenHeight // 2 - 40, arcade.color.WHITE, 20, anchor_x="center")

    def on_update(self, delta_time):
        """UPDATE EVERYTHING"""
        if self.paused or self.game_over or self.game_win:
            return  # Skip updates when paused or game is over

        self.player_list.update()
        self.player_list.update_animation(delta_time)
        self.projectile_list.update()  # Update projectiles
        self.enemy_list.update()  # Update all enemies

        # Optimize projectile management by removing off-screen projectiles immediately
        for projectile in self.projectile_list:
            if not (0 <= projectile.center_x <= ScreenWidth and 0 <= projectile.center_y <= ScreenHeight):
                projectile.remove_from_sprite_lists()

        # Optimize enemy updates by only updating enemies near the player
        player_x, player_y = self.player_sprite.center_x, self.player_sprite.center_y
        for enemy in self.enemy_list:
            if abs(enemy.center_x - player_x) < 300 and abs(enemy.center_y - player_y) < 300:  # Adjust range as needed
                enemy.update()

        # Ensure only active enemies are processed
        for enemy in self.enemy_list:
            if enemy.hp > 0:
                enemy.update()
                enemy.check_line_of_sight(self.player_sprite, self.wall_list)

        # Optimize health bar rendering by only drawing health bars for visible enemies
        camera_x, camera_y = self.camera_sprites.position
        for enemy in self.enemy_list:
            if 0 <= enemy.center_x - camera_x <= ScreenWidth and 0 <= enemy.center_y - camera_y <= ScreenHeight:
                enemy.draw_health_bar(camera_x, camera_y)

        # Call the monster's attack method
        if self.enemy1_sprite.hp > 0:  # Ensure the enemy is alive
            self.enemy1_sprite.check_line_of_sight(self.player_sprite, self.wall_list)

        # Check for projectile collisions with walls and enemies
        for projectile in self.projectile_list:
            # Check collision with walls
            hit_walls = arcade.check_for_collision_with_list(projectile, self.wall_list)
            if hit_walls:
                print(f"Projectile at ({projectile.center_x:.1f}, {projectile.center_y:.1f}) collided with wall(s):")
                for wall in hit_walls:
                    print(f"  Wall at ({wall.center_x:.1f}, {wall.center_y:.1f})")
                projectile.remove_from_sprite_lists()
                continue

            # Check collision with enemies
            hit_enemies = arcade.check_for_collision_with_list(projectile, self.enemy_list)
            for enemy in hit_enemies:
                if isinstance(enemy, monster_melee):  # Ensure it's an enemy
                    enemy.hp -= self.player_sprite.atk  # Deal damage to the enemy
                    projectile.remove_from_sprite_lists()
                    break

        # Check for collision with health refills
        health_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.health_refill_list)
        for health in health_hit_list:
            self.player_sprite.hp = min(self.player_sprite.hp + 50, 100)  # Heal up to max 100
            health.remove_from_sprite_lists()

        # Check for collision with portal
        portal_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.portal_list)
        if portal_hit_list:
            self.game_win = True
            return

        # Handle player movement
        self.handle_player_movement()

        # Update the camera to follow the player
        self.physics_engine.update()
        self.scroll_to_player()

        # Check all enemies for death
        for enemy in self.enemy_list:
            if enemy.hp <= 0:
                # If the boss dies, spawn the portal
                if isinstance(enemy, monster_boss):
                    portal = arcade.Sprite("tileset/portal.png", scale=1)
                    portal.center_x = 1501
                    portal.center_y = 770
                    self.portal_list.append(portal)
                self.money += 500  # Add 500 money per kill
                enemy.remove_from_sprite_lists()
                # Ensure the enemy is completely removed from all lists
                

        # Dash cooldown timer
        if self.dash_cooldown > 0:
            self.dash_cooldown -= delta_time
            if self.dash_cooldown < 0:
                self.dash_cooldown = 0

        # Handle dashing
        if self.dashing:
            self.dash_timer -= delta_time
            if self.dash_timer > 0:
                self.player_sprite.center_x += self.dash_direction[0] * self.dash_speed
                self.player_sprite.center_y += self.dash_direction[1] * self.dash_speed
            else:
                self.dashing = False
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                
        # Spawn boss only when player passes x=1205 and enemy1 is dead
        if not self.boss_spawned and self.player_sprite.center_x > 1205 and self.enemy1_sprite.hp <= 0:
            self.boss_sprite = monster_boss("tileset/BOSS.png", scale=1, hp=600, atk=25, atk_speed=1.5, spawn_x=1512, spawn_y=763)
            self.enemy_list.append(self.boss_sprite)
            self.boss_spawned = True

        # Boss damage and death logic (similar to enemy1)
        from arcade import SpriteList
        boss_sprites = SpriteList()
        for e in self.enemy_list:
            if isinstance(e, monster_boss):
                boss_sprites.append(e)
        for projectile in self.projectile_list:
            hit_bosses = arcade.check_for_collision_with_list(projectile, boss_sprites)
            for boss in hit_bosses:
                boss.hp -= self.player_sprite.atk
                projectile.remove_from_sprite_lists()
                if boss.hp <= 0:
                    boss.remove_from_sprite_lists()
                break

        # Check for game over
        if self.player_sprite.hp <= 0 and not self.game_over:
            self.game_over = True

        # Handle restart if requested
        if self.game_over and self.restart_requested:
            self.restart_requested = False
            self.game_over = False
            self.setup()

    def on_mouse_press(self, x, y, button, modifiers):
        """Called when the mouse is pressed."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player_sprite.player_gun(x, y)
        # Dash with right click
        if button == arcade.MOUSE_BUTTON_RIGHT and not self.dashing and self.dash_cooldown == 0 and not self.paused:
            # Dash in the direction of the mouse
            camera_x, camera_y = self.camera_sprites.position
            world_mouse_x = x + camera_x
            world_mouse_y = y + camera_y
            dx = world_mouse_x - self.player_sprite.center_x
            dy = world_mouse_y - self.player_sprite.center_y
            length = math.hypot(dx, dy)
            if length > 0:
                self.dash_direction = (dx / length, dy / length)
                self.dashing = True
                self.dash_timer = self.dash_time
                self.dash_cooldown = self.dash_cooldown_max

    def scroll_to_player(self):
        window_width, window_height = self.window.get_size()
        position = Vec2(self.player_sprite.center_x - window_width / 2,
                        self.player_sprite.center_y - window_height / 2)
        self.camera_sprites.move_to(position, CameraSpeed)
# movement here
    def on_key_press(self, key, modifiers):
        """Called when a key is pressed."""
        if key == arcade.key.ESCAPE:
            if self.game_over or (hasattr(self, 'game_win') and self.game_win):
                arcade.close_window()  # Quit the game if on game over or win screen
            else:
                self.paused = not self.paused  # Toggle pause state
        elif key == arcade.key.R:
            if self.game_over:
                pass  # No longer restart on R
            else:
                self.player_sprite.reload()  # Trigger reload
        elif key == arcade.key.I:
            self.money += 10000  # Cheat key for money
        else:
            self.pressed_keys.add(key)
            # Set animation frames for movement
            if key == arcade.key.W:
                self.player_sprite.set_direction_frames("up")
                self.player_sprite.change_y = self.player_sprite.spd
            elif key == arcade.key.S:
                self.player_sprite.set_direction_frames("down")
                self.player_sprite.change_y = -self.player_sprite.spd
            elif key == arcade.key.A:
                self.player_sprite.set_direction_frames("left")
                self.player_sprite.change_x = -self.player_sprite.spd
            elif key == arcade.key.D:
                self.player_sprite.set_direction_frames("right")
                self.player_sprite.change_x = self.player_sprite.spd
            # Instantly kill the boss with key 'K'
            elif key == arcade.key.K:
                for enemy in self.enemy_list:
                    if isinstance(enemy, monster_boss):
                        enemy.hp = 0

    def on_key_release(self, key, modifiers):
        """Called when a key is released."""
        self.pressed_keys.discard(key)
        # Stop movement and set idle frame
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
            self.player_sprite.load_idle_frames()
        if key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0
            self.player_sprite.load_idle_frames()

    def handle_player_movement(self):
        """Handle player movement based on key presses."""
        if arcade.key.A in self.pressed_keys:
            self.player_sprite.change_x = self.player_sprite.spd * -1
        elif arcade.key.D in self.pressed_keys:
            self.player_sprite.change_x = self.player_sprite.spd
        else:
            self.player_sprite.change_x = 0

        if arcade.key.W in self.pressed_keys:
            self.player_sprite.change_y = self.player_sprite.spd
        elif arcade.key.S in self.pressed_keys:
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
        if distance <= 15 and not player_sprite.invincible:
            # Attack the player
            player_sprite.hp -= self.atk

            # Make the player temporarily invincible
            player_sprite.invincible = True
            arcade.schedule(player_sprite.remove_invincibility, 2.0)  # 2 seconds of invincibility
    

    def draw_health_bar(self, camera_x, camera_y):
        """Draw the health bar above the enemy."""
        # Calculate screen position relative to the camera
        screen_x = self.center_x - camera_x
        screen_y = self.center_y - camera_y

        # Calculate health bar dimensions
        bar_width = 40
        bar_height = 5
        health_percentage = max(self.hp / 100, 0)  # Ensure it doesn't go below 0
        health_bar_width = bar_width * health_percentage

        # Draw the health bar background
        arcade.draw_rectangle_filled(
            screen_x, screen_y + 20,  # Position above the enemy
            bar_width, bar_height,
            arcade.color.RED
        )

        # Draw the current health bar
        arcade.draw_rectangle_filled(
            screen_x - (bar_width - health_bar_width) / 2, screen_y + 20,
            health_bar_width, bar_height,
            arcade.color.GREEN
        )
    
class monster_boss(arcade.Sprite):
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
            self.attack(player_sprite)
        else:
            self.change_x = 0
            self.change_y = 0

    def attack(self, player_sprite):
        direction = Vec2(
            player_sprite.center_x - self.center_x,
            player_sprite.center_y - self.center_y).normalize()
        self.change_x = direction.x * self.atk_speed
        self.change_y = direction.y * self.atk_speed
        distance = math.sqrt(
            (self.center_x - player_sprite.center_x) ** 2 +
            (self.center_y - player_sprite.center_y) ** 2)
        if distance <= 30 and not player_sprite.invincible:
            player_sprite.hp -= self.atk
            player_sprite.invincible = True
            arcade.schedule(player_sprite.remove_invincibility, 2.0)

    def draw_health_bar(self, camera_x, camera_y):
        screen_x = self.center_x - camera_x
        screen_y = self.center_y - camera_y
        bar_width = 40
        bar_height = 5
        health_percentage = max(self.hp / 600, 0)
        health_bar_width = bar_width * health_percentage
        bar_y = screen_y + self.height // 2 + 10
        arcade.draw_rectangle_filled(
            screen_x, bar_y,
            bar_width, bar_height,
            arcade.color.RED
        )
        arcade.draw_rectangle_filled(
            screen_x - (bar_width - health_bar_width) / 2, bar_y,
            health_bar_width, bar_height,
            arcade.color.GREEN
        )
    
    def load_level2(self):
        """Load Level 2: change map and reset player position."""
        self.title_map = arcade.load_tilemap("tileset/map2.json", use_spatial_hash=True)
        self.wall_list = self.title_map.sprite_lists["Walls"]
        self.floor_list = self.title_map.sprite_lists["Floor"]
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.enemy_list = arcade.SpriteList()
        self.projectile_list = arcade.SpriteList()
        self.portal_list = arcade.SpriteList()
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

class StartScreen(arcade.View):
    def on_show_view(self):
        arcade.set_background_color((45, 188, 227))

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "BEN'S UNNAMMED GAME",
            ScreenWidth // 2, ScreenHeight // 2 + 100,
            arcade.color.WHITE, 40, anchor_x="center"
        )

        # Draw start button
        btn_x = ScreenWidth // 2
        btn_y = ScreenHeight // 2 - 40
        btn_w = 200
        btn_h = 60
        arcade.draw_rectangle_filled(btn_x, btn_y, btn_w, btn_h, arcade.color.GREEN)
        arcade.draw_text("START", btn_x, btn_y - 15, arcade.color.BLACK, 28, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        btn_x = ScreenWidth // 2
        btn_y = ScreenHeight // 2 - 40
        btn_w = 200
        btn_h = 60
        if btn_x - btn_w // 2 <= x <= btn_x + btn_w // 2 and btn_y - btn_h // 2 <= y <= btn_y + btn_h // 2:
            game = Game()
            game.setup()
            self.window.show_view(game)

def main():
    window = arcade.Window(ScreenWidth, ScreenHeight - 100, "Game Window")
    start_view = StartScreen()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
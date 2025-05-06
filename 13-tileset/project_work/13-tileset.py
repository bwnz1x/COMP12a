import arcade
from pyglet.math import Vec2
# constant
SPRITE_SCALE_PLAYER = 2
SPRITE_SCALE_BOX = 1.75
COIN_COUNT = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVE_SPEED = 5
CAMERA_SPEED = 0.1
GRAVITY = 0.5
JUMP_SPEED = 10
VIEWPORT_MARGIN = 220

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite and Collision")

        self.set_location(100, 100)

        self.player_list = None
        self.player_sprite = None
        self.coin_list = None
        self.score = 0
        self.wall_list = None
        self.title_list = None
        self.physics_engine = None

        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.set_mouse_visible(False)


    def setup(self):
        # map setup
        map_name = "../data/maps/level1.json"

        self.title_map = arcade.load_tilemap(map_name, scaling=SPRITE_SCALE_BOX)
        self.wall_list = self.title_map.sprite_lists["Walls"]
        self.coin_list = self.title_map.sprite_lists["Coins"]
        if self.title_map.background_color:
            arcade.set_background_color(self.title_map.background_color)

        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.AnimatedTimeBasedSprite()



        texture = arcade.load_texture("../data/sprite/sprite.png", 0, 0, 32, 32)
        anim = arcade.AnimationKeyframe(1,10,texture)
        self.player_sprite.frames.append(anim)
        self.player_sprite.scale = SPRITE_SCALE_PLAYER



        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.wall_list, gravity_constant=GRAVITY
        )

    def on_draw(self):
        # Use the camera for sprites
        self.camera_sprites.use()
        # Start rendering
        arcade.start_render()
        # Draw the sprites
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        # Use the GUI camera for GUI elements
        self.camera_gui.use()

        # Draw GUI elements (e.g., text)
        output2 = f"Position: {self.player_sprite.center_x}, {self.player_sprite.center_y}"
        arcade.draw_text(output2, 10, 50, arcade.color.WHITE, 14)
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update(self, delta_time):

        self.player_list.update()
        self.player_list.update_animation()

        self.coin_list.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        self.physics_engine.update()
        self.scroll_to_player()

    def scroll_to_player(self):
        position = Vec2(self.player_sprite.center_x - self.width / 2,
                        self.player_sprite.center_y - self.height / 2)
        self.camera_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):

        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))

    def on_key_press(self, key, modifiers):
        if key is arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED

        # if key == arcade.key.UP:
        #     self.player_sprite.change_y = MOVE_SPEED
        #     self.player_sprite.frames.clear()
        #     for i in range(4):
        #         texture = arcade.load_texture("../data/sprite/sprite.png", i * 32, y = 32, width = 32, height = 32)
        #         anim = arcade.AnimationKeyframe(i, 250, texture)
        #         self.player_sprite.frames.append(anim)
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVE_SPEED
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("../data/sprite/sprite.png", i * 32, y = 0, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 200, texture)
                self.player_sprite.frames.append(anim)
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVE_SPEED
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("../data/sprite/sprite.png", i * 32, y = 64, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVE_SPEED
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("../data/sprite/sprite.png", i * 32, y = 96, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)

    def on_key_release(self, key, modifiers):

        if key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("../data/sprite/sprite.png", 0, 0, 32, 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)
        if key == arcade.key.UP:
            self.player_sprite.change_y = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("../data/sprite/sprite.png", 0, 32, 32, 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("../data/sprite/sprite.png", 0, 64, 32, 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)
        if key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("../data/sprite/sprite.png", 32, 96, 32, 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)

    def close(self):
        super().close()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
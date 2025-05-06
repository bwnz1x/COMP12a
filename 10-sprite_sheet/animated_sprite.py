import random
import arcade

# constant
SPRITE_SCALE_PLAYER = 2
SPRITE_SCALE_COIN = 2
COIN_COUNT = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVE_SPEED = 5

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite and Collision")

        self.bgm = None
        self.sfxpop = None
        self.set_location(100, 100)

        self.player_list = None
        self.coin_list = None

        self.player_sprite = None
        self.score = 0

        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.AnimatedTimeBasedSprite()
        self.coin_list = arcade.SpriteList()

        texture = arcade.load_texture("data\sprite\sprite.png", 0, 0, 32, 32)
        anim = arcade.AnimationKeyframe(1,10,texture)
        self.player_sprite.frames.append(anim)
        self.player_sprite.scale = SPRITE_SCALE_PLAYER

        self.score = 0
        self.bgm = arcade.load_sound("data/sound/bgm.mp3")
        arcade.play_sound(self.bgm, 1, 0, True)

        self.sfxpop = arcade.load_sound("data/sound/pop.wav")

        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player_sprite)

        for i in range(COIN_COUNT):
            coin = arcade.Sprite()
            coin.texture = arcade.load_texture("data\sprite\sprite.png", x = 32, y = 128, width = 32, height = 32)
            coin.scale = SPRITE_SCALE_COIN

            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            self.coin_list.append(coin)

    def on_draw(self):
        arcade.start_render()
        self.coin_list.draw()
        self.player_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        output2 = f"Position: {self.player_sprite.center_x}, {self.player_sprite.center_y}"
        arcade.draw_text(output2, 10, 50, arcade.color.WHITE, 14)

    def update(self, delta_time):
        self.coin_list.update()
        self.player_list.update()
        self.player_list.update_animation()

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.sfxpop)

        if self.player_sprite.center_x + 32 > SCREEN_WIDTH:
            self.player_sprite.center_x = SCREEN_WIDTH - 32
        if self.player_sprite.center_y + 32 > SCREEN_HEIGHT:
            self.player_sprite.center_y = SCREEN_HEIGHT - 32
        if self.player_sprite.center_x < 32:
            self.player_sprite.center_x = 32
        if self.player_sprite.center_y < 32:
            self.player_sprite.center_y = 32

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVE_SPEED
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprite\sprite.png", i * 32, y = 32, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVE_SPEED
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprite\sprite.png", i * 32, y = 0, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 200, texture)
                self.player_sprite.frames.append(anim)
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVE_SPEED
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprite\sprite.png", i * 32, y = 64, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVE_SPEED
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprite\sprite.png", i * 32, y = 96, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)

    def on_key_release(self, key, modifiers):

        if key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprite\sprite.png", 0, 0, 32, 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)
        if key == arcade.key.UP:
            self.player_sprite.change_y = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprite\sprite.png", 0, 32, 32, 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprite\sprite.png", 0, 64, 32, 32)
                anim = arcade.AnimationKeyframe(i, 250, texture)
                self.player_sprite.frames.append(anim)
        if key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprite\sprite.png", 32, 96, 32, 32)
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
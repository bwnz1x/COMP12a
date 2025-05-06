import arcade

# load sound and play the background music
pop = arcade.load_sound('pop.wav')
bgm = arcade.load_sound("bgm.mp3")
arcade.play_sound(bgm, 0.2, 0, True)

# constant
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
MOVEMENT_SPEED = 5

class Ball:
    def __init__(self, position_x, position_y, change_x, change_y, radius, colour):

        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.colour = colour

    # drawing the ball
    def draw(self):
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.colour)

    # ensure ball stay in screen
    def update(self):
        self.position_x += self.change_x
        self.position_y += self.change_y

        if self.position_x < self.radius:
            self.position_x = self.radius

        if self.position_y < self.radius:
            self.position_y = self.radius

        if self.position_x > SCREEN_WIDTH - self.radius:
            self.position_x = SCREEN_WIDTH - self.radius

        if self.position_y > SCREEN_HEIGHT - self.radius:
            self.position_y = SCREEN_HEIGHT - self.radius


class MyGame(arcade.Window):
    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)

        self.set_mouse_visible(False)

        # Set the background color
        arcade.set_background_color(arcade.color.ASH_GREY)

        # Attributes to store where our ball is
        self.ball = Ball(50, 50,  0, 0,15, arcade.color.YELLOW)


    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        self.ball.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.ball.position_x = x
        self.ball.position_y = y

    def update(self, delta_time):
        self.ball.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.ball.change_y = MOVEMENT_SPEED
        if key == arcade.key.DOWN:
            self.ball.change_y = -MOVEMENT_SPEED
        if key == arcade.key.LEFT:
            self.ball.change_x = -MOVEMENT_SPEED
        if key == arcade.key.RIGHT:
            self.ball.change_x = MOVEMENT_SPEED

        if key == arcade.key.SPACE:
            arcade.play_sound(pop)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            arcade.play_sound(pop)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.ball.change_x = 0
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.ball.change_y = 0


def main():
    window = MyGame(640, 480, "Drawing Example")
    arcade.run()


main()
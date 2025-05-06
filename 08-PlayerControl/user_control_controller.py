import arcade

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
MOVEMENT_SPEED = 3
DEAD_ZONE = 0.02

class Ball:
    def __init__(self, position_x, position_y, change_x, change_y, radius, colour):

        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.colour = colour


    def draw(self):
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.colour)


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

        joystick = arcade.get_joysticks()


        if joystick:
            self.joystick = joystick[0]
            self.joystick.open()
        else:
            print("No joystick found")
            self.joystick = None


    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        self.ball.draw()


    def update(self, delta_time):
        if self.joystick:
            print(self.joystick.x, self.joystick.y)




def main():
    window = MyGame(640, 480, "Drawing Example")

    arcade.run()


main()

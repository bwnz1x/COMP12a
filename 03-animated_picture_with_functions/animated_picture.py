"""
Ben Phan
Comp 12 Blk 3
01/30/2025

Bouncing DVD screensaver
Description: I'm going to make an animation similar to what the DVD logo screen saver
Reference: https://youtu.be/5mGuCdlCcNM?si=huLSlMi4dBvo7XX5
!!! CODED ON ARCADE 3.0.0, HAVE NOT TEST ON ARCADE 2.6.17
"""
import time


# import the arcade library
import arcade as ac
from numpy.random import randint




def draw_icon(x, y, colour):
    """This function will be used to draw the icon while the it is bouncing around"""

    # Draw the DVD text
    ac.draw_text("DVD", x - 22, y - 10, colour, 16, 5,"center", "Arial", True)

    # Draw the DVD logo
    ac.draw_ellipse_filled(x, y + 20, 80, 20, colour)
    ac.draw_ellipse_filled(x, y + 20, 20, 5, ac.color.BLACK)


def set_up():
    """Draw the background for the base program"""

    ac.draw_text("Loading . . .",500, 450, (255, 255, 255, 50), 24,5,
                 "center", "Arial", True )


def on_draw(x, y):
    """Function to draw the program. Most of my animation logic is in here"""


    colour = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255)]
    current_colour = 0
    direction_x = True
    direction_y = True

    while True:
        ac.start_render()
        set_up()
        if x == 0 or x == 1000:
            direction_x = not direction_x
            current_colour = randint(5)

        if y == 0  or y == 900:
            direction_y = not direction_y
            current_colour = randint(5)

        if direction_x is True:
            x += 1
        else:
            x -= 1

        if direction_y is True:
            y += 1
        else:
            y -= 1

        # draw the actual the moving icon
        draw_icon(x, y, colour[current_colour])
        ac.finish_render()
        time.sleep(0.016)






def main():
    """This is the main function that will be use to call all of the command"""
    ac.open_window(1000, 900)
    ac.set_background_color(ac.color.DARK_BLUE)

    while True:
        on_draw(500, 450)





main()
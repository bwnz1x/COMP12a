# Advanced Looping Graphics in Arcade
# Ben Phan
# 05/01/2025

import arcade



def draw_section_outlines():
    ''' Create a grid of rectangles where 8 different patterns will be drawn '''
    # Draw squares on bottom
    arcade.draw_rectangle_outline(150, 150, 300, 300, arcade.color.BLACK)
    arcade.draw_rectangle_outline(450, 150, 300, 300, arcade.color.BLACK)
    arcade.draw_rectangle_outline(750, 150, 300, 300, arcade.color.BLACK)
    arcade.draw_rectangle_outline(1050, 150, 300, 300, arcade.color.BLACK)

    # Draw squares on top
    arcade.draw_rectangle_outline(150, 450, 300, 300, arcade.color.BLACK)
    arcade.draw_rectangle_outline(450, 450, 300, 300, arcade.color.BLACK)
    arcade.draw_rectangle_outline(750, 450, 300, 300, arcade.color.BLACK)
    arcade.draw_rectangle_outline(1050, 450, 300, 300, arcade.color.BLACK)


def draw_section_1():
    ''' Creates a grid of 30x30 white squares evenly distributed in a 300x300 
    pixel space '''
    for row in range(30):
        for column in range(30):
            x = 10 * column + 5 # Instead of zero, calculate the proper x location using 'column'
            y = 10 * row + 5 # Instead of zero, calculate the proper y location using 'row'
            arcade.draw_rectangle_filled(x, y, 5, 5, arcade.color.WHITE)


def draw_section_2():
    ''' Creates a grid of 30x30 alternating white and black columns of squares
    evenly distributed in a 300x300 pixel space '''
    # Below, replace "pass" with your code for the loop.
    # Use the modulus operator and an if statement to select the color
    # Don't loop from 30 to 60 to shift everything over, just add 300 to x.
    for row in range(30):
        for column in range(30):
            x = 10 * column + 5 + 300
            y = 10 * row + 5
            if column % 2 == 1:
                arcade.draw_rectangle_filled(x, y, 5, 5, arcade.color.BLACK)
            else:
                arcade.draw_rectangle_filled(x, y, 5, 5, arcade.color.WHITE)


def draw_section_3():
    ''' Creates a grid of 30x30 alternating white and black rows of squares
    evenly distributed in a 300x300 pixel space '''    
    # Use the modulus operator and an if/else statement to select the color.
    # Don't use multiple 'if' statements.
    for row in range(30):
        for column in range(30):
            x = 10 * column + 5 + 600
            y = 10 * row + 5
            if row % 2 == 1:
                arcade.draw_rectangle_filled(x, y, 5, 5, arcade.color.BLACK)
            else:
                arcade.draw_rectangle_filled(x, y, 5, 5, arcade.color.WHITE)


def draw_section_4():
    ''' Creates a grid of 30x30 alternating black rows of squares with
    white/black patterned rows (like in section_2) evenly distributed in a 
    300x300 pixel space '''     
    # Use the modulus operator and just one 'if' statement to select the color.
    for row in range(30):
        for column in range(30):
            x = 10 * column + 5 + 900
            y = 10 * row + 5
            if row % 2 == 1 or column % 2 == 1:
                arcade.draw_rectangle_filled(x, y, 5, 5, arcade.color.BLACK)
            else:
                arcade.draw_rectangle_filled(x, y, 5, 5, arcade.color.WHITE)


def draw_section_5():
    ''' fills half of a 300 x 300 pixel space with a right triangle composed
    of small white squares '''
    # Do NOT use 'if' statements to complete 5-8. Manipulate the loops instead.
    for row in range(30):
        for column in range(29 - row):
            x = 295 - column * 10
            y = 10 * row + 305
            arcade.draw_rectangle_filled(x, y, 5, 5, arcade.color.WHITE)



def draw_section_6():
    ''' fills half of a 300 x 300 pixel space with a right triangle composed
    of small white squares '''    
    for row in range(30):
        for column in range(30 - row):
            x = 10 * column + 305
            y = 10 * row + 305
            arcade.draw_rectangle_filled(x, y, 5, 5, arcade.color.WHITE)


def draw_section_7():
    ''' fills half of a 300 x 300 pixel space with a right triangle composed
    of small white squares '''    
    for row in range(30):
        for column in range(row + 1):
            x = 10 * column + 605
            y = 10 * row + 305
            arcade.draw_rectangle_filled(x, y, 5, 5, arcade.color.WHITE)


def draw_section_8():
    ''' fills half of a 300 x 300 pixel space with a right triangle composed
    of small white squares '''
    for row in range(30):
        for column in range(row + 1):
            x = - 10 * column + 1195
            y = 10 * row + 305
            arcade.draw_rectangle_filled(x, y, 5, 5, arcade.color.WHITE)


def main():
    # Create a window
    arcade.open_window(1200, 600, "Advanced Looping Graphics in Arcade")
    arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)

    arcade.start_render()

    # Draw the outlines for the sections
    draw_section_outlines()

    # Draw the sections
    draw_section_1()
    draw_section_2()
    draw_section_3()
    draw_section_4()
    draw_section_5()
    draw_section_6()
    draw_section_7()
    draw_section_8()

    arcade.finish_render()

    arcade.run()


main()
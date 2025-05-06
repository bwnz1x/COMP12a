"""
Ben Phan
2025/01/27
COMP 12


Drawing A Picture
Description: Using Python Arcade Library to recreate the reference image
"""

# import arcade library
import arcade as ac

# setup window
ac.open_window(300, 300, "dark side of the moon")
ac.set_background_color(ac.csscolor.BLACK)

# setup for drawing
ac.start_render()

# drawing the rainbow with stacked line on top of each other
ac.draw_line(169, 198, 299, 177, (197,32,28), 4) # red
ac.draw_line(171, 195, 299, 171, (220,134,28), 4) # orange
ac.draw_line(173, 192, 299, 165, (228,210,5), 4) # yellow
ac.draw_line(175, 189, 299, 159, (2,150,77), 4) # green
ac.draw_line(177, 186, 299, 153, (1,118,179), 4) # blue
ac.draw_line(179, 183, 299, 146, (105,50,129), 4) # purple

# draw the center triangle
ac.draw_triangle_outline(103, 147, 151, 229, 197, 147, (87,133,149), 2)

# draw out the white lines
ac.draw_line(0, 158, 129, 191, ac.csscolor.WHITE, 1.5)

# drawing the faded triangle
# to tackle this, I will start to draw stacked triangle, with increasing opacity to replicate the triangle
for i in range(1,4):
    ac.draw_triangle_filled(129,191,(154 + i*5),(178 + i),(154 + i*5),(201 - i),(255,255,255,2 + i*20))



# function to complete drawing and keeping the window open
ac.finish_render()
ac.run()




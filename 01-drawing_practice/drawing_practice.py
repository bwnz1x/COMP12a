"""
!! WRITTEN ON 3.0 ARCADE !!
Ben Phan
2025/01/27
"""


# import library need for program
import arcade

# open a window 300x300 px with a title
arcade.open_window(300, 300, "banana cheesecake")

# set bgcolor of window
# noinspection PyTypeChecker
arcade.set_background_color((51, 153, 255))

# start drawing
# function to allow drawing of shapes
arcade.start_render()

# draw filled rectangle
arcade.draw_rect_filled(arcade.XYWH(150, 150, 200, 150), arcade.csscolor.VIOLET)

# draw outlined circle by first drawing the filled circle, then drawing the circle outline
arcade.draw_circle_filled(150,150,70,(100, 3, 255))
arcade.draw_circle_outline(150,150,70,(159, 0, 212),5)

# draw text on top of the shape
arcade.draw_text("Ben", 150, 150,(140, 215, 255), 16, None,"center",
                 "arial", True, False, "center","center" )

arcade.finish_render()
# keep the windows up
arcade.run()
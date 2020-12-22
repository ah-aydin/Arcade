# Python modules
import pygame as pg

# App modules
import app

# Game modules
from .game_variables import GameVariables as gv

class PlayArea():
    def __init__(self):
        self.dimention = (10, 21)

        # Get screen dimentions
        swidth = app.App.get_surface().get_width()
        sheight = app.App.get_surface().get_height()

        # Calculate the render variables
        render_height = sheight
        self.tile_width = render_height // self.dimention[1]
        render_width = self.tile_width * self.dimention[0]
        gv.TILE_WIDTH = self.tile_width

        # Calculate the render offset
        gv.PLAY_AREA_TOP_LEFT = (
            (swidth - self.dimention[0] * self.tile_width) // 2,
            0
        )

        self.top_left = gv.PLAY_AREA_TOP_LEFT
        self.bottom_right = (
            self.top_left[0] + self.dimention[0] * self.tile_width,
            sheight
        )

    def render(self):
        # Draw the play area lines
        pg.draw.line(
            app.App.get_surface(),
            gv.WHITE,
            (self.top_left[0] - 1, self.top_left[1]),
            (self.top_left[0] - 1, self.bottom_right[1])
        )
        pg.draw.line(
            app.App.get_surface(),
            gv.WHITE,
            (self.bottom_right[0] + 1, self.bottom_right[1]),
            (self.bottom_right[0] + 1, self.top_left[1])
        )
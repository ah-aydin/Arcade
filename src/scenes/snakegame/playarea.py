# Python modules
import pygame as pg

# App modules
import app

# Game modules
from .game_variables import GameVariables as gv

class PlayArea():
    """
    Represents the play area of the game in a 2D square matrix
    dimention = the number of rows and columns the play area will have
    tile_width = the height and width of 1 cell
    """
    def __init__(self, dimention : int, tile_width : int):
        # Get screen dimentions
        swidth = app.App.get_surface().get_width()
        sheight = app.App.get_surface().get_height()
        # Calculate PlayArea dimention
        self._dimention = dimention * tile_width
        self.tile_count = dimention

        # Calculate render offsets
        top_offset = (sheight - self._dimention) // 2
        right_offset = (swidth - self._dimention) // 2

        # Store these for future reference in other classes as well
        gv.PLAY_AREA_TOP_LEFT = (right_offset, top_offset)
        gv.TILE_WIDTH = tile_width

        # Calculate play area limits
        self._top_left = gv.PLAY_AREA_TOP_LEFT
        self._bottom_right = (gv.PLAY_AREA_TOP_LEFT[0] + self._dimention, gv.PLAY_AREA_TOP_LEFT[1] + self._dimention)

    def render(self):
        """
        Renders the play area
        """
        # Draw play area lines clockwise starting from top-left corner
        pg.draw.line(
            app.App.get_surface(),
            gv.WHITE,
            self._top_left,
            (self._bottom_right[0], self._top_left[1])
        )
        pg.draw.line(
            app.App.get_surface(),
            gv.WHITE,
            (self._bottom_right[0], self._top_left[1]),
            self._bottom_right
        )
        pg.draw.line(
            app.App.get_surface(),
            gv.WHITE,
            self._bottom_right,
            (self._top_left[0], self._bottom_right[1])
        )
        pg.draw.line(
            app.App.get_surface(),
            gv.WHITE,
            (self._top_left[0], self._bottom_right[1]),
            self._top_left
        )
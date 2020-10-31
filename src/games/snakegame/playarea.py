# Python modules
import pygame as pg

# App modules
from app import App

# Game modules
from .game_variables import GameVariables as gv

class PlayArea():

    def __init__(self, dimention, tile_width):
        # Get screen dimentions
        swidth = App.get_surface().get_width()
        sheight = App.get_surface().get_height()
        # Calculate PlayArea dimention
        self.dimention = dimention * tile_width
        self.tile_count = dimention

        # Calculate render offsets
        top_offset = (sheight - self.dimention) // 2
        right_offset = (swidth - self.dimention) // 2

        gv.PLAY_AREA_TOP_LEFT = (right_offset, top_offset)
        gv.TILE_WIDTH = tile_width

        # Calculate play area limits
        self.top_left = gv.PLAY_AREA_TOP_LEFT
        self.bottom_right = (gv.PLAY_AREA_TOP_LEFT[0] + self.dimention, gv.PLAY_AREA_TOP_LEFT[1] + self.dimention)

    def render(self):
        # Draw play area lines clockwise starting from top-left corner
        pg.draw.line(
            App.get_surface(),
            gv.WHITE,
            self.top_left,
            (self.bottom_right[0], self.top_left[1])
        )
        pg.draw.line(
            App.get_surface(),
            gv.WHITE,
            (self.bottom_right[0], self.top_left[1]),
            self.bottom_right
        )
        pg.draw.line(
            App.get_surface(),
            gv.WHITE,
            self.bottom_right,
            (self.top_left[0], self.bottom_right[1])
        )
        pg.draw.line(
            App.get_surface(),
            gv.WHITE,
            (self.top_left[0], self.bottom_right[1]),
            self.top_left
        )
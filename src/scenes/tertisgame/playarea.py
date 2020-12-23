# Python modules
import pygame as pg

# App modules
import app

# Game modules
from .game_variables import GameVariables as gv

class PlayArea():
    def __init__(self):
        self.dimention = (10, 20)
        self.grid = [[(0, 0, 0) for i in range(self.dimention[0])] for j in range(self.dimention[1])]
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

        # Other variables
        self.play_area_width = self.tile_width * self.dimention[0]
        play_area_height = self.tile_width * self.dimention[1]
        self.play_area_height_offset = sheight - play_area_height

    def render(self):
        # Draw the grid
        for row in range(self.dimention[1]):
            for col in range(self.dimention[0]):
                draw_cord = (
                    self.top_left[0] + gv.TILE_WIDTH * col,
                    self.top_left[1] + gv.TILE_WIDTH * row
                )
                pg.draw.rect(
                    app.App.get_surface(),
                    self.grid[row][col],
                    (
                        draw_cord[0],
                        draw_cord[1],
                        gv.TILE_WIDTH,
                        gv.TILE_WIDTH
                    )
                )

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
            (self.bottom_right[0], self.bottom_right[1]),
            (self.bottom_right[0], self.top_left[1])
        )
        pg.draw.rect(
            app.App.get_surface(),
            gv.WHITE,
            (
                self.top_left[0] + 1,
                self.bottom_right[1] + 1,
                self.play_area_width,
                self.play_area_height_offset
            )
        )
    
    def add_to_grid(self, tetromino):
        for block in tetromino.blocks:
            pos = (tetromino.pos[0] + block.offset[0], tetromino.pos[1] + block.offset[1])
            self.grid[pos[1]][pos[0]] = tetromino.color
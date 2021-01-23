# Python modules
import pygame as pg

# App modules
import app

# Game modules
from .game_variables import GameVariables as gv

class PlayArea():
    """
    Represents the play area of the game in a 2D matrix
    """
    def __init__(self):
        # Create local variables for use
        self.dimention = (10, 20)
        self.grid = [[(0, 0, 0) for i in range(self.dimention[0])] for j in range(self.dimention[1])]
        # Get screen dimentions
        swidth = app.App.get_surface().get_width()
        sheight = app.App.get_surface().get_height()

        # Calculate the render variables
        render_height = sheight
        self.tile_width = render_height // self.dimention[1]
        gv.TILE_WIDTH = self.tile_width

        # Calculate the render offset
        gv.PLAY_AREA_TOP_LEFT = (
            (swidth - self.dimention[0] * self.tile_width) // 2,
            0
        )

        self._top_left = gv.PLAY_AREA_TOP_LEFT
        self._bottom_right = (
            self._top_left[0] + self.dimention[0] * self.tile_width,
            sheight
        )

        # Local variables created using the above calculations
        self._play_area_width = self.tile_width * self.dimention[0]
        play_area_height = self.tile_width * self.dimention[1]
        self._play_area_height_offset = sheight - play_area_height

    def render(self):
        """
        Renders the play area
        """
        # Draw the grid
        for row in range(self.dimention[1]):
            for col in range(self.dimention[0]):
                draw_cord = (
                    self._top_left[0] + gv.TILE_WIDTH * col,
                    self._top_left[1] + gv.TILE_WIDTH * row
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
            (self._top_left[0] - 1, self._top_left[1]),
            (self._top_left[0] - 1, self._bottom_right[1])
        )
        pg.draw.line(
            app.App.get_surface(),
            gv.WHITE,
            (self._bottom_right[0], self._bottom_right[1]),
            (self._bottom_right[0], self._top_left[1])
        )
        pg.draw.rect(
            app.App.get_surface(),
            gv.WHITE,
            (
                self._top_left[0] + 1,
                self._bottom_right[1] + 1,
                self._play_area_width,
                self._play_area_height_offset
            )
        )
    
    def add_to_grid(self, tetromino):
        """
        Add the given tetromino to the grid
        -1 = returned when the game is over
        0, 1, 2, 3, 4 = returned when there are a number of filled rows
        """
        # Add the tetromino to the grid
        for block in tetromino.blocks:
            pos = (tetromino.pos[0] + block.offset[0], tetromino.pos[1] + block.offset[1])
            # Game over
            if pos[1] == -1:
                return -1
            self.grid[pos[1]][pos[0]] = tetromino.color
        
        # Check if there are full rows, and return how many are there
        full_row_count = 0
        for row in range(self.dimention[1]):
            is_full = True
            for col in range(self.dimention[0]):
                # If it is not full get to the next row
                if self.grid[row][col] == (0, 0, 0):
                    is_full = False
                    break
            # If there is a full row, remove it and push all the rows on top of it down
            # Go bottom-up
            if is_full:
                full_row_count += 1
                for r in range(row, 0, -1):
                    for c in range(self.dimention[0]):
                        self.grid[r][c] = self.grid[r - 1][c]
                # If there is a full row the top row will be empty no matter what
                for c in range(self.dimention[0]):
                    self.grid[0][c] = (0, 0, 0)
        return full_row_count
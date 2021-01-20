# Python modules
import pygame as pg

# App modules
import app

# Game modules
from .game_variables import GameVariables as gv

class Block():
    """
    Represends one 1 of 4 blocks of a tetromino
    color = color of the block
    offset = the offset from the center of the tetromino in coordinates
    """
    def __init__(self, color, offset):
        self.color = color
        self.tile_width = gv.TILE_WIDTH
        self.offset = offset
    
    def render(self, position):
        """
        Renders the block
        """
        # Calculate the top left coordinate of the block
        draw_coord = (
            (position[0] + self.offset[0]) * self.tile_width + gv.PLAY_AREA_TOP_LEFT[0], 
            (position[1] + self.offset[1]) * self.tile_width + gv.PLAY_AREA_TOP_LEFT[1]
        )
        # Then draw it
        pg.draw.rect(
            app.App.get_surface(),
            self.color,
            (
                draw_coord[0],
                draw_coord[1],
                self.tile_width,
                self.tile_width
            )
        )

class Tetromino():
    """
    A tetromino class
    template = the template according to witch the tetromino will be created
    """
    def __init__(self, template):
        self.rotation_distributions = template[0].copy()
        self.number_of_rotations = len(self.rotation_distributions)
        self.rotation = 0
        self.color = template[1]
        self.pos = (5, 0)
        self.blocks = []
        
        self.generate_blocks()
    
    def render(self):
        """
        Renders the tetromino
        """
        # Render each block of the tetromino
        for block in self.blocks:
            block.render(self.pos)
    
    # Functions to manipulate the coordinates of the tetromino
    def move_up(self):
        """
        Moves the tetromino up
        """
        self.pos = (self.pos[0], self.pos[1] - 1)
    def move_down(self):
        """
        Moves the tetromino down
        """
        self.pos = (self.pos[0], self.pos[1] + 1)
    def move_right(self):
        """
        Moves the tetromino right
        """
        self.pos = (self.pos[0] + 1, self.pos[1])
    def move_left(self):
        """
        Moves the tetromino left
        """
        self.pos = (self.pos[0] - 1, self.pos[1])
    
    # Functions to manipulate the rotation of the tetromino
    def rotate_clockwise(self):
        """
        Rotates the tetromino clockwise
        """
        self.rotation += 1
        self.generate_blocks()
    def rotate_anticlockwise(self):
        """
        Rotates the tetromino anti-clockwise
        """
        self.rotation -= 1
        self.generate_blocks()

    def generate_blocks(self):
        """
        Genereates the blocks of the tetromino according to its blueprint and its rotation
        """
        # Delete the old blocks
        for block in self.blocks:
            del block
        self.blocks.clear()

        # Add the new blocks
        current_rotation_distribution = self.rotation_distributions[self.rotation % self.number_of_rotations]
        for i in range(5):
            for j in range(5):
                # If there is a block in the piece
                if current_rotation_distribution[j][i] == 1:
                    self.blocks.append(
                        Block(
                            self.color,
                            # Calculate the offset from the tetrominos position
                            (-(2 - i), -(2 - j))
                        )
                    )
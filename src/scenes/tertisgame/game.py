# Python modules
import random as rnd
import pygame as pg

# App modules
import app
from scenes.scene import Scene

# Game modules
from .playarea import PlayArea
from .tetromino import Tetromino
from .shapes import SHAPES

class Game(Scene):

    def __init__(self):
        self.pa = PlayArea()
        self.current_tetromino = None
        self.get_next_tetromino()
        
        self.count = 0
    
    def key_event(self, key):
        if key == pg.K_RIGHT:
            self.current_tetromino.move_right()
            if self.collision():
                self.current_tetromino.move_left()
        if key == pg.K_LEFT:
            self.current_tetromino.move_left()
            if self.collision():
                self.current_tetromino.move_right()
        if key == pg.K_RCTRL or key == pg.K_LCTRL or key == pg.K_z:
            self.current_tetromino.rotate_anticlockwise()
            if self.collision():
                # Check if it can rotate by moving left and right
                if not self.rotate_plus_movement_check():
                    return
                self.current_tetromino.rotate_clockwise()
        if key == pg.K_UP or key == pg.K_x:
            self.current_tetromino.rotate_clockwise()
            if self.collision():
                if not self.rotate_plus_movement_check():
                    return
                self.current_tetromino.rotate_anticlockwise()

    def update(self):
        self.count += 1
        if self.count >= 15:
            self.count = 0
            self.current_tetromino.move_down()
            if self.landed():
                self.get_next_tetromino()

        self.render()
    
    def render(self):
        self.pa.render()
        self.current_tetromino.render()
    
    def get_next_tetromino(self):
        # TODO Add in a second one to show the next tetromino in order
        # Delete the current tetromino
        del self.current_tetromino
        # Create the new tetromino
        self.current_tetromino = Tetromino(rnd.choice(SHAPES))

    # Collision checkers
    # Checks if the tetromino can be positioned elsewhere by moving it arround the area left and right
    def rotate_plus_movement_check(self):
        self.current_tetromino.move_right()
        if self.collision():
            self.current_tetromino.move_left()
        else:
            return False
        self.current_tetromino.move_right()
        self.current_tetromino.move_right()
        if self.collision():
            self.current_tetromino.move_left()
            self.current_tetromino.move_left()
        else:
            return False
        
        self.current_tetromino.move_left()
        if self.collision():
            self.current_tetromino.move_right()
        else:
            return False
        self.current_tetromino.move_left()
        self.current_tetromino.move_left()
        if self.collision():
            self.current_tetromino.move_right()
            self.current_tetromino.move_right()
        else:
            return False
        
        return True

    # Checks if tetromino is landed
    def landed(self):
        for block in self.current_tetromino.blocks:
            # Check if there is a piece under it
            # Or if it has reached the bottom of the play area
            pos = (self.current_tetromino.pos[0] + block.offset[0], self.current_tetromino.pos[1] + block.offset[1])
            if pos[1] >= self.pa.dimention[1]:
                self.current_tetromino.move_up()
                self.pa.add_to_grid(self.current_tetromino)
                return True
            if self.pa.grid[pos[1]][pos[0]] != (0, 0, 0):
                self.current_tetromino.move_up()
                self.pa.add_to_grid(self.current_tetromino)
                return True
        return False

    # Checks if the tetromino is out of bounds
    def out_of_bounds(self):
        for block in self.current_tetromino.blocks:
            # Check if it is out of bounds or not
            pos = (self.current_tetromino.pos[0] + block.offset[0], self.current_tetromino.pos[1] + block.offset[1])
            if pos[0] < 0 or pos[0] >= self.pa.dimention[0] or pos[1] < 0 or pos[1] >= self.pa.dimention[1]:
                return True
        return False

    # Checks if the tetromiino is colliding with the allready placed tetrominos
    def tetromino_collision(self):
        for block in self.current_tetromino.blocks:
            # Check if it is colliding with other tetrominos that are allready placed
            pos = (self.current_tetromino.pos[0] + block.offset[0], self.current_tetromino.pos[1] + block.offset[1])
            if self.pa.grid[pos[1]][pos[0]] != (0, 0, 0):
                return True
        return False

    # Checks for collisions that the current tetromino has with the edges and the other tetrominos
    def collision(self):
        if self.out_of_bounds():
            return True
        if self.tetromino_collision():
            return True
        return False
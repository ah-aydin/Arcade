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
        self.current_tetromino = Tetromino(rnd.choice(SHAPES))
        
        self.count = 0
    
    def key_event(self, key):
        if key == pg.K_RIGHT:
            self.current_tetromino.move_right()
        if key == pg.K_LEFT:
            self.current_tetromino.move_left()

    def update(self):
        self.count += 1
        if self.count >= 30:
            self.count = 0
            self.current_tetromino.move_down()

        self.render()
    
    def render(self):
        self.pa.render()
        self.current_tetromino.render()
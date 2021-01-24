# Python modules
import pygame as pg

# App modules
import app
import scenes as s
from scenes.scene import BaseGame

from .game_variables import GameVariables as gv

class Game(BaseGame):
    """
    The game class for space shooty shooty
    """
    def __init__(self):
        super(Game, self).__init__()
    
    def update(self):
        if not self._pause:
            pass

        self.render()
    
    def render(self):
        self._renderUI()
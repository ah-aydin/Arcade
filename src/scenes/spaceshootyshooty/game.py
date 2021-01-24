# Python modules
import pygame as pg

# App modules
import app
import scenes as s
from scenes.scene import BaseGame

# Game modules
from .space_ship import SpaceShip
from .game_variables import GameVariables as gv

class Game(BaseGame):
    """
    The game class for space shooty shooty
    """
    def __init__(self):
        super(Game, self).__init__()

        self._space_ship = SpaceShip(
            (500, 500),
            0,
            (100, 30),
            gv.SPACE_SHIP_SPEED,
            gv.SPACE_SHIP_ROTATION_SPEED
        )

        # Variales to keep track of the ship's movement
        self._FORWARD = 0
        self._BACKWARD = 0
        self._TURN_RIGHT = 0
        self._TURN_LEFT = 0
    
    def key_up_event(self, key):
        if key == pg.K_UP:
            self._FORWARD = 0
        if key == pg.K_DOWN:
            self._BACKWARD = 0
        if key == pg.K_RIGHT:
            self._TURN_RIGHT = 0
        if key == pg.K_LEFT:
            self._TURN_LEFT = 0

    def key_event(self, key):
        if key == pg.K_UP:
            self._FORWARD = 1
        if key == pg.K_DOWN:
            self._BACKWARD = 1
        if key == pg.K_RIGHT:
            self._TURN_RIGHT = 1
        if key == pg.K_LEFT:
            self._TURN_LEFT = 1
        

    def update(self):
        if not self._pause:
            self._space_ship.move(self._FORWARD - self._BACKWARD)
            self._space_ship.turn(self._TURN_RIGHT - self._TURN_LEFT)
        self.render()
    
    def render(self):
        self._space_ship.render()
        self._renderUI()
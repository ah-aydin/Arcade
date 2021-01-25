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
            (100, 100),
            gv.SPACE_SHIP_SPEED,
            gv.SPACE_SHIP_ROTATION_SPEED
        )

        self._gameObjects.append(self._space_ship)

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
        if key == pg.K_SPACE:
            self._space_ship.fire()
        

    def update(self):
        if not self._pause:
            # Pass along the movement variables to th ship
            self._space_ship.pass_input(self._FORWARD - self._BACKWARD, self._TURN_RIGHT - self._TURN_LEFT)
            for gameObject in self._gameObjects:
                gameObject.update()
        self.render()
    
    def render(self):
        # Render the game objects
        self._space_ship.render()
        for gameObject in self._gameObjects:
            gameObject.render()
        # Render the UI
        self._renderUI()
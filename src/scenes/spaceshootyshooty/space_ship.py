# Python modules
import math
import pygame as pg
import pygame.transform as T

# App modules
import app

# Game modules
from .game_variables import GameVariables as gv

class SpaceShip():
    """
    Class for the space ship
    pos = starting position of the ship
    rotation = starting rotation of the ship
    size = size of the ship
    speed = the movement speed of the ship
    rotation_speed = the rotation speed of the ship
    """    

    def __init__(
        self,
        pos: (int, int) = (0, 0),
        rotation: int = 0,
        size: (int, int) = (50, 50),
        speed: int = 15,
        rotation_speed: int = 5
    ):
        self._pos = pos
        self._rotation = rotation
        self._size = size
        self._speed = speed
        self._rotation_speed = rotation_speed
        self._rect = pg.Rect(*pos, *size)

        # Default surface to hold the sprite
        self._surface = pg.Surface(self._rect.size)
        pg.draw.ellipse(self._surface, (255, 0, 0), (0, 0, *size))

    def render(self):
        """
        Render's the object
        """
        # Create a rotated version of the object
        render_surface = T.rotate(self._surface, -self._rotation)
        # Put the newly created surface to the screen
        app.App.get_surface().blit(render_surface, render_surface.get_rect(center = self._rect.center))
        # Draw a line that indicates the forward vector of the ship
        pg.draw.line(
            app.App.get_surface(),
            (255, 255, 255),
            self._rect.center,
            (
                self._rect.center[0] + int(self._speed * math.cos(math.radians(self._rotation))),
                self._rect.center[1] + int(self._speed * math.sin(math.radians(self._rotation)))
            )
        )
    
    def move(self, m):
        """
        Moves the ship
        """
        self._rect = pg.Rect(
            self._rect.x + m * int(self._speed * math.cos(math.radians(self._rotation))),
            self._rect.y + m * int(self._speed * math.sin(math.radians(self._rotation))),
            *self._size
        )
    
    def turn(self, ammount):
        """
        Turn the ship
        """
        self._rotation += ammount * self._rotation_speed
        if self._rotation > 359:
            self._rotation -= 360
        if self._rotation < 0 :
            self._rotation += 360

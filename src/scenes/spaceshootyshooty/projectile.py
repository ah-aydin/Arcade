# Python modules
import math
import pygame as pg
import pygame.transform as T

# App modules
import app

# Game modules
from .game_variables import GameVariables as gv

class Projectile():
    """
    Class for the projectile
    """
    def __init__(
        self,
        pos: (int, int) = (0, 0),
        rotation: int = 0,
        size: (int, int) = (30, 10),
        speed: int = 20
    ):
        self._pos = pos
        self._rotation = rotation
        self._size = size
        self._speed = speed
        self._rect = pg.Rect(
            pos[0] - size[0] // 2,
            pos[1] - size[1] // 2,
            *size
        )

        # Default surface to hold the sprite
        self._surface = pg.Surface(self._rect.size, flags=pg.SRCALPHA)
        pg.draw.ellipse(self._surface, (0, 0, 255), (0, 0, *size))
    
    def update(self):
        self._rect = pg.Rect(
            self._rect.x + int(self._speed * math.cos(math.radians(self._rotation))),
            self._rect.y + int(self._speed * math.sin(math.radians(self._rotation))),
            *self._size
        )
    
    def render(self):
        """
        Render's the object
        """
        # Create a rotated version of the object
        render_surface = T.rotate(self._surface, -self._rotation)
        # Put the newly created surface to the screen
        app.App.get_surface().blit(render_surface, render_surface.get_rect(center = self._rect.center))
        # Draw a line that indicates the forward vector of the projectile
        pg.draw.line(
            app.App.get_surface(),
            (255, 255, 255),
            self._rect.center,
            (
                self._rect.center[0] + int(self._speed * math.cos(math.radians(self._rotation))),
                self._rect.center[1] + int(self._speed * math.sin(math.radians(self._rotation)))
            )
        )
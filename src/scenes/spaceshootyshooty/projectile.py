# Python modules
import math
import pygame as pg
import pygame.transform as T
import os

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
        size: (int, int) = (70, 30),
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

        # Load in the sprite
        self._sprite = pg.image.load(os.path.join("res", "projectile.png"))
        self._sprite = pg.transform.scale(self._sprite, size)

        # Default surface to hold the sprite
        self._surface = pg.Surface(self._rect.size, flags=pg.SRCALPHA)
        self._surface.blit(self._sprite, (0, 0))
    
    def update(self):
        new_x = self._rect.x + int(self._speed * math.cos(math.radians(self._rotation)))
        new_y = self._rect.y + int(self._speed * math.sin(math.radians(self._rotation)))

        self._rect = pg.Rect(
            new_x,
            new_y,
            *self._size
        )
        self._pos = self._rect.center

        self._out_of_bounds()
    
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
    
    def _out_of_bounds(self):
        """
        Checks if the projectile is out of bounds.
        If it is, it gets removed from the game
        """
        # Check if it is out of bounds
        if self._pos[0] < 0 or self._pos[0] > gv.PLAY_AREA_WIDTH or self._pos[1] < 0 or self._pos[1] > gv.PLAY_AREA_HEIGHT:
            # Remove it from the game
            app.App.get_current_scene().remove_game_object(self)
        
        del self
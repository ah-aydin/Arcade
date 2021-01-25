# Python modules
import math
import pygame as pg
import pygame.transform as T

# App modules
import app

# Game modules
from .projectile import Projectile as P
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
        self._rect = pg.Rect(
            pos[0] - size[0] // 2,
            pos[1] - size[1] // 2,
            *size
        )

        self._movement = 0
        self._turning = 0

        # Default surface to hold the sprite
        self._surface = pg.Surface(self._rect.size, flags=pg.SRCALPHA)
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
    
    def pass_input(self, movement, turning):
        self._movement = movement
        self._turning = turning

    def update(self):
        self._move()
        self._turn()

    def _move(self):
        """
        Moves the ship
        """
        # If the ship is not in move state, return
        if self._movement == 0:
            return

        # Get the new positons
        new_x = self._pos[0] + self._movement * int(self._speed * math.cos(math.radians(self._rotation)))
        new_y = self._pos[1] + self._movement * int(self._speed * math.sin(math.radians(self._rotation)))

        # Check if the new positions are outside the play area
        if new_x < 0: new_x = 0
        if new_x > gv.PLAY_AREA_WIDTH: new_x = gv.PLAY_AREA_WIDTH
        if new_y < 0: new_y = 0
        if new_y > gv.PLAY_AREA_HEIGHT: new_y = gv.PLAY_AREA_HEIGHT

        self._pos = (new_x, new_y)

        self._rect = pg.Rect(
            self._pos[0] - self._size[0] // 2,
            self._pos[1] - self._size[1] // 2,
            *self._size
        )
    
    def _turn(self):
        """
        Turn the ship
        """
        self._rotation += self._turning * self._rotation_speed
        if self._rotation > 359:
            self._rotation -= 360
        if self._rotation < 0 :
            self._rotation += 360

    def get_rotation(self):
        """
        Returns the rotation of the object
        """
        return self._rotation
    
    def fire(self):
        """
        The function name is self explenatory
        """
        # Spawn a projectile
        app.App().get_current_scene().add_game_object(P(self._rect.center, self._rotation, speed = gv.PROJECTILE_SPEED))
        
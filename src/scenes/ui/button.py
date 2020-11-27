# Pygame
import pygame as pg

# App module
import app

from .widget import Clickable

class Button(Clickable):
    def __init__(
        self,
        pos: (int, int) = (0, 0),
        size: (int, int) = (0, 0),
        color: (int, int, int) = (0, 0, 0),
        hover_color: (int, int, int) = (0, 0, 0)
    ):
        super(Button, self).__init__(pos, size, color)

        self.hover_color = hover_color

        # Other local variables
        self.current_color = self.color
    
    def self_render(self):
        pg.draw.rect(
            app.App.get_surface(),
            self.current_color,
            (self.pos[0], self.pos[1], self.size[0], self.size[1])
        )
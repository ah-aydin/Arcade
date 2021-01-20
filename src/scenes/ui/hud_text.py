# App module
import app

# Pygame
import pygame as pg

from .widget import Widget

class HudText(Widget):
    """
    A simple widget to display text on the screen
    """
    def __init__(
        self,
        pos: (int, int) = (0, 0),
        size: (int, int) = (0, 0),
        color: (int, int, int) = (0, 0, 0),
        text: str = "",
        font_size: int = 16
    ):
        super(HudText, self).__init__(pos, size, color)
        self.text = text
        self.font = pg.font.SysFont("Consolas", font_size)
    
    def set_font_size(self, font_size: int):
        self.font = pg.font.SysFont("Consolas", font_size)
    
    def set_text(self, text: str):
        self.text = text

    def self_render(self):
        text_render = self.font.render(self.text, True, self.color)
        app.App.get_surface().blit(text_render, self.pos)
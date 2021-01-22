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
        font_size: int = 16,
        text_centered = False
    ):
        super(HudText, self).__init__(pos, size, color)
        self.text = text
        self.font = pg.font.SysFont("Consolas", font_size)
        self.text_centered = text_centered
        
        self.text_size = (0, 0)
        self.centered_pos = (0, 0)

        self._calculate_text_size()
        if text_centered:
            self._calculate_centered_pos()

    def _calculate_text_size(self):
        """
        Calculates the text size in pixels
        """
        self.text_size = self.font.size(self.text)
    
    def _calculate_centered_pos(self):
        """
        Calculates the position on the screen where the text will be centered inside the widget
        """
        self.centered_pos = (
            self.pos[0] + (self.size[0] - self.text_size[0]) // 2,
            self.pos[1] + (self.size[1] - self.text_size[1]) // 2
        )

    def set_font_size(self, font_size: int):
        """
        Set's the font size with the given parameter
        """
        self.font = pg.font.SysFont("Consolas", font_size)
    
    def set_text(self, text: str):
        """
        Changes the contents of the text with the given parameter
        """
        self.text = text
        # Calculate the text size and the centered position if needed every time the text is changed
        self._calculate_text_size()
        if self.text_centered:
            self._calculate_centered_pos()

    def self_render(self):
        text_render = self.font.render(self.text, True, self.color)
        # If the text is not centered, render it at the top left corner of the widget
        if not self.text_centered:
            app.App.get_surface().blit(text_render, self.pos)
        else: # Otherwise, render the text in the middle of the widget
            app.App.get_surface().blit(text_render, self.centered_pos)
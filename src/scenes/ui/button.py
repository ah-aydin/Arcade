# Pygame
import pygame as pg

# App module
import app

from .widget import Clickable
from .hud_text import HudText

class Button(Clickable):
    """
    A button widget that is clickable
    pos = Position of the button
    size = Size of the button
    color = Default color of the buttom
    hover_color = The color when the button is hovered
    text = The text that will be displayed on the button
    text_color = Color of the button text
    font_size = font size for the text
    """
    def __init__(
        self,
        pos: (int, int) = (0, 0),
        size: (int, int) = (0, 0),
        color: (int, int, int) = (0, 0, 0),
        hover_color: (int, int, int) = (0, 0, 0),
        text: str = "",
        text_color: (int, int, int) = (255, 255, 255),
        font_size: int = 16
    ):
        super(Button, self).__init__(pos, size, color)

        self.hover_color = hover_color

        # Other local variables
        self.current_color = self.color

        # If there is a supplied string, create a text child text object for the button
        if text != "":
            # Calculate the position of the text so that it is centered on the button
            text_size = pg.font.SysFont("Consolas", font_size).size(text)
            pos_x = self.pos[0] + (self.size[0] - text_size[0]) // 2
            pos_y = self.pos[1] + (self.size[1] - text_size[1]) // 2
            # Create and add the text as a child of button
            self._children.append(
                HudText(
                    ( # Position
                        pos_x,
                        pos_y
                    ),
                    text_size,
                    text_color,
                    text,
                    font_size
                )
            )
    
    def _self_render(self):
        pg.draw.rect(
            app.App.get_surface(),
            self.current_color,
            (self.pos[0], self.pos[1], self.size[0], self.size[1])
        )
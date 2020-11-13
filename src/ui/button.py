# Python modules
import pygame as pg

# App modules
from app import App

class Button:
    def __init__(self, 
        size: (int, int), 
        pos: (int, int), 
        color: (int, int, int),
        hover_color: (int, int, int),
        text="", 
        font_size=16, 
        font_color=(0, 0, 0)
    ):
        self.size = size
        self.pos = pos
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font_color = font_color

        self.current_color = self.color
        self.is_hovered = False
        self.font = pg.font.SysFont("Consolas", font_size, True)
    
    def key_event(self, key):
        pass

    def render(self):
        pg.draw.rect(
            App.get_surface(),  # surface
            self.current_color,         # color
            (                   # rect
                self.pos[0],
                self.pos[1],
                self.size[0],
                self.size[1]
            )
        )
        text = self.font.render(self.text, False, self.font_color)
        App.get_surface().blit(text, self.pos)
    
    def set_on_click(self, click_func):
        self.click_func = click_func
    
    def on_click(self):
        self.click_func()
    
    def on_hover(self):
        self.is_hovered = True
        self.current_color = self.hover_color
    
    def un_hover(self):
        self.is_hovered = False
        self.current_color = self.color

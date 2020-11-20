# Python modules
import pygame as pg

# App modules
from app import App

# Games
from scenes import SnakeGame

# Ui elements
from .button import Button

class MainMenu:
    def __init__(self):
        self.elements = []
        self.elements.append(
            Button(
                (200, 100),
                (500, 500),
                (255, 0, 0),
                (0, 255, 0),
                "Play",
                16,
                (0, 0, 0)
            )
        )

        self.elements[0].set_on_click(lambda: App.set_current_game(SnakeGame()))
    
    def key_event(self, key):
        pass

    def update(self):
        self.render()

    def render(self):
        for elem in self.elements:
            elem.render()
    
    def mouse_move_event(self, pos):
        for elem in self.elements:
            if pos[0] >= elem.pos[0] and pos[0] <= elem.pos[0] + elem.size[0] and pos[1] >= elem.pos[1] and pos[1] <= elem.pos[1] + elem.size[1]:
                elem.on_hover()
            else:
                elem.un_hover()
    
    def mouse_click_event(self, pos):
        for elem in self.elements:
            if elem.is_hovered:
                elem.on_click()
            
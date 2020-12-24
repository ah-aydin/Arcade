# Python modules
import pygame as pg

# App modules
import app

# Scene
from scenes import SnakeGame
from scenes.scene import Scene

from scenes import SnakeGame, TetrisGame

# Ui elements
from .button import Button
from .widget import Clickable

class MainMenu(Scene):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.uiElements = [
            Button((100, 100), (300, 150), (255, 0, 0)),
            Button((500, 100), (300, 150), (255, 0, 0)),
            Button((900, 100), (300, 150), (255, 0, 0)),
            Button((100, 400), (300, 150), (255, 0, 0)),
        ]

        self.uiElements[0].set_on_mouse_click(lambda: app.App.set_current_game(SnakeGame()))
        self.uiElements[1].set_on_mouse_click(lambda: app.App.set_current_game(TetrisGame(0)))
        self.uiElements[2].set_on_mouse_click(lambda: print(3))
        self.uiElements[3].set_on_mouse_click(lambda: app.App.set_running(False))

        screen_size = app.App.get_surface().get_size()
        self.mouseClickMapping = [[None for y in range(screen_size[0])] for x in range(screen_size[1])]
        self.generateMouseClickMapping()

    def generateMouseClickMapping(self):
        for elem in self.uiElements:
            if issubclass(type(elem), Clickable):
                xpos, ypos = elem.pos
                for x in range(elem.size[0]):
                    for y in range(elem.size[1]):
                        if ypos + y < len(self.mouseClickMapping) and xpos + x < len(self.mouseClickMapping[0]) and ypos + y >= 0 and xpos + x >= 0:
                            self.mouseClickMapping[ypos + y][xpos + x] = elem
    
    def key_event(self, key):
        pass

    def update(self):
        self.render()

    def render(self):
        for elem in self.uiElements:
            elem.render()
    
    def mouse_move_event(self, pos):
        return
    
    def mouse_click_event(self, pos):
        elem = self.mouseClickMapping[pos[1]][pos[0]]
        if elem != None:
            elem.on_mouse_click()

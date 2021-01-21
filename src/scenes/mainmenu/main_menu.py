# Python modules
import pygame as pg

# App modules
import app

# Scene
from scenes.scene import Scene

from scenes import SnakeMenu, TetrisGame

# Ui elements
from scenes import Button
from scenes import Clickable

class MainMenu(Scene):
    """
    The main menu of the game
    """
    def __init__(self):
        super(MainMenu, self).__init__()
        # Create the buttons for the menu
        self.uiElements = [
            Button((100, 100), (300, 150), (255, 0, 0), text="Snake", font_size=30),
            Button((500, 100), (300, 150), (255, 0, 0), text="Tetris", font_size=30),
            Button((900, 100), (300, 150), (255, 0, 0), text="Nothing here at the moment", font_size=30),
            Button((100, 400), (300, 150), (255, 0, 0), text="Exit", font_size=30),
        ]

        # Set the buttons functionality
        self.uiElements[0].set_on_mouse_click(lambda: app.App.set_current_game(SnakeMenu())) # This opens the snake game menu
        self.uiElements[1].set_on_mouse_click(lambda: app.App.set_current_game(TetrisGame(0))) # This opens the tetris game
        self.uiElements[2].set_on_mouse_click(lambda: print(3)) # This prints 3
        self.uiElements[3].set_on_mouse_click(lambda: app.App.set_running(False)) # This exits the application

        # Map the mouse click mapping for the clickable objects
        screen_size = app.App.get_surface().get_size()
        self.mouseClickMapping = [[None for y in range(screen_size[0])] for x in range(screen_size[1])]
        self.generateMouseClickMapping()

    def generateMouseClickMapping(self):
        """
        Generates the moue click mapping
        """
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
        """
        Called every frame
        """
        self.render()

    def render(self):
        """
        Renders the menu
        """
        # Render the UI
        for elem in self.uiElements:
            elem.render()
    
    def mouse_move_event(self, pos):
        return
    
    def mouse_click_event(self, pos):
        """
        Called when there is a mouse click event
        """
        elem = self.mouseClickMapping[pos[1]][pos[0]]
        if elem != None:
            elem.on_mouse_click()

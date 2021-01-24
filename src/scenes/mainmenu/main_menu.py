# Python modules
import pygame as pg

# App modules
import app

# Scene
from scenes.scene import BaseMenu

from scenes import SnakeMenu, TetrisMenu, SpaceShootyShootyMenu

# Ui elements
from scenes import Button
from scenes import Clickable

class MainMenu(BaseMenu):
    """
    The main menu of the game
    """
    def __init__(self):
        super(MainMenu, self).__init__()
        # Create the buttons for the menu
        self._uiElements += [
            Button((100, 100), (300, 150), (255, 0, 0), text="Snake", font_size=30),
            Button((500, 100), (300, 150), (255, 0, 0), text="Tetris", font_size=30),
            Button((900, 100), (300, 150), (255, 0, 0), text="Space Shooty Shooty", font_size=30),
            Button((100, 400), (300, 150), (255, 0, 0), text="Exit", font_size=30),
        ]

        # Set the buttons functionality
        self._uiElements[0].set_on_mouse_click(lambda: app.App.set_current_scene(SnakeMenu())) # Opens the snake menu
        self._uiElements[1].set_on_mouse_click(lambda: app.App.set_current_scene(TetrisMenu())) # opens the tetris menu
        self._uiElements[2].set_on_mouse_click(lambda: app.App.set_current_scene(SpaceShootyShootyMenu())) # Opens the space shooty shooty menu
        self._uiElements[3].set_on_mouse_click(lambda: app.App.set_running(False)) # This exits the application

        self._generateMouseClickMapping()
    
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
        for elem in self._uiElements:
            elem.render()
    
    def mouse_move_event(self, pos):
        return
    

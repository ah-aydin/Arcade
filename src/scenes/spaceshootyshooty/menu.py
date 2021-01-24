# Python modules
import pygame as pg

# App modules
import app

# Scene
import scenes as s
from scenes.scene import BaseMenu

# Game modules
from .game_variables import GameVariables as gv
from .game import Game

class Menu(BaseMenu):

    def __init__(self):
        super(Menu, self).__init__()

        screen_size = app.App.get_surface().get_size()

        # Calculate the button size's according to the screen resolution
        button_size = (
            screen_size[0] * 10 // 100,
            screen_size[0] * 10 // 100
        )

        # Create the UI elements
        self._uiElements += [
            s.Button( # The start button
                (
                    screen_size[0] // 2 - button_size[0] * 2,
                    screen_size[1] // 2 + button_size[1] // 2 + 9
                ),
                (
                    button_size[0] * 4,
                    int(button_size[1] * 0.5)
                ),
                (0, 255, 0),
                text = "START",
                font_size = 50,
            ),
            s.HudText( # Just displays the text "SPACE SHOOTY SHOOTY" on the screen
                (
                    screen_size[0] // 2 - button_size[0] * 2,
                    screen_size[1] // 2 - button_size[1] * 2 - 40
                ),
                (
                    button_size[0] * 4,
                    button_size[1]
                ),
                (255, 0, 0),
                text = "SPACE SHOOTY SHOOTY",
                font_size = 150,
                text_centered = True
            ),
            s.Button( # Back to main menu button
                (
                    screen_size[0] // 2 - button_size[0] * 2,
                    screen_size[1] // 2 + button_size[1] + 18
                ),
                (
                    button_size[0] * 4,
                    int(button_size[1] * 0.5)
                ),
                (110, 110, 100),
                text = "BACK TO MENU",
                font_size = 50,
            )
        ]

        # Set the onclick methods for the buttons
        self._uiElements[0].set_on_mouse_click(lambda: app.App.set_current_scene(Game())) # Start's the game
        self._uiElements[2].set_on_mouse_click(lambda: app.App.set_current_scene(s.MainMenu())) # Goes back to main menu

        self._generateMouseClickMapping()

        # Varaible to keep track of the starting level
        self._starting_level = 0

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
        self._renderUI()
        
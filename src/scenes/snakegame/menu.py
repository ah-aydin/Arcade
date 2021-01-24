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
    """
    Menu for the snake game
    """
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
            s.Button( # Button to increment the level
                (
                    screen_size[0] // 2 + button_size[0],
                    screen_size[1] // 2 - button_size[1] // 2
                ),
                button_size,
                (255, 0, 0),
                text = "+",
                font_size = 50
            ),
            s.Button( # Button to decrement the level
                (
                    screen_size[0] // 2 - button_size[0] * 2,
                    screen_size[1] // 2 - button_size[1] // 2
                ),
                button_size,
                (255, 0, 0),
                text = "-",
                font_size = 50
            ),
            s.HudText( # Displays the current starting level of the game
                (
                    screen_size[0] // 2 - button_size[0],
                    screen_size[1] // 2 - button_size[1] // 2
                ),
                (
                    button_size[0] * 2,
                    button_size[1]
                ),
                (255, 255, 255),
                text = "Level: 0",
                font_size = 40,
                text_centered = True
            ),
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
            s.HudText( # Just displays the text "SNAKE" on the screen
                (
                    screen_size[0] // 2 - button_size[0] * 2,
                    screen_size[1] // 2 - button_size[1] * 2 - 40
                ),
                (
                    button_size[0] * 4,
                    button_size[1]
                ),
                (255, 0, 0),
                text = "SNAKE",
                font_size = 200,
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
        self._uiElements[0].set_on_mouse_click(lambda: self._increment_starting_level()) # Increment level
        self._uiElements[1].set_on_mouse_click(lambda: self._decrement_starting_level()) # Decrement level
        self._uiElements[3].set_on_mouse_click(lambda: app.App.set_current_scene(Game(self._starting_level))) # Start's the game
        self._uiElements[5].set_on_mouse_click(lambda: app.App.set_current_scene(s.MainMenu())) # Goes back to main menu

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
        
    def _increment_starting_level(self):
        """
        Increment's the starting level
        """
        self._starting_level += 1
        # If the starting level goes outside the level range, undo the operation
        if self._starting_level < 0 or self._starting_level >= len(gv.LEVEL_FPS):
            self._starting_level -= 1
        self._uiElements[2].set_text("Level: " + str(self._starting_level))
    def _decrement_starting_level(self):
        """
        Decrement's the starting level
        """
        self._starting_level -= 1
        # If the starting level goes outside the level range, undo the operation
        if self._starting_level < 0 or self._starting_level >= len(gv.LEVEL_FPS):
            self._starting_level += 1
        self._uiElements[2].set_text("Level: " + str(self._starting_level))
# Python modules
import pygame as pg

# App modules
import app

# Scene
import scenes as s
from scenes.scene import Scene

# Game modules
from .game_variables import GameVariables as gv
from .game import Game

class Menu(Scene):
    def __init__(self):
        super(Menu, self).__init__()

        screen_size = app.App.get_surface().get_size()

        # Calculate the button size's according to the screen resolution
        button_size = (
            screen_size[0] * 10 // 100,
            screen_size[0] * 10 // 100
        )

        # Create the UI elements
        self.uiElements = [
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
            s.HudText( # Just displays the text "TETRIS" on the screen
                (
                    screen_size[0] // 2 - button_size[0] * 2,
                    screen_size[1] // 2 - button_size[1] * 2 - 40
                ),
                (
                    button_size[0] * 4,
                    button_size[1]
                ),
                (255, 0, 0),
                text = "TETRIS",
                font_size = 200,
                text_centered = True
            )
        ]

        # Set the onclick methods for the buttons
        self.uiElements[0].set_on_mouse_click(lambda: self.increment_starting_level()) # Increment level
        self.uiElements[1].set_on_mouse_click(lambda: self.decrement_starting_level()) # Decrement level
        self.uiElements[3].set_on_mouse_click(lambda: app.App.set_current_game(Game(self.starting_level))) # Start's the game

        # Map the mouse click mapping for the clickable objects
        self.mouseClickMapping = [[None for y in range(screen_size[0])] for x in range(screen_size[1])]
        self.generateMouseClickMapping()

        # Varaible to keep track of the starting level
        self.starting_level = 0

    def generateMouseClickMapping(self):
        """
        Generates the moue click mapping
        """
        for elem in self.uiElements:
            if issubclass(type(elem), s.Clickable):
                xpos, ypos = elem.pos
                for x in range(elem.size[0]):
                    for y in range(elem.size[1]):
                        if ypos + y < len(self.mouseClickMapping) and xpos + x < len(self.mouseClickMapping[0]) and ypos + y >= 0 and xpos + x >= 0:
                            self.mouseClickMapping[ypos + y][xpos + x] = elem

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
    
    def increment_starting_level(self):
        """
        Increment's the starting level
        """
        self.starting_level += 1
        # If the starting level goes outside the level range, undo the operation
        if self.starting_level < 0 or self.starting_level >= len(gv.LEVEL_FPS):
            self.starting_level -= 1
        self.uiElements[2].set_text("Level: " + str(self.starting_level))
    def decrement_starting_level(self):
        """
        Decrement's the starting level
        """
        self.starting_level -= 1
        # If the starting level goes outside the level range, undo the operation
        if self.starting_level < 0 or self.starting_level >= len(gv.LEVEL_FPS):
            self.starting_level += 1
        self.uiElements[2].set_text("Level: " + str(self.starting_level))
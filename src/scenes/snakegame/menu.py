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
            screen_size[0] * 20 // 100,
            screen_size[1] * 15 // 100
        )

        # Create the UI elements
        self.uiElements = [
            s.Button( # Button for level 0
                (
                    screen_size[0] * 27 // 100,
                    screen_size[1] * 30 // 100
                ), 
                button_size, 
                (255, 0, 0),
                text = "Level 0",
                font_size = 34
            ),
            s.Button( # Button for level 1
                (
                    screen_size[0] * 27 // 100 + screen_size[0] * 26 // 100,
                    screen_size[1] * 30 // 100
                ), 
                button_size, 
                (255, 0, 0),
                text = "Level 1",
                font_size = 34
            ),
            s.Button( # Button for level 2
                (
                    screen_size[0] * 27 // 100,
                    screen_size[1] * 30 // 100 + screen_size[1] * 25 // 100
                ), 
                button_size, 
                (255, 0, 0),
                text = "Level 2",
                font_size = 34
            ),
            s.Button( # Button for level 3
                (
                    screen_size[0] * 27 // 100 + screen_size[0] * 26 // 100,
                    screen_size[1] * 30 // 100 + screen_size[1] * 25 // 100
                ), 
                button_size, 
                (255, 0, 0),
                text = "Level 3",
                font_size = 34
            )
        ]

        # Set the onclick methods for the buttons
        self.uiElements[0].set_on_mouse_click(lambda: app.App.set_current_game(Game(0))) # Level 0
        self.uiElements[1].set_on_mouse_click(lambda: app.App.set_current_game(Game(1))) # Level 1
        self.uiElements[2].set_on_mouse_click(lambda: app.App.set_current_game(Game(2))) # Level 2
        self.uiElements[3].set_on_mouse_click(lambda: app.App.set_current_game(Game(3))) # Level 3

        # Map the mouse click mapping for the clickable objects
        self.mouseClickMapping = [[None for y in range(screen_size[0])] for x in range(screen_size[1])]
        self.generateMouseClickMapping()

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
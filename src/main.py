# Python modules
import pygame as pg
import time
import sys

# App modules
from app import App

from games import SnakeGame
from ui import *

# Initialize pygame
pg.init()
pg.font.init()

# Global variables
FRAMES = 60
ONE_FRAME_IN_SECONDS = 1 / FRAMES
TIMER = 0
LAST_FRAME = time.time()
CURRENT_FRAME = 0
BLACK = (0, 0, 0)

# Create the render target
App.set_surface(pg.display.set_mode(flags=pg.FULLSCREEN))

# Create the game
#game = SnakeGame()
App.set_current_game(MainMenu())

while App.running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            App.set_running(False)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                App.set_running(False)
            App.get_current_game().key_event(event.key)
        if event.type == pg.MOUSEMOTION:
            App.get_current_game().mouse_move_event(pg.mouse.get_pos())
        if event.type == pg.MOUSEBUTTONDOWN:
            App.get_current_game().mouse_click_event(pg.mouse.get_pos())

    # Update the timer
    CURRENT_FRAME = time.time()
    TIMER += CURRENT_FRAME - LAST_FRAME
    LAST_FRAME = CURRENT_FRAME

    # Render at the given FPS
    if TIMER >= ONE_FRAME_IN_SECONDS:
        TIMER -= ONE_FRAME_IN_SECONDS

        # Clear the surface
        App.clear_surface(BLACK)

        # Update the game state
        App.get_current_game().update()

        # Update the display
        pg.display.update()

pg.quit()

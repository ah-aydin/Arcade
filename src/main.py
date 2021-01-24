# Python modules
import pygame as pg
import time

# App modules
from app import App

from scenes import MainMenu, BaseGame

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

# Create and mark the MainMenu as the current game
App.set_current_scene(MainMenu())

while App.running:
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            App.set_running(False)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                # If the current scenes is a game, pause it
                if issubclass(type(App.get_current_scene()), BaseGame):
                    App.get_current_scene().toggle_pause()
            # Pass the key to the current scenes key event managment function
            App.get_current_scene().key_event(event.key)
        if event.type == pg.KEYUP:
            App.get_current_scene().key_up_event(event.key)

        if event.type == pg.MOUSEMOTION:
            # Pass the mouse move event to the current scenes mouse event managment function
            App.get_current_scene().mouse_move_event(pg.mouse.get_pos())

        if event.type == pg.MOUSEBUTTONDOWN:
            # Pass the mouse click event to the current scenes mouse event management function
            App.get_current_scene().mouse_click_event(pg.mouse.get_pos())

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
        App.get_current_scene().update()

        # Update the display
        pg.display.update()
        
App.set_current_scene(None)
pg.quit()

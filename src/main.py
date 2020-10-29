# Python modules
import pygame as pg
import time
import sys

# App modules
from app import App

from snakegame import *

pg.init()

# Global variables
global FRAMES, ONE_FRAME_IN_SECONDS, TIMER, LAST_FRAME, CURRENT_FRAME
FRAMES = 60
ONE_FRAME_IN_SECONDS = 1 / FRAMES
TIMER = 0
LAST_FRAME = time.time()
CURRENT_FRAME = 0
BLACK = (0, 0, 0)

default_font = pg.font.SysFont("Consolas", 30)

def main():
    global FRAMES, ONE_FRAME_IN_SECONDS, TIMER, LAST_FRAME, CURRENT_FRAME

    # Create the render target
    App.set_surface(pg.display.set_mode(flags=pg.FULLSCREEN))

    # Temporary game elements
    pa = PlayArea(20, 30)
    snake = Snake(16, (17, 10), 30, BLUE, 3)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False
                if event.key == pg.K_UP:
                    snake.set_direction(UP)
                if event.key == pg.K_DOWN:
                    snake.set_direction(DOWN)
                if event.key == pg.K_RIGHT:
                    snake.set_direction(RIGHT)
                if event.key == pg.K_LEFT:
                    snake.set_direction(LEFT)

        # Update the timer
        CURRENT_FRAME = time.time()
        TIMER += CURRENT_FRAME - LAST_FRAME
        LAST_FRAME = CURRENT_FRAME

        # Render at the given FPS
        if TIMER >= ONE_FRAME_IN_SECONDS:
            TIMER -= ONE_FRAME_IN_SECONDS

            # Clear the surface
            App.clear_surface(BLACK)

            # Render game elements
            pa.render()
            snake.render()
            snake.move()

            pg.display.update()
    
    pg.quit()

if __name__ == '__main__':
    main()

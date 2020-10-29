DEBUG = False

# Python modules
import pygame as pg

# App modules
from app import App

"""
    Constants
"""
# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Direction variables
UP      = 'UP'
RIGHT   = 'RIGHT'
DOWN    = 'DOWN'
LEFT    = 'LEFT'

# Game variables
PLAY_AREA_DIMENTION = 20
TILE_WIDTH = 0
PLAY_AREA_TOP_LEFT = (0, 0)

class Part():

    def __init__(self, pos, size, direction, color, snake):
        self.pos = pos
        self.size = size
        self.color = color
        self.direction = direction
        self.snake_reference = snake

    def set_direction(self, direction):
        self.direction = direction
    
    def move(self):
        # Move the part according to its direction
        if self.direction == UP:
            self.pos = (self.pos[0], self.pos[1] - 1)
        if self.direction == DOWN:
            self.pos = (self.pos[0], self.pos[1] + 1)
        if self.direction == LEFT:
            self.pos = (self.pos[0] - 1, self.pos[1])
        if self.direction == RIGHT:
            self.pos = (self.pos[0] + 1, self.pos[1])
        # Keep the position within the play area
        self.pos = (self.pos[0] % PLAY_AREA_DIMENTION, self.pos[1] % PLAY_AREA_DIMENTION)

        # Check if there is a turn point
        if self.pos in self.snake_reference.turnpoints.keys():
            self.set_direction(self.snake_reference.turnpoints[self.pos])
            # If it is the tail of the snake remove the turnpoint
            if self == self.snake_reference.tail:
                del self.snake_reference.turnpoints[self.pos]

    def render(self):
        pg.draw.rect(
            App.get_surface(),  # surface
            self.color,         # color
            (                   # rect
                self.pos[0] * TILE_WIDTH + 1 + PLAY_AREA_TOP_LEFT[0],
                self.pos[1] * TILE_WIDTH + 1 + PLAY_AREA_TOP_LEFT[1],
                self.size - 1,
                self.size - 1
            )
        )

class Snake():

    def __init__(self, length, start_pos, size, color, speed):
        # Create the parts of the snake
        self.parts = []
        startx = start_pos[0]
        starty = start_pos[1]
        for i in range(length):
            c = color
            if i == 0:
                c = RED
            part = Part((startx - i, starty), size, RIGHT, c, self)
            self.parts.append(part)
        self.tail = self.parts[len(self.parts) - 1]

        self.size = size
        self.direction = RIGHT
        self.color = color
        
        self.speed = speed
        self.frame = 0

        self.turnpoints = {}
    
    def set_speed(self, speed):
        self.speed = speed

    def move(self):
        # Only move if it is the move frame
        self.frame += 1
        if self.frame != self.speed:
            return
        self.frame = 0
        for part in self.parts:
            part.move()
    
    def render(self):
        for part in self.parts:
            part.render()
    
    def set_direction(self, direction):
        self.direction = direction
        self.turnpoints[self.parts[0].pos] = direction # Mark this head of the snake as a turn point
        self.parts[0].set_direction(direction)

class PlayArea():

    def __init__(self, dimention, tile_width):
        # Get screen dimentions
        swidth = App.get_surface().get_width()
        sheight = App.get_surface().get_height()
        # Calculate PlayArea dimention
        self.dimention = dimention * tile_width
        self.tile_count = dimention

        # Calculate render offsets
        top_offset = (sheight - self.dimention) // 2
        right_offset = (swidth - self.dimention) // 2

        global PLAY_AREA_TOP_LEFT, TILE_WIDTH
        PLAY_AREA_TOP_LEFT = (right_offset, top_offset)
        TILE_WIDTH = tile_width

        # Calculate play area limits
        self.top_left = PLAY_AREA_TOP_LEFT
        self.bottom_right = (PLAY_AREA_TOP_LEFT[0] + self.dimention, PLAY_AREA_TOP_LEFT[1] + self.dimention)

    def render(self):
        # Draw play area lines clockwise starting from top-left corner
        pg.draw.line(
            App.get_surface(),
            WHITE,
            self.top_left,
            (self.bottom_right[0], self.top_left[1])
        )
        pg.draw.line(
            App.get_surface(),
            WHITE,
            (self.bottom_right[0], self.top_left[1]),
            self.bottom_right
        )
        pg.draw.line(
            App.get_surface(),
            WHITE,
            self.bottom_right,
            (self.top_left[0], self.bottom_right[1])
        )
        pg.draw.line(
            App.get_surface(),
            WHITE,
            (self.top_left[0], self.bottom_right[1]),
            self.top_left
        )

        if DEBUG:
            # Draw grid for now for debuging purposes
            for i in range(self.tile_count):
                pg.draw.line(
                    App.get_surface(),
                    WHITE,
                    (self.top_left[0] + i * TILE_WIDTH, self.top_left[1]),
                    (self.top_left[0] + i * TILE_WIDTH, self.bottom_right[1])
                )
            for i in range(self.tile_count):
                pg.draw.line(
                    App.get_surface(),
                    WHITE,
                    (self.top_left[0], self.top_left[1] + i * TILE_WIDTH),
                    (self.bottom_right[0], self.top_left[1] + i * TILE_WIDTH)
                )

# Python modules
import random as rnd
import pygame as pg

# App modules
import app

# Game modules
from .game_variables import GameVariables as gv

class Food():

    def __init__(self, color, size):
        self.pos = (0, 0)
        self.size = size
        self.color = color
    
    def render(self):
        pg.draw.rect(
            app.App.get_surface(),  # surface
            self.color,         # color
            (                   # rect
                self.pos[0] * gv.TILE_WIDTH + 1 + gv.PLAY_AREA_TOP_LEFT[0],
                self.pos[1] * gv.TILE_WIDTH + 1 + gv.PLAY_AREA_TOP_LEFT[1],
                self.size - 1,
                self.size - 1
            )
        )

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
        if self.direction == gv.UP:
            self.pos = (self.pos[0], self.pos[1] - 1)
        if self.direction == gv.DOWN:
            self.pos = (self.pos[0], self.pos[1] + 1)
        if self.direction == gv.LEFT:
            self.pos = (self.pos[0] - 1, self.pos[1])
        if self.direction == gv.RIGHT:
            self.pos = (self.pos[0] + 1, self.pos[1])
        # Keep the position within the play area
        self.pos = (self.pos[0] % gv.PLAY_AREA_DIMENTION, self.pos[1] % gv.PLAY_AREA_DIMENTION)

        # Check if there is a turn point
        if self.pos in self.snake_reference.turnpoints.keys():
            self.set_direction(self.snake_reference.turnpoints[self.pos])
            # If it is the tail of the snake remove the turnpoint
            if self == self.snake_reference.tail:
                del self.snake_reference.turnpoints[self.pos]

    def render(self):
        pg.draw.rect(
            app.App.get_surface(),  # surface
            self.color,         # color
            (                   # rect
                self.pos[0] * gv.TILE_WIDTH + 1 + gv.PLAY_AREA_TOP_LEFT[0],
                self.pos[1] * gv.TILE_WIDTH + 1 + gv.PLAY_AREA_TOP_LEFT[1],
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
                c = gv.RED
            part = Part((startx - i, starty), size, gv.RIGHT, c, self)
            self.parts.append(part)
        self.head = self.parts[0]
        self.tail = self.parts[len(self.parts) - 1]

        self.size = size
        self.direction = gv.RIGHT
        self.color = color
        
        self.speed = speed
        self.frame = 0

        self.turnpoints = {}
    
    def set_speed(self, speed):
        self.speed = speed

    def move(self): 
        """
        0 = not moved
        1 = moved
        2 = game over
        """
        # Only move if it is the move frame
        self.frame += 1
        if self.frame != self.speed:
            return 0
        # Reset the frame counter
        self.frame = 0

        # First move the head and check for collisions while moving the rest of the parts
        self.head.move()
        for i in range(1, len(self.parts)):
            # TODO Instead of ending the program return to the main menu
            if self.head.pos == self.parts[i].pos:
                return 2
            self.parts[i].move()
        
        return 1
    
    def render(self):
        for part in self.parts:
            part.render()
    
    def set_direction(self, direction):
        self.direction = direction
        self.turnpoints[self.parts[0].pos] = direction # Mark this head of the snake as a turn point
        self.parts[0].set_direction(direction)
    
    def add_part(self):
        new_pos = (
            self.tail.pos[0] + gv.DIRECTION_STEPS[self.tail.direction][0], 
            self.tail.pos[1] + gv.DIRECTION_STEPS[self.tail.direction][1]
        )
        new_part = Part(new_pos, self.size, self.tail.direction, self.color, self)
        self.parts.append(new_part)
        self.tail = new_part
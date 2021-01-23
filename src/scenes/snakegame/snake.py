# Python modules
import random as rnd
import pygame as pg

# App modules
import app

# Game modules
from .game_variables import GameVariables as gv

class Food():
    """
    This class represents the foods that the snake can collect on the play area
    color = the color of the food
    size = the size in pixels of the food
    """
    def __init__(self,
        color : (int, int, int), 
        size : int
    ):
        self.pos = (0, 0)
        self.size = size
        self.color = color
    
    def render(self):
        """
        Renders the food
        """
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
    """
    A block that represents a part of the snake.
    pos = the initial position of the part
    size = the size in pixels of the part
    direction = the initial move direction of the part
    color = the color of the part
    snake = reference to the snake that it belongs to
    """
    def __init__(self,
        pos : (int, int), 
        size : (int), 
        direction, 
        color : (int, int, int), 
        snake
        ):
        self.pos = pos
        self.size = size
        self.color = color
        self.direction = direction
        self._snake_reference = snake

    def set_direction(self, direction):
        """
        Changes the move direction of the snake
        """
        self.direction = direction

    def move(self):
        """
        Moves the part to according to its current direction
        """
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
        if self.pos in self._snake_reference.turnpoints.keys():
            self.set_direction(self._snake_reference.turnpoints[self.pos])
            # If it is the tail of the snake remove the turnpoint
            if self == self._snake_reference.tail:
                del self._snake_reference.turnpoints[self.pos]

    def render(self):
        """
        Renders the part
        """
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
    """
        Creates a snake object
        length = starting length of the snake
        start_pos = starting position of the snake
        size = size of one block of the snake in pixels
        color = color of the snake
        speed = number of frames when a move command will be executed
    """
    def __init__(self, 
        length : int, 
        start_pos : (int, int), 
        size : int, 
        color : (int, int, int), 
        speed : int
    ):
        # Create the parts of the snake given the values in the constructor
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

        # Create other local variables to be used in the class
        self.size = size
        self.direction = gv.RIGHT
        self.color = color
        
        self.speed = speed
        self.frame = 0

        # Hash-map to keep track of the points where the snake will have to
        # turn it's parts
        self.turnpoints = {}
    
    def set_speed(self, speed):
        self.speed = speed

    def move(self): 
        """
        Moves the snake
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
        """
        Renders the snake on the screen
        """
        # Render each part of the snake
        for part in self.parts:
            part.render()
    
    def set_direction(self, direction):
        """
        Change the direction to witch the snake is moving
        """
        self.direction = direction
        self.turnpoints[self.parts[0].pos] = direction # Mark the position of the head of the snake as a turn point
        self.parts[0].set_direction(direction)
    
    def add_part(self):
        """
        Add's a new part to the snake to it's tail
        """
        # Calculate the new position of the new part
        new_pos = (
            self.tail.pos[0] + gv.DIRECTION_STEPS[self.tail.direction][0], 
            self.tail.pos[1] + gv.DIRECTION_STEPS[self.tail.direction][1]
        )
        # Create the new part
        new_part = Part(new_pos, self.size, self.tail.direction, self.color, self)
        # Add it to the list of parts and set it as the tail of the snake
        self.parts.append(new_part)
        self.tail = new_part
        # If the snake is as long as the total play area then the game is won
        # Returns 1
        if len(self.parts) == gv.PLAY_AREA_DIMENTION ** 2:
            return 1
        # Otherwise, return 0
        return 0
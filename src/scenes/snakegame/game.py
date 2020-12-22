# Python modules
import random as rnd
import pygame as pg

# App modules
import app
from scenes.scene import Scene

# Game modules
from .playarea import PlayArea
from .snake import Snake, Food
from .game_variables import GameVariables as gv


class Game(Scene):

    def __init__(self):
        gv.TILE_WIDTH = (app.App.get_surface().get_height() - 200) // gv.PLAY_AREA_DIMENTION
        self.pa = PlayArea(gv.PLAY_AREA_DIMENTION, gv.TILE_WIDTH)
        self.snake = Snake(5, (gv.PLAY_AREA_DIMENTION / 2, gv.PLAY_AREA_DIMENTION / 2), gv.TILE_WIDTH, gv.BLUE, 4)
        self.food = Food(gv.PURPLE, gv.TILE_WIDTH)
        
        self.default_grid = {}
        for x in range(gv.PLAY_AREA_DIMENTION):
            for y in range(gv.PLAY_AREA_DIMENTION):
                self.default_grid[(x, y)] = 0
        self.grid = self.default_grid.copy()

        self.summon_food()
    
    def key_event(self, key):
        if key == pg.K_UP:
            self.snake.set_direction(gv.UP)
        if key == pg.K_DOWN:
            self.snake.set_direction(gv.DOWN)
        if key == pg.K_RIGHT:
            self.snake.set_direction(gv.RIGHT)
        if key == pg.K_LEFT:
            self.snake.set_direction(gv.LEFT)

    def update(self):
        self.snake.move()
        self.update_grid()

        self.render()

        if self.snake.head.pos == self.food.pos:
            # TODO Add a scoring system
            self.summon_food()
            self.snake.add_part()
    
    def render(self):
        self.pa.render()
        self.snake.render()
        self.food.render()

    def update_grid(self):
        self.grid = self.default_grid.copy()
        for part in self.snake.parts:
            try:
                del self.grid[part.pos]
            except:
                pass

    def summon_food(self):
        new_pos = rnd.choice(list(self.grid.keys()))
        self.food.pos = new_pos

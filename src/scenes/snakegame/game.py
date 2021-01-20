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

# UI module
import scenes as s

class Game(Scene):
    """
    The game class for the snake game
    """
    def __init__(self):
        # TODO add ability to choose the starting level
        # Create some local variables to keep track of the game
        self.steps_made = 0
        self.score = 0

        self.base_level = 2
        self.level = 2
        self.times_scored = 0

        self.game_over = False

        # Calculate the width of one tile (cell) of the 2D square matrix play area
        gv.TILE_WIDTH = (app.App.get_surface().get_height() - 200) // gv.PLAY_AREA_DIMENTION

        # Create the play area
        self.pa = PlayArea(gv.PLAY_AREA_DIMENTION, gv.TILE_WIDTH)
        # Create the snake
        self.snake = Snake(5, (gv.PLAY_AREA_DIMENTION / 2, gv.PLAY_AREA_DIMENTION / 2), gv.TILE_WIDTH, gv.BLUE, gv.LEVEL_FPS[self.level])
        # Create the first food
        self.food = Food(gv.PURPLE, gv.TILE_WIDTH)

        # Create ui elements
        self.ui_elements = [
            s.HudText( # Displays the current score
                (20, 30),
                (100, 100),
                (255, 255, 255),
                "Score: 0",
                23
            ),
            s.HudText( # Displays the current level
                (20, 60),
                (100, 100),
                (255, 255, 255),
                "Level: 0",
                23
            ),
            s.VerticalProgressBar( # Displays how much score will be earn if the food is eaten at that point in time
                (gv.PLAY_AREA_TOP_LEFT[0] + gv.TILE_WIDTH * (gv.PLAY_AREA_DIMENTION + 1), gv.PLAY_AREA_TOP_LEFT[1]),
                (gv.TILE_WIDTH, gv.TILE_WIDTH * gv.PLAY_AREA_DIMENTION),
                (0, 255, 0),
                (0, 0, 0),
                gv.STEPS_LIMIT,
                gv.STEPS_LIMIT,
                False
            )
        ]

        # Create an instance of the grid that is empty
        self.default_grid = {}
        for x in range(gv.PLAY_AREA_DIMENTION):
            for y in range(gv.PLAY_AREA_DIMENTION):
                self.default_grid[(x, y)] = 0
        # This grid will keep track of the filled in spots in the play area
        self.grid = self.default_grid.copy()

        # Summon a food
        self.summon_food()
    
    def key_event(self, key):
        """
        Handle the key events
        """
        # Change the direction of the snake according to the input
        if key == pg.K_UP:
            self.snake.set_direction(gv.UP)
        if key == pg.K_DOWN:
            self.snake.set_direction(gv.DOWN)
        if key == pg.K_RIGHT:
            self.snake.set_direction(gv.RIGHT)
        if key == pg.K_LEFT:
            self.snake.set_direction(gv.LEFT)

    def update(self):
        """
        Function that will be called every frame of the game
        """
        # If the game is not over
        if not self.game_over:
            # Try moving the snake
            s = self.snake.move()
            if s == 1: # If the snake has moved
                self.steps_made += 1
                self.ui_elements[2].set_progress(max(0, gv.STEPS_LIMIT - self.steps_made))
            if s == 2: # The snake has run over one of it's own parts
                # The game is over
                self.game_over = True
                return
            self.update_grid()

        # Render the game
        self.render()

        # If the snake's head is located on the food
        if self.snake.head.pos == self.food.pos:
            # Calculate score
            # formula = base level * 20 + 100 - 2 * min(steps made, 40) * (level + 1)
            self.score += self.base_level * 20 + (gv.DEFAULT_SCORE - gv.PENALTY_PER_STEP * min(self.steps_made, gv.STEPS_LIMIT)) * (self.level + 1)
            # Update the score text
            self.ui_elements[0].set_text("Score: " + str(self.score))
            # Reset the number of steps made
            self.steps_made = 0

            # After every gv.JUMP_LEVEL_AFTER pickups, bump up the level
            self.times_scored += 1
            if self.times_scored >= gv.JUMP_LEVEL_AFTER:
                self.times_scored = 0
                self.level += 1
                # Check if there is a next level
                if self.level == len(gv.LEVEL_FPS):
                    self.level -= 1
                self.snake.set_speed(gv.LEVEL_FPS[self.level])
                self.ui_elements[1].set_text("Level: " + str(self.level))

            # Summon new food and add a part to the snake
            self.summon_food()
            self.snake.add_part()
    
    def render(self):
        """
        Renders the game
        """
        # Render every game element present
        self.pa.render()
        self.snake.render()
        self.food.render()
        # Render every UI element
        for ui_element in self.ui_elements:
            ui_element.render()

    def update_grid(self):
        """
        Update the grid
        """
        self.grid = self.default_grid.copy()
        for part in self.snake.parts:
            try:
                del self.grid[part.pos]
            except:
                pass

    def summon_food(self):
        """
        Summon new food
        """
        new_pos = rnd.choice(list(self.grid.keys()))
        self.food.pos = new_pos

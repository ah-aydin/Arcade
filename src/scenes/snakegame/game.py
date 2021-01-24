# Python modules
import random as rnd
import pygame as pg

# App modules
import app
from scenes.scene import BaseGame

# Game modules
from .playarea import PlayArea
from .snake import Snake, Food
from .game_variables import GameVariables as gv

# UI module
import scenes as s

class Game(BaseGame):
    """
    The game class for the snake game
    starting_level = The starting level of the game
    """
    def __init__(self, starting_level):
        super(Game, self).__init__()

        # Create some local variables to keep track of the game
        self._steps_made = 0
        self._score = 0

        self._base_level = starting_level
        self._level = starting_level
        self._times_scored = 0

        self._game_over = False

        # Calculate the width of one tile (cell) of the 2D square matrix play area
        gv.TILE_WIDTH = (app.App.get_surface().get_height() - 200) // gv.PLAY_AREA_DIMENTION

        # Create the play area
        self._pa = PlayArea(gv.PLAY_AREA_DIMENTION, gv.TILE_WIDTH)
        # Create the _snake
        self._snake = Snake(5, (gv.PLAY_AREA_DIMENTION / 2, gv.PLAY_AREA_DIMENTION / 2), gv.TILE_WIDTH, gv.BLUE, gv.LEVEL_FPS[self._level])
        # Create the first _food
        self._food = Food(gv.PURPLE, gv.TILE_WIDTH)

        # Create ui elements
        self._uiElements += [
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
                "Level: " + str(starting_level),
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
        self._default_grid = {}
        for x in range(gv.PLAY_AREA_DIMENTION):
            for y in range(gv.PLAY_AREA_DIMENTION):
                self._default_grid[(x, y)] = 0
        # This grid will keep track of the filled in spots in the play area
        self._grid = self._default_grid.copy()

        # Summon a food
        self._summon_food()

    def key_event(self, key):
        """
        Handle the key events
        """
        if self._pause:
            return
        
        # Change the direction of the snake according to the input
        if key == pg.K_UP:
            self._snake.set_direction(gv.UP)
        if key == pg.K_DOWN:
            self._snake.set_direction(gv.DOWN)
        if key == pg.K_RIGHT:
            self._snake.set_direction(gv.RIGHT)
        if key == pg.K_LEFT:
            self._snake.set_direction(gv.LEFT)

    def update(self):
        """
        Function that will be called every frame of the game
        """
        # If the game is not over
        if not self._game_over and not self._pause:
            # Try moving the snake
            s = self._snake.move()
            if s == 1: # If the snake has moved
                self._steps_made += 1
                self._uiElements[2].set_progress(max(0, gv.STEPS_LIMIT - self._steps_made))
            if s == 2: # The snake has run over one of it's own parts
                # The game is over
                self._end()
                return
            self.update_grid()

        # Render the game
        self.render()

        # If the _snake's head is located on the _food
        if self._snake.head.pos == self._food.pos:
            # Calculate _score
            # formula = base _level * 20 + 100 - 2 * min(steps made, 40) * (_level + 1)
            self._score += self._base_level * 20 + (gv.DEFAULT_SCORE - gv.PENALTY_PER_STEP * min(self._steps_made, gv.STEPS_LIMIT)) * (self._level + 1)
            # Update the _score text
            self._uiElements[0].set_text("Score: " + str(self._score))
            # Reset the number of steps made
            self._steps_made = 0

            # After every gv.JUMP_LEVEL_AFTER pickups, bump up the _level
            self._times_scored += 1
            if self._times_scored >= gv.JUMP_LEVEL_AFTER:
                self._times_scored = 0
                self._level += 1
                # Check if there is a next _level
                if self._level == len(gv.LEVEL_FPS):
                    self._level -= 1
                self._snake.set_speed(gv.LEVEL_FPS[self._level])
                self._uiElements[1].set_text("Level: " + str(self._level))

            # Summon new _food and add a part to the _snake
            self._summon_food()
            self._snake.add_part()
    
    def render(self):
        """
        Renders the game
        """
        # Render every game element present
        self._pa.render()
        self._snake.render()
        self._food.render()
        # Render the UI
        self._renderUI()

    def update_grid(self):
        """
        Update the _grid
        """
        self._grid = self._default_grid.copy()
        for part in self._snake.parts:
            try:
                del self._grid[part.pos]
            except:
                pass

    def _summon_food(self):
        """
        Summon new food
        """
        new_pos = rnd.choice(list(self._grid.keys()))
        self._food.pos = new_pos

    def _end(self):
        """
        The function that gets called when the game ends
        """
        # Set the game as over
        self._game_over = True

        # Add in the UI elements for the game over state
        screen_size = app.App.get_surface().get_size()
        button_size = (
            screen_size[1] // 10 * 2,
            screen_size[1] // 10
        )

        self._uiElements += [
            s.Button( # This is just to have a back drop behind all the newly added ui elements
                (
                    int(screen_size[0] // 2 - screen_size[0] * 0.6 // 2),
                    int(screen_size[1] // 2 - screen_size[1] * 0.8 // 2)
                ),
                (
                    int(screen_size[0] * 0.6),
                    int(screen_size[1] * 0.8)
                ),
                (110, 110, 110)
            ),
            s.HudText( # Displays "GAME OVER"
                (screen_size[0] // 2, screen_size[1] // 4),
                (0, 0),
                (255, 0, 0),
                "GAME OVER",
                150,
                text_centered = True
            ),
            s.Button( # Button that will return to the main menu
                (
                    screen_size[0] // 2 - button_size[0] - 40,
                    (screen_size[1] + button_size[1]) // 2
                ),
                button_size,
                (255, 0, 0),
                text = "Main Menu",
                text_color = (255, 255, 255),
                font_size = 35
            ),
            s.Button( # Button that will return to the level selection menu
                (
                    screen_size[0] // 2 + 40,
                    (screen_size[1] + button_size[1]) // 2
                ),
                button_size,
                (255, 0, 0),
                text = "Play Again",
                text_color = (255, 255, 255),
                font_size = 35
            )
        ]

        self._uiElements[-2].set_on_mouse_click(lambda: app.App.set_current_scene(s.MainMenu()))
        self._uiElements[-1].set_on_mouse_click(lambda: app.App.set_current_scene(s.SnakeMenu()))
        # Since some buttons are added to the screen
        # Generate the mouse click mapping
        self._generateMouseClickMapping()
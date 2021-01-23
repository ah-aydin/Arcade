# Python modules
import random as rnd
import pygame as pg

# App modules
import app
from scenes.scene import BaseGame

# Game modules
from .playarea import PlayArea
from .tetromino import Tetromino
from .shapes import SHAPES
from .game_variables import GameVariables as gv

# UI modules
import scenes as s

class Game(BaseGame):
    """
    The game class for the tetris game
    """
    def __init__(self, start_level):
        super(Game, self).__init__()

        # Create all the objects that will be used in the game
        # Create the play area
        self.pa = PlayArea()
        # Create 2 tetrominos
        self._current_tetromino = Tetromino(rnd.choice(SHAPES))
        self._next_tetromino_template = rnd.choice(SHAPES)
        self._next_tetromino_preview = Tetromino(self._next_tetromino_template)
        self._next_tetromino_preview.pos = (12, 4) # Move the next tetromino to the right side of the play area to display it

        # Create UI elements
        self._uiElements += [
            s.HudText( # Displays the score
                (20, 30),
                (100, 100),
                (255, 255, 255),
                "Score: 0",
                23
            ),
            s.HudText( # Displays current level
                (20, 60),
                (100, 100),
                (255, 255, 255),
                "Level: " + str(start_level),
                23
            )
        ]
        
        # Some local variables to keep track of the game
        self._frame_count = 0
        self._total_score = 0
        self._level = start_level
        self._start_level = start_level
        self._rows_filled_count = 0
        self._fast_drop = False
        self._game_over = False

        # Map the mouse click mapping for the clickable objects
        self._generateMouseClickMapping()
    
    def key_up_event(self, key):
        """
        Called when a key_up_event is triggered
        """
        if self._pause:
            return
        
        # Stop dropping faster if the down arrow is released
        if key == pg.K_DOWN:
            self._fast_drop = False

    def key_event(self, key):
        """
        Called when a key_event is triggered
        """
        if self._pause:
            return
        
        # Left-right movement events
        if key == pg.K_RIGHT:
            self._current_tetromino.move_right()
            if self._collision():
                self._current_tetromino.move_left()
        if key == pg.K_LEFT:
            self._current_tetromino.move_left()
            if self._collision():
                self._current_tetromino.move_right()

        # Rotating events
        if key == pg.K_RCTRL or key == pg.K_LCTRL or key == pg.K_z:
            self._current_tetromino.rotate_anticlockwise()
            if self._collision():
                # Check if it can rotate by moving left and right
                if not self._rotate_plus_movement_check():
                    return
                self._current_tetromino.rotate_clockwise()
        if key == pg.K_UP or key == pg.K_x:
            self._current_tetromino.rotate_clockwise()
            if self._collision():
                # Check if it can rotate by moving left and right
                if not self._rotate_plus_movement_check():
                    return
                self._current_tetromino.rotate_anticlockwise()
        
        # Drop faster if the down arrow is pressed
        if key == pg.K_DOWN:
            self._fast_drop = True

    def update(self):
        """
        Called every frame
        """
        # If the game is not over
        if not self._game_over and not self._pause:
            # Check if it is time to move the tetromino down
            self._frame_count += 1
            f = gv.LEVEL_FPS[min(self._level, len(gv.LEVEL_FPS) - 1)]
            if self._fast_drop:
                f = 2
            # If it is time, move it down
            if self._frame_count >= f:
                self._frame_count = 0
                self._current_tetromino.move_down()
                if self._landed():
                    self._get_next_tetromino()

        # Render the game
        self.render()

    def render(self):
        """
        Renders the game
        """
        # Render all the game objects
        self.pa.render()
        self._current_tetromino.render()
        self._next_tetromino_preview.render()
        # Render the UI
        for ui_element in self._uiElements:
            ui_element.render()
    
    def _calculate_score(self, rows_filled):
        """
        Calculates the score according to the numberof rows that are filled
        """
        if rows_filled == 0:
            return
        # First calculate the total score
        score_gained = [40, 100, 300, 1200][rows_filled - 1] * (self._level + 1)
        self._total_score += score_gained

        # Then check if the player has advanced to the next _level
        self._rows_filled_count += rows_filled
        if self._rows_filled_count >= min(self._start_level * 10 + 10, max(100, self._start_level * 10 - 50)):
            # If it has advanced, bump up the _level by 1
            self._level += 1
            self._uiElements[1].set_text("Level: " + str(self._level))
            self._rows_filled_count = 0
        
        # Update the score text
        self._uiElements[0].set_text("Score: " + str(self._total_score))

    def _get_next_tetromino(self):
        """
        Create the next tetromino
        """
        # Delete the current tetromino and create a new one from the next one's template
        del self._current_tetromino
        self._current_tetromino = Tetromino(self._next_tetromino_template)
        # Create the next tetromino template and preview
        self._next_tetromino_template = rnd.choice(SHAPES)
        del self._next_tetromino_preview
        self._next_tetromino_preview = Tetromino(self._next_tetromino_template)
        self._next_tetromino_preview.pos = (12, 4)

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
            s.Button( # Button that will return to the _level selection menu
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
        self._uiElements[-1].set_on_mouse_click(lambda: app.App.set_current_scene(s.TetrisMenu()))
        # Since some buttons are added to the screen
        # Generate the mouse click mapping
        self._generateMouseClickMapping()
    
    # Collision checkers
    def _rotate_plus_movement_check(self):
        """
        Checks if the tetromino can be positioned elsewhere by moving it arround the area left and right
        """
        self._current_tetromino.move_right()
        if self._collision():
            self._current_tetromino.move_left()
        else:
            return False
        self._current_tetromino.move_right()
        self._current_tetromino.move_right()
        if self._collision():
            self._current_tetromino.move_left()
            self._current_tetromino.move_left()
        else:
            return False
        
        self._current_tetromino.move_left()
        if self._collision():
            self._current_tetromino.move_right()
        else:
            return False
        self._current_tetromino.move_left()
        self._current_tetromino.move_left()
        if self._collision():
            self._current_tetromino.move_right()
            self._current_tetromino.move_right()
        else:
            return False
        
        return True

    def _landed(self):
        """
        Checks if tetromino is _landed
        """
        # Also calculate the ammount of score that has been gained
        rows_filled = 0
        _landed = False
        for block in self._current_tetromino.blocks:
            # Check if there is a piece under it
            # Or if it has reached the bottom of the play area
            pos = (self._current_tetromino.pos[0] + block.offset[0], self._current_tetromino.pos[1] + block.offset[1])
            if pos[1] >= self.pa.dimention[1]:
                self._current_tetromino.move_up()
                rows_filled = self.pa.add_to_grid(self._current_tetromino)
                _landed = True
                break
            if self.pa.grid[pos[1]][pos[0]] != (0, 0, 0):
                self._current_tetromino.move_up()
                rows_filled = self.pa.add_to_grid(self._current_tetromino)
                _landed = True
                break
        
        # If the returned value is -1, the game is over
        if rows_filled == -1:
            self._end()
            return

        # Calculate total score
        self._calculate_score(rows_filled)

        return _landed

    def _out_of_bounds(self):
        """
        Checks if the tetromino is out of bounds
        """
        for block in self._current_tetromino.blocks:
            # Check if it is out of bounds or not
            pos = (self._current_tetromino.pos[0] + block.offset[0], self._current_tetromino.pos[1] + block.offset[1])
            if pos[0] < 0 or pos[0] >= self.pa.dimention[0] or pos[1] < 0 or pos[1] >= self.pa.dimention[1]:
                return True
        return False

    def _tetromino_collision(self):
        """
        Checks if the tetromiino is colliding with the allready placed tetrominos
        """
        for block in self._current_tetromino.blocks:
            # Check if it is colliding with other tetrominos that are allready placed
            pos = (self._current_tetromino.pos[0] + block.offset[0], self._current_tetromino.pos[1] + block.offset[1])
            if self.pa.grid[pos[1]][pos[0]] != (0, 0, 0):
                return True
        return False

    def _collision(self):
        """
        Checks for collisions that the current tetromino has with the edges and the other tetrominos
        """
        if self._out_of_bounds():
            return True
        if self._tetromino_collision():
            return True
        return False
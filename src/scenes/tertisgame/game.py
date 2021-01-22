# Python modules
import random as rnd
import pygame as pg

# App modules
import app
from scenes.scene import Scene

# Game modules
from .playarea import PlayArea
from .tetromino import Tetromino
from .shapes import SHAPES
from .game_variables import GameVariables as gv

# UI modules
import scenes as s

class Game(Scene):
    """
    The game class for the tetris game
    """
    def __init__(self, start_level):
        # Create all the objects that will be used in the game
        # Create the play area
        self.pa = PlayArea()
        # Create a tetromino
        self.current_tetromino = None
        self.get_next_tetromino()

        # Create UI elements
        self.ui_elements = [
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
        self.frame_count = 0
        self.total_score = 0
        self.level = start_level
        self.start_level = start_level
        self.rows_filled_count = 0
        self.fast_drop = False
        self.game_over = False
    
    def key_up_event(self, key):
        """
        Called when a key_up_event is triggered
        """
        # Stop dropping faster if the down arrow is released
        if key == pg.K_DOWN:
            self.fast_drop = False

    def key_event(self, key):
        """
        Called when a key_event is triggered
        """
        # Left-right movement events
        if key == pg.K_RIGHT:
            self.current_tetromino.move_right()
            if self.collision():
                self.current_tetromino.move_left()
        if key == pg.K_LEFT:
            self.current_tetromino.move_left()
            if self.collision():
                self.current_tetromino.move_right()

        # Rotating events
        if key == pg.K_RCTRL or key == pg.K_LCTRL or key == pg.K_z:
            self.current_tetromino.rotate_anticlockwise()
            if self.collision():
                # Check if it can rotate by moving left and right
                if not self.rotate_plus_movement_check():
                    return
                self.current_tetromino.rotate_clockwise()
        if key == pg.K_UP or key == pg.K_x:
            self.current_tetromino.rotate_clockwise()
            if self.collision():
                # Check if it can rotate by moving left and right
                if not self.rotate_plus_movement_check():
                    return
                self.current_tetromino.rotate_anticlockwise()
        
        # Drop faster if the down arrow is pressed
        if key == pg.K_DOWN:
            self.fast_drop = True

    def update(self):
        """
        Called every frame
        """
        # If the game is not over
        if not self.game_over:
            # Check if it is time to move the tetromino down
            self.frame_count += 1
            f = gv.LEVEL_FPS[min(self.level, len(gv.LEVEL_FPS) - 1)]
            if self.fast_drop:
                f = 2
            # If it is time, move it down
            if self.frame_count >= f:
                self.frame_count = 0
                self.current_tetromino.move_down()
                if self.landed():
                    self.get_next_tetromino()

        # Render the game
        self.render()

    def render(self):
        """
        Renders the game
        """
        # Render all the game objects
        self.pa.render()
        self.current_tetromino.render()
        # Render the UI
        for ui_element in self.ui_elements:
            ui_element.render()
    
    def calculate_score(self, rows_filled):
        """
        Calculates the score according to the numberof rows that are filled
        """
        if rows_filled == 0:
            return
        # First calculate the total score
        score_gained = [40, 100, 300, 1200][rows_filled - 1] * (self.level + 1)
        self.total_score += score_gained

        # Then check if the player has advanced to the next level
        self.rows_filled_count += rows_filled
        if self.rows_filled_count >= min(self.start_level * 10 + 10, max(100, self.start_level * 10 - 50)):
            # If it has advanced, bump up the level by 1
            self.level += 1
            self.ui_elements[1].set_text("Level: " + str(self.level))
            self.rows_filled_count = 0
        
        # Update the score text
        self.ui_elements[0].set_text("Score: " + str(self.total_score))

    def get_next_tetromino(self):
        """
        Create the next tetromino
        """
        # TODO Add in a second one to show the next tetromino in order
        # Delete the current tetromino
        del self.current_tetromino
        # Create the new tetromino
        self.current_tetromino = Tetromino(rnd.choice(SHAPES))

    def end(self):
        """
        The function that gets called when the game ends
        """
        # TODO Make it more complete
        self.game_over = True
        self.ui_elements.append(
            s.HudText(
                (400, 400),
                (100, 100),
                (255, 0, 0),
                "GAME OVER",
                40
            )
        )
    
    # Collision checkers
    def rotate_plus_movement_check(self):
        """
        Checks if the tetromino can be positioned elsewhere by moving it arround the area left and right
        """
        self.current_tetromino.move_right()
        if self.collision():
            self.current_tetromino.move_left()
        else:
            return False
        self.current_tetromino.move_right()
        self.current_tetromino.move_right()
        if self.collision():
            self.current_tetromino.move_left()
            self.current_tetromino.move_left()
        else:
            return False
        
        self.current_tetromino.move_left()
        if self.collision():
            self.current_tetromino.move_right()
        else:
            return False
        self.current_tetromino.move_left()
        self.current_tetromino.move_left()
        if self.collision():
            self.current_tetromino.move_right()
            self.current_tetromino.move_right()
        else:
            return False
        
        return True

    def landed(self):
        """
        Checks if tetromino is landed
        """
        # Also calculate the ammount of score that has been gained
        rows_filled = 0
        landed = False
        for block in self.current_tetromino.blocks:
            # Check if there is a piece under it
            # Or if it has reached the bottom of the play area
            pos = (self.current_tetromino.pos[0] + block.offset[0], self.current_tetromino.pos[1] + block.offset[1])
            if pos[1] >= self.pa.dimention[1]:
                self.current_tetromino.move_up()
                rows_filled = self.pa.add_to_grid(self.current_tetromino)
                landed = True
                break
            if self.pa.grid[pos[1]][pos[0]] != (0, 0, 0):
                self.current_tetromino.move_up()
                rows_filled = self.pa.add_to_grid(self.current_tetromino)
                landed = True
                break
        
        # If the returned value is -1, the game is over
        if rows_filled == -1:
            self.end()
            return

        # Calculate total score
        self.calculate_score(rows_filled)

        return landed

    def out_of_bounds(self):
        """
        Checks if the tetromino is out of bounds
        """
        for block in self.current_tetromino.blocks:
            # Check if it is out of bounds or not
            pos = (self.current_tetromino.pos[0] + block.offset[0], self.current_tetromino.pos[1] + block.offset[1])
            if pos[0] < 0 or pos[0] >= self.pa.dimention[0] or pos[1] < 0 or pos[1] >= self.pa.dimention[1]:
                return True
        return False

    def tetromino_collision(self):
        """
        Checks if the tetromiino is colliding with the allready placed tetrominos
        """
        for block in self.current_tetromino.blocks:
            # Check if it is colliding with other tetrominos that are allready placed
            pos = (self.current_tetromino.pos[0] + block.offset[0], self.current_tetromino.pos[1] + block.offset[1])
            if self.pa.grid[pos[1]][pos[0]] != (0, 0, 0):
                return True
        return False

    def collision(self):
        """
        Checks for collisions that the current tetromino has with the edges and the other tetrominos
        """
        if self.out_of_bounds():
            return True
        if self.tetromino_collision():
            return True
        return False
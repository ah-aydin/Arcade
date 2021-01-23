# App module
import app

# Pygame
import pygame as pg

from .widget import Widget

class HorizontalProgressBar(Widget):
    """
    A horizontal progress bar
    pos = position
    size = dimentions of the element
    color = default color
    blank_color = color displayed for the unfilled parts of the element
    progress_count = how many "cells" the progress bar has
    starting_progress = the starting progress
    left_to_right = set's the direction of the progress bar
    """
    def __init__(
        self,
        pos: (int, int) = (0, 0),
        size: (int, int) = (0, 0),
        color: (int, int, int) = (0, 255, 0),
        blank_color: (int, int, int) = (0, 0, 0),
        progress_count : int = 0,
        starting_progress : int = 0,
        left_to_right : bool = False
    ):
        super(HorizontalProgressBar, self).__init__(pos, size, color)
        self.blank_color = blank_color
        self.progress_count = progress_count
        self.left_to_right = left_to_right
        self.progress = starting_progress

        # Calculate size of 1 progress
        self.progress_size = size[0] // progress_count
    
    def set_progress(self, progress):
        """
        Set the current progress
        """
        # Make sure that the given value is within the limits of the object
        if progress < 0 or progress >= self.progress_count:
            return
        self.progress = progress
    
    def _self_render(self):
        """
        Renders the object
        """
        if self.left_to_right:
            # Draw full part
            pg.draw.rect(
                app.App.get_surface(),  # surface
                self.color,         # color
                (                   # rect
                    self.pos[0],
                    self.pos[1],
                    self.progress_size * (self.progress),
                    self.size[1]
                    
                )
            )
            # Draw non-full part
            pg.draw.rect(
                app.App.get_surface(),  # surface
                self.blank_color,         # color
                (                   # rect
                    self.pos[0] + self.progress * self.progress_size,
                    self.pos[1],
                    self.progress_size * (self.progress_count - self.progress),
                    self.size[1]
                    
                )
            )
        else:
            # Draw full part
            pg.draw.rect(
                app.App.get_surface(),  # surface
                self.color,         # color
                (                   # rect
                    self.pos[0] + (self.progress_count - self.progress) * self.progress_size,
                    self.pos[1],
                    self.progress_size * (self.progress),
                    self.size[1]
                )
            )
            # Draw non-full part
            pg.draw.rect(
                app.App.get_surface(),  # surface
                self.blank_color,         # color
                (                   # rect
                    self.pos[0],
                    self.pos[1],
                    self.progress_size * (self.progress_count - self.progress),
                    self.size[1]
                )
            )

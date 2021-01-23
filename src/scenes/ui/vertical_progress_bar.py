# App module
import app

# Pygame
import pygame as pg

from .widget import Widget

class VerticalProgressBar(Widget):
    """
    A vertical progress bar
    pos = position
    size = dimentions of the element
    color = default color
    blank_color = color displayed for the unfilled parts of the element
    progress_count = how many "cells" the progress bar has
    starting_progress = the starting progress
    up_to_down = set's the direction of the progress bar
    """
    def __init__(
        self,
        pos: (int, int) = (0, 0),
        size: (int, int) = (0, 0),
        color: (int, int, int) = (0, 255, 0),
        blank_color: (int, int, int) = (0, 0, 0),
        progress_count : int = 0,
        starting_progress : int = 0,
        up_to_down : bool = False
    ):
        super(VerticalProgressBar, self).__init__(pos, size, color)
        self.blank_color = blank_color
        self.progress_count = progress_count
        self.up_to_down = up_to_down
        self.progress = starting_progress

        # Calculate size of 1 progress
        self.progress_size = size[1] // progress_count
    
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
        if self.up_to_down:
            # Draw full part
            pg.draw.rect(
                app.App.get_surface(),  # surface
                self.color,         # color
                (                   # rect
                    self.pos[0],
                    self.pos[1],
                    self.size[0],
                    self.progress_size * (self.progress)
                )
            )
            # Draw non-full part
            pg.draw.rect(
                app.App.get_surface(),  # surface
                self.blank_color,         # color
                (                   # rect
                    self.pos[0],
                    self.pos[1] + self.progress * self.progress_size,
                    self.size[0],
                    self.progress_size * (self.progress_count - self.progress)
                )
            )
        else:
            # Draw full part
            pg.draw.rect(
                app.App.get_surface(),  # surface
                self.color,         # color
                (                   # rect
                    self.pos[0],
                    self.pos[1] + (self.progress_count - self.progress) * self.progress_size,
                    self.size[0],
                    self.progress_size * (self.progress)
                )
            )
            # Draw non-full part
            pg.draw.rect(
                app.App.get_surface(),  # surface
                self.blank_color,         # color
                (                   # rect
                    self.pos[0],
                    self.pos[1],
                    self.size[0],
                    self.progress_size * (self.progress_count - self.progress)
                )
            )

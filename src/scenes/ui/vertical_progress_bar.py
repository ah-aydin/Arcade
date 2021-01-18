# App module
import app

# Pygame
import pygame as pg

from .widget import Widget

class VerticalProgressBar(Widget):
    def __init__(
        self,
        pos: (int, int) = (0, 0),
        size: (int, int) = (0, 0),
        color: (int, int, int) = (0, 255, 0),
        blank_color: (int, int, int) = (0, 0, 0),
        progress_count = 0,
        starting_progress = 0,
        up_to_down = False
    ):
        super(VerticalProgressBar, self).__init__(pos, size, color)
        self.blank_color = blank_color
        self.progress_count = progress_count
        self.starting_progress = starting_progress
        self.up_to_down = up_to_down
        self.progress = 0

        # Calculate size of 1 progress
        self.progress_size = size[1] // progress_count
    
    def set_progress(self, progress):
        if progress < 0 or progress >= self.progress_count:
            return
        self.progress = progress
    
    def self_render(self):
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

# App module
import app

# Pygame
import pygame as pg

class Widget:
    """
    The default class from witch all the UI elements are extended from
    """
    def __init__(
        self,
        pos: (int, int) = (0, 0),
        size: (int, int) = (0, 0),
        color: (int, int, int) = (0, 0, 0),
    ):
        self.pos = pos
        self.size = size
        self.color = color

        self._children = []
    
    def render(self):
        """
        Renders the object and it's childred
        """
        self._self_render()
        for child in self._children:
            child.render()
    
    def _self_render(self):
        """
        Function to render itself
        """
        pass

class Clickable(Widget):
    """
    A widget that is clickable
    """
    def __init__(
        self,
        pos: (int, int) = (0, 0),
        size: (int, int) = (0, 0),
        color: (int, int, int) = (0, 0, 0),
    ):
        super(Clickable, self).__init__(pos, size, color)

        self._mouse_click_func = None

    def set_on_mouse_click(self, func):
        """
        Set the functino to be called when the object is clicked
        """
        self._mouse_click_func = func

    def on_mouse_click(self):
        """
        Called when the object is clicked
        """
        if self._mouse_click_func is None:
            return
        self._mouse_click_func()
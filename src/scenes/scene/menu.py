import app
import scenes as s
from .scene import Scene

class BaseMenu(Scene):
    """
    Base class from where all the menu's are derived from
    """
    def __init__(self):
        super(BaseMenu, self).__init__()
import app
import scenes as s

class Scene:
    """
    A class the provids a set of functions every game class should always have in posession and
    implementations of the ones that will exist regardless of class.
    """
    def __init__(self):
        self._uiElements = []

        screen_size = app.App.get_surface().get_size()
        self._mouseClickMapping = [[None for y in range(screen_size[0])] for x in range(screen_size[1])]
    
    def key_up_event(self, key):
        pass

    def key_event(self, key):
        pass

    def mouse_move_event(self, pos):
        pass

    def mouse_click_event(self, pos):
        """
        Called when there is a mouse click event
        """
        elem = self._mouseClickMapping[pos[1]][pos[0]]
        if elem != None:
            elem.on_mouse_click()

    def update(self):
        pass
    
    def _render(self):
        pass
    
    def _generateMouseClickMapping(self):
        """
        Generates the moue click mapping
        """
        for elem in self._uiElements:
            if issubclass(type(elem), s.Clickable):
                xpos, ypos = elem.pos
                for x in range(elem.size[0]):
                    for y in range(elem.size[1]):
                        if ypos + y < len(self._mouseClickMapping) and xpos + x < len(self._mouseClickMapping[0]) and ypos + y >= 0 and xpos + x >= 0:
                            self._mouseClickMapping[ypos + y][xpos + x] = elem

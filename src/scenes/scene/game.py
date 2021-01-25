import app
import scenes as s
from .scene import Scene

class BaseGame(Scene):
    """
    Base class from where all the game's are derived from
    """

    def __init__(self):
        super(BaseGame, self).__init__()

        self._gameObjects = []

        self._pause = False
        screen_size = app.App.get_surface().get_size()

        # Create the _pause menu
        button_size = (
            screen_size[1] // 10 * 2,
            screen_size[1] // 10
        )
        self._pauseMenuUiElements = [
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
            s.HudText( # Displays "PAUSE"
                (screen_size[0] // 2, screen_size[1] // 4),
                (0, 0),
                (255, 0, 0),
                "PAUSE",
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
            s.Button( # Button that will unpause the game
                (
                    screen_size[0] // 2 + 40,
                    (screen_size[1] + button_size[1]) // 2
                ),
                button_size,
                (255, 0, 0),
                text = "Continue",
                text_color = (255, 255, 255),
                font_size = 35
            )
        ]
        
        self._pauseMenuUiElements[2].set_on_mouse_click(lambda: app.App.set_current_scene(s.MainMenu()))
        self._pauseMenuUiElements[3].set_on_mouse_click(lambda: self.toggle_pause())

    def toggle_pause(self):
        if not self._pause:
            self._on_pause()
        else:
            self._on_unpause()
    
    def _on_pause(self):
        self._pause = True
        
        # Add in the UI elements for the _pause state
        self._uiElements += self._pauseMenuUiElements

        # Since some buttons are added to the screen
        # Generate the mouse click mapping
        self._generateMouseClickMapping()

    def _on_unpause(self):
        self._pause = False

        # Remove the _pause menu items from the UI
        self._uiElements = self._uiElements[:-len(self._pauseMenuUiElements)]
    
    def add_game_object(self, obj):
        """
        Add's the given objects to the list of game objects of the scene
        """
        self._gameObjects.append(obj)
    
    def remove_game_object(self, obj):
        """
        Remove's the given game object from the list of the game objects
        """
        try:
            self._gameObjects.remove(obj)
        except:
            print("Game object in question is not in the game object list")
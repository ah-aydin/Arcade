class App():

    ##################################################################
    # surface methods
    surface = None
    @classmethod
    def set_surface(cls, surface):
        cls.surface = surface
    @classmethod
    def get_surface(cls):
        return cls.surface
    @classmethod
    def clear_surface(cls, color):
        cls.surface.fill(color)
    ##################################################################

    ##################################################################
    # running methods
    running = True
    @classmethod
    def set_running(cls, val):
        cls.running = val
    @classmethod
    def get_running(cls):
        return cls.running
    ##################################################################

    ##################################################################
    # current game/menu methods
    current_game = None
    @classmethod
    def set_current_game(cls, game):
        cls.current_game = game
    @classmethod
    def get_current_game(cls):
        return cls.current_game
    ##################################################################
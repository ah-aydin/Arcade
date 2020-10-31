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
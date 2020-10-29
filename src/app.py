class App():
    @classmethod
    def set_surface(cls, surface):
        cls.surface = surface
    
    @classmethod
    def get_surface(cls):
        return cls.surface
    
    @classmethod
    def clear_surface(cls, color):
        cls.surface.fill(color)
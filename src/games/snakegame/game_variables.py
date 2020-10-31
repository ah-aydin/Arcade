class GameVariables():
    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    PURPLE = (255, 0, 255)

    # Direction variables
    UP      = 'UP'
    RIGHT   = 'RIGHT'
    DOWN    = 'DOWN'
    LEFT    = 'LEFT'
    DIRECTION_STEPS = {
        UP:     ( 0, 1),
        DOWN:   ( 0,-1),
        RIGHT:  (-1, 0),
        LEFT:   ( 1, 0)
    }

    # Transform variables
    PLAY_AREA_DIMENTION = 20
    TILE_WIDTH = 30
    PLAY_AREA_TOP_LEFT = (0, 0)
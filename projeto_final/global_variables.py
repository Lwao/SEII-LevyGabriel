WIDTH, HEIGHT = (800,489)
TITLE = 'DDAir - Drone Dynamics in the Air'

BACKGROUND_INTERACTABLE_RANGE = (WIDTH,HEIGHT-100)

DRONE_RADIUS = 0.1 # m
DRONE_IMG_DIM = (512,330)
DRONE_IMG_SCALER = 6.4
DRONE_BOX = (DRONE_IMG_DIM[0]/DRONE_IMG_SCALER,DRONE_IMG_DIM[1]/DRONE_IMG_SCALER)
DRONE_LOCATION = (WIDTH/2,HEIGHT/2)

PIXEL_DENSITY = DRONE_BOX[0]/(2*DRONE_RADIUS) # px/m

FPS = 30
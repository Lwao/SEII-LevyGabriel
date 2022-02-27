import numpy as np

WIDTH, HEIGHT = (800,489)
TITLE = 'DDAir - Drone Dynamics in the Air'

BACKGROUND_INTERACTABLE_RANGE = (WIDTH,HEIGHT-100)

DRONE_RADIUS = 0.1 # m
DRONE_IMG_DIM = (512,330)
DRONE_IMG_SCALER = 6.4
DRONE_BOX = (DRONE_IMG_DIM[0]/DRONE_IMG_SCALER,DRONE_IMG_DIM[1]/DRONE_IMG_SCALER)

PIXEL_DENSITY = DRONE_BOX[0]/(2*DRONE_RADIUS*8) # px/m

"""
- canvas: (0 to 800px, 0 to 389px)
- real: (-2.5 to 2.5m, -1.25 to 1.25m)

 Xp - 0      Xm - (-2.5)
--------  = ------------
800 - 0      2.5 - (-2.5)

 Yp - 389       Ym - (-1.25)
----------  = ----------------
 0 - 389        1.25 - (-1.25)

 Xm = Xp * 5/800 - 2.5
 Ym = (Yp-389) * 2.5/(-389) - 1.25

 Xp = (Xm+2.5)*800/5
 Yp = (Ym+1.25)*(-389)/2.5 + 389

"""
pixel2meter = lambda px : np.array([px[0]*5/800-2.5, (px[1]-389)*2.5/(-389)-1.25]) 
meter2pixel = lambda m: np.array([(m[0]+2.5)*800/5, (m[1]+1.25)*(-389)/2.5 + 389])

FPS = 50
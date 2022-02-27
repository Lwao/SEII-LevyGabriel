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
- real: (0 to 20m, 0 to 15m)

 Xp - 0      Xm - 0
--------  = --------
800 - 0      20 - 0

 Yp - 389       Ym - 0
----------  = -----------
 0 - 389       9.725 - 0

 Xm = Xp * 20 /800
 Ym = (Yp-389) * 9.725/(-389)

 Xp = Xm*800/20
 Yp = Ym*(-389)/9.725 + 389

"""
# pixel2meter = lambda px : np.array([px[0]*20/800, (px[1]-389)*9.725/(-389)]) 
# meter2pixel = lambda m: np.array([m[0]*800/20, m[1]*(-389)/9.725 + 389])

"""
- canvas: (0 to 800px, 0 to 389px)
- real: (0 to 20m, 0 to 15m)

 Xp - 0      Xm - (-10)
--------  = ------------
800 - 0      10 - (-10)

 Yp - 389       Ym - (-0.725)
----------  = ----------------
 0 - 389        9 - (-0.725)

 Xm = Xp * 20/800 - 10
 Ym = (Yp-389) * 9.725/(-389) - 0.725

 Xp = (Xm+10)*800/20
 Yp = (Ym+0.725)*(-389)/9.725 + 389

"""
pixel2meter = lambda px : np.array([px[0]*20/800-10, (px[1]-389)*9.725/(-389)-0.725]) 
meter2pixel = lambda m: np.array([(m[0]+10)*800/20, (m[1]+0.725)*(-389)/9.725 + 389])

FPS = 50
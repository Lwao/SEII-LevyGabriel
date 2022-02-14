import numpy as np
from re import M
import pygame
from pygame.locals import *
from sys import exit

from Background import Background
from Drone import Drone
from Waypoint import Waypoint
from ControlSystem import ControlSystem

from global_variables import *

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(TITLE)

background = Background('img/background_resized.jpg', (WIDTH,HEIGHT))
drone = Drone(pd=PIXEL_DENSITY, box_=DRONE_BOX, range_=BACKGROUND_INTERACTABLE_RANGE)
waypoint = Waypoint(range_=BACKGROUND_INTERACTABLE_RANGE)
control_system = ControlSystem(drone.get_static_dict())

sprites = pygame.sprite.Group()
sprites.add(drone)
sprites.add(waypoint)

while True:
    dt = clock.tick(FPS)/1000
    screen.fill((0,0,0))
    screen.blit(background.image, background.rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
    keys = pygame.key.get_pressed()
    
    # if keys[pygame.K_LEFT] or keys[pygame.K_a]: drone.tilt(5)
    # if keys[pygame.K_RIGHT] or keys[pygame.K_d]: drone.tilt(-5)
    # if keys[pygame.K_SPACE] or keys[pygame.K_w]: drone.gas()

    # if keys[pygame.K_LEFT] or keys[pygame.K_a]: waypoint.move(waypoint.left)
    # if keys[pygame.K_RIGHT] or keys[pygame.K_d]: waypoint.move(waypoint.right)
    # if keys[pygame.K_UP] or keys[pygame.K_w]: waypoint.move(waypoint.up)
    # if keys[pygame.K_DOWN] or keys[pygame.K_s]: waypoint.move(waypoint.down)
    # drone.track(waypoint)

    # if keys[pygame.K_d]: drone.gas(drone.rotor_left)
    # if keys[pygame.K_a]: drone.brake(drone.rotor_left)
    # if keys[pygame.K_l]: drone.gas(drone.rotor_right)
    # if keys[pygame.K_j]: drone.brake(drone.rotor_right)

    speed_ = control_system.step(drone.get_actual_state(), np.array([100,100]))

    drone.rotor_left.set_speed_ref(speed_[0])
    drone.rotor_right.set_speed_ref(speed_[1])
    
    sprites.update(dt)
    sprites.draw(screen)
    
    
    pygame.display.flip()

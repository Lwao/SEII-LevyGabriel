import numpy as np
from re import M
import pygame
from pygame.locals import *
from sys import exit

from Background import Background
from Drone import Drone
from Waypoint import Waypoint

from global_variables import *

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(TITLE)

background = Background('img/background_resized.jpg', (WIDTH,HEIGHT))
drone = Drone(pd=PIXEL_DENSITY, box_=DRONE_BOX, location_=DRONE_LOCATION, range_=BACKGROUND_INTERACTABLE_RANGE)
waypoint = Waypoint(range_=BACKGROUND_INTERACTABLE_RANGE)

sprites = pygame.sprite.Group()
sprites.add(drone)
sprites.add(waypoint)

def mat_rot(angle): 
    angle *= np.pi/180
    #return np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]], dtype=np.float32) # direct
    return np.array([[np.cos(angle), np.sin(angle)],[-np.sin(angle), np.cos(angle)]], dtype=np.float32).reshape(2,2) # inverse

a = 0
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

    # if keys[pygame.K_LEFT] or keys[pygame.K_a]: drone.gas(5)
    # if keys[pygame.K_RIGHT] or keys[pygame.K_d]: drone.tilt(-5)
    
    # center = np.array(drone.rect.center).reshape(-1)
    # d = np.array([0,-100]).reshape(-1)
    # w = (mat_rot(drone.angle)@d).reshape(-1)
    # pygame.draw.line(screen, 'red', center, center+d)
    # pygame.draw.line(screen, 'blue', center, center+w)

    sprites.update()
    sprites.draw(screen)
    
    
    pygame.display.flip()

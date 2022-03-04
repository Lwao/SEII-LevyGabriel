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
drone = Drone(box_=DRONE_BOX, range_=BACKGROUND_INTERACTABLE_RANGE)
waypoint = Waypoint(range_=BACKGROUND_INTERACTABLE_RANGE)

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

    if keys[pygame.K_LEFT] or keys[pygame.K_a]: waypoint.move(waypoint.left)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: waypoint.move(waypoint.right)
    if keys[pygame.K_UP] or keys[pygame.K_w]: waypoint.move(waypoint.up)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]: waypoint.move(waypoint.down)
    
    # drone.track([100,100])
    drone.track(waypoint.rect.center)
  
    sprites.update(dt)
    sprites.draw(screen)
    
    pygame.display.flip()

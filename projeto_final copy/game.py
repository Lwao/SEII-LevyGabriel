import math
import pygame
from pygame.locals import *
from sys import exit

from Background import Background
from Drone import Drone
from Waypoint import Waypoint

pygame.init()

WIDTH, HEIGHT = (800,489)
FPS = 30

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('DDAir - Drone Dynamics in the Air')

background = Background('background_resized.jpg', [0,0], WIDTH, HEIGHT)
drone = Drone(location_=[WIDTH/2,HEIGHT/2], range_=(WIDTH,HEIGHT-100))
waypoint = Waypoint(range_=(WIDTH,HEIGHT-100))

sprites = pygame.sprite.Group()
sprites.add(drone)
sprites.add(waypoint)

while True:
    clock.tick(FPS)
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

    if keys[pygame.K_LEFT] or keys[pygame.K_a]: waypoint.move(waypoint.left)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: waypoint.move(waypoint.right)
    if keys[pygame.K_UP] or keys[pygame.K_w]: waypoint.move(waypoint.up)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]: waypoint.move(waypoint.down)

    drone.track(waypoint)

    sprites.draw(screen)
    sprites.update()

    
    pygame.display.flip()

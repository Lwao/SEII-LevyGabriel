import math
import pygame
from pygame.locals import *
from sys import exit

pygame.init()

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, width, height):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (width,height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Drone(pygame.sprite.Sprite):
    def __init__(self, location_, range_):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.sprites = []
        self.sprites.append(pygame.image.load('drone1.png'))
        self.sprites.append(pygame.image.load('drone2.png'))
        self.sprites_num = len(self.sprites)
        
        self.inertia = {'W':0,'A':0,'S':0,'D':0}

        self.actual = 0
        self.angle = 0
        self.image = self.sprites[self.actual]
        self.image = pygame.transform.scale(self.image, (80,80))

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location_
        self.range = {'x':range_[0], 'y':range_[1]}
        self.in_range = {'up':True,'down':True,'right':True,'left':False}

    def update(self):
        self.actual += 0.25 # increment sprite
        self.actual %= self.sprites_num # limit to the number of sprites
        self.image = self.sprites[int(self.actual)]
        self.image = pygame.transform.scale(self.image, (80,80))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update_position(self, func_, step, inertia): 
        func_(step, inertia)

        self.in_range['up'] = self.rect.y>=0
        self.in_range['left'] = self.rect.x>=0
        self.in_range['down'] = self.rect.y<=self.range['y']
        self.in_range['right'] = self.rect.x<=self.range['x']

    def go_up(self, step, inertia):
        if(self.in_range['up']):
            self.rect.y-=step
            self.inertia['W']+=inertia
        else: self.go_down(step, 2*inertia)
    def go_left(self, step, inertia):
        # self.rotate(1)
        # step = step*abs(self.angle)/30
        if(self.in_range['left']):
            self.rect.x-=step
            self.inertia['A']+=inertia
        else: self.go_right(step, 2*inertia)
    def go_down(self, step, inertia):
        if(self.in_range['down']):
            self.rect.y+=step
            self.inertia['S']+=inertia
        else: self.go_up(step, 2*inertia)
    def go_right(self, step, inertia):
        # self.rotate(-1)
        # step = step*abs(self.angle)/30
        if(self.in_range['right']):
            self.rect.x+=step
            self.inertia['D']+=inertia
        else: self.go_left(step, 2*inertia)

    def fade_inertia(self, limit):
        if(self.inertia['W']>0):
            self.rect.y-=self.inertia['W']
            self.inertia['W']-=1
        if(self.inertia['A']>0):
            self.rect.x-=self.inertia['A']
            self.inertia['A']-=1
        if(self.inertia['S']>0):
            self.rect.y+=self.inertia['S']
            self.inertia['S']-=1
        if(self.inertia['D']>0):
            self.rect.x+=self.inertia['D']
            self.inertia['D']-=1
        if(self.inertia['W']>limit): self.inertia['W']=limit
        if(self.inertia['A']>limit): self.inertia['A']=limit
        if(self.inertia['S']>limit): self.inertia['S']=limit
        if(self.inertia['D']>limit): self.inertia['D']=limit

    def fade_angle(self):
        if(self.angle!=0): self.rotate(math.copysign(1,self.angle*(-1)))

    def rotate(self, inc_angle):
        self.angle += inc_angle
        self.angle %= 360
        if((self.angle>30) or (self.angle<-30)): inc_angle=0
        self.image = pygame.transform.rotate(self.image, inc_angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        

    

WIDTH, HEIGHT = (800,489)
FPS = 30
STEP = 5
INERTIA = 2
INERTIA_CAP = 5

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('DDAir - Drone Dynamics in the Air')

background = Background('background_resized.jpg', [0,0], WIDTH, HEIGHT)
drone = Drone(location_=[WIDTH/2,HEIGHT/2], range_=(WIDTH-85,HEIGHT-180))

sprites = pygame.sprite.Group()
sprites.add(drone)

while True:
    clock.tick(FPS)
    screen.fill((0,0,0))
    screen.blit(background.image, background.rect)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP] or keys[pygame.K_w]: drone.update_position(drone.go_up, STEP, INERTIA)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: drone.update_position(drone.go_left, STEP, INERTIA)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]: drone.update_position(drone.go_down, STEP, INERTIA)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: drone.update_position(drone.go_right, STEP, INERTIA)
    
    drone.fade_inertia(INERTIA_CAP)
    # drone.fade_angle()

    sprites.draw(screen)
    sprites.update()
    
    pygame.display.flip()

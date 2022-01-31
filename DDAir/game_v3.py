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

        self.STEP = 5
        self.ANGLE_INC = 5
        self.INERTIA_INC = 2
        self.INERTIA_CAP = 5
        self.SPEED_CAP = 0.25
        self.NEG_ACEL = 0.05
        self.POS_ACEL = 0.1

        self.speed = self.SPEED_CAP
        self.actual = 0
        self.angle = 0
        self.image = self.sprites[self.actual]
        self.image = pygame.transform.scale(self.image, (80,80))

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location_
        self.range = {'x':range_[0], 'y':range_[1]}
        self.in_range = {'up':True,'down':True,'right':True,'left':False}

    def update(self):
        if(self.speed>self.SPEED_CAP): self.speed = self.SPEED_CAP
        self.actual += self.speed # increment sprite
        self.actual %= self.sprites_num # limit to the number of sprites
        self.image = self.sprites[int(self.actual)]
        self.image = pygame.transform.scale(self.image, (80,80))

        # check ranges
        self.in_range['up'] = self.rect.y>=0
        self.in_range['left'] = self.rect.x>=0
        self.in_range['down'] = self.rect.y<=self.range['y']
        self.in_range['right'] = self.rect.x<=self.range['x']

        # physics
        self.gravity()
        self.fade_inertia(self.INERTIA_CAP)
        self.fade_speed()
        
        # rotate
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, func_): func_()

    def gas(self):
        inc_x = int(self.STEP*math.sin(abs(self.angle)*math.pi/180))
        inc_y = int(self.STEP*math.cos(abs(self.angle)*math.pi/180))

        self.speed += self.POS_ACEL
        if(self.angle>0): 
            if(self.in_range['left']): 
                self.rect.x -= inc_x
                self.inertia['A']+=self.INERTIA_INC
            else: 
                self.rect.x += inc_x
                self.inertia['D'] = self.inertia['A']
                self.inertia['A'] = 0
        if(self.angle<0): 
            if(self.in_range['right']): 
                self.rect.x += inc_x
                self.inertia['D']+=self.INERTIA_INC
            else: 
                self.rect.x -= inc_x
                self.inertia['A'] = self.inertia['D']
                self.inertia['D'] = 0
        
        if(self.in_range['up']): 
            self.rect.y -= inc_y
            self.inertia['W']+=self.INERTIA_INC
        else: 
            self.rect.y += inc_y
            self.inertia['S'] = self.inertia['W']
            self.inertia['W'] = 0


    def gravity(self):
        if(self.in_range['down']):
            self.rect.y += 0.5
            self.inertia['S']+=self.INERTIA_INC
        else: # change W for S inertia
            self.inertia['W'] += self.inertia['S']
            self.inertia['S'] = 0
            

    def turn_aclkwise(self):
        self.angle += self.ANGLE_INC
        if self.angle>45: self.angle=45

    def turn_clkwise(self):
        self.angle += -self.ANGLE_INC
        if self.angle<-45: self.angle=-45

    def fade_speed(self):
        self.speed -= self.NEG_ACEL
        if(self.speed<0): self.speed=0

    def fade_inertia(self, limit):
        if(self.inertia['W']>0):
            self.rect.y-=self.inertia['W']
            self.inertia['W']-=1
        if(self.inertia['A']>0):
            self.rect.x-=self.inertia['A']
            self.inertia['A']-=0.1
        if(self.inertia['S']>0):
            self.rect.y+=self.inertia['S']
            self.inertia['S']-=1
        if(self.inertia['D']>0):
            self.rect.x+=self.inertia['D']
            self.inertia['D']-=0.1
        if(self.inertia['W']>limit): self.inertia['W']=limit
        if(self.inertia['A']>limit): self.inertia['A']=limit
        if(self.inertia['S']>limit): self.inertia['S']=limit
        if(self.inertia['D']>limit): self.inertia['D']=limit

WIDTH, HEIGHT = (800,489)
FPS = 30

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('DDAir - Drone Dynamics in the Air')

background = Background('background_resized.jpg', [0,0], WIDTH, HEIGHT)
drone = Drone(location_=[WIDTH/2,HEIGHT/2], range_=(WIDTH-80,HEIGHT-180))

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
    
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: drone.move(drone.turn_aclkwise)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: drone.move(drone.turn_clkwise)
    if keys[pygame.K_SPACE] or keys[pygame.K_w]: drone.move(drone.gas)

    sprites.draw(screen)
    sprites.update()
    
    pygame.display.flip()

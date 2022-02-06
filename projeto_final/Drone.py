import pygame
import math

SPEED_CAP = 0.25
POS_ACEL = 0.5
NEG_ACEL = 0.005
ANGLE_INC = 5
STEP = 10

class Drone(pygame.sprite.Sprite):
    def __init__(self, location_, range_):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        
        self.sprites = []
        self.box = (512/7,330/7)
        self.actual = 0

        self.sprites.append(pygame.image.load('drone1.png'))
        self.sprites.append(pygame.image.load('drone2.png'))
        self.sprites_num = len(self.sprites)
        self.image = self.sprites[self.actual]
        self.image = pygame.transform.scale(self.image, self.box)
        
        self.mass = 0.25 # Kg
        self.ang_momentum = 0.0002 # Kg m2
        self.radius = 0.1 # m
        self.max_rot = 15000 # rpm

        self.speed = SPEED_CAP
        self.angle = 0

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location_
        self.range = {'x':range_[0], 'y':range_[1]}
        self.in_range = {'up':True,'down':True,'right':True,'left':True}

    def update(self):
        if(self.speed>SPEED_CAP): self.speed = SPEED_CAP
        self.actual += self.speed # increment sprite
        self.actual %= self.sprites_num # limit to the number of sprites
        self.image = self.sprites[int(self.actual)]
        self.image = pygame.transform.scale(self.image, self.box)

        # physics
        self.colision()
        self.gravity()
        self.fade_speed()
        
        # rotate
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def colision(self):
        self.in_range['up'] = self.rect.y>=0
        self.in_range['left'] = self.rect.x>=0
        self.in_range['down'] = (self.rect.y+self.box[1])<=self.range['y']
        self.in_range['right'] = (self.rect.x+self.box[0])<=self.range['x']

    def gas(self):
        inc_x = int(STEP*math.sin(abs(self.angle)*math.pi/180))
        inc_y = int(STEP*math.cos(abs(self.angle)*math.pi/180))

        self.speed += POS_ACEL

        if(self.angle>0): 
            if(self.in_range['left']): self.rect.x -= inc_x
            if self.rect.x<0: self.rect.x=0
        
        if(self.angle<0): 
            if(self.in_range['right']): self.rect.x += inc_x
            if (self.rect.x+self.box[0])>self.range['x']: self.rect.x=self.range['x']-self.box[0]

        if ((self.in_range['up']) and (inc_y>0)) or ((self.in_range['down']) and (inc_y<0)): self.rect.y -= inc_y
        if self.rect.y<0: self.rect.y=0
        if (self.rect.y+self.box[1])>self.range['y']: self.rect.y=self.range['y']-self.box[1]

    def gravity(self):
        if(self.in_range['down']): self.rect.y += 2
            
    def tilt(self, inc):
        self.angle += inc
        if self.angle>180: self.angle-=360
        if self.angle<-180: self.angle+=360
        

    def fade_speed(self):
        self.speed -= NEG_ACEL
        if(self.speed<0): self.speed=0


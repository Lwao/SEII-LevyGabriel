from xml.dom import xmlbuilder
import pygame
import math
import numpy as np

from Rotor import *

SPEED_CAP = 0.25
POS_ACEL = 0.5
NEG_ACEL = 0.005
ANGLE_INC = 5
STEP = 10

def mat_rot(angle): 
    angle *= np.pi/180
    #return np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]], dtype=np.float32) # direct
    return np.array([[np.cos(angle), np.sin(angle)],[-np.sin(angle), np.cos(angle)]], dtype=np.float32).reshape(2,2) # inverse


class Drone(pygame.sprite.Sprite):
    def __init__(self, pd, box_, location_, range_, 
                mass=0.25, ang_momentum=0.0002, radius=0.1, max_rot=15000, gravity=9.81,
                force_constant=1.744e-8, time_constant=0.005):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        
        # sprite initialization
        self.sprites = []
        self.box = box_
        self.actual = 0
        self.sprites.append(pygame.image.load('img/drone1.png'))
        self.sprites.append(pygame.image.load('img/drone2.png'))
        self.sprites_num = len(self.sprites)
        self.image = self.sprites[self.actual]
        self.image = pygame.transform.scale(self.image, self.box)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location_
        self.range = {'up':0, 'down':range_[1], 'right':range_[0], 'left':0}
        self.rect.x, self.rect.y = (range_[0]-self.box[0])/2, (range_[1]-self.box[1])/2
        
        # static variables
        self.pixel_density = pd # px/m
        self.mass = mass # Kg
        self.gravity = gravity # m/s2
        self.ang_momentum = ang_momentum # Kg m2
        self.radius = radius # m
        self.weight = np.array([0.0, self.mass*self.gravity], dtype=np.float32) # N
        
        # objects
        self.rotor_left = Rotor(speed=0.0, force_constant=force_constant, time_constant=time_constant, max_speed=max_rot)
        self.rotor_right = Rotor(speed=0.0, force_constant=force_constant, time_constant=time_constant, max_speed=max_rot)

        # kinematic and dynamic variables
        self.position = np.array([0.0, 0.0], dtype=np.float32) # m
        self.linear_speed = np.array([0.0, 0.0], dtype=np.float32) # m/s 
        self.angle = np.float32(0.0) # rad/s2 
        self.rotational_speed = np.float32(0.0) # rad/s 
        self.rotational_accel = np.float32(0.0) # rad/s2 
        self.control_force = np.array([0.0, self.rotor_left.force+self.rotor_left.force], dtype=np.float32) # N
        self.control_torque = np.float32(self.radius*(self.rotor_left.force-self.rotor_left.force)) # N
        self.rotor_speed = np.array([self.rotor_left.speed, self.rotor_right.speed], dtype=np.float32)
        self.sprite_speed = SPEED_CAP

    def update(self):
        # shift sprite accordingly
        if(self.sprite_speed>SPEED_CAP): self.sprite_speed = SPEED_CAP
        self.actual += self.sprite_speed # increment sprite
        self.actual %= self.sprites_num # limit to the number of sprites
        self.image = self.sprites[int(self.actual)]
        self.image = pygame.transform.scale(self.image, self.box)

        # rotate sprite accordingly
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # physics
        self.colision()
        
    def colision(self):
        if self.rect.left<self.range['left']: self.rect.left=self.range['left'] # left
        if self.rect.right>self.range['right']: self.rect.right=self.range['right'] # right
        if self.rect.top<self.range['up']: self.rect.top=self.range['up'] # up
        if self.rect.bottom>self.range['down']: self.rect.bottom=self.range['down'] # down
        

    def gas(self):
        inc_x = int(STEP*math.sin(abs(self.angle)*math.pi/180))
        inc_y = int(STEP*math.cos(abs(self.angle)*math.pi/180))

        self.sprite_speed += POS_ACEL

        if(self.angle>0): self.rect.x -= inc_x
        if(self.angle<0): self.rect.x += inc_x
        self.rect.y -= inc_y
        
    def tilt(self, inc):
        self.angle += inc
        if self.angle>180: self.angle-=360
        if self.angle<-180: self.angle+=360

    def track(self, waypoint):
        print('centers')
        print(waypoint.rect.center)
        print(self.rect.center)
        xf, yf = waypoint.rect.center
        xi, yi = self.rect.center

        diffy = math.copysign(1,yf-yi)
        diffx = math.copysign(1,xf-xi)

        move_step = 1#STEP

        self.rect.x += xf-xi
        self.rect.y += yf-yi
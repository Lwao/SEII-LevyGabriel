from xml.dom import xmlbuilder
import pygame
import math

SPEED_CAP = 0.25
POS_ACEL = 0.5
NEG_ACEL = 0.005
ANGLE_INC = 5
STEP = 10

class Drone(pygame.sprite.Sprite):
    def __init__(self, pd, box_, location_, range_, 
                mass=0.25, ang_momentum=0.0002, radius=0.1, max_rot=15000, gravity=9.81,
                force_constant=1.744e-8, time_constant=0.005):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        
        self.sprites = []
        self.box = box_
        self.actual = 0
        self.sprites.append(pygame.image.load('img/drone1.png'))
        self.sprites.append(pygame.image.load('img/drone2.png'))
        self.sprites_num = len(self.sprites)
        self.image = self.sprites[self.actual]
        self.image = pygame.transform.scale(self.image, self.box)
        
        self.pixel_density = pd # px/m
        self.mass = mass # Kg
        self.ang_momentum = ang_momentum # Kg m2
        self.radius = radius # m
        self.max_rot = max_rot # rpm
        self.gravity = gravity # m/s2
        self.force_constant = force_constant
        self.time_constant = time_constant

        self.speed = 0 # m/s
        self.sprite_speed = SPEED_CAP
        self.angle = 0

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location_
        self.range = {'x':range_[0], 'y':range_[1]}
        self.in_range = {'up':True,'down':True,'right':True,'left':True}
        self.rect.x, self.rect.y = (range_[0]-self.box[0])/2, (range_[1]-self.box[1])/2

    def update(self):
        if(self.sprite_speed>SPEED_CAP): self.sprite_speed = SPEED_CAP
        self.actual += self.sprite_speed # increment sprite
        self.actual %= self.sprites_num # limit to the number of sprites
        self.image = self.sprites[int(self.actual)]
        self.image = pygame.transform.scale(self.image, self.box)

        # physics
        self.colision()
        self.apply_gravity()
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

        self.sprite_speed += POS_ACEL

        if(self.angle>0): 
            self.rect.x -= inc_x
            if self.rect.x<0: self.rect.x=0
        
        if(self.angle<0): 
            self.rect.x += inc_x
            if (self.rect.x+self.box[0])>self.range['x']: self.rect.x=self.range['x']-self.box[0]

        self.rect.y -= inc_y
        if self.rect.y<0: self.rect.y=0
        if (self.rect.y+self.box[1])>self.range['y']: self.rect.y=self.range['y']-self.box[1]

    def apply_gravity(self):
        if(self.in_range['down']): self.rect.y += 2
            
    def tilt(self, inc):
        self.angle += inc
        if self.angle>180: self.angle-=360
        if self.angle<-180: self.angle+=360
        
    def fade_speed(self):
        self.sprite_speed -= NEG_ACEL
        if(self.sprite_speed<0): self.sprite_speed=0

    def track(self, waypoint):
        yf = waypoint.rect.y + waypoint.r
        xf = waypoint.rect.x + waypoint.r

        yi = self.rect.y + self.box[1]/2
        xi = self.rect.x + self.box[0]/2

        diffy = math.copysign(1,yf-yi)
        diffx = math.copysign(1,xf-xi)

        move_step = 5#STEP

        self.rect.x += move_step*diffx
        self.rect.y += move_step*diffy

        

    # def track(self, waypoint):
    #     yf = waypoint.rect.y
    #     xf = waypoint.rect.x

    #     yi = self.rect.y
    #     xi = self.rect.x

    #     diffy = yf-yi
    #     diffx = xf-xi

    #     d = math.sqrt(diffy**2 + diffx**2)
    #     theta = math.atan2(abs(diffy), abs(diffx)) 

    #     move_step = 5#STEP

    #     if xi>xf and yi>yf: # 1st quadrant
    #         # theta = math.atan2(abs(diffy), abs(diffx)) 
    #         inc_x = move_step*math.sin(theta)
    #         inc_y = move_step*math.cos(theta)

    #         # left
    #         self.rect.x -= inc_x
    #         if self.rect.x<0: self.rect.x=0
    #         # up
    #         self.rect.y -= inc_y
    #         if self.rect.y<0: self.rect.y=0
    #     elif xi>xf and yi<yf: # 2nd quadrant
    #         # theta = math.atan2(abs(diffy), abs(diffx)) + 90*math.pi/180
    #         inc_x = move_step*math.cos(theta)
    #         inc_y = move_step*math.sin(theta)

    #         # left
    #         self.rect.x -= inc_x
    #         if self.rect.x<0: self.rect.x=0
    #         # down
    #         self.rect.y += inc_y
    #         if (self.rect.y+self.box[1])>self.range['y']: self.rect.y=self.range['y']-self.box[1]
    #     elif xi<xf and yi<yf: # 3rd quadrant
    #         # theta = math.atan2(abs(diffy), abs(diffx)) + 180*math.pi/180
    #         inc_x = move_step*math.sin(theta)
    #         inc_y = move_step*math.cos(theta)

    #         # right
    #         self.rect.x += inc_x
    #         if (self.rect.x+self.box[0])>self.range['x']: self.rect.x=self.range['x']-self.box[0]
    #         # down
    #         self.rect.y += inc_y
    #         if (self.rect.y+self.box[1])>self.range['y']: self.rect.y=self.range['y']-self.box[1]
    #     elif xi<xf and yi>yf: # 4th quadrant
    #         # theta = math.atan2(abs(diffy), abs(diffx)) + 270*math.pi/180
    #         inc_x = move_step*math.cos(theta)
    #         inc_y = move_step*math.sin(theta)

    #         # right
    #         self.rect.x += inc_x
    #         if (self.rect.x+self.box[0])>self.range['x']: self.rect.x=self.range['x']-self.box[0]
    #         # up
    #         self.rect.y -= inc_y
    #         if self.rect.y<0: self.rect.y=0



from xml.dom import xmlbuilder
import pygame
import math
import numpy as np

from Rotor import *

SPEED_CAP=3

def rotation_matrix(angle, orientation='inverse'): 
    # angle *= np.pi/180
    if(orientation=='direct'): return np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]], dtype=np.float32) # direct
    elif(orientation=='inverse'): return np.array([[np.cos(angle), np.sin(angle)],[-np.sin(angle), np.cos(angle)]], dtype=np.float32).reshape(2,2) # inverse

class Drone(pygame.sprite.Sprite):
    def __init__(self, pd, box_, range_, 
                mass=0.25, angular_momentum=2e-4, radius=0.1, gravity=9.81):
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
        self.range = {'up':0, 'down':range_[1], 'right':range_[0], 'left':0}
        self.rect.x, self.rect.y = (range_[0]-self.box[0])/2, (range_[1]-self.box[1])/2
        
        # objects
        self.rotor_left = Rotor()
        self.rotor_right = Rotor()

        # static variables
        self.pixel_density = pd # px/m
        self.mass = mass # Kg
        self.gravity = gravity # m/s2
        self.angular_momentum = angular_momentum # Kg m2
        self.radius = radius # m
        self.weight_force = np.array([0.0, self.mass*self.gravity], dtype=np.float32) # N

        self.max_rotor_speed = self.rotor_left.max_speed # rpm
        self.max_control_force = self.rotor_left.force_constant*self.max_rotor_speed**2 # N
        self.max_control_torque = self.radius*self.max_control_force # Nm

        # kinematic and dynamic variables
        self.position = np.array(self.rect.center, dtype=np.float32)/self.pixel_density # m
        self.linear_speed = np.array([0.0, 0.0], dtype=np.float32) # m/s 
        self.angle = np.float32(0.0) # rad
        self.rotational_speed = np.float32(0.0) #rpm
        self.control_force = np.array([0.0, self.rotor_left.force+self.rotor_right.force], dtype=np.float32) # N
        self.control_torque = np.float32(self.radius*(self.rotor_left.force-self.rotor_right.force)) # N
        self.rotor_speed = np.array([self.rotor_left.speed, self.rotor_right.speed], dtype=np.float32)
        self.sprite_speed = SPEED_CAP

        self.count=0


    def update(self, h):
        # shift sprite accordingly
        if(self.sprite_speed>SPEED_CAP): self.sprite_speed = SPEED_CAP
        self.actual += self.sprite_speed # increment sprite
        self.actual %= self.sprites_num # limit to the number of sprites
        self.image = self.sprites[int(self.actual)]
        self.image = pygame.transform.scale(self.image, self.box)

        # rotate sprite accordingly
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # update drone and rotor variables to map actual state
        self.rotor_left.update() # compute force
        self.rotor_right.update() # compute force
        self.control_force = np.array([0.0, self.rotor_left.force+self.rotor_right.force], dtype=np.float32) 
        self.control_torque = np.float32(self.radius*(self.rotor_left.force-self.rotor_right.force))
        self.rotor_speed = np.array([self.rotor_left.speed, self.rotor_right.speed], dtype=np.float32)
        self.position = np.array(self.rect.center, dtype=np.float32)/self.pixel_density

        # physics
        self.process(h)
        self.colision()

        # print(self.control_force, self.rotor_speed, [self.rotor_left.speed_ref, self.rotor_right.speed_ref]) 

    def get_static_dict(self):
        # return dictionary with some static info to the control system
        return {'weight_force': self.weight_force[1],
                'max_rotor_speed': self.max_rotor_speed,
                'max_control_force': self.max_control_force,
                'max_control_torque':self.max_control_torque,
                'max_angle': 15*np.pi/180,
                'force_constant_rotor_left': self.rotor_left.force_constant,
                'force_constant_rotor_right': self.rotor_right.force_constant}

    def get_actual_state(self):
        # return actual state
        return np.concatenate([ self.rotor_speed, 
                                self.position, 
                                self.linear_speed, 
                                np.array([self.angle]), 
                                np.array([self.rotational_speed]) ])
    
    def get_input(self): 
        # return input vector based in rotors speed reference value
        return np.array([   self.rotor_left.speed_ref, 
                            self.rotor_right.speed_ref], dtype=np.float32)

    def get_state_vector_derivative(self, actual_state, input_):
        # rename inputs and actual state
        w_ = input_
        w = actual_state[0:2]
        r = actual_state[2:4]
        v = actual_state[4:6]
        phi = actual_state[6]
        ome = actual_state[7]

        # compute state vector derivative
        w_dot = (w_ - w)/self.rotor_left.time_constant
        r_dot = v
        v_dot = ((rotation_matrix(phi)@self.control_force + self.weight_force)/self.mass).reshape(2,)
        phi_dot = np.array([ome])
        ome_dot = np.array([self.control_torque/self.angular_momentum])
        
        return np.concatenate([ w_dot, 
                                r_dot, 
                                v_dot, 
                                phi_dot, 
                                ome_dot])

    def rk4(self, h, actual_state, input_):
        # compute 4th order Runge-Kutta
        k1 = self.get_state_vector_derivative(actual_state, input_)
        k2 = self.get_state_vector_derivative(actual_state + h*k1/2.0, input_)
        k3 = self.get_state_vector_derivative(actual_state + h*k2/2.0, input_)
        k4 = self.get_state_vector_derivative(actual_state + h*k3, input_)
        next_state = actual_state + (h/6.0)*(k1+2*k2+2*k3+k4)
        return next_state

    def process(self, h):
        self.count+=1
        # get next state
        next_state = self.rk4(h, self.get_actual_state(), self.get_input())
        if(self.count>100):
            print(f"w = [%f, %f]\nr = [%f, %f]\nv= [%f, %f]\nphi = %f\nome = %f\n" % (next_state[0],next_state[1],next_state[2],next_state[3],next_state[4],next_state[5],next_state[6],next_state[7]))
            self.count=0
        # distribute state variables
        self.rotor_left.set_speed(next_state[0])
        self.rotor_right.set_speed(next_state[1])
        self.rect.x = next_state[2]*self.pixel_density-self.rect.width/2
        self.rect.y = next_state[3]*self.pixel_density-self.rect.height/2
        self.linear_speed = next_state[4:6]
        self.angle = next_state[6]%360
        self.rotational_speed = next_state[7]

    def colision(self):
        if self.rect.left<self.range['left']: self.rect.left=self.range['left'] # left
        if self.rect.right>self.range['right']: self.rect.right=self.range['right'] # right
        if self.rect.top<self.range['up']: self.rect.top=self.range['up'] # up
        if self.rect.bottom>self.range['down']: self.rect.bottom=self.range['down'] # down
        
    def gas(self, rotor):
        rotor.set_speed_ref(rotor.speed_ref+100)
    
    def brake(self, rotor):
        rotor.set_speed_ref(rotor.speed_ref-100)
        
    def track(self, waypoint):
        xf, yf = waypoint.rect.center
        xi, yi = self.rect.center

        diffy = math.copysign(1,yf-yi)
        diffx = math.copysign(1,xf-xi)

        move_step = 1

        self.rect.x += xf-xi
        self.rect.y += yf-yi
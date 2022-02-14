import numpy as np

class Rotor:
    def __init__(self, speed=0, force_constant=1.744e-8, time_constant=0.005, max_speed=15000, mass=0):
        self.speed_ref = 0
        self.speed = np.float32(speed) # rad/s
        self.max_speed = np.float32(max_speed)*np.pi/30 # rpm to rad/s
        self.force_constant = np.float32(force_constant)
        self.time_constant = np.float32(time_constant)
        self.force = np.float32(self.force_constant*self.speed**2) # N
        self.mass = np.float32(mass) # Kg

    def update(self): 
        self.force = np.float32(self.force_constant*self.speed**2)
    def set_speed_ref(self, speed): 
        self.speed_ref = speed
        if(self.speed_ref>self.max_speed): self.speed_ref=self.max_speed
        elif(self.speed_ref<0): self.speed_ref=0
    def set_speed(self, speed): 
        self.speed = np.abs(speed)
        if(self.speed>self.max_speed): self.speed=self.max_speed
    def set_mass(self, mass): self.mass = mass

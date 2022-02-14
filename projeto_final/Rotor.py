import numpy as np

class Rotor:
    def __init__(self, speed, force_constant, time_constant, max_speed, mass=0):
        self.speed = np.float32(speed) # rad/s
        self.max_speed = np.float32(max_speed)
        self.force_constant = np.float32(force_constant)
        self.time_constant = np.float32(time_constant)
        self.force = np.float32(self.force_constant*self.speed**2) # N
        self.mass = np.float32(mass) # Kg

    def update(self): self.force = np.float32(self.force_constant*self.speed**2)
    def set_speed(self, speed): self.speed = speed
    def set_mass(self, mass): self.mass = mass

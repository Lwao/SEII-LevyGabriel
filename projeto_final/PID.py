import numpy as np

class PID:
    def __init__(self, Kp=1, Ki=0, Kd=0):
        self.Kp = np.float32(Kp)
        self.Ki = np.float32(Ki)
        self.Kd = np.float32(Kd)
        self.integral= np.float32(0)
        self.last_error = np.float32(0)
        self.error = np.float32(0)

    def step(self, input_error, h):
        # update errors
        self.last_error = self.error
        self.error = input_error
        # process output
        proportional = self.Kp*self.error
        self.integral = self.integral + proportional*h
        derivative = (proportional-self.last_error)/h
        # output control signal
        return proportional + self.Ki*self.integral + self.Kd*derivative
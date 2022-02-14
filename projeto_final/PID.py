import numpy as np

class PID:
    def __init__(self, Kp=1, Ki=0, Kd=0):
        self.Kp = np.float32(Kp)
        self.Ki = np.float32(Ki)
        self.Kd = np.float32(Kd)
        self.integral= np.float32(0)

    def step(self, proportional_error, derivative_error):
        # update errors
        # self.derivative = derivative_error
        # self.error = proportional_error
        # process output
        proportional = self.Kp*proportional_error
        self.integral += proportional_error#*h
        derivative = derivative_error#/h
        # output control signal
        return proportional + self.Ki*self.integral + self.Kd*derivative
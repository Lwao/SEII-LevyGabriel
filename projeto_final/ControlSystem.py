import numpy as np

from PID import *

class ControlSystem:
    def __init__(self, static_dict):
        self.PositionControllerX = PID(Kp=.075, Kd=.25)
        self.PositionControllerY = PID(Kp=.075, Kd=.25)
        self.TiltController = PID(Kp=.75, Kd=.05)
        self.static_dict = static_dict

        self.count=0
        
    def step(self, readings, reference):
        r = readings[2:4]
        v = readings[4:6]
        phi = readings[6]
        ome = readings[7]

        # position control
        r_ = reference.reshape(2,)
        v_ = np.zeros(2).reshape(2,)
        error_r = r_ - r
        error_v = v_ - v
        
        # self.count+=1
        # if self.count>10:
        #     print(f"r = [%f,%f]\nr_ = [%f,%f]\nr_e = [%f,%f]\n" % (r[0],r[1],r_[0],r_[1],error_r[0],error_r[1]))
        #     self.count=0

        # position error is low and is not the last waypoint
        if np.linalg.norm(error_r)<.1: #and r_ID < (r_IDN): 
            print('Waypoint reached')
        
        Fx = self.PositionControllerX.step(error_r[0], error_v[0])
        Fy = self.PositionControllerY.step(error_r[1], error_v[1]) - self.static_dict['weight_force']
        Fy = np.maximum(0.2*self.static_dict['max_control_force'], np.minimum(Fy, 0.8*self.static_dict['max_control_force']))

        # tilt control
        phi_ = np.arctan2(-Fx, Fy)
        ome_ = np.float32(0)

        if np.abs(phi_) > self.static_dict['max_angle']:
            signal = phi_/np.absolute(phi_)
            phi_ = signal * self.static_dict['max_angle']
            Fx = Fy * np.tan(phi_) # limiting angle
        
        Fxy = np.array([Fx, Fy])
        Fc = np.linalg.norm(Fxy)
        F12 = np.array([Fc/2.0, Fc/2.0])

        error_phi = phi_ - phi
        error_ome = ome_ - ome
        
        Tc = self.TiltController.step(error_phi, error_ome)
        Tc = np.maximum(-0.4*self.static_dict['max_control_torque'], np.minimum(Tc, 0.4*self.static_dict['max_control_torque']))
        
        # force increment
        dF12 = np.absolute(Tc)/2.0
        if (Tc >= 0.0):
            F12[0] = F12[0] + dF12
            F12[1] = F12[1] - dF12
        else:
            F12[0] = F12[0] - dF12
            F12[1] = F12[1] + dF12

        # Comando de rpm dos motores
        w1_ = np.sqrt(F12[0]/(self.static_dict['force_constant_rotor_left']))
        w2_ = np.sqrt(F12[1]/(self.static_dict['force_constant_rotor_right']))

        w1 = np.maximum(0., np.minimum(w1_, self.static_dict['max_rotor_speed']))
        w2 = np.maximum(0., np.minimum(w2_, self.static_dict['max_rotor_speed']))

        return np.array([w1, w2])
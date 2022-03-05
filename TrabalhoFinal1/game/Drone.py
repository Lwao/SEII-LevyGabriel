from xml.dom import xmlbuilder
import pygame
import numpy as np

from global_variables import *

SPEED_CAP=3

def rotation_matrix(angle, orientation='inverse'): 
    # angle *= np.pi/180
    if(orientation=='direct'): return np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]], dtype=np.float32) # direct
    elif(orientation=='inverse'): return np.array([[np.cos(angle), np.sin(angle)],[-np.sin(angle), np.cos(angle)]], dtype=np.float32).reshape(2,2) # inverse

class Drone(pygame.sprite.Sprite):
    def __init__(self, box_, range_, h_sys=2.5e-3, h_ctrl=10e-3,
                mass=0.25, angular_momentum=2e-4, radius=0.1, gravity=9.81):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        
        self.h_sys = h_sys
        self.h_ctrl = h_ctrl

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
        self.sprite_speed = SPEED_CAP
        self.angle = 0

        self.pos2track = pixel2meter(self.rect.center)

        self.x = np.array([ 0., 0., \
                            0., 0., \
                            0., .0, \
                            0*np.pi/180., \
                            0*np.pi/180.])
        self.w_ = np.zeros(2).reshape(2,)

        self.reach_destination = False
        self.count=0

    def track(self, pos): 
        self.pos2track = pixel2meter(pos)

    def update(self, h):
        h_acc = 0
        for _ in range(round(h/self.h_sys)): 
            h_acc += self.h_sys
            if (h_acc % self.h_ctrl) == 0: self.w_, self.reach_destination = self.control_step(self.x, self.pos2track)
            self.x = self.rk4(self.h_sys, self.x, self.w_) # simulação um passo a frente

        # self.count+=1
        # if self.count>=100:
        #     print(f"r_ = (%f, %f)" % (self.pos2track[0], self.pos2track[1]))
        #     print(f"w = [%f, %f]\nr = [%f, %f]\nv = [%f, %f]\nphi = %f\nome = %f\n" % tuple(self.x))
        #     print()
        #     self.count=0
        

        self.rect.x, self.rect.y = meter2pixel(self.x[2:4]).reshape(2,) - np.array([self.rect.width/2,self.rect.height/2]).reshape(2,)
        
        self.colision()

        # shift sprite accordingly
        if(self.sprite_speed>SPEED_CAP): self.sprite_speed = SPEED_CAP
        self.actual += self.sprite_speed # increment sprite
        self.actual %= self.sprites_num # limit to the number of sprites
        self.image = self.sprites[int(self.actual)]
        self.image = pygame.transform.smoothscale(self.image, self.box)

        # rotate sprite accordingly
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def colision(self):
        if self.rect.left<self.range['left']: self.rect.left=self.range['left'] # left
        if self.rect.right>self.range['right']: self.rect.right=self.range['right'] # right
        if self.rect.top<self.range['up']: self.rect.top=self.range['up'] # up
        if self.rect.bottom>self.range['down']: self.rect.bottom=self.range['down'] # down

    def get_sys_const(self):
        m = 0.25 # massa
        g = 9.81 # aceleração da gravidade
        l = 0.1 # tamanho
        kf = 1.744e-08 # constante de força
        Iz = 2e-4 # momento de inércia
        tal = 0.05 # constante de tempo rotor
        Fg = -m*g # força da gravidade

        # Restrições do controle
        phi_max = 15*np.pi/180. # ângulo máximo
        w_max = 15000
        Fc_max = kf*w_max**2 # Força de controle máximo
        Tc_max = l*kf*w_max**2

        return m, g, l, kf, Iz, tal, Fg, phi_max, w_max, Fc_max, Tc_max

    def x_dot(self, x, w_):
        # State vector
        # x = [ w r_xy v_xy phi omega]' \in R^8
        
        ## Parâmetros
        m, _, l, kf, Iz, tal, Fg, _, _, _, _ = self.get_sys_const()
        Fg = np.array([[0],\
                        [Fg]])

        ## Estados atuais
        w = x[0:2]
        r = x[2:4]
        v = x[4:6]
        phi = x[6]
        ome = x[7]
        
        ## Variáveis auxiliares

        # forças
        f1 = kf * w[0]**2
        f2 = kf * w[1]**2

        # Torque
        Tc = l * (f1 - f2)

        # Força de controle
        Fc_B = np.array( [[0], \
                        [(f1 + f2)]])
        
        # Matriz de atitude
        D_RB = np.array([ [ np.cos(phi), -np.sin(phi)], \
                        [ np.sin(phi), np.cos(phi)]])

        ## Derivadas
        w_dot = (-w + w_)/tal
        r_dot = v
        v_dot = (1/m)*(D_RB @ Fc_B + Fg)
        v_dot = v_dot.reshape(2,)
        phi_dot = np.array([ome])
        ome_dot = np.array([Tc/Iz])
        
        xkp1 = np.concatenate([ w_dot, \
                                r_dot, \
                                v_dot, \
                                phi_dot,\
                                ome_dot ])
        return xkp1
    
    def rk4(self, h, xk, uk):
        k1 = self.x_dot(xk, uk)
        k2 = self.x_dot(xk + h*k1/2.0, uk)
        k3 = self.x_dot(xk + h*k2/2.0, uk)
        k4 = self.x_dot(xk + h*k3, uk)
        xkp1 = xk +(h/6.0)*(k1 + 2*k2 + 2*k3 + k4)
        return xkp1

    def control_step(self, x, r_):
        reach_destination = False
        ### Execução da simulação

        _, _, _, kf, _, _, Fg, phi_max, w_max, Fc_max, Tc_max = self.get_sys_const()
        Fg = np.array([Fg])
        
        # Sistema de controle

        # Extrai os dados do vetor
        r = x[2:4]
        v = x[4:6]
        phi = x[6]
        ome = x[7]

        # Comando de posição
        v_ = np.array([0,0])
        
        #####################
        # Controle de Posição
        kpP = np.array([.075])
        kdP = np.array([0.25])
        eP = r_ - r
        eV = v_ - v
        
        # Definição do próximo waypoint
        if np.linalg.norm(eP) < .1:
            reach_destination = True

        Fx = kpP * eP[0] + kdP * eV[0]
        Fy = kpP * eP[1] + kdP * eV[1] - Fg
        Fy = np.maximum(0.2*Fc_max, np.minimum(Fy, 0.8*Fc_max))

        #####################
        # Controle de Atitude
        
        phi_ = np.arctan2(-Fx, Fy)
        
        if np.abs(phi_) > phi_max:
            #print(phi_*180/np.pi)
            signal = phi_/np.absolute(phi_)
            phi_ = signal * phi_max

            # Limitando o ângulo
            Fx = Fy * np.tan(phi_)
        
        Fxy = np.array([Fx, Fy])
        Fc = np.linalg.norm(Fxy)
        f12 = np.array([Fc/2.0, Fc/2.0])
        
        # Constantes Kp e Kd
        kpA = np.array([.75])
        kdA = np.array([0.05])
        ePhi = phi_ - phi
        eOme = 0 - ome
        
        Tc = kpA * ePhi + kdA * eOme
        Tc = np.maximum(-0.4*Tc_max, np.minimum(Tc, 0.4*Tc_max))
        
        # Delta de forças
        df12 = np.absolute(Tc)/2.0

        # Forças f1 e f2 final f12' = f12 + deltf12
        if (Tc >= 0.0):
            f12[0] = f12[0] + df12
            f12[1] = f12[1] - df12
        else:
            f12[0] = f12[0] - df12
            f12[1] = f12[1] + df12

        # Comando de rpm dos motores
        w1_ = np.sqrt(f12[0]/(kf))
        w2_ = np.sqrt(f12[1]/(kf))

        # Limitando o comando do motor entre 0 - 15000 rpm
        w1 = np.maximum(0., np.minimum(w1_, w_max))
        w2 = np.maximum(0., np.minimum(w2_, w_max))

        # Determinação do comando de entrada
        w_ = np.array([w1, w2])

        return w_, reach_destination

        
        
import pygame
from gui_utils.Button import Button
import psutil
import math

class GUI():
    def __init__(self):

        scale = 0.05
        y = 10
        x = 10
        step_x = 30

        self.buttons = dict()

        self.buttons['mode']      = Button(x=x+0*step_x, y=y, image_off="img/joystick_mode_on.png",  image_on="img/waypoint_mode_on.png", scale=scale)
        self.buttons['plot']      = Button(x=x+1*step_x, y=y, image_off="img/plot_off.png",          image_on="img/plot_on.png",          scale=scale)
        self.buttons['analytics'] = Button(x=x+2*step_x, y=y, image_off="img/analytics_off.png",     image_on="img/analytics_on.png",     scale=scale)
        self.buttons['csv']       = Button(x=x+3*step_x, y=y, image_off="img/csv_off.png",           image_on="img/csv_on.png",           scale=scale)
        self.buttons['debug']     = Button(x=x+4*step_x, y=y, image_off="img/debug_off.png",         image_on="img/debug_on.png",         scale=scale)
        self.buttons['power']     = Button(x=x+5*step_x, y=y, image_off="img/power.png",             image_on="img/power.png",            scale=scale)
        # self.buttons['joystick']  = Button(x=x+0*step_x, y=y, image_off="img/joystick_mode_off.png", image_on="img/joystick_mode_on.png", scale=scale)
        # self.buttons['waypoint']  = Button(x=x+1*step_x, y=y, image_off="img/waypoint_mode_off.png", image_on="img/waypoint_mode_on.png", scale=scale)
        # self.buttons['settings']  = Button(x=x+7*step_x, y=y, image_off="img/settings_off.png",      image_on="img/settings_on.png",      scale=scale)

        self.actions = self.init_actions()
        self.init_labels()

        # toggle on at init
        self.buttons['debug'].toggle = True
        self.actions['debug'] = True

    def init_actions(self):
        keys = list(self.buttons.keys())
        values = [False,False,False,False,False,False]
        actions = dict(zip(keys, values))
        return actions

    def init_labels(self):
        self.labels = dict()
        fontsize = 22
        font = pygame.font.SysFont('calibri', fontsize)

        label = []
        text = ['Game mode running in joystick mode.', 'Use the keyboard arrows keys or WASD to move.']
        for line in text: label.append(font.render(line, True, (0, 0, 0)))
        self.labels['joystick'] = label

        label = []
        text = ['Game mode running in waypoint mode.', 'Use the mouse to set the next destination of the drone.']
        for line in text: label.append(font.render(line, True, (0, 0, 0)))
        self.labels['waypoint'] = label

        label = []
        text = ['Turn on/off plots for drone\'s state variable']
        for line in text: label.append(font.render(line, True, (0, 0, 0)))
        self.labels['plot'] = label

        label = []
        text = ['Turn on/off print on screen the analytics', 'regarding the game performance on the host machine.']
        for line in text: label.append(font.render(line, True, (0, 0, 0)))
        self.labels['analytics'] = label

        label = []
        text = ['Turn on/off export the drone\'s state variable to a .csv file']
        for line in text: label.append(font.render(line, True, (0, 0, 0)))
        self.labels['csv'] = label

        label = []
        text = ['Turn on/off debug mode highlighting waypoints.']
        for line in text: label.append(font.render(line, True, (0, 0, 0)))
        self.labels['debug'] = label

        label = []
        text = ['Turn off the application.']
        for line in text: label.append(font.render(line, True, (0, 0, 0)))
        self.labels['power'] = label

    def draw(self, screen):
        final_colision = False
        
        for key in list(self.buttons.keys()): 
            colision, self.actions[key] = self.buttons[key].draw(screen)
            final_colision = final_colision or colision

            if colision:
                fontsize = 22
                if (key=='mode') and (self.actions['mode']==0): label = self.labels['joystick']
                if (key=='mode') and (self.actions['mode']==1): label = self.labels['waypoint']
                if key=='plot': label = self.labels['plot']
                if key=='analytics': label = self.labels['analytics']
                if key=='csv': label = self.labels['csv']
                if key=='debug': label = self.labels['debug']
                if key=='power': label = self.labels['power']

                for line in range(len(label)):
                    text = label[line]
                    text_rect = text.get_rect(center=(screen.get_width()//2,screen.get_height()//2))
                    text_rect = (text_rect[0], text_rect[1]+(line*fontsize)+(15*line))
                    screen.blit(text, text_rect)

        if final_colision: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def get_system_utils(self, dt, screen):
        cpu_percent = round(psutil.cpu_percent(),1) # %
        cpu_freq = round(psutil.cpu_freq().current) # MHz
        fps = round(1/dt) # FPS
        mem_available = round(psutil.virtual_memory().available / (1024*1024))
        mem_percent = round(psutil.virtual_memory().percent,1)
        
        text = ["CPU %.1f%% %.0f MHz" % (cpu_percent, cpu_freq), 
                "RAM %.1f%% Avl:%.0f MB" % (mem_percent, mem_available), 
                "FPS %.0f" % fps]

        
        fontsize = 10
        font = pygame.font.SysFont('calibri', fontsize)
        label = []
        text = ['Game mode running in joystick mode.', 'Use the keyboard arrows keys or WASD to move.']
        for line in text: label.append(font.render(line, True, (0, 0, 0)))
        for line in range(len(label)):
            text = label[line]
            text_rect = (600, 10+(line*fontsize)+(15*line))
            screen.blit(text, text_rect)

        
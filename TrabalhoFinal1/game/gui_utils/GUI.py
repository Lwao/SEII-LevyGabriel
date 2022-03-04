import pygame
from gui_utils.Button import Button

class GUI():
    def __init__(self):

        scale = 0.05
        y = 10
        x = 10
        step_x = 30

        self.buttons = dict()

        self.buttons['joystick']  = Button(x=x+0*step_x, y=y, image_off="img/joystick_mode_off.png", image_on="img/joystick_mode_on.png", scale=scale)
        self.buttons['waypoint']  = Button(x=x+1*step_x, y=y, image_off="img/waypoint_mode_off.png", image_on="img/waypoint_mode_on.png", scale=scale)
        self.buttons['plot']      = Button(x=x+2*step_x, y=y, image_off="img/plot_off.png",          image_on="img/plot_on.png",          scale=scale)
        self.buttons['analytics'] = Button(x=x+3*step_x, y=y, image_off="img/analytics_off.png",     image_on="img/analytics_on.png",     scale=scale)
        self.buttons['csv']       = Button(x=x+4*step_x, y=y, image_off="img/csv_off.png",           image_on="img/csv_on.png",           scale=scale)
        self.buttons['debug']     = Button(x=x+5*step_x, y=y, image_off="img/debug_off.png",         image_on="img/debug_on.png",         scale=scale)
        self.buttons['power']     = Button(x=x+6*step_x, y=y, image_off="img/power.png",             image_on="img/power.png",            scale=scale)
        #self.buttons['settings']  = Button(x=x+7*step_x, y=y, image_off="img/settings_off.png",      image_on="img/settings_on.png",      scale=scale)

    def draw(self, screen):
        final_colision = False
        actions = dict()
        for key in list(self.buttons.keys()): 
            colision, actions[key] = self.buttons[key].draw(screen)

                

            final_colision = final_colision or colision

        if final_colision: pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else: pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

            
            


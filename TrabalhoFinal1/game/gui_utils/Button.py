import pygame
from sqlalchemy import true

class Button():
    def __init__(self, x, y, image_off, image_on, scale):
        self.x, self.y = (x,y)
        self.scale = scale
        self.image_off = pygame.image.load(image_off)#.convert_alpha()
        self.image_on = pygame.image.load(image_on)#.convert_alpha()
        self.clicked = False
        self.toggle = False

        self.set_image(self.image_off, self.x, self.y)
    
        
    
    def draw(self, screen):
        action = False
        colision = False

        pos = pygame.mouse.get_pos() # get mouse position
    
        if self.rect.collidepoint(pos): # check mouseover and click (toggle mode)
            colision = True
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
            else:
                if self.clicked: 
                    self.clicked = False
                    self.toggle = not self.toggle
        else:
            colision = False

        if self.toggle: 
            self.set_image(self.image_on, self.x, self.y)
            action = True
        else:
            self.set_image(self.image_off, self.x, self.y)
            action = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return colision, action

    def block(self):
        

    def set_image(self, image, x, y):
        self.image = pygame.transform.smoothscale(      image, 
                                                    (   image.get_width()*self.scale, 
                                                        image.get_height()*self.scale
                                                    )
                                                    )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
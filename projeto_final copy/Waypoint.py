import pygame
import pygame.gfxdraw

STEP = 10

class Waypoint(pygame.sprite.Sprite):
    def __init__(self, range_):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        
        self.r = 5
        self.range = {'x':range_[0], 'y':range_[1]}
        self.in_range = {'up':True,'down':True,'right':True,'left':True}
        self.debug_mode = True

        self.image = pygame.Surface((2*self.r,2*self.r), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
         
        pygame.gfxdraw.aacircle(self.image, self.rect.x+self.r, self.rect.y+self.r, self.r, (255,0,0))
        pygame.gfxdraw.filled_circle(self.image, self.rect.x+self.r, self.rect.y+self.r, self.r, (255,0,0))

        self.rect.x, self.rect.y = range_[0]/2, range_[1]/2        
        
        
    def update(self): 
        self.colision()

    def move(self, func_): func_()
    
    def left(self): 
        self.rect.x -= STEP
        if self.rect.x<0: self.rect.x=0
    def right(self): 
        self.rect.x += STEP
        if (self.rect.x+2*self.r)>self.range['x']: self.rect.x=self.range['x']-2*self.r
    def up(self): 
        self.rect.y -= STEP
        if self.rect.y<0: self.rect.y=0
    def down(self): 
        self.rect.y += STEP
        if (self.rect.y+2*self.r)>self.range['y']: self.rect.y=self.range['y']-2*self.r

    def colision(self):
        self.in_range['up'] = self.rect.y>=0
        self.in_range['left'] = self.rect.x>=0
        self.in_range['down'] = (self.rect.y+2*self.r)<=self.range['y']
        self.in_range['right'] = (self.rect.x+2*self.r)<=self.range['x']

    def debug(self, val): 
        if(val): self.debug_mode=True
        else: self.debug_mode=False

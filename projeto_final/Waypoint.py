import pygame
import pygame.gfxdraw

STEP = 10

class Waypoint(pygame.sprite.Sprite):
    def __init__(self, range_):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        
        self.r = 4
        self.range = {'up':0, 'down':range_[1], 'right':range_[0], 'left':0}
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
    
    def left(self): self.rect.x -= STEP
    def right(self): self.rect.x += STEP
    def up(self): self.rect.y -= STEP
    def down(self): self.rect.y += STEP

    def colision(self):
        if self.rect.left<self.range['left']: self.rect.left=self.range['left'] # left
        if self.rect.right>self.range['right']: self.rect.right=self.range['right'] # right
        if self.rect.top<self.range['up']: self.rect.top=self.range['up'] # up
        if self.rect.bottom>self.range['down']: self.rect.bottom=self.range['down'] # down

    def debug(self, val): 
        if(val): self.debug_mode=True
        else: self.debug_mode=False

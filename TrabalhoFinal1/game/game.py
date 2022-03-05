from json.encoder import ESCAPE
import numpy as np
from re import M
import collections
import pygame
from pygame.locals import *
from sys import exit

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
matplotlib.use("Agg")

from Background import Background
from Drone import Drone
from Waypoint import Waypoint

from gui_utils.GUI import GUI

from global_variables import *

def draw_waypoint_pool(screen_, pool_, r_=4, color_=(0,0,255)):
    for pos_ in pool_:
        pygame.gfxdraw.aacircle(screen_, pos_[0]+r_, pos_[1]+r_, r_, color_)
        pygame.gfxdraw.filled_circle(screen_, pos_[0]+r_, pos_[1]+r_, r_, color_)

def plot_variables(buffer):
    [plot_deque.popleft() for _ in range(SIZE_WIN)]
    plot_deque.extend(np.array(buffer))
    
    ax.cla() # clear axis
    ax.plot(np.array(plot_deque)[:,0], linewidth=1, color='blue', label='x')
    ax.plot(np.array(plot_deque)[:,1], linewidth=1, color='red', label='y')
    ax.set_ylabel('Position [px]')
    ax.set_ylim(-10, 810)
    ax.set_xticks([])
    ax.legend(loc = 'center left', bbox_to_anchor=(1,0.5))

    fig.patch.set_alpha(0) 

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.buffer_rgba()
    
    return raw_data, canvas.get_width_height()

pygame.init()
pygame.font.init()

gui = GUI()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption(TITLE)
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

background = Background('img/background_resized.jpg', (WIDTH,HEIGHT))
light_background = Background('img/light_background_resized.jpg', (WIDTH,HEIGHT))
drone = Drone(box_=DRONE_BOX, range_=BACKGROUND_INTERACTABLE_RANGE)
waypoint = Waypoint(range_=BACKGROUND_INTERACTABLE_RANGE)

waypoint_deque = collections.deque()
plot_deque = collections.deque(list(map(tuple,np.zeros((8*SIZE_WIN,2)))))
plot_buffer = []
csv_buffer = []

fig, ax = plt.subplots(figsize=(8,1), nrows=1, ncols=1)
raw_data, size = plot_variables(list(map(tuple,np.zeros((SIZE_WIN,2)))))

sprites = pygame.sprite.Group()
sprites.add(drone)
sprites.add(waypoint)

pause = False
clicked = False
while True:
    dt = clock.tick(FPS)/1000
    screen.fill((0,0,0))
    
    # gui.draw(screen)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif (event.type == KEYDOWN) and (event.key == K_ESCAPE): pause = not pause

    if not pause: # not pause
        screen.blit(background.image, background.rect)

        keys = pygame.key.get_pressed()

        if gui.actions['mode'] == 0: # joystick mode
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: waypoint.move(waypoint.left)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: waypoint.move(waypoint.right)
            if keys[pygame.K_UP] or keys[pygame.K_w]: waypoint.move(waypoint.up)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: waypoint.move(waypoint.down)
        if gui.actions['mode'] == 1: # waypoint mode
            if pygame.mouse.get_pressed()[0]:
                clicked = True
            else:
                if clicked: 
                    clicked = False
                    pos = pygame.mouse.get_pos() # get mouse position
                    waypoint_deque.append(pos) # append mouse position to waypoint deque

            if drone.reach_destination:
                if len(waypoint_deque)!=0: # while there are position to be reached the waypoint is set to it
                    waypoint.set_position(waypoint_deque.popleft())                        

        if gui.actions['debug']:
            draw_waypoint_pool(screen, waypoint_deque)
            waypoint.debug(True)
        else:
            waypoint.debug(False)

        if gui.actions['plot']: 
            plot_buffer.append(drone.rect.center)
            if len(plot_buffer) == SIZE_WIN:
                raw_data, size = plot_variables(plot_buffer)
                plot_buffer = []
            screen.blit(pygame.image.frombuffer(raw_data, size, "RGBA"), (0,489-100))

        if gui.actions['csv']:
            csv_buffer.append(drone.x)
            if len(csv_buffer) == 8*SIZE_WIN:
                np.savetxt('data/data.csv', np.array(csv_buffer), delimiter=',')
                csv_buffer = []

        drone.track(waypoint.rect.center)
    
        sprites.update(dt)
        sprites.draw(screen)
    else: # pause
        screen.blit(light_background.image, light_background.rect)
        gui.draw(screen)

    
    pygame.display.flip()

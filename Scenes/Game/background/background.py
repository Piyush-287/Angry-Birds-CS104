import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from load import *
from Physics.config import * 
def generate_background(Surface : pygame.Surface):
    global IMAGES
    if RESIZED["BACKGROUND_IMAGE"].get_size() != Surface.get_size():
        RESIZED["BACKGROUND_IMAGE"]=pygame.transform.scale(IMAGES["BACKGROUND_IMAGE"],Surface.get_size())
    Surface.blit(RESIZED["BACKGROUND_IMAGE"],(0,0),)

def generate_mountains(Surface : pygame.Surface):
    global IMAGES
    if RESIZED["MOUNTAIN"].get_size() != Surface.get_size():
        RESIZED["MOUNTAIN"]=pygame.transform.scale(IMAGES["MOUNTAIN"],Surface.get_size())
    Surface.blit(RESIZED["MOUNTAIN"],(0,0),)

if __name__=="__main__":
    import pygame
    import random 
    import Scenes.Game.background.background as Background
    import load 
    import Entities.Birds as Birds
    import Entities.slingshot as slingshot
    # Colors 
    COLORS = {
        "red": (255,0,0), "green": (0,255,0), "blue": (0,0,255), "white": (255,255,255),
        "black": (0,0,0), "yellow": (255,255,0), "pink": (255,192,203), "orange": (255,165,0),
        "violet": (138,43,226), "gray": (128,128,128), "cyan": (0,255,255), "magenta": (255,0,255)
    }
    BG_COLOR=COLORS["blue"]
    
    # STANDARD VARIABLES
    WINDOW_SIZE=(500,500)
    TICKS=50
    # INGAME VARIABLES
    screen=pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("")
    clock=pygame.time.Clock()
    IMAGES,RESIZED=load_images()
    ABIRD=Birds.Bird((10,470),1,(20,0))
    RESIZED["LSLING"]=pygame.transform.scale_by(IMAGES["LSLING"],0.2)
    SLINGSHOT=slingshot.slingshot((150,450),RESIZED["LSLING"])
    game = True
    while game:
        dt=clock.tick(TICKS)/1000
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game = False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if  event.button == 1:
                    mouse_x,mouse_y=pygame.mouse.get_pos()
                    SLINGSHOT.enable((mouse_x,mouse_y))
            if event.type==pygame.MOUSEBUTTONUP:
                if SLINGSHOT.enabled and event.button ==1:
                    mouse_x,mouse_y=pygame.mouse.get_pos()
                    ABIRD.vx,ABIRD.vy=SLINGSHOT.launchvel((mouse_x,mouse_y))
            if event.type==pygame.VIDEORESIZE:
                SLINGSHOT.posn=(150,screen.get_size()[1]-150)
                SLINGSHOT.rect=pygame.Rect(*SLINGSHOT.posn,20,40)
        #Game Calculations
    
        # Update Everything
        ABIRD.update(dt,screen)
        if SLINGSHOT.enabled:
            ABIRD.x,ABIRD.y=pygame.mouse.get_pos()
            SLINGSHOT.update((ABIRD.x,ABIRD.y))
            ABIRD.x-=10
            ABIRD.y-=10
            ABIRD.xm,ABIRD.ym=ABIRD.x / Birds.Physics.config.METER,ABIRD.y / Birds.Physics.config.METER
        #Background 
        screen.fill(BG_COLOR)
        generate_background(screen)
        generate_mountains(screen)
        ABIRD.draw(screen)
        SLINGSHOT.draw(screen)
        # display everything
    
        pygame.display.flip()
    
    pygame.display.quit()
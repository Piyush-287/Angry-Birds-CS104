import sys, os

import Utils.colors
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import pygame 
import Utils
from Physics.config import *
class slingshot(pygame.sprite.Sprite):
    def __init__(self,posn, *groups):
        self.posn=posn
        self.enabled=False
        self.image=pygame.Surface((20,40))
        self.image.fill(Utils.colors.COLORS["green"])
        self.rect=pygame.Rect(*posn,20,40)
        self.traj=list()
        super().__init__(*groups)

    def enable(self,mouse_posn):
        if self.rect.collidepoint(*mouse_posn):
            self.gettraj(mouse_posn)
            self.enabled=True
        return self.enabled
    def launchvel(self,mouse_posn):
        self.enabled=False
        self.gettraj(mouse_posn)
        return (-mouse_posn[0]+self.rect.center[0],-mouse_posn[1]+self.rect.center[1])
    def draw(self,screen:pygame.surface.Surface):
        screen.blit(self.image,self.posn)
        if self.enabled:
            print("entered here")
            for point in self.traj:
                pygame.draw.circle(screen,Utils.colors.COLORS["gray"],point,2)
            print(self.traj)
    
    def gettraj(self,mouse_posn):
        self.traj.clear()
        vx,vy=(-mouse_posn[0]+self.rect.center[0],-mouse_posn[1]+self.rect.center[1])
        x,y=mouse_posn[0],mouse_posn[1]
        for i in range(10):
            x+=vx * METER *0.1
            y+=vy * METER *0.1
            vy += GRAVITY *0.1
            self.traj.append((x,y))

    def update(self,mouse_posn, *args, **kwargs):
        self.gettraj(mouse_posn)
        return super().update(*args, **kwargs)
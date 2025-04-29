import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import pygame 
from Physics.config import *
VIRTUAL_SIZE=(1920,1080)
class slingshot(pygame.sprite.Sprite):
    def __init__(self,posn,image,bird_size,screen_height,leftfacing, *groups):
        self.dirn=leftfacing
        self.posn=posn
        self.enabled=False
        self.image=image
        self.bird_size=bird_size
        self.screen_height=screen_height
        self.rect=self.image.get_rect(topleft=posn)
        self.traj=list()
        self.prev_mouse_posn=(self.rect.center[0],self.rect.center[1]-0.35*self.rect.height)
        super().__init__(*groups)
    def enable(self,mouse_posn):
        if self.rect.collidepoint(*mouse_posn):
            self.gettraj(mouse_posn)
            self.enabled=True
        return self.enabled
    def launchvel(self,mouse_posn):
        if mouse_posn[1]+self.bird_size[1] > self.screen_height -200:
            mouse_posn=(mouse_posn[0],self.prev_mouse_posn[1])
        else : self.prev_mouse_posn=mouse_posn
        self.enabled=False
        self.gettraj(mouse_posn)
        return ((-mouse_posn[0]+self.rect.center[0])*0.7,(-mouse_posn[1]+self.rect.center[1]-0.35*self.rect.height))
    def draw(self,screen:pygame.surface.Surface):
        screen.blit(self.image,self.posn)
        if self.enabled:
            if self.dirn:
                pygame.draw.line(screen,"black",self.prev_mouse_posn,(int(self.rect.x+self.rect.width*0.215),int(self.rect.y+self.rect.height*0.165)),10)
                pygame.draw.line(screen,"black",self.prev_mouse_posn,(int(self.rect.x+self.rect.width*0.833),int(self.rect.y+self.rect.height*0.182)),10)
            else:
                pygame.draw.line(screen,"black",self.prev_mouse_posn,(int(self.rect.x+self.rect.width*0.833),int(self.rect.y+self.rect.height*0.165)),10)
                pygame.draw.line(screen,"black",self.prev_mouse_posn,(int(self.rect.x+self.rect.width*0.215),int(self.rect.y+self.rect.height*0.182)),10)
            for i, point in enumerate(self.traj):
                alpha = int(255- 255 * (i / len(self.traj)))  
                radius = int(5 * ((7-i) / len(self.traj))) + 1
                color = (255, 255, 255, alpha)

                fade_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                pygame.draw.circle(fade_surf, color, (radius, radius), radius)
                screen.blit(fade_surf, (point[0]-radius, point[1]-radius))
    
    def gettraj(self,mouse_posn):
        if mouse_posn[1]+self.bird_size[1] > VIRTUAL_SIZE[1] -200:
            mouse_posn=(mouse_posn[0],self.prev_mouse_posn[1])
        else : self.prev_mouse_posn=mouse_posn
        self.traj.clear()
        vx,vy=((-mouse_posn[0]+self.rect.center[0])*0.7,(-mouse_posn[1]+self.rect.center[1]-0.35*self.rect.height))
        x,y=mouse_posn[0],mouse_posn[1]
        x+=vx * METER *0.07
        y+=vy * METER *0.07
        vy += GRAVITY *0.07
        for i in range(7):
            x+=vx * METER *0.07
            y+=vy * METER *0.07
            vy += GRAVITY *0.07
            self.traj.append((x,y))

    def update(self,mouse_posn, *args, **kwargs):
        self.gettraj(mouse_posn)
        super().update(*args, **kwargs)
        return ((-mouse_posn[0]+self.rect.center[0])*0.7,(-mouse_posn[1]+self.rect.center[1]-0.35*self.rect.height))
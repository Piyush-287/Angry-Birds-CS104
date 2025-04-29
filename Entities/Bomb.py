import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import pygame
import Utils.config
import Utils
import load
from settings import SETTINGS
from Entities.Birds import *
class Bomb(Bird):
    def __init__(self, posn, vel=(0, 0), *groups):
        super().__init__(posn, vel, *groups)
        self.radius=20
        load.RESIZED["BOMB"]=pygame.transform.scale_by(load.SPRITE["BOMB"][0],self.radius*2/load.SPRITE["BOMB"][0].get_size()[0])
        self.damage={
            1:5,
            2:5,
            3:40
        }
        self.Tower=None
        self.visited=None
        self.image=load.RESIZED["BOMB"]
        self.image=self.image
        self.type=3
        self.time=0
        self.activated=False
    def update_animation(self, *args, **kwargs):
        self.index+=1
        if self.index>=100:self.index=0
        if (self.index//10)%3==0:
            self.playing_image=load.SPRITE["BOMB"][1]
        elif (self.index//20)==0:
            self.playing_image=load.SPRITE["BOMB"][2]
        else :self.playing_image=load.SPRITE["BOMB"][0]
    def draw(self, screen):
        if self.activated and self.time<30:
            self.time+=1
            circle_surface = pygame.Surface((self.time*60, self.time*60), pygame.SRCALPHA)
            alpha = max(0, 255 - self.time * 8)
            color = (0, 0, 0, alpha)
            pygame.draw.circle(circle_surface, color, (self.time*30, self.time*30), self.time * 30)
            screen.blit(circle_surface, (self.x - self.time*30, self.y - self.time*30))
        super().draw(screen)
    def update(self, dt, surface, *args, **kwargs):
        if self.activated:
            for i in range(len(self.Tower)):
                for j in range(len(self.Tower[0])):
                    if self.visited[i][j]==False and self.Tower[i][j].type!=0:
                        print(self.x,self.y,self.Tower[i][j].posn,self.time)
                        distance=min(
                            math.dist((self.x-self.Tower[i][j].size[0],self.y-self.Tower[i][j].size[1]),self.Tower[i][j].posn),
                            math.dist((self.x-self.Tower[i][j].size[0],self.y),self.Tower[i][j].posn),
                            math.dist((self.x,self.y-self.Tower[i][j].size[1]),self.Tower[i][j].posn),
                            math.dist((self.x,self.y),self.Tower[i][j].posn)
                        )
                        if distance!=0 and distance < self.time*30:
                            self.visited[i][j]=True 
                            self.Tower[i][j].health -= 10000/(distance)
                            if self.Tower[i][j].health < 0:
                                SOUND[Block_Types[self.Tower[i][j].type]].set_volume(SETTINGS["Volume"]/100)
                                SOUND[Block_Types[self.Tower[i][j].type]].play()
                                self.Tower[i][j].image=None
                                self.Tower[i][j].falling=False
                                self.Tower[i][j].type=0
                            print(self.Tower[i][j].health)
        return super().update(dt, surface, *args, **kwargs)
    def activate(self,screen,Tower,SelfTower):
        self.Tower=Tower
        self.visited=[[False for _ in range(len(self.Tower[0]))] for _ in range(len(self.Tower))]
        self.image=pygame.transform.scale_by(load.SPRITE["BOMB"][5],self.radius*2/load.SPRITE["BOMB"][5].get_size()[0])
        self.activated=True

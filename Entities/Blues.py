import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import pygame
import Utils.config
import Utils
import load
from Entities.Birds import *
class Blues(Bird):
    def __init__(self, posn, vel=(0, 0), *groups):
        super().__init__(posn, vel, *groups)
        self.radius=15
        load.RESIZED["BLUES"]=pygame.transform.scale_by(load.SPRITE["BLUES"][0],self.radius*4/load.SPRITE["BLUES"][0].get_size()[0])
        self.damage={
            1:5,
            2:40,
            3:5
        }
        self.Tower=None
        self.image=load.RESIZED["BLUES"]
        self.playing_image=self.image
        self.type=2
        self.activated=False
        self.mini_blues=[]
        self.time_wait=-1
        self.mini_collided=False
    def update_animation(self, *args, **kwargs):
        self.index+=1
        if self.index>=100:self.index=0
        if (self.index//10)==9:
            self.playing_image=load.SPRITE["BLUES"][3]
        elif (self.index//20)==1:
            self.playing_image=load.SPRITE["BLUES"][2]
        else :self.playing_image=load.SPRITE["BLUES"][0]
    def update(self, dt, surface, *args, **kwargs):
        global STATE,VIRTUAL_SIZE
        if self.activated:
            for blue in self.mini_blues:
                blue.update(dt,surface)
                if blue.y+blue.radius==VIRTUAL_SIZE[1]-BASE_LOC:
                    blue.time_wait+=1
                    if blue.time_wait==1:
                        self.mini_blues.remove(blue)
                else :
                    blue.time_wait=-1
        else:
            return super().update(dt, surface, *args, **kwargs)
    def draw(self, screen):
        if self.activated:
            for blue in self.mini_blues:
                blue.draw(screen)
        else :
            super().draw(screen)
    def activate(self,screen,Tower,SelfTower):
        self.Tower=Tower
        self.activated=True
        self.mini_blues=[
            Blues((self.x,self.y),(self.vx*1.5,self.vy+30)),
            Blues((self.x,self.y),(self.vx*1.5,self.vy)),
            Blues((self.x,self.y),(self.vx*1.5,self.vy-30))
        ]
    def collision_check(self, block):
        if self.activated:
            self.mini_collided = False
            for bird in self.mini_blues:
                collision=bird.collision_check(block)
                if collision != 0 : 
                    self.vx,self.vy=bird.vx*2,bird.vy*2
                if collision == 2 : self.mini_blues.remove(bird)
                if collision == 1 : self.mini_collided=True
            if self.mini_collided : return 1
            if len(self.mini_blues)==0:
                return 2
            return 0
        return super().collision_check(block)

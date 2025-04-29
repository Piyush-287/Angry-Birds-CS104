import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import pygame
import Utils.config
import Utils
import load
from Entities.Birds import *
class Chuck(Bird):
    def __init__(self, posn, vel=(0, 0), *groups):
        super().__init__(posn, vel, *groups)
        self.radius=20
        load.RESIZED["CHUCK"]=pygame.transform.scale_by(load.SPRITE["CHUCK"][0],self.radius*2/load.SPRITE["CHUCK"][0].get_size()[0])
        self.damage={
            1:40,
            2:5,
            3:5
        }
        self.image=load.RESIZED["CHUCK"]
        self.playing_image=self.image
        self.activated=False
        self.type=4
    def update_animation(self, *args, **kwargs):
        self.index+=1
        if self.index>=100:self.index=0
        if (self.index//10)%3==0:
            self.playing_image=load.SPRITE["CHUCK"][1]
        elif (self.index//20)==0:
            self.playing_image=load.SPRITE["CHUCK"][2]
        else :self.playing_image=load.SPRITE["CHUCK"][0]
    def draw(self, screen):
        super().draw(screen)
    def activate(self,screen,Tower,Selftower):
        self.activated=True
        self.vx += min(self.vx,100)
        load.RESIZED["SUPER_CHUCK"]=pygame.transform.scale_by(load.IMAGES["SUPER_CHUCK"],self.radius*2/load.IMAGES["SUPER_CHUCK"].get_size()[0])
        self.image=load.RESIZED["SUPER_CHUCK"]
    def collision_check(self, block):
        if self.activated:
            if (block.posn[1]-self.radius < self.y < block.posn[1] + block.size[1]+self.radius and (self.prev_x<block.posn[0] - self.radius< self.x and self.vx > 0)):
                self.xm=self.x/Utils.config.METER
                self.vx*=Utils.config.FRICTION*0.8
                self.vy*=Utils.config.FRICTION*0.8
                return 1
            if (block.posn[1]-self.radius < self.y < block.posn[1] + block.size[1]+self.radius and (self.prev_x>block.posn[0] + block.size[0] - self.radius> self.x and self.vx < 0)):
                self.xm=self.x/Utils.config.METER
                self.vx*=Utils.config.FRICTION*0.8
                self.vy*=Utils.config.FRICTION*0.8
                return 1
            if (block.posn[0]-self.radius < self.x < block.posn[0] + block.size[0]+self.radius and (self.prev_y<block.posn[1] - self.radius< self.y and self.vy > 0)):
                self.vx*=Utils.config.FRICTION*0.8
                self.vy*=Utils.config.FRICTION*0.8
                return 2
            return 0
        return super().collision_check(block)

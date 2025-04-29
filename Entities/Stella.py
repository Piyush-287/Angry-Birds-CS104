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
class Stella(Bird):
    def __init__(self, posn, vel=(0, 0), *groups):
        super().__init__(posn, vel, *groups)
        self.Tower=None
        self.radius=15
        load.RESIZED["STELLA"]=pygame.transform.scale_by(load.SPRITE["STELLA"][0],self.radius*4/load.SPRITE["STELLA"][0].get_size()[0])
        self.damage={
            1:15,
            2:20,
            3:5,
        }
        self.healed_list=[]
        self.image=load.RESIZED["STELLA"]
        self.playing_image=self.image
        self.type=5
        self.absorbed=0
        self.activated=False
    def update_animation(self, *args, **kwargs):
        self.index+=1
        if self.index>=100:self.index=0
        if (self.index//10)%3==0:
            self.playing_image=load.SPRITE["STELLA"][1]
        elif (self.index//20)==0:
            self.playing_image=load.SPRITE["STELLA"][2]
        else :self.playing_image=load.SPRITE["STELLA"][0]
    def draw(self, screen:pygame.Surface):
        for block in self.healed_list:
            if block[2] >0:
                pygame.draw.rect(screen,"pink",(block[0],block[1]),3)
                block[2] -= 1
        super().draw(screen)
    def activate(self,screen,Tower,SelfTower):
        self.activated=True
        self.Tower=SelfTower
        self.image=pygame.transform.scale_by(load.IMAGES["SUPER_STELLA"],self.radius*4/load.IMAGES["SUPER_STELLA"].get_size()[0])

    def update(self, dt, surface, *args, **kwargs):
        if self.absorbed > 0:
            minm=100
            minm_block=None
            for layer in self.Tower:
                for block in layer:
                    if block.type>0 and 0<block.health<minm:
                        minm_block=block
                        minm=block.health
            if minm_block is not None:
                if self.absorbed < minm_block.health:
                    minm_block.health += self.absorbed
                    self.absorbed=0
                else:
                    self.absorbed-= (100-minm_block.health)
                    minm_block.health=100
                self.healed_list.append([minm_block.posn,minm_block.size,20])

        return super().update(dt, surface, *args, **kwargs)
    def collision_check(self,block):
        if (block.posn[1]-self.radius < self.y < block.posn[1] + block.size[1]+self.radius and (self.prev_x<block.posn[0] - self.radius< self.x and self.vx > 0)):
            self.x=block.posn[0]-2*self.radius
            self.xm=self.x/Utils.config.METER
            if self.activated:
                self.absorbed += abs(self.vx * SCALING_DAMAGE_FACTOR * self.damage[block.type]) * 10
            self.vx*=(-1 *Utils.config.E)
            self.vy*=Utils.config.FRICTION
            return 1
        if (block.posn[1]-self.radius < self.y < block.posn[1] + block.size[1]+self.radius and (self.prev_x>block.posn[0] + block.size[0] - self.radius> self.x and self.vx < 0)):
            self.x=block.posn[0] + block.size[0] + 2*self.radius
            self.xm=self.x/Utils.config.METER
            if self.activated:
                self.absorbed += abs(self.vx * SCALING_DAMAGE_FACTOR * self.damage[block.type]) * 10
            self.vx*=(-1 *Utils.config.E)
            self.vy*=Utils.config.FRICTION
            return 1
        if (block.posn[0]-self.radius < self.x < block.posn[0] + block.size[0]+self.radius and (self.prev_y<block.posn[1] - self.radius< self.y and self.vy > 0)):
            self.y=block.posn[1]-self.radius
            if self.activated:
                self.absorbed += abs(self.vy * SCALING_DAMAGE_FACTOR * self.damage[block.type]) * 2
            self.vx*=Utils.config.FRICTION
            self.vy*=(-1 *Utils.config.E)
            return 2
        return 0

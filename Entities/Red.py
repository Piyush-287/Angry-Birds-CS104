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
class Red(Bird):
    def __init__(self, posn, vel=(0, 0), *groups):
        super().__init__(posn, vel, *groups)
        self.radius=20
        load.RESIZED["RED"]=pygame.transform.scale_by(load.SPRITE["RED"][0],self.radius*2/load.SPRITE["RED"][0].get_size()[0])
        self.damage={
            1:15,
            2:15,
            3:15
        }
        self.image=load.RESIZED["RED"]
        self.playing_image=self.image
        self.activated=False
        self.type=1
    def update_animation(self, *args, **kwargs):
        self.index+=1
        if self.index>=100:self.index=0
        if (self.index//10)%3==0:
            self.playing_image=load.SPRITE["RED"][1]
        elif (self.index//20)==0:
            self.playing_image=load.SPRITE["RED"][2]
        else :self.playing_image=load.SPRITE["RED"][0]
    def draw(self, screen):
        super().draw(screen)
    def activate(self,screen,Tower,selfTower):
        self.damage={
            1:30,2:30,3:30
        }
        self.Tower=Tower
        self.activated=True
        load.RESIZED["SUPER_RED"]=pygame.transform.scale_by(load.IMAGES["SUPER_RED"],self.radius*4/load.IMAGES["SUPER_RED"].get_size()[0])
        self.image=load.RESIZED["SUPER_RED"]
    def collision_check(self, block):
        def crush_tower():
            visited=[[False for _ in range(len(self.Tower[0]))] for _ in range(len(self.Tower))]
            q=[[x,y,damage]]
            dirn=[[0,1],[0,-1],[1,0],[-1,0]]
            while q:
                for dir in dirn:
                    xn,yn=q[0][0]+dir[0],q[0][1]+dir[1]
                    if 0 <= xn < len(self.Tower) and 0 <= yn < len(self.Tower[0]) and visited[xn][yn]==False and self.Tower[xn][yn].type!=0:
                        self.Tower[xn][yn].health-=(q[0][2]*0.8)
                        q.append([xn,yn,q[0][2]*0.6])
                        if self.Tower[xn][yn].health <0 :
                            SOUND[Block_Types[self.Tower[xn][yn].type]].set_volume(SETTINGS["Volume"]/100)
                            SOUND[Block_Types[self.Tower[xn][yn].type]].play()
                            self.Tower[xn][yn]=Block(self.Tower[i][j].posn,self.Tower[i][j].size,0)
                        print(self.Tower[xn][yn].health)
                        visited[xn][yn]=True
                print(q)
                q=q[1:]

        if self.activated:
            x,y=None,None
            for i in range(len(self.Tower)):
                for j in range(len(self.Tower[0])):
                    if self.Tower[i][j].posn==block.posn:
                        x,y=i,j
            if (block.posn[1]-self.radius < self.y < block.posn[1] + block.size[1]+self.radius and (self.prev_x<block.posn[0] - self.radius< self.x and self.vx > 0)):
                self.x=block.posn[0]-2*self.radius
                self.xm=self.x/Utils.config.METER
                self.vx*=(-1 *Utils.config.E)
                self.vy*=Utils.config.FRICTION
                damage= abs(self.vx) * self.damage[self.type] * SCALING_DAMAGE_FACTOR /Utils.config.E
                crush_tower()
                return 1
            if (block.posn[1]-self.radius < self.y < block.posn[1] + block.size[1]+self.radius and (self.prev_x>block.posn[0] + block.size[0] - self.radius> self.x and self.vx < 0)):
                self.x=block.posn[0] + block.size[0] + 2*self.radius
                self.xm=self.x/Utils.config.METER
                self.vx*=(-1 *Utils.config.E)
                self.vy*=Utils.config.FRICTION
                damage= abs(self.vx) * self.damage[self.type] * SCALING_DAMAGE_FACTOR /Utils.config.E
                crush_tower()
                return 1
            if (block.posn[0]-self.radius < self.x < block.posn[0] + block.size[0]+self.radius and (self.prev_y<block.posn[1] - self.radius< self.y and self.vy > 0)):
                self.y=block.posn[1]-self.radius
                self.vx*=Utils.config.FRICTION
                self.vy*=(-1 *Utils.config.E)
                damage= abs(self.vy) * self.damage[self.type] * SCALING_DAMAGE_FACTOR /Utils.config.E
                crush_tower()
                return 2
            return 0
        return super().collision_check(block)

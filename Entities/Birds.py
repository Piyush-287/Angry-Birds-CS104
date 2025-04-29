import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import pygame
import Physics.config
import Physics
import load
import math
from settings import SETTINGS
BASE_LOC=200
SOUND=load.load_sound()
SCALING_DAMAGE_FACTOR=0.02
VIRTUAL_SIZE=(1920,1080)
BIRDS={
    1:"RED",
    2:"BLUES",
    3:"BOMB",
    4:"CHUCK",
    5:"STELLA"
}
class Bird(pygame.sprite.Sprite):
    def __init__(self,posn,vel=(0,0),*groups):
        self.x,self.y=posn[0],posn[1]
        self.vx,self.vy=vel[0],vel[1]
        self.index=0
        self.xm,self.ym=self.x/Physics.config.METER,self.y/Physics.config.METER
        self.prev_x,self.prev_y=self.xm,self.ym
        self.radius=20
        self.type=0
        self.damage={
            1:10,
            2:10,
            3:10
        }
        self.image=pygame.Surface((20,20))
        self.image.fill("red")
        self.playing_image=self.image
        self.rect=self.image.get_rect()
        super().__init__(*groups)
    
    def update(self, dt, surface: pygame.surface.Surface, *args, **kwargs):
        self.prev_x,self.prev_y=self.x,self.y
        surface_width, surface_height = surface.get_size()
        bird_width, bird_height = self.image.get_size()
        velocity_threshold = 0.1

        # Gravity only if not settled
        self.vy += Physics.config.GRAVITY * dt

        # Integrate motion
        self.xm += self.vx * dt
        self.ym += self.vy * dt

        # Convert back to pixels
        self.y = self.ym * Physics.config.METER
        self.x = self.xm * Physics.config.METER
        # === Collision with floor ===
        if self.y + self.radius > surface_height-BASE_LOC:
            self.y = surface_height -BASE_LOC - self.radius
            self.ym = self.y / Physics.config.METER
            if abs(self.vy) < velocity_threshold:
                self.vy = 0
                self.vx = 0
                return True
            else:
                self.vy *= -1 * Physics.config.E
                self.vx *= 0.5
        return super().update(*args, **kwargs)
    def draw(self, screen: pygame.surface.Surface):
        angle = math.degrees(math.atan2(-self.vy, self.vx)) 
        if self.vx < 0:
            rotated_image = pygame.transform.rotate(self.image, 180-angle)
            rotated_image = pygame.transform.flip(rotated_image, True, False)
        else:
            rotated_image = pygame.transform.rotate(self.image,angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect)
    
    def collision_check(self,block):
        if (block.posn[1]-self.radius < self.y < block.posn[1] + block.size[1]+self.radius and (self.prev_x<block.posn[0] - self.radius< self.x and self.vx > 0)):
            self.x=block.posn[0]-2*self.radius
            self.xm=self.x/Physics.config.METER
            self.vx*=(-1 *Physics.config.E)
            self.vy*=Physics.config.FRICTION
            return 1
        if (block.posn[1]-self.radius < self.y < block.posn[1] + block.size[1]+self.radius and (self.prev_x>block.posn[0] + block.size[0] - self.radius> self.x and self.vx < 0)):
            self.x=block.posn[0] + block.size[0] + 2*self.radius
            self.xm=self.x/Physics.config.METER
            self.vx*=(-1 *Physics.config.E)
            self.vy*=Physics.config.FRICTION
            return 1
        if (block.posn[0]-self.radius < self.x < block.posn[0] + block.size[0]+self.radius and (self.prev_y<block.posn[1] - self.radius< self.y and self.vy > 0)):
            self.y=block.posn[1]-self.radius
            self.vx*=Physics.config.FRICTION
            self.vy*=(-1 *Physics.config.E)
            return 2
        return 0
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
                self.xm=self.x/Physics.config.METER
                self.vx*=(-1 *Physics.config.E)
                self.vy*=Physics.config.FRICTION
                damage= abs(self.vx) * self.damage[self.type] * SCALING_DAMAGE_FACTOR /Physics.config.E
                crush_tower()
                return 1
            if (block.posn[1]-self.radius < self.y < block.posn[1] + block.size[1]+self.radius and (self.prev_x>block.posn[0] + block.size[0] - self.radius> self.x and self.vx < 0)):
                self.x=block.posn[0] + block.size[0] + 2*self.radius
                self.xm=self.x/Physics.config.METER
                self.vx*=(-1 *Physics.config.E)
                self.vy*=Physics.config.FRICTION
                damage= abs(self.vx) * self.damage[self.type] * SCALING_DAMAGE_FACTOR /Physics.config.E
                crush_tower()
                return 1
            if (block.posn[0]-self.radius < self.x < block.posn[0] + block.size[0]+self.radius and (self.prev_y<block.posn[1] - self.radius< self.y and self.vy > 0)):
                self.y=block.posn[1]-self.radius
                self.vx*=Physics.config.FRICTION
                self.vy*=(-1 *Physics.config.E)
                damage= abs(self.vy) * self.damage[self.type] * SCALING_DAMAGE_FACTOR /Physics.config.E
                crush_tower()
                return 2
            return 0
        return super().collision_check(block)
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
                self.xm=self.x/Physics.config.METER
                self.vx*=Physics.config.FRICTION*0.8
                self.vy*=Physics.config.FRICTION*0.8
                return 1
            if (block.posn[1]-self.radius < self.y < block.posn[1] + block.size[1]+self.radius and (self.prev_x>block.posn[0] + block.size[0] - self.radius> self.x and self.vx < 0)):
                self.xm=self.x/Physics.config.METER
                self.vx*=Physics.config.FRICTION*0.8
                self.vy*=Physics.config.FRICTION*0.8
                return 1
            if (block.posn[0]-self.radius < self.x < block.posn[0] + block.size[0]+self.radius and (self.prev_y<block.posn[1] - self.radius< self.y and self.vy > 0)):
                self.vx*=Physics.config.FRICTION*0.8
                self.vy*=Physics.config.FRICTION*0.8
                return 2
            return 0
        return super().collision_check(block)
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
            self.xm=self.x/Physics.config.METER
            if self.activated:
                self.absorbed += abs(self.vx * SCALING_DAMAGE_FACTOR * self.damage[block.type]) * 10
            self.vx*=(-1 *Physics.config.E)
            self.vy*=Physics.config.FRICTION
            return 1
        if (block.posn[1]-self.radius < self.y < block.posn[1] + block.size[1]+self.radius and (self.prev_x>block.posn[0] + block.size[0] - self.radius> self.x and self.vx < 0)):
            self.x=block.posn[0] + block.size[0] + 2*self.radius
            self.xm=self.x/Physics.config.METER
            if self.activated:
                self.absorbed += abs(self.vx * SCALING_DAMAGE_FACTOR * self.damage[block.type]) * 10
            self.vx*=(-1 *Physics.config.E)
            self.vy*=Physics.config.FRICTION
            return 1
        if (block.posn[0]-self.radius < self.x < block.posn[0] + block.size[0]+self.radius and (self.prev_y<block.posn[1] - self.radius< self.y and self.vy > 0)):
            self.y=block.posn[1]-self.radius
            if self.activated:
                self.absorbed += abs(self.vy * SCALING_DAMAGE_FACTOR * self.damage[block.type]) * 2
            self.vx*=Physics.config.FRICTION
            self.vy*=(-1 *Physics.config.E)
            return 2
        return 0
Block_Types={
    1: "WOOD",
    2: "GLASS",
    3: "STONE"
}
DAMAGE_FALLING={
    1:1.5,
    2:2.5,
    3:0.8
}
class Block(pygame.sprite.Sprite):
    def __init__(self,posn,size,type,*groups):
        self.health=100
        self.posn=list(posn)
        self.target_posn = list(posn)
        self.falling = False
        self.gravity = Physics.config.GRAVITY * 100
        self.velocity = 0
        self.size=size
        self.type=type
        if self.type!=0:
            load.RESIZED[f"{Block_Types[self.type]}_4"]=pygame.transform.scale_by(load.IMAGES[f"{Block_Types[self.type]}_4"],self.size[0]/load.IMAGES[f"{Block_Types[self.type]}_4"].get_size()[0])
            self.image=load.RESIZED[f"{Block_Types[self.type]}_4"]
        else:
            self.image=None
        super().__init__(*groups)
    
    def update(self,dt, *args, **kwargs):
        if self.falling:
            self.velocity += self.gravity * dt
            self.posn[1] += self.velocity * dt

            if self.posn[1] >= self.target_posn[1]:
                self.posn[1] = self.target_posn[1]
                self.falling = False
                self.health-=self.velocity/100 * DAMAGE_FALLING[self.type]
                self.velocity = 0
                if self.health < 0 :
                    SOUND[Block_Types[self.type]].set_volume(SETTINGS["Volume"]/100)
                    SOUND[Block_Types[self.type]].play()
                    return False
        if self.health < 0 :
            return False
        if self.type!=0 and self.health >= 0:
            load.RESIZED[f"{Block_Types[self.type]}_{min(max(int((self.health-1)//20),0),4)}"]=pygame.transform.scale_by(load.IMAGES[f"{Block_Types[self.type]}_{min(max(int((self.health-1)//20),0),4)}"],self.size[0]/load.IMAGES[f"{Block_Types[self.type]}_{min(max(int((self.health-1)//20),0),4)}"].get_size()[0])
            self.image=load.RESIZED[f"{Block_Types[self.type]}_{min(max(int((self.health-1)//20),0),4)}"]
        else:
            self.image=None
            self.falling=False
            self.type=0
        return True
    
    def update_collision(self,bird:Bird):
        if self.type!=0:
            colnno=bird.collision_check(self)
            if self.type!=0 and colnno!=0:
                self.health -= abs(bird.vx if colnno==1 else bird.vy) * bird.damage[self.type] * SCALING_DAMAGE_FACTOR /Physics.config.E
                print(self.health)
                if self.health < 0:
                    return colnno,True
                return colnno,False
        return False,False
    def draw(self,screen:pygame.Surface):
        if self.type!=0 :screen.blit(self.image,self.posn)

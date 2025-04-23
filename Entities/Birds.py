import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import pygame
import Physics.config
import Utils.colors
import Physics
import load
import math
BASE_LOC=200
SCALING_DAMAGE_FACTOR=0.02

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
        self.image.fill(Utils.colors.COLORS["red"])
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

        # === Collision with right wall ===
        if self.x + self.radius > surface_width:
            self.x = surface_width - bird_width
            self.xm = self.x / Physics.config.METER
            if abs(self.vx) < velocity_threshold:
                self.vx = 0
                return True
            else:
                self.vx *= -1 * Physics.config.E
                self.vy *= Physics.config.FRICTION

        # === Collision with left wall ===
        if self.x < 0:
            self.x = 0
            self.xm = self.x / Physics.config.METER
            if abs(self.vx) < velocity_threshold:
                self.vx = 0
                return True
            else:
                self.vx *= -1 * Physics.config.E
                self.vy *= Physics.config.FRICTION

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
        load.RESIZED["SUPER_RED"]=pygame.transform.scale_by(load.IMAGES["SUPER_RED"],self.radius*4/load.IMAGES["SUPER_RED"].get_size()[0])
        self.image=load.RESIZED["SUPER_RED"]
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
        self.image=load.RESIZED["BLUES"]
        self.playing_image=self.image
        self.type=2
        self.activated=False
        self.mini_blues=[]
    def update_animation(self, *args, **kwargs):
        self.index+=1
        if self.index>=100:self.index=0
        if (self.index//10)==9:
            self.playing_image=load.SPRITE["BLUES"][3]
        elif (self.index//20)==1:
            self.playing_image=load.SPRITE["BLUES"][2]
        else :self.playing_image=load.SPRITE["BLUES"][0]
    def update(self, dt, surface, *args, **kwargs):
        if self.activated:
            for blue in self.mini_blues:
                blue.update(dt,surface)
        return super().update(dt, surface, *args, **kwargs)
    def draw(self, screen):
        if self.activated:
            for blue in self.mini_blues:
                blue.draw(screen)
        super().draw(screen)
    def activate(self,screen,Tower,SelfTower):
        self.activated=True
        self.mini_blues=[
            Blues((self.x,self.y),(self.vx,self.vy+10)),
            Blues((self.x,self.y),(self.vx,self.vy-10))
        ]
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
        if self.activated and self.time<15:
            self.time+=1
            circle_surface = pygame.Surface((self.time*30, self.time*30), pygame.SRCALPHA)
            alpha = max(0, 255 - self.time * 10)
            color = (0, 0, 0, alpha)
            pygame.draw.circle(circle_surface, color, (self.time*15, self.time*15), self.time * 15)
            screen.blit(circle_surface, (self.x - self.time*15, self.y - self.time*15))
        super().draw(screen)
    def update(self, dt, surface, *args, **kwargs):
        if self.activated:
            for i in range(len(self.Tower)):
                for j in range(len(self.Tower[0])):
                    if not self.visited[i][j]:
                        self.visited[i][j]=True 
                        distance=math.dist((self.x,self.y),self.Tower[i][j].posn)
                        if distance!=0 :self.Tower[i][j].health -= 2500000/(distance**2)
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
        self.vx += min(self.vx,100)
        load.RESIZED["SUPER_CHUCK"]=pygame.transform.scale_by(load.IMAGES["SUPER_CHUCK"],self.radius*2/load.IMAGES["SUPER_CHUCK"].get_size()[0])
        self.image=load.RESIZED["SUPER_CHUCK"]
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
                self.absorbed += abs(self.vx * SCALING_DAMAGE_FACTOR * self.damage[block.type])
            self.vx*=(-1 *Physics.config.E)
            self.vy*=Physics.config.FRICTION
            return 1
        if (block.posn[1]-self.radius < self.y < block.posn[1] + block.size[1]+self.radius and (self.prev_x>block.posn[0] + block.size[0] - self.radius> self.x and self.vx < 0)):
            self.x=block.posn[0] + block.size[0] + 2*self.radius
            self.xm=self.x/Physics.config.METER
            if self.activated:
                self.absorbed += abs(self.vx * SCALING_DAMAGE_FACTOR * self.damage[block.type])
            self.vx*=(-1 *Physics.config.E)
            self.vy*=Physics.config.FRICTION
            return 1
        if (block.posn[0]-self.radius < self.x < block.posn[0] + block.size[0]+self.radius and (self.prev_y<block.posn[1] - self.radius< self.y and self.vy > 0)):
            self.y=block.posn[1]-self.radius
            if self.activated:
                self.absorbed += abs(self.vy * SCALING_DAMAGE_FACTOR * self.damage[block.type])
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
            load.RESIZED[Block_Types[self.type]]=pygame.transform.scale_by(load.IMAGES[Block_Types[self.type]],self.size[0]/load.IMAGES[Block_Types[self.type]].get_size()[0])
            self.image=load.RESIZED[Block_Types[self.type]]
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
                    return False
        return True
    
    def update_collision(self,bird:Bird):
        if self.type!=0:
            colnno=bird.collision_check(self)
            if self.type!=0 and colnno!=0:
                self.health -= abs(bird.vx if colnno==1 else bird.vy) * bird.damage[self.type] * SCALING_DAMAGE_FACTOR /Physics.config.E
                if self.health < 0:
                    return colnno,True
                return colnno,False
        return False,False
    def draw(self,screen:pygame.Surface):
        if self.type!=0 :screen.blit(self.image,self.posn)

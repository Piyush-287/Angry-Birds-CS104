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
        self.x = self.xm * Physics.config.METER
        self.y = self.ym * Physics.config.METER

        # === Collision with right wall ===
        if self.x + self.radius > surface_width:
            self.x = surface_width - bird_width
            self.xm = self.x / Physics.config.METER
            if abs(self.vx) < velocity_threshold:
                self.vx = 0
                return True
            else:
                self.vx *= -1 * Physics.config.E

        # === Collision with left wall ===
        if self.x < 0:
            self.x = 0
            self.xm = self.x / Physics.config.METER
            if abs(self.vx) < velocity_threshold:
                self.vx = 0
                return True
            else:
                self.vx *= -1 * Physics.config.E

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
        if (block.posn[1] < self.y < block.posn[1] + block.size[1] and (self.prev_x<block.posn[0] - self.radius< self.x and self.vx > 0)):
            return 1
        if (block.posn[1] < self.y < block.posn[1] + block.size[1] and (self.prev_x>block.posn[0] + block.size[0] - self.radius> self.x and self.vx < 0)):
            return 1
        if (block.posn[0] < self.x < block.posn[0] + block.size[0] and (self.prev_y<block.posn[1] - self.radius< self.y and self.vy > 0)):
            return 2
        return 0
        

class Red(Bird):
    def __init__(self, posn, vel=(0, 0), *groups):
        super().__init__(posn, vel, *groups)
        self.radius=20
        load.RESIZED["RED"]=pygame.transform.scale_by(load.SPRITE["RED"][0],self.radius*2/load.SPRITE["RED"][0].get_size()[0])
        self.damage={
            1:20,
            2:20,
            3:20
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
class Blues(Bird):
    def __init__(self, posn, vel=(0, 0), *groups):
        super().__init__(posn, vel, *groups)
        self.radius=20
        load.RESIZED["BLUES"]=pygame.transform.scale_by(load.SPRITE["BLUES"][0],self.radius*2/load.SPRITE["BLUES"][0].get_size()[0])
        self.damage={
            1:5,
            2:40,
            3:5
        }
        self.image=load.RESIZED["BLUES"]
        self.playing_image=self.image
        self.type=2
    def update_animation(self, *args, **kwargs):
        self.index+=1
        if self.index>=100:self.index=0
        if (self.index//10)==9:
            self.playing_image=load.SPRITE["BLUES"][3]
        elif (self.index//20)==1:
            self.playing_image=load.SPRITE["BLUES"][2]
        else :self.playing_image=load.SPRITE["BLUES"][0]
    def draw(self, screen):
        super().draw(screen)
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
        self.image=load.RESIZED["BOMB"]
        self.image=self.image
        self.type=3
    def update_animation(self, *args, **kwargs):
        self.index+=1
        if self.index>=100:self.index=0
        if (self.index//10)%3==0:
            self.playing_image=load.SPRITE["BOMB"][1]
        elif (self.index//20)==0:
            self.playing_image=load.SPRITE["BOMB"][2]
        else :self.playing_image=load.SPRITE["BOMB"][0]
    def draw(self, screen):
        super().draw(screen)
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

class Stella(Bird):
    def __init__(self, posn, vel=(0, 0), *groups):
        super().__init__(posn, vel, *groups)
        self.radius=20
        load.RESIZED["STELLA"]=pygame.transform.scale_by(load.SPRITE["STELLA"][0],self.radius*2/load.SPRITE["STELLA"][0].get_size()[0])
        self.damage={
            1:20,
            2:25,
            3:10,
        }
        self.image=load.RESIZED["STELLA"]
        self.playing_image=self.image
        self.type=5
    def update_animation(self, *args, **kwargs):
        self.index+=1
        if self.index>=100:self.index=0
        if (self.index//10)%3==0:
            self.playing_image=load.SPRITE["STELLA"][1]
        elif (self.index//20)==0:
            self.playing_image=load.SPRITE["STELLA"][2]
        else :self.playing_image=load.SPRITE["STELLA"][0]
    def draw(self, screen):
        super().draw(screen)

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
                print(self.health)
        return True
    
    def update_collision(self,bird:Bird):
        colnno=bird.collision_check(self)
        if self.type!=0 and colnno!=0:
            self.health -= abs(bird.vx if colnno==1 else bird.vy) * bird.damage[self.type] * 0.03
            print(self.health)
            # to update sprite as per health 
            if self.health < 0:
                return True,True
            return True,False
        return False,False
    def draw(self,screen:pygame.Surface):
        if self.type!=0 :screen.blit(self.image,self.posn)

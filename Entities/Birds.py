import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import pygame
import Utils.config
import Utils
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
        self.xm,self.ym=self.x/Utils.config.METER,self.y/Utils.config.METER
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
        self.vy += Utils.config.GRAVITY * dt

        # Integrate motion
        self.xm += self.vx * dt
        self.ym += self.vy * dt

        # Convert back to pixels
        self.y = self.ym * Utils.config.METER
        self.x = self.xm * Utils.config.METER
        # === Collision with floor ===
        if self.y + self.radius > surface_height-BASE_LOC:
            self.y = surface_height -BASE_LOC - self.radius
            self.ym = self.y / Utils.config.METER
            if abs(self.vy) < velocity_threshold:
                self.vy = 0
                self.vx = 0
                return True
            else:
                self.vy *= -1 * Utils.config.E
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
            self.xm=self.x/Utils.config.METER
            self.vx*=(-1 *Utils.config.E)
            self.vy*=Utils.config.FRICTION
            return 1
        if (block.posn[1]-self.radius < self.y < block.posn[1] + block.size[1]+self.radius and (self.prev_x>block.posn[0] + block.size[0] - self.radius> self.x and self.vx < 0)):
            self.x=block.posn[0] + block.size[0] + 2*self.radius
            self.xm=self.x/Utils.config.METER
            self.vx*=(-1 *Utils.config.E)
            self.vy*=Utils.config.FRICTION
            return 1
        if (block.posn[0]-self.radius < self.x < block.posn[0] + block.size[0]+self.radius and (self.prev_y<block.posn[1] - self.radius< self.y and self.vy > 0)):
            self.y=block.posn[1]-self.radius
            self.vx*=Utils.config.FRICTION
            self.vy*=(-1 *Utils.config.E)
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
        self.gravity = Utils.config.GRAVITY * 100
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
                self.health -= abs(bird.vx if colnno==1 else bird.vy) * bird.damage[self.type] * SCALING_DAMAGE_FACTOR /Utils.config.E
                print(self.health)
                if self.health < 0:
                    return colnno,True
                return colnno,False
        return False,False
    def draw(self,screen:pygame.Surface):
        if self.type!=0 :screen.blit(self.image,self.posn)

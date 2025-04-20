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
        self.xm,self.ym=self.x/Physics.config.METER,self.y/Physics.config.METER
        self.prev_x,self.prev_y=self.xm,self.ym
        self.radius=20
        self.damage={
            1:10,
            2:10,
            3:10
        }
        self.image=pygame.Surface((20,20))
        self.image.fill(Utils.colors.COLORS["red"])
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
    def draw(self, screen):
        super().draw(screen)

Block_Types={
    1: "WOOD",
    2: "GLASS",
    3: "STONE"
}

class Block(pygame.sprite.Sprite):
    def __init__(self,posn,size,type,*groups):
        self.health=100
        self.posn=posn
        self.size=size
        self.type=type
        if self.type!=0:
            load.RESIZED[Block_Types[self.type]]=pygame.transform.scale_by(load.IMAGES[Block_Types[self.type]],self.size[0]/load.IMAGES[Block_Types[self.type]].get_size()[0])
            self.image=load.RESIZED[Block_Types[self.type]]
        else:
            self.image=None
        super().__init__(*groups)
    
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

            

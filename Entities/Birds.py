import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import pygame
import Physics.config
import Utils.colors
import Physics
class Bird(pygame.sprite.Sprite):
    def __init__(self,posn,type,vel=(0,0),*groups):
        self.x,self.y=posn[0],posn[1]
        self.vx,self.vy=vel[0],vel[1]
        self.xm,self.ym=self.x/Physics.config.METER,self.y/Physics.config.METER
        match type:
            case 1:
                self.image=pygame.Surface((20,20))
                self.image.fill(Utils.colors.COLORS["red"])
                self.rect=self.image.get_rect()
        super().__init__(*groups)
    
    def update(self, dt, surface: pygame.surface.Surface, *args, **kwargs):
        surface_width, surface_height = surface.get_size()
        bird_width, bird_height = self.image.get_size()
        velocity_threshold = 2  # px/s — tweak this as needed

        # Gravity only if not settled
        self.vy += Physics.config.GRAVITY * dt

        # Integrate motion
        self.xm += self.vx * dt
        self.ym += self.vy * dt

        # Convert back to pixels
        self.x = self.xm * Physics.config.METER
        self.y = self.ym * Physics.config.METER

        # === Collision with right wall ===
        if self.x + bird_width > surface_width:
            self.x = surface_width - bird_width
            self.xm = self.x / Physics.config.METER
            if abs(self.vx) < velocity_threshold:
                self.vx = 0
            else:
                self.vx *= -1 * Physics.config.E

        # === Collision with left wall ===
        if self.x < 0:
            self.x = 0
            self.xm = self.x / Physics.config.METER
            if abs(self.vx) < velocity_threshold:
                self.vx = 0
            else:
                self.vx *= -1 * Physics.config.E

        # === Collision with floor ===
        if self.y + bird_height > surface_height:
            self.y = surface_height - bird_height
            self.ym = self.y / Physics.config.METER
            if abs(self.vy) < velocity_threshold:
                self.vy = 0
            else:
                self.vy *= -1 * Physics.config.E

        # === Collision with ceiling ===
        # if self.y < 0:
        #     self.y = 0
        #     self.ym = self.y / Physics.config.METER
        #     if abs(self.vy) < velocity_threshold:
        #         self.vy = 0
        #     else:
        #         self.vy *= -1 * Physics.config.E

        return super().update(*args, **kwargs)

    
    def draw(self,screen:pygame.surface.Surface):
        screen.blit(self.image,(self.x,self.y))
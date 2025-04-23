import pygame
class Button:
    def __init__(self,posn_pct,size, image, screen, on_click,redraw_callback=None):
        """
        posn_pct: Tuple of (x_percentage, y_percentage) e.g. (0.5, 0.3)
        image: pygame.Surface (pre-loaded image)
        screen: pygame display Surface (to get size for positioning)
        on_click: Function to call when button is clicked
        """
        self.posn_pct = posn_pct
        self.original_image = image
        self.screen = screen
        self.on_click = on_click
        self.size=size
        self.original_size=size
        self.scale_up=size *1.05
        self.redraw_callback = redraw_callback

        # Get screen dimensions
        screen_width, screen_height = self.screen.get_size()

        # Calculate position in pixels
        self.x = int(self.posn_pct[0] * screen_width)
        self.y = int(self.posn_pct[1] * screen_height)
        self.original_image_size=self.original_image.get_size()
        self.width=int(self.size  * screen_width)
        self.height=int(self.size * self.original_image_size[1]/self.original_image_size[0] * screen_width)

        # Get image rect and center it at (x, y)
        self.image=pygame.transform.smoothscale(self.original_image,(self.width,self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self):
        # Draw the image
        self.screen.blit(self.image, self.rect)

    def update(self,screen):
        self.screen=screen
        screen_width, screen_height = screen.get_size()
        self.x = int(self.posn_pct[0] * screen_width)
        self.y = int(self.posn_pct[1] * screen_height)
        self.width=int(self.size  * screen_width)
        self.height=int(self.size * self.original_image_size[1]/self.original_image_size[0] * screen_width)
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update_center(self,screen):
        self.screen=screen
        screen_width, screen_height = screen.get_size()
        self.width=int(self.size  * screen_width)
        self.height=int(self.size * self.original_image_size[1]/self.original_image_size[0] * screen_width)
        center_new=(self.x+self.width//2, self.y+self.height//2)
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))
        self.rect = self.image.get_rect(center=center_new)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.animate_click()
            return True,self.on_click()
        return False,None

    def animate_click(self):
        clock = pygame.time.Clock()
        frames = 5
        grow_size = self.scale_up
        grow_step = (grow_size - self.size) / (frames // 2)

        for _ in range(frames // 2):
            self.size += grow_step
            self.update_center(self.screen)
            if self.redraw_callback: self.redraw_callback()  # 🔥 redraw screen
            self.draw()
            pygame.display.flip()
            clock.tick(60)

        for _ in range(frames // 2):
            self.size -= grow_step
            self.update_center(self.screen)
            if self.redraw_callback: self.redraw_callback()
            self.draw()
            pygame.display.flip()
            clock.tick(60)

        self.size = self.original_size
        self.update_center(self.screen)
        if self.redraw_callback: self.redraw_callback()
        self.draw()
        pygame.display.flip()

import pygame
import sys
import Scenes.Game.background.background as Background
import load 
import Entities.Birds as Birds

pygame.init()
screen = pygame.display.set_mode((2000, 1200), pygame.RESIZABLE)
clock = pygame.time.Clock()

# World surface to draw everything
world_size = pygame.Vector2(2000, 1200)
world_surface = pygame.Surface((int(world_size.x), int(world_size.y)))
load.load_images()

# Camera settings
camera_offset = pygame.Vector2(0, 0)
target_offset = pygame.Vector2(0, 0)
zoom = 1.0
target_zoom = 1.0

# Bird
bird = Birds.Bird((100, 1000), 1, (10, -100))

# Drag
dragging = False
last_mouse_pos = pygame.Vector2()

# Initial Zoom: Fit world inside screen
def calculate_min_zoom():
    sw, sh = screen.get_size()
    return min(sw / world_size.x, sh / world_size.y)

min_zoom = calculate_min_zoom()
zoom = target_zoom = min_zoom  # Start fully zoomed out to fit
max_zoom = 3.0

def clamp_camera():
    screen_w, screen_h = screen.get_size()
    visible_width = screen_w / zoom
    visible_height = screen_h / zoom

    # Clamp offset so the camera doesn’t go out of bounds
    target_offset.x = max(0, min(world_size.x - visible_width, target_offset.x))
    target_offset.y = max(0, min(world_size.y - visible_height, target_offset.y))

def draw_world(surface):
    surface.fill((30, 30, 30))
    
    # Draw background (no scaling or offset)
    Background.generate_background(surface)  # This should be done first to avoid any scaling issues
    
    # Draw game objects (this includes birds, blocks, etc.)
    for x in range(0, int(world_size.x), 100):
        pygame.draw.line(surface, (50, 50, 50), (x, 0), (x, world_size.y))
    for y in range(0, int(world_size.y), 100):
        pygame.draw.line(surface, (50, 50, 50), (0, y), (world_size.x, y))
    for i in range(10):
        pygame.draw.rect(surface, (100 + i * 15, 50, 200), pygame.Rect(100 + i * 120, 200 + i * 50, 80, 80))
    bird.draw(surface)

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            min_zoom = calculate_min_zoom()
            target_zoom = max(min_zoom, min(target_zoom, max_zoom))  # Re-clamp zoom on resize

        elif event.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            before_zoom = pygame.Vector2(mx, my) / zoom + camera_offset

            target_zoom += event.y * 0.1
            target_zoom = max(min_zoom, min(target_zoom, max_zoom))

            after_zoom = pygame.Vector2(mx, my) / target_zoom + camera_offset
            target_offset += before_zoom - after_zoom

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                dragging = True
                last_mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                dragging = False

    if dragging:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        delta = (mouse_pos - last_mouse_pos) / zoom
        target_offset -= delta
        last_mouse_pos = mouse_pos

    # Smooth movement
    zoom += (target_zoom - zoom) * 0.1
    clamp_camera()
    camera_offset += (target_offset - camera_offset) * 0.1

    bird.update(dt, world_surface)
    draw_world(world_surface)

    # Zoomed world surface
    zoomed_size = (int(world_size.x * zoom), int(world_size.y * zoom))
    zoomed_surface = pygame.transform.smoothscale(world_surface, zoomed_size)

    # Top-left corner of what to draw
    top_left = -camera_offset * zoom
    screen.fill((0, 0, 0))
    screen.blit(zoomed_surface, top_left)
    pygame.display.flip()

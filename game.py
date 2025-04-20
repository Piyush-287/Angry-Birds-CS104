import random 
import load
from Scenes.Game.background.background import *
from Physics.config import * 
from Entities.slingshot import * 
from Entities.Birds import * 
from PlayerData import *

BASE_LOC=200
def display_unzoomed(screen,Surface):
    scale_x = screen_width / VIRTUAL_SIZE[0]
    scale_y = screen_height / VIRTUAL_SIZE[1]
    scale = max(scale_x, scale_y)

    scaled_size = (int(VIRTUAL_SIZE[0] * scale), int(VIRTUAL_SIZE[1] * scale))
    scaled_surface = pygame.transform.smoothscale(Surface, scaled_size)
    crop_x = (scaled_size[0] - screen_width) // 2
    crop_y = scaled_size[1] - screen_height 
    screen.blit(scaled_surface, (-crop_x, -crop_y))
def screen_to_virtual(mouse_pos, screen_size, virtual_size):
    screen_w, screen_h = screen_size
    virtual_w, virtual_h = virtual_size

    scale_x = screen_w / virtual_w
    scale_y = screen_h / virtual_h
    scale = max(scale_x, scale_y)

    scaled_w = virtual_w * scale
    scaled_h = virtual_h * scale

    crop_x = (scaled_w - screen_w) / 2
    crop_y = scaled_h - screen_h  # top cropping only

    virtual_x = (mouse_pos[0] + crop_x) / scale
    virtual_y = (mouse_pos[1] + crop_y) / scale
    return (int(virtual_x), int(virtual_y))          
def initialise_tower(Design:list,size:tuple,surface:pygame.Surface,location,leftside):
    per_tile_area=min(100,(location[1]-location[0])/size[0])
    Tower=list()
    for j in range(size[1]):
        Layer=list()
        for i in range(size[0]):
            posn=(location[0]+i*per_tile_area,surface.get_height()-BASE_LOC-(j+1)*per_tile_area)
            Layer.append(Block(posn,(per_tile_area,per_tile_area),Design[j*size[0]+(i if leftside else size[0]-i-1)]))
        Tower.append(Layer)
    return Tower
def draw_tower(Tower,Surface):
    for layer in Tower:
        for tile in layer:
            tile.draw(Surface)
pygame.init()
import pygame
def display_animation_of_choosing(Surface, leftside, birds_list, n_frames=30):
    screen_w, screen_h = Surface.get_size()
    box_size    = int(0.1 * screen_h)
    spacing     = box_size + int(0.02 * screen_h)
    outline_w   = max(1, int(screen_w * 0.005))
    total_width = 3 * box_size + 2 * (spacing - box_size)
    margin      = int(0.05 * screen_h)

    if leftside:
        start_x = -total_width
        end_x   = margin
    else:
        start_x = screen_w
        end_x   = screen_w - total_width - margin

    y_pos = margin
    scaled_sprites = []
    for i  in range(3):
        surf = SPRITE[str(type(birds_list[i]))[23:-2].upper()][2]
        scaled = pygame.transform.smoothscale(surf, (box_size, box_size))
        scaled_sprites.append(scaled)

    overlay = pygame.Surface((total_width, box_size), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))

    def _draw_frame(x_offset):
        Surface.blit(overlay, (x_offset, y_pos))
        for i, img in enumerate(scaled_sprites):
            rx = x_offset + i * spacing
            pygame.draw.rect(Surface, "black", (rx, y_pos, box_size, box_size), width=outline_w)
            pygame.draw.rect(Surface, "orange",(rx, y_pos, box_size, box_size),width=1)
            Surface.blit(img, (rx, y_pos))
    for frame in range(n_frames):
        t = frame / (n_frames - 1)
        current_x = int(start_x + (end_x - start_x) * t)
        _draw_frame(current_x)
        yield
    while True:
        _draw_frame(end_x)
        yield

def get_bird(leftside):
    no=random.randint(1,5)
    match no:
        case 1: return Red(((0.25 if leftside else 0.75)*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0))
        case 2: return Bomb(((0.25 if leftside else 0.75)*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0))
        case 3: return Blues(((0.25 if leftside else 0.75)*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0))
        case 4: return Chuck(((0.25 if leftside else 0.75)*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0))
        case 5: return Stella(((0.25 if leftside else 0.75)*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0)) 
# STANDARD VARIABLES
WINDOW_SIZE=(1000,500)
VIRTUAL_SIZE=(1920,1080)
ASPECT_RATIO = VIRTUAL_SIZE[0] / VIRTUAL_SIZE[1]
TICKS=90
Surface=pygame.surface.Surface(VIRTUAL_SIZE)
# INGAME VARIABLES
screen=pygame.display.set_mode(WINDOW_SIZE,pygame.RESIZABLE)
pygame.display.set_caption("")
clock=pygame.time.Clock()
IMAGES,RESIZED,SPRITE=load.load_images()
FONTS=load.load_fonts()
game = True
zoomed=False
RESIZED["LSLING"]=pygame.transform.scale_by(IMAGES["LSLING"],0.15)
RESIZED["RSLING"]=pygame.transform.scale_by(IMAGES["RSLING"],0.15)
Left_Sling=slingshot((0.25*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-0.15*IMAGES["LSLING"].get_size()[1]-195),RESIZED["LSLING"],(10,10),Surface.get_size()[1],True)
Right_SLing=slingshot((0.75*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-0.15*IMAGES["RSLING"].get_size()[1]-195),RESIZED["RSLING"],(10,10),Surface.get_size()[1],False)
player1turn=True
curr_bird=get_bird(True)
Tower_left=Designs[2]
Tower_left_size=Sizes[2]
Tower_left=initialise_tower(Tower_left,Tower_left_size,Surface,(0.01*VIRTUAL_SIZE[0],0.20*VIRTUAL_SIZE[0]),True)
Tower_right=Designs[3]
Tower_right_size=Sizes[3]
Tower_right=initialise_tower(Tower_right,Tower_right_size,Surface,(0.80*VIRTUAL_SIZE[0],0.99*VIRTUAL_SIZE[0]),False)
left_list=[get_bird(True) for _ in range(5)]
right_list=[get_bird(False) for _ in range(5)]
anim = display_animation_of_choosing(screen, True, left_list)
bird_launched=False
time_wait=-1
while game:
    dt = clock.tick(TICKS)/1000
    curr_bird=left_list[0] if player1turn else right_list[0]
    screen_width, screen_height = screen.get_size()
    mouse_posn_screen = pygame.mouse.get_pos()
    mouse_posn = screen_to_virtual(mouse_posn_screen, (screen_width, screen_height), VIRTUAL_SIZE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                if player1turn:Left_Sling.enable(mouse_posn)
                else: Right_SLing.enable(mouse_posn)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button==1 and Left_Sling.enabled:
                curr_bird.vx,curr_bird.vy=Left_Sling.launchvel(mouse_posn)
                bird_launched=True
            if event.button==1 and Right_SLing.enabled:
                curr_bird.vx,curr_bird.vy=Right_SLing.launchvel(mouse_posn)
                bird_launched=True
        if event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = screen.get_size()
            mouse_posn_screen = pygame.mouse.get_pos()
            mouse_posn = screen_to_virtual(mouse_posn_screen, (screen_width, screen_height), VIRTUAL_SIZE)
    curr_bird.update(dt,Surface)
    if curr_bird.y==860 and bird_launched:
        time_wait+=1
        if time_wait==1:
            bird_launched=False
            if not player1turn:
                left_list.append(get_bird(True))
                left_list = left_list[1:]
                anim = display_animation_of_choosing(screen, (not player1turn), left_list)
            else:
                right_list.append(get_bird(False))
                right_list = right_list[1:] 
                anim = display_animation_of_choosing(screen, (not player1turn), right_list)
            player1turn=not player1turn
    else :
        time_wait=-1

    if Left_Sling.enabled:
        if mouse_posn[1]+Left_Sling.bird_size[1] > Left_Sling.screen_height -BASE_LOC:
            mouse_posn=(mouse_posn[0],Left_Sling.prev_mouse_posn[1])
        curr_bird.x,curr_bird.y=mouse_posn
        curr_bird.vx,curr_bird.vy=Left_Sling.update(mouse_posn)
        curr_bird.xm,curr_bird.ym=curr_bird.x / METER,curr_bird.y /METER
    elif Right_SLing.enabled:
        if mouse_posn[1]+Right_SLing.bird_size[1]> Right_SLing.screen_height -BASE_LOC:
            mouse_posn=(mouse_posn[0],Right_SLing.prev_mouse_posn[1])
        curr_bird.x,curr_bird.y=mouse_posn
        curr_bird.vx,curr_bird.vy=Right_SLing.update(mouse_posn)
        curr_bird.xm,curr_bird.ym=curr_bird.x / METER,curr_bird.y /METER
    elif bird_launched:
        for layer in (Tower_right if player1turn  else Tower_left  ):
            for tile in layer:
                collided,destroyed=tile.update_collision(curr_bird)
                if collided:
                    bird_launched=False
                    if not player1turn:
                        left_list.append(get_bird(True))
                        left_list = left_list[1:]
                        anim = display_animation_of_choosing(screen, (not player1turn), left_list)
                    else:
                        right_list.append(get_bird(False))
                        right_list = right_list[1:] 
                        anim = display_animation_of_choosing(screen, (not player1turn), right_list)
                    if destroyed:
                        layer.remove(tile)
                    player1turn=not player1turn
                    break
            else :continue
            break
        
    # Draw on surface
    generate_background(Surface)
    generate_mountains(Surface)
    draw_tower(Tower_left,Surface)
    draw_tower(Tower_right,Surface)
    pygame.draw.rect(Surface,BASE_COLOR,(0,VIRTUAL_SIZE[1]-BASE_LOC,VIRTUAL_SIZE[0],BASE_LOC))
    Left_Sling.draw(Surface)
    Right_SLing.draw(Surface)
    curr_bird.draw(Surface)
    if not zoomed: display_unzoomed(screen,Surface)
    try:
        next(anim)
    except StopIteration:
        pass

    pygame.display.flip()

pygame.quit()
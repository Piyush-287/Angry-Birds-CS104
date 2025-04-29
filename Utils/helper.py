import pygame
from Utils.config import *
from Entities import *
def screen_to_virtual(mouse_pos, screen_size, virtual_size):
    screen_w, screen_h = screen_size
    virtual_w, virtual_h = virtual_size

    scale_x = screen_w / virtual_w
    scale_y = screen_h / virtual_h
    scale = max(scale_x, scale_y)

    scaled_w = virtual_w * scale
    scaled_h = virtual_h * scale

    crop_x = (scaled_w - screen_w) / 2
    crop_y = scaled_h - screen_h 

    virtual_x = (mouse_pos[0] + crop_x) / scale
    virtual_y = (mouse_pos[1] + crop_y) / scale
    return (int(virtual_x), int(virtual_y)) 

def display_animation_of_choosing(Surface, leftside, birds_list,playerdata,super_points,FONTS,SPRITE,STATE,n_frames=10):
    screen_w, screen_h = Surface.get_size()
    box_size    = int(0.1 * screen_h)
    spacing     = box_size + int(0.001 * screen_h)
    outline_w   = max(1, int(screen_w * 0.005))
    total_width = 3 * box_size + 2 * (spacing - box_size)
    margin      = int(0.05 * screen_h)
    text=FONTS["ShadowFight_256"].render(playerdata[0 if leftside else 1],True,"White")
    text=pygame.transform.smoothscale_by(text,screen_h*0.1/text.get_height())
    STATE["selected_rect"]=None
    if leftside:
        start_x = -total_width
        end_x   = margin
    else:
        start_x = screen_w
        end_x   = screen_w - total_width - margin

    y_pos = margin * 2
    scaled_sprites = []
    for i  in range(3):
        print(str(type(birds_list[i])).upper())
        surf = SPRITE[str(type(birds_list[i])).split(".")[1].upper()][2]
        scaled = pygame.transform.smoothscale(surf, (int(0.8*box_size), int(0.8*box_size)))
        if not leftside:
            scaled=pygame.transform.flip(scaled,True,False)
        scaled_sprites.append(scaled)

    overlay = pygame.Surface((total_width, box_size), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))

    def _draw_frame(x_offset):
        nonlocal STATE
        Surface.blit(overlay, (x_offset, y_pos))
        if leftside:
            Surface.blit(text,(x_offset,y_pos-text.get_height()))
        else:
            Surface.blit(text,(x_offset-text.get_width()+total_width,y_pos-text.get_height()))
        Rects=[]
        for i, img in enumerate(scaled_sprites):
            rx = x_offset + i * spacing
            if STATE["super"]:
                if super_points[birds_list[i].type-1] >= 300:
                    pygame.draw.rect(Surface,"green",( rx,y_pos, box_size, box_size))
                else :
                    temp=pygame.Surface((box_size,box_size),pygame.SRCALPHA)
                    pygame.draw.rect(temp,"green",(0,0,box_size,int(super_points[birds_list[i].type-1]*box_size/300)))
                    temp.set_alpha(32)
                    Surface.blit(temp,(rx,y_pos+int(box_size-super_points[birds_list[i].type-1]*box_size/300)))
            rectangle=pygame.draw.rect(Surface, "black", ( rx,y_pos, box_size, box_size), width=outline_w)
            pygame.draw.rect(Surface, "orange",rectangle,width=2)
            if STATE["selected_rect"]==rectangle:
                STATE["selected_bird"]=birds_list[i]
                image=pygame.transform.smoothscale(STATE["selected_bird"].playing_image,(int(1.2*box_size), int(1.2*box_size)))
                if not leftside:
                    image=pygame.transform.flip(image,True,False)
                Surface.blit(image,(rx - box_size*0.1,y_pos-box_size*0.1))
                STATE["selected_bird"].update_animation()
            else :
                Surface.blit(img, (rx + box_size*0.1, y_pos + box_size*0.1))
            Rects.append(rectangle)
        return Rects
    for frame in range(n_frames):
        t = frame / (n_frames - 1)
        current_x = int(start_x + (end_x - start_x) * t)
        yield _draw_frame(current_x)
    while True:
        yield _draw_frame(end_x) 

def initialise_tower(Design:list,size:tuple,surface:pygame.Surface,location,leftside):
    per_tile_area=min(100,(location[1]-location[0])/size[0])
    Tower=list()
    for j in range(size[1]):
        Layer=list()
        for i in range(size[0]):
            if leftside:
                x_pos = location[0] + i * per_tile_area
            else:
                x_pos = location[1] - (i + 1) * per_tile_area 
            y_pos = surface.get_height() - BASE_LOC - (j + 1) * per_tile_area
            posn = (x_pos, y_pos)
            index = j * size[0] + i
            block = Birds.Block(posn, (per_tile_area, per_tile_area), Design[index][0])
            block.health = Design[index][1]
            Layer.append(block)
        Tower.append(Layer)
    return Tower
def initialize(screen,location,Sizes,STATE):
    with open("Data/lastgame.txt", "r") as file:lines = file.readlines()
    player_data = eval(lines[0].strip())
    left_list_types = eval(lines[1].strip())
    left_list=[get_bird(True,no) for no in left_list_types]
    right_list_types = eval(lines[2].strip())
    right_list=[get_bird(False,no) for no in right_list_types]
    tower_left_data = eval(lines[3].strip())
    tower_left=initialise_tower(tower_left_data,Sizes[player_data[2]],screen,location[0],True)
    tower_right_data = eval(lines[4].strip())
    tower_right=initialise_tower(tower_right_data,Sizes[player_data[3]],screen,location[1],False)
    STATE["player1turn"]=eval(lines[5].strip())
    return player_data,left_list,right_list,tower_left,tower_right
def get_bird(leftside,no):
    match no:
        case 1: return Red(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0))
        case 2: return Blues(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0))
        case 3: return Bomb(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0))
        case 4: return Chuck(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0))
        case 5: return Stella(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0)) 
def display_zoomed(screen, Surface, offset_x, offset_y, zoom, player1turn):
    screen_width, screen_height = screen.get_size()
    scale_x = zoom * screen_width / VIRTUAL_SIZE[0]
    scale_y = zoom * screen_height / VIRTUAL_SIZE[1]
    scale = max(scale_x, scale_y)
    scaled_size = (int(VIRTUAL_SIZE[0] * scale), int(VIRTUAL_SIZE[1] * scale))
    scaled_surface = pygame.transform.smoothscale(Surface, scaled_size) 
    if player1turn:
        focus_x = 0.1
    else:
        focus_x = 0.9

    focus_pixel_x = int(VIRTUAL_SIZE[0] * focus_x)
    focus_pixel_y = int(VIRTUAL_SIZE[1]*0.8 - BASE_LOC)
    scaled_focus_x = int(focus_pixel_x * scale)
    scaled_focus_y = int(focus_pixel_y * scale)
    crop_x = scaled_focus_x - screen_width // 2 - offset_x
    crop_y = scaled_focus_y - screen_height // 2 - offset_y
    crop_x = max(0, min(crop_x, scaled_size[0] - screen_width))
    crop_y = max(0, min(crop_y, scaled_size[1] - screen_height))
    screen.blit(scaled_surface, (-crop_x, -crop_y))  
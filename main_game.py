import pygame
VIRTUAL_SIZE=(1920,1080)
import random 
import Physics.collision
import load
from Scenes.Game.background.background import *
from Physics.config import * 
from Entities.slingshot import * 
from Entities.Birds import * 
from PlayerData import *
pygame.init()
BASE_LOC=200
WINDOW_SIZE=(1000,500)
screen=pygame.display.set_mode(WINDOW_SIZE,pygame.RESIZABLE)
clock=pygame.time.Clock()
pygame.display.set_caption("AngryBirds")
IMAGES,RESIZED,SPRITE=load.load_images()
FONTS=load.load_fonts()
TICKS=90
SETTINGS={
    "autozoom" : False,
    "zoom_speed" : 5,
    "offset_speed" : 3,
    "default_zoom" : 2
}
STATE={
    "zoomed"   : False,
    "player1turn" : True,
    "birdlaunched": False,
    "offset" : False,
    "offset_x" : 0,
    "offset_y" : 0,
    "target_zoom" : 1,
    "zoom" : 1,
    "selected_bird":None,
    "selected_rect":None
}
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
def update_bird_list(bird_list:list[Bird],selected,leftside):
    bird_list.remove(selected)
    bird_list.append(get_bird(leftside,selected.type))
    selected=None
def display_animation_of_choosing(Surface, leftside, birds_list, n_frames=10):
    global STATE
    screen_w, screen_h = Surface.get_size()
    box_size    = int(0.1 * screen_h)
    spacing     = box_size + int(0.02 * screen_h)
    outline_w   = max(1, int(screen_w * 0.005))
    total_width = 3 * box_size + 2 * (spacing - box_size)
    margin      = int(0.05 * screen_h)
    STATE["selected_rect"]=None
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
        scaled = pygame.transform.smoothscale(surf, (int(0.8*box_size), int(0.8*box_size)))
        scaled_sprites.append(scaled)

    overlay = pygame.Surface((total_width, box_size), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))

    def _draw_frame(x_offset):
        global STATE
        Surface.blit(overlay, (x_offset, y_pos))
        Rects=[]
        for i, img in enumerate(scaled_sprites):
            rx = x_offset + i * spacing
            rectangle=pygame.draw.rect(Surface, "black", ( rx,y_pos, box_size, box_size), width=outline_w)
            pygame.draw.rect(Surface, "orange",rectangle,width=1)
            if STATE["selected_rect"]==rectangle:
                STATE["selected_bird"]=birds_list[i]
                Surface.blit(pygame.transform.smoothscale(STATE["selected_bird"].playing_image,(int(1.4*box_size), int(1.4*box_size))),(rx - box_size*0.2,y_pos-box_size*0.2))
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
def get_bird(leftside,no):
    match no:
        case 1: return Red(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0))
        case 2: return Blues(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0))
        case 3: return Bomb(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0))
        case 4: return Chuck(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0))
        case 5: return Stella(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0)) 
def main_game(screen,clock,player_data):
    def change_chances():
        nonlocal left_list,right_list,anim
        global STATE
        STATE["birdlaunched"]=False
        if not STATE["player1turn"]:
            anim = display_animation_of_choosing(screen, (not STATE["player1turn"]), left_list)
        else:
            anim = display_animation_of_choosing(screen, (not STATE["player1turn"]), right_list)
        STATE["player1turn"]=not STATE["player1turn"]
    Surface=pygame.surface.Surface(VIRTUAL_SIZE)
    global STATE,SETTINGS
    game = True
    to_update_for=False
    RESIZED["LSLING"]=pygame.transform.scale_by(IMAGES["LSLING"],0.15)
    RESIZED["RSLING"]=pygame.transform.scale_by(IMAGES["RSLING"],0.15)
    Left_Sling=slingshot((0.25*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-0.15*IMAGES["LSLING"].get_size()[1]-195),RESIZED["LSLING"],(10,10),Surface.get_size()[1],True)
    Right_SLing=slingshot((0.75*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-0.15*IMAGES["RSLING"].get_size()[1]-195),RESIZED["RSLING"],(10,10),Surface.get_size()[1],False)
    STATE["player1turn"]=True
    Tower_left,Tower_left_size,Tower_right,Tower_right_size=Designs[player_data[2]],Sizes[player_data[2]],Designs[player_data[3]],Sizes[player_data[3]]
    Tower_left=initialise_tower(Tower_left,Tower_left_size,Surface,(0.01*VIRTUAL_SIZE[0],0.20*VIRTUAL_SIZE[0]),True)
    Tower_right=initialise_tower(Tower_right,Tower_right_size,Surface,(0.80*VIRTUAL_SIZE[0],0.99*VIRTUAL_SIZE[0]),False)
    left_list=[
        Red((0.25*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0)),
        Chuck((0.25*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0)),
        Bomb((0.25*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0)),
        Blues((0.25*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0)),
        Stella((0.25*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0))
    ]
    right_list=[
        Red((0.5*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0)),
        Chuck((0.5*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0)),
        Bomb((0.5*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0)),
        Blues((0.5*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0)),
        Stella((0.5*Surface.get_width(),Surface.get_height()-BASE_LOC-10),(0,0))    
    ]
    random.shuffle(left_list)
    random.shuffle(right_list)
    anim = display_animation_of_choosing(screen, True, left_list)
    time_wait=-1
    selection_ui_boxes:list[pygame.Rect]=[]
    curr_bird=None
    while game:
        if STATE["selected_rect"] and STATE["selected_bird"]:
            curr_bird=STATE["selected_bird"]
        dt = clock.tick(TICKS)/1000
        screen_width, screen_height = screen.get_size()
        mouse_posn_screen = pygame.mouse.get_pos()
        mouse_posn = screen_to_virtual(mouse_posn_screen, (screen_width, screen_height), VIRTUAL_SIZE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    STATE["offset_x"],STATE["offset_y"]=0,0
                    STATE["target_zoom"]=1
                    STATE["zoomed"]=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if STATE["selected_bird"] and STATE["selected_rect"]:
                        if STATE["player1turn"]:Left_Sling.enable(mouse_posn)
                        else: Right_SLing.enable(mouse_posn)
                    for rect in selection_ui_boxes:
                        if rect.collidepoint(mouse_posn_screen):
                            STATE["selected_rect"]=rect

                if event.button==3:
                    pygame.mouse.get_rel() 
                    STATE["offset"]=True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button==1 and Left_Sling.enabled and curr_bird:
                    curr_bird.vx,curr_bird.vy=Left_Sling.launchvel(mouse_posn)
                    STATE["birdlaunched"]=True
                    STATE["selected_bird"]=None
                if event.button==1 and Right_SLing.enabled and curr_bird:
                    curr_bird.vx,curr_bird.vy=Right_SLing.launchvel(mouse_posn)
                    STATE["birdlaunched"]=True
                    STATE["selected_bird"]=None
                if event.button==3 and STATE["offset"]:
                    STATE["offset"]=False
                if event.button == 4 and STATE["zoomed"]:
                    STATE["target_zoom"] = min(STATE["target_zoom"] + 0.5, 10)
                if event.button == 5 and STATE["zoomed"]:
                    STATE["target_zoom"] = max(STATE["target_zoom"] - 0.5, 1)
            if event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = screen.get_size()
                mouse_posn_screen = pygame.mouse.get_pos()
                mouse_posn = screen_to_virtual(mouse_posn_screen, (screen_width, screen_height), VIRTUAL_SIZE)
        if curr_bird:
            curr_bird.update(dt,Surface)
            if curr_bird.y+curr_bird.radius==VIRTUAL_SIZE[1]-BASE_LOC and STATE["birdlaunched"]:
                time_wait+=1
                if time_wait==1:
                    update_bird_list(right_list if not STATE["player1turn"] else left_list,STATE["selected_bird"],STATE["player1turn"])
                    change_chances()
                    curr_bird=None
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
        elif STATE["birdlaunched"]:
            curr_tower=(Tower_right if STATE["player1turn"]  else Tower_left)
            for layer in curr_tower:
                for i in range(len(layer)):
                    collided,destroyed=layer[i].update_collision(curr_bird)
                    to_update_for=STATE["player1turn"]
                    if collided!=0:
                        if collided==2:
                            update_bird_list(right_list if not STATE["player1turn"] else left_list,STATE["selected_bird"],STATE["player1turn"])
                            change_chances()
                            curr_bird=None
                        if destroyed:
                            layer[i]=Block(layer[i].posn,layer[i].size,0)
                            curr_tower=Physics.collision.tower_check(Surface,curr_tower)
                            if to_update_for:
                                Tower_right=curr_tower
                            else : 
                                Tower_left=curr_tower
                            if SETTINGS["autozoom"]:
                                STATE["target_zoom"]=SETTINGS["default_zoom"]
                                STATE["zoomed"]=True
                        break
                else :continue
                break
        if STATE["offset"]:
            rel_change=pygame.mouse.get_rel()
            STATE["offset_x"]+=rel_change[0] * SETTINGS["offset_speed"]
            STATE["offset_y"]+=rel_change[1] * SETTINGS["offset_speed"]
        for layer in Tower_left:
            for i in range(len(layer)):
                if layer[i].update(dt)==False:
                    layer[i]=Block(layer[i].posn,layer[i].size,0)
                    
        for layer in Tower_right:
            for i in range(len(layer)):
                if layer[i].update(dt)==False:
                    layer[i]=Block(layer[i].posn,layer[i].size,0)
                    

        # Draw on surface
        generate_background(Surface)
        generate_mountains(Surface)
        draw_tower(Tower_left,Surface)
        draw_tower(Tower_right,Surface)
        pygame.draw.rect(Surface,BASE_COLOR,(0,VIRTUAL_SIZE[1]-BASE_LOC,VIRTUAL_SIZE[0],BASE_LOC))
        Left_Sling.draw(Surface)
        Right_SLing.draw(Surface)
        if curr_bird and (Left_Sling.enabled or Right_SLing.enabled or STATE["birdlaunched"]):
            curr_bird.draw(Surface)
        STATE["zoom"] += (STATE["target_zoom"] - STATE["zoom"]) * min(1, SETTINGS["zoom_speed"] * dt)
        if STATE["zoom"] == 1:
            STATE["zoomed"]=False
        display_zoomed(screen,Surface,STATE["offset_x"],STATE["offset_y"],STATE["zoom"],not to_update_for)
        pygame.draw.circle(screen,"red",pygame.mouse.get_pos(),3)
        try:
            selection_ui_boxes=next(anim)
        except StopIteration:
            pass
        pygame.display.flip()
if __name__=="__main__":
    main_game(screen,clock,[0,1,11,1])
    pygame.quit()
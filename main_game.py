import pygame
import tutorial
VIRTUAL_SIZE=(1920,1080)
import random 
import math
import Physics.collision
import load
from Scenes.Game.background.background import *
from Physics.config import * 
from Entities.slingshot import * 
from Entities.Birds import * 
from PlayerData import *
from settings import *
pygame.init()
BASE_LOC=200
WINDOW_SIZE=(1000,500)
screen=pygame.display.set_mode(WINDOW_SIZE,pygame.RESIZABLE)
clock=pygame.time.Clock()
pygame.display.set_caption("AngryBirds")
IMAGES,RESIZED,SPRITE=load.load_images()
SOUND=load.load_sound()
FONTS=load.load_fonts()
TICKS=90
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
    "selected_rect":None,
    "anyfall":False,
    "super":False
}
def reload():
    with open("data/lastgame.txt","r") as file:lines=file.readlines()
    data,list1,list2=eval(lines[0]),eval(lines[1]),eval(lines[2])
    random.shuffle(list1)
    random.shuffle(list2)
    lines[1]=str(list1)+"\n"
    lines[2]=str(list2)+"\n"
    lines[3]=str([(tile,100) for tile in Designs[data[2]]])+"\n"
    lines[4]=str([(tile,100) for tile in Designs[data[3]]])+"\n"
    lines[5]="True"
    with open("data/lastgame.txt","w") as file:file.writelines(lines)   
def tut():
    tutorial.tutorial(screen,clock)
    return 1
def cont():return 1
def save_data():return 3
def restart():return 2 
def paused(surface,screen,scale_factor):
    Buttons=[
        Button((0.4,0.1),0.2,IMAGES["CONTINUE"],screen,cont),
        Button((0.4,0.3),0.2,IMAGES["RESTART"],screen,restart),
        Button((0.4,0.5),0.2,IMAGES["CONTROLS_1"],screen,tut),
        Button((0.4,0.7),0.2,IMAGES["SAVE"],screen,save_data)
    ] 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    mouse=pygame.mouse.get_pos()
                    for button in Buttons:
                        clicked,result=button.check_click(mouse)
                        if clicked:
                            return result
        size = surface.get_size()
        scaled_down = pygame.transform.smoothscale(surface, 
            (int(size[0] * scale_factor), int(size[1] * scale_factor)))
        blurred= pygame.transform.smoothscale(scaled_down, size)
        screen.fill((100, 100, 255))
        # Blit to screen
        display_zoomed(screen,blurred,0,0,1,True)
        for button in Buttons:
            button.update(screen)
            button.draw()
        pygame.display.flip()
        clock.tick(60)
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
            if leftside:
                x_pos = location[0] + i * per_tile_area
            else:
                x_pos = location[1] - (i + 1) * per_tile_area 
            y_pos = surface.get_height() - BASE_LOC - (j + 1) * per_tile_area
            posn = (x_pos, y_pos)
            index = j * size[0] + i
            block = Block(posn, (per_tile_area, per_tile_area), Design[index][0])
            block.health = Design[index][1]
            Layer.append(block)
        Tower.append(Layer)
    return Tower
def initialize(screen,location):
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

def draw_tower(Tower,Surface):
    for layer in Tower:
        for tile in layer:
            tile.draw(Surface)
def update_bird_list(bird_list:list[Bird],selected,leftside):
    bird_list.remove(selected)
    bird_list.append(get_bird(leftside,selected.type))
    selected=None
def display_animation_of_choosing(Surface, leftside, birds_list,playerdata,super_points,n_frames=10):
    global STATE
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
        surf = SPRITE[str(type(birds_list[i]))[23:-2].upper()][2]
        scaled = pygame.transform.smoothscale(surf, (int(0.8*box_size), int(0.8*box_size)))
        if not leftside:
            scaled=pygame.transform.flip(scaled,True,False)
        scaled_sprites.append(scaled)

    overlay = pygame.Surface((total_width, box_size), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))

    def _draw_frame(x_offset):
        global STATE
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
def get_bird(leftside,no):
    match no:
        case 1: return Red(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0))
        case 2: return Blues(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0))
        case 3: return Bomb(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0))
        case 4: return Chuck(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0))
        case 5: return Stella(((0.25 if leftside else 0.75)*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-BASE_LOC-10),(0,0)) 
def main_game(screen:pygame.Surface,clock):
    global STATE,SETTINGS
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
        "selected_rect":None,
        "anyfall":False,
        "super":False
    }
    def save_data():
        with open("Data/lastgame.txt","w") as file:
            file.write(str(player_data)+"\n")
            file.write(str([bird.type for bird in left_list])+"\n")
            file.write(str([bird.type for bird in right_list])+"\n")
            file.write(str([(block.type,block.health) for layer in Tower_left for block in layer])+"\n")
            file.write(str([(block.type,block.health) for layer in Tower_right for block in layer])+"\n")
            file.write(str(STATE["player1turn"]))
    def change_chances():
        nonlocal left_list,right_list,anim,super_points_left,super_points_right
        global STATE
        STATE["birdlaunched"]=False
        if not STATE["player1turn"]:
            anim = display_animation_of_choosing(screen, (not STATE["player1turn"]), left_list,player_data,super_points_left)
        else:
            anim = display_animation_of_choosing(screen, (not STATE["player1turn"]), right_list,player_data,super_points_right)
        STATE["player1turn"]=not STATE["player1turn"]
        STATE["super"]=False
    Surface=pygame.surface.Surface(VIRTUAL_SIZE)
    game = True
    STATE["selected_bird"]=None
    STATE["selected_rect"]=None
    STATE["anyfall"]=False
    STATE["super"]=False
    to_update_for=False
    RESIZED["LSLING"]=pygame.transform.scale_by(IMAGES["LSLING"],0.15)
    RESIZED["RSLING"]=pygame.transform.scale_by(IMAGES["RSLING"],0.15)
    Left_Sling=slingshot((0.25*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-0.15*IMAGES["LSLING"].get_size()[1]-195),RESIZED["LSLING"],(10,10),Surface.get_size()[1],True)
    Right_SLing=slingshot((0.75*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-0.15*IMAGES["RSLING"].get_size()[1]-195),RESIZED["RSLING"],(10,10),Surface.get_size()[1],False)
    player_data,left_list,right_list,Tower_left,Tower_right=initialize(Surface,[(0.01*VIRTUAL_SIZE[0],0.20*VIRTUAL_SIZE[0]),(0.80*VIRTUAL_SIZE[0],0.99*VIRTUAL_SIZE[0])])
    super_points_left=[0,0,0,0,0]
    super_points_right=[0,0,0,0,0]
    anim = display_animation_of_choosing(screen, STATE["player1turn"], left_list if STATE["player1turn"] else right_list,player_data,super_points_left if STATE["player1turn"] else super_points_right)
    time_wait=-1
    prev_left_health=sum(block.health for layer in Tower_left for block in layer)
    prev_right_health=sum(block.health for layer in Tower_right for block in layer)
    left_health,right_health=prev_left_health,prev_right_health
    selection_ui_boxes:list[pygame.Rect]=[]
    frame_capture=0
    curr_bird,text=None,None
    wait=0
    def fade_in():
        temp=pygame.Surface(VIRTUAL_SIZE,pygame.SRCALPHA)
        temp.fill("black")
        for i in range(32):
            temp.set_alpha(256-8*i)
            Surface.blit(temp,(0,0))
            display_zoomed(screen,Surface,0,0,STATE["zoom"],not to_update_for)
            generate_background(Surface)
            generate_mountains(Surface)
            draw_tower(Tower_left,Surface)
            draw_tower(Tower_right,Surface)
            pygame.draw.rect(Surface,BASE_COLOR,(0,VIRTUAL_SIZE[1]-BASE_LOC,VIRTUAL_SIZE[0],BASE_LOC))
            Left_Sling.draw(Surface)
            Right_SLing.draw(Surface)
            pygame.display.flip()
    def win(player1won,score):
        if player1won:
            Winner,Loser=leaderboard.get_player(player_data[0]),leaderboard.get_player(player_data[1])
        else:
            Winner,Loser=leaderboard.get_player(player_data[1]),leaderboard.get_player(player_data[0])
        Winner_prev_rating,Loser_prev_rating=Winner.rating,Loser.rating
        leaderboard.update_rating(Winner,Loser,score)
        win_change=Winner.rating-Winner_prev_rating
        lose_change=Loser.rating-Loser_prev_rating
        temp = pygame.Surface(VIRTUAL_SIZE, pygame.SRCALPHA)
        temp.fill("black")
        temp.set_alpha(192)
        Surface.blit(temp, (0, 0))
        screen_width, screen_height = screen.get_size()
        base_text = FONTS["ShadowFight_256"].render(Winner.name, True, "black")
        text_scale = 0.30 * screen_height / 256
        reveal_progress = 0
        clock = pygame.time.Clock()
        y=0
        leaderboard.save_data()
        while True:
            screen_width, screen_height = screen.get_size()
            text_scale = 0.30 * screen_height / 256
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_posn=pygame.mouse.get_pos()
                    Button_1=pygame.Rect((screen_width//4 - RESIZED["NEW_GAME"].get_width())//2+screen_width*0//4,y-RESIZED["NEW_GAME"].get_height()//2,*RESIZED["NEW_GAME"].get_size())
                    Button_2=pygame.Rect((screen_width//4 - RESIZED["RESTART_1"].get_width())//2+screen_width*1//4,y-RESIZED["RESTART_1"].get_height()//2,*RESIZED["RESTART_1"].get_size())
                    Button_3=pygame.Rect((screen_width//4 - RESIZED["LEADERBOARD"].get_width())//2+screen_width*2//4,y-RESIZED["LEADERBOARD"].get_height()//2,*RESIZED["LEADERBOARD"].get_size())
                    Button_4=pygame.Rect((screen_width//4 - RESIZED["QUIT"].get_width())//2+screen_width*3//4,y-RESIZED["NEW_GAME"].get_height()//2,*RESIZED["NEW_GAME"].get_size())
                    if Button_1.collidepoint(mouse_posn):return 2
                    if Button_2.collidepoint(mouse_posn):
                        reload()
                        return 1
                    if Button_3.collidepoint(mouse_posn):leaderboard.show_leaderboard(screen,clock)
                    if Button_4.collidepoint(mouse_posn):return 0
                    continue
            text = pygame.transform.smoothscale_by(base_text, min(text_scale,0.8*screen_width/base_text.get_width()))
            text_1 = pygame.transform.smoothscale_by(FONTS["ShadowFight_256"].render("WINS", True, "white"),min(0.1 * screen_height / 256,0.8*screen_width/256))
            reveal_progress = min(reveal_progress + 0.02, 1.0)
            visible_height = int(text.get_height() * reveal_progress)
            if visible_height > 0:
                visible_text = text.subsurface(pygame.Rect(0,0 ,text.get_width(), visible_height))
            display_zoomed(screen, Surface, 0, 0, STATE["zoom"], not to_update_for)
            RESIZED["BACK_PLANK"]=pygame.transform.scale(IMAGES["BACK_PLANK"],(screen_width*0.88,screen_height*0.04 + text.get_height() + text_1.get_height()))
            screen.blit(RESIZED["BACK_PLANK"],(0.06*screen_width,0.06*screen_height))
            if visible_height > 0:
                screen.blit(visible_text, ((screen_width - text.get_width()) // 2,int(0.05 * screen_height)))
            screen.blit(text_1, ((screen_width - text_1.get_width()) // 2,int(0.05 * screen_height) + text.get_height()))
            score=pygame.transform.smoothscale_by(FONTS["AngryBirds_32"].render(f"{Winner.name}: +{int(reveal_progress*(win_change))}", True, "green"), text_scale)
            screen.blit(score,(
                    (screen_width//2 - score.get_width()) // 2,
                    int(0.05 * screen_height + text.get_height() + text_1.get_height())                 
            ))
            score=pygame.transform.smoothscale_by(FONTS["AngryBirds_32"].render(f"{Loser.name}: -{int(reveal_progress*(lose_change))}", True, "red"), text_scale)
            screen.blit(score,(
                    (screen_width//2 - score.get_width()) // 2 + screen_width//2,
                    int(0.05 * screen_height + text.get_height() + text_1.get_height())                 
            ))
            y=(screen_height+int(0.05 * screen_height + text.get_height() + text_1.get_height() + score.get_height()))//2
            RESIZED["NEW_GAME"]=pygame.transform.scale_by(IMAGES["NEW_GAME"],0.2 * screen_width/IMAGES["NEW_GAME"].get_width())
            RESIZED["RESTART_1"]=pygame.transform.scale_by(IMAGES["RESTART_1"],0.2 * screen_width/IMAGES["RESTART_1"].get_width())
            RESIZED["LEADERBOARD"]=pygame.transform.scale_by(IMAGES["LEADERBOARD"],0.2 * screen_width/IMAGES["LEADERBOARD"].get_width())
            RESIZED["QUIT"]=pygame.transform.scale_by(IMAGES["QUIT"],0.2 * screen_width/IMAGES["QUIT"].get_width())
            screen.blit(RESIZED["NEW_GAME"],(((screen_width//4 - RESIZED["NEW_GAME"].get_width()))//2+screen_width*0//4,y-RESIZED["NEW_GAME"].get_height()//2))
            screen.blit(RESIZED["RESTART_1"],(((screen_width//4 - RESIZED["RESTART_1"].get_width()))//2+screen_width*1//4,y-RESIZED["RESTART_1"].get_height()//2))
            screen.blit(RESIZED["LEADERBOARD"],(((screen_width//4 - RESIZED["LEADERBOARD"].get_width()))//2+screen_width*2//4,y-RESIZED["LEADERBOARD"].get_height()//2))
            screen.blit(RESIZED["QUIT"],(((screen_width//4 - RESIZED["QUIT"].get_width()))//2+screen_width*3//4,y-RESIZED["QUIT"].get_height()//2))

            pygame.display.flip()
            clock.tick(60)
    fade_in()
    while game:
        if STATE["selected_rect"] and STATE["selected_bird"]:
            curr_bird=STATE["selected_bird"]
        dt = clock.tick(TICKS)/1000
        screen_width, screen_height = screen.get_size()
        mouse_posn_screen = pygame.mouse.get_pos()
        mouse_posn = screen_to_virtual(mouse_posn_screen, (screen_width, screen_height), VIRTUAL_SIZE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if SETTINGS["autosave"]:save_data()
                game=False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE:
                        STATE["offset_x"],STATE["offset_y"]=0,0
                        STATE["target_zoom"]=1
                        STATE["zoomed"]=False
                    case pygame.K_ESCAPE:
                        match paused(Surface,screen,0.02):
                            case 0:
                                game=False
                            case 1:
                                continue
                            case 2:
                                reload()
                                curr_bird=None
                                return 1
                            case 3:
                                save_data()
                                game=False
                    case pygame.K_s:
                        if curr_bird is not None and STATE["birdlaunched"] and SETTINGS["Super"]:
                            if (STATE["player1turn"] and super_points_left[curr_bird.type-1] >= 300) or (not STATE["player1turn"] and super_points_right[curr_bird.type-1] >= 300):
                                print(str(curr_bird)[1:-21].upper())
                                SOUND[str(curr_bird)[1:-21].upper()].set_volume(SETTINGS["Volume"] / 100 * 0.8)
                                SOUND[str(curr_bird)[1:-21].upper()].play()
                                curr_bird.activate(
                                    Surface,
                                    Tower_right if STATE["player1turn"] else Tower_left,
                                    Tower_left if STATE["player1turn"] else Tower_right
                                )
                                STATE["super"] = True

                                if STATE["player1turn"]:
                                    super_points_left[curr_bird.type-1] = 0
                                else:
                                    super_points_right[curr_bird.type-1] = 0
                    case pygame.K_p:
                        if frame_capture==0:frame_capture=1
                        else :
                            frame_capture=0
                    case _:
                        pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if STATE["selected_bird"] and STATE["selected_rect"]:
                        if STATE["player1turn"]:
                            if Left_Sling.enable(mouse_posn):
                                SOUND["SLINGSHOT"].set_volume(SETTINGS["Volume"]/100)
                                SOUND["SLINGSHOT"].play()
                        else: 
                            if Right_SLing.enable(mouse_posn):
                                SOUND["SLINGSHOT"].set_volume(SETTINGS["Volume"]/100)
                                SOUND["SLINGSHOT"].play()
                    for rect in selection_ui_boxes:
                        if rect.collidepoint(mouse_posn_screen):
                            STATE["selected_rect"]=rect
                if event.button==3:
                    pygame.mouse.get_rel() 
                    STATE["offset"]=True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button==1 and Left_Sling.enabled and curr_bird:
                    curr_bird.vx,curr_bird.vy=Left_Sling.launchvel(mouse_posn)
                    SOUND["LAUNCH"].set_volume(SETTINGS["Volume"]/100)
                    SOUND["LAUNCH"].play()
                    STATE["birdlaunched"]=True
                    STATE["selected_bird"]=None
                if event.button==1 and Right_SLing.enabled and curr_bird:
                    curr_bird.vx,curr_bird.vy=Right_SLing.launchvel(mouse_posn)
                    SOUND["LAUNCH"].set_volume(SETTINGS["Volume"]/100)
                    SOUND["LAUNCH"].play()
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
        curr_tower=(Tower_right if STATE["player1turn"]  else Tower_left)
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
            for layer in curr_tower:
                if not curr_bird: break
                for i in range(len(layer)-1,-1,-1):
                    collided,destroyed=layer[i].update_collision(curr_bird)
                    to_update_for=STATE["player1turn"]
                    if collided!=0:
                        type=curr_bird.type-1
                        if collided==2:
                            update_bird_list(right_list if not STATE["player1turn"] else left_list,STATE["selected_bird"],STATE["player1turn"])
                            change_chances()
                            curr_bird=None
                            curr_tower= Physics.collision.tower_check(Surface, curr_tower)
                            break
                        if destroyed:
                            if not STATE["super"]:
                                if STATE["player1turn"]:
                                    print(super_points_left)
                                    super_points_left[curr_bird.type-1]+=100
                                    print(super_points_left)
                                else:
                                    print(super_points_right)
                                    super_points_right[curr_bird.type-1]+=100
                                    print(super_points_right)
                            layer[i]=Block(layer[i].posn,layer[i].size,0)
                            if to_update_for:
                                Tower_right=curr_tower
                            else : 
                                Tower_left=curr_tower
                            curr_tower= Physics.collision.tower_check(Surface, curr_tower)
                            if SETTINGS["autozoom"]:
                                STATE["target_zoom"]=SETTINGS["default_zoom"]
                                STATE["zoomed"]=True
                        prev_left_health,prev_right_health=left_health,right_health
                        left_health=sum(block.health for layer in Tower_left for block in layer)
                        right_health=sum(block.health for layer in Tower_right for block in layer)
                        if STATE["player1turn"]:
                            super_points_left[curr_bird.type-1]-=right_health-prev_left_health
                            print(super_points_left)
                        else:
                            super_points_right[curr_bird.type-1]-=left_health-prev_left_health
                            print(super_points_right)

        if STATE["anyfall"]:
            curr_tower= Physics.collision.tower_check(Surface, curr_tower)
        if any(block.falling for layer in curr_tower for block in layer):
            STATE["anyfall"]=True
            wait=0
        else :
            wait+=1
            if wait>1:
                STATE["anyfall"]=False
        
        if all(block.type==0 or block.health<=0 for layer in Tower_left for block in layer):
            curr_bird=None
            print(player_data[1],"won")
            return win(False,0.6)
        if all(block.type==0 or block.health<=0 for layer in Tower_right for block in layer):
            print(player_data[0],"won")
            curr_bird=None
            return win(True,0.6)
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
                    curr_tower= Physics.collision.tower_check(Surface, curr_tower)
                    layer[i]=Block(layer[i].posn,layer[i].size,0)
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
        if text:screen.blit(text,(0,0))
        if frame_capture:
            frame_capture+=1
            pygame.image.save(screen, f"Assets/captures/capture{frame_capture}.png")
        try:
            selection_ui_boxes=next(anim)
        except StopIteration:
            pass
        pygame.display.flip()


if __name__=="__main__":
    main_game(screen,clock)
    pygame.quit()
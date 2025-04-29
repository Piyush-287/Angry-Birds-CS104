import pygame
import tutorial
import random 
import math
import Utils.collision
import load
from Scenes.background import *
from Utils.config import * 
from Utils import helper
from Entities.slingshot import * 
from Entities.Birds import * 
from Entities.Red import * 
from Entities.Blues import * 
from Entities.Bomb import * 
from Entities.Chuck import * 
from Entities.Stella import * 
from PlayerData import *
from settings import *
BASE_LOC=200
WINDOW_SIZE=(1000,500)
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
def paused(surface,screen,scale_factor,clock):
    Buttons=[
        Button((0.4,0.1),0.2,IMAGES["CONTINUE"],screen,lambda : 1),
        Button((0.4,0.3),0.2,IMAGES["RESTART"],screen,lambda :2),
        Button((0.4,0.5),0.2,IMAGES["HOW_TO_PLAY"],screen,lambda :4),
        Button((0.4,0.7),0.2,IMAGES["SAVE"],screen,lambda :3)
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
        helper.display_zoomed(screen,blurred,0,0,1,True)
        for button in Buttons:
            button.update(screen)
            button.draw()
        pygame.display.flip()
        clock.tick(60)         
def draw_tower(Tower,Surface):
    for layer in Tower:
        for tile in layer:
            tile.draw(Surface)
def update_bird_list(bird_list:list[Bird],selected,leftside):
    bird_list.remove(selected)
    bird_list.append(helper.get_bird(leftside,selected.type))
    selected=None
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
            file.write(str(STATE["player1turn"])+"\n")
            file.write(str(super_points_left)+"\n")
            file.write(str(super_points_right))
    def change_chances():
        nonlocal left_list,right_list,anim,super_points_left,super_points_right
        global STATE
        STATE["birdlaunched"]=False
        if not STATE["player1turn"]:
            anim = helper.display_animation_of_choosing(screen, (not STATE["player1turn"]), left_list,player_data,super_points_left,FONTS,SPRITE,STATE,SETTINGS["Super"])
        else:
            anim = helper.display_animation_of_choosing(screen, (not STATE["player1turn"]), right_list,player_data,super_points_right,FONTS,SPRITE,STATE,SETTINGS["Super"])
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
    player_data,left_list,right_list,Tower_left,Tower_right,super_points_left,super_points_right=helper.initialize(Surface,[(0.01*VIRTUAL_SIZE[0],0.20*VIRTUAL_SIZE[0]),(0.80*VIRTUAL_SIZE[0],0.99*VIRTUAL_SIZE[0])],Sizes,STATE)
    anim = helper.display_animation_of_choosing(screen, STATE["player1turn"], left_list if STATE["player1turn"] else right_list,player_data,super_points_left if STATE["player1turn"] else super_points_right,FONTS,SPRITE,STATE,SETTINGS["Super"])
    time_wait=-1
    prev_left_health=sum(block.health for layer in Tower_left for block in layer)
    prev_right_health=sum(block.health for layer in Tower_right for block in layer)
    left_health,right_health=prev_left_health,prev_right_health
    selection_ui_boxes:list[pygame.Rect]=[]
    curr_bird,text=None,None
    no_of_block=sum(1 for block in Designs[player_data[2]] if block!=0)
    wait=0
    def fade_in():
        temp=pygame.Surface(VIRTUAL_SIZE,pygame.SRCALPHA)
        temp.fill("black")
        for i in range(32):
            temp.set_alpha(256-8*i)
            Surface.blit(temp,(0,0))
            helper.display_zoomed(screen,Surface,0,0,STATE["zoom"],not to_update_for)
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
        lose_change=+Loser.rating-Loser_prev_rating
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
        load.reload()
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
                        load.reload(Designs)
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
            helper.display_zoomed(screen, Surface, 0, 0, STATE["zoom"], not to_update_for)
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
        mouse_posn = helper.screen_to_virtual(mouse_posn_screen, (screen_width, screen_height), VIRTUAL_SIZE)
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
                        match paused(Surface,screen,0.02,clock):
                            case 0:
                                game=False
                            case 1:
                                continue
                            case 2:
                                load.reload(Designs)
                                curr_bird=None
                                return 1
                            case 3:
                                save_data()
                                game=False
                            case 4:
                                tutorial.tutorial(screen,clock)
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
                mouse_posn = helper.screen_to_virtual(mouse_posn_screen, (screen_width, screen_height), VIRTUAL_SIZE)
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
                            curr_tower= Utils.collision.tower_check(Surface, curr_tower)
                            break
                        if destroyed:
                            if not STATE["super"]:
                                if STATE["player1turn"]:
                                    super_points_left[curr_bird.type-1]+=100
                                else:
                                    super_points_right[curr_bird.type-1]+=100
                            layer[i]=Block(layer[i].posn,layer[i].size,0)
                            if to_update_for:
                                Tower_right=curr_tower
                            else : 
                                Tower_left=curr_tower
                            curr_tower= Utils.collision.tower_check(Surface, curr_tower)
                            if SETTINGS["autozoom"]:
                                STATE["target_zoom"]=SETTINGS["default_zoom"]
                                STATE["zoomed"]=True
                        prev_left_health,prev_right_health=left_health,right_health
                        left_health=sum(block.health for layer in Tower_left for block in layer)
                        right_health=sum(block.health for layer in Tower_right for block in layer)
                        if STATE["player1turn"]:
                            super_points_left[curr_bird.type-1]-=right_health-prev_left_health
                        else:
                            super_points_right[curr_bird.type-1]-=left_health-prev_left_health

        if STATE["anyfall"]:
            curr_tower= Utils.collision.tower_check(Surface, curr_tower)
        if any(block.falling for layer in curr_tower for block in layer):
            STATE["anyfall"]=True
            wait=0
        else :
            wait+=1
            if wait>1:
                STATE["anyfall"]=False
        
        if all(block.type==0 or block.health<=0 for layer in Tower_left for block in layer):
            curr_bird=None
            return win(False,1-right_health/(200*no_of_block))
        if all(block.type==0 or block.health<=0 for layer in Tower_right for block in layer):
            curr_bird=None
            return win(True,1-right_health/(200*no_of_block))
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
                    curr_tower= Utils.collision.tower_check(Surface, curr_tower)
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
        helper.display_zoomed(screen,Surface,STATE["offset_x"],STATE["offset_y"],STATE["zoom"],not to_update_for)
        if text:screen.blit(text,(0,0))
        try:
            selection_ui_boxes=next(anim)
        except StopIteration:
            pass
        pygame.display.flip()
import pygame
VIRTUAL_SIZE=(1920,1080)
import load
from Scenes.background import *
from Utils.config import * 
from Entities.slingshot import * 
from Entities.Birds import * 
from Entities.Red import * 
from Entities.Blues import * 
from Entities.Chuck import * 
from Entities.Bomb import * 
from Entities.Stella import * 
from PlayerData import *
import main_game
import Utils.helper
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
def display_final_choice(Surface, leftside, birds_list, playerdata):
    screen_w, screen_h = Surface.get_size()
    box_size = int(0.1 * screen_h)
    spacing = box_size + int(0.001 * screen_h)
    outline_w = max(1, int(screen_w * 0.005))
    total_width = 3 * box_size + 2 * (spacing - box_size)
    margin = int(0.05 * screen_h)
    
    text = FONTS["ShadowFight_256"].render(playerdata[0 if leftside else 1], True, "White")
    text = pygame.transform.smoothscale(text, (screen_h * 0.1 / text.get_height(), screen_h * 0.1))

    if leftside:
        end_x = margin
    else:
        end_x = screen_w - total_width - margin

    y_pos = margin * 2
    scaled_sprites = [pygame.transform.smoothscale(SPRITE[str(type(bird)).split(".")[1].upper()][2], (int(0.8 * box_size), int(0.8 * box_size))) for bird in birds_list]

    overlay = pygame.Surface((total_width, box_size), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))

    Surface.blit(overlay, (end_x, y_pos))
    Surface.blit(text, (end_x, y_pos - text.get_height()))

    Rects = []
    for i, img in enumerate(scaled_sprites):
        rx = end_x + i * spacing
        rectangle = pygame.draw.rect(Surface, "black", (rx, y_pos, box_size, box_size), width=outline_w)
        pygame.draw.rect(Surface, "orange", rectangle, width=2)
        if STATE["selected_rect"] == rectangle:
            STATE["selected_bird"] = birds_list[i]
            image = pygame.transform.smoothscale(STATE["selected_bird"].playing_image, (int(1.2 * box_size), int(1.2 * box_size)))
            Surface.blit(image, (rx - box_size * 0.1, y_pos - box_size * 0.1))
            STATE["selected_bird"].update_animation()
        else:
            Surface.blit(img, (rx + box_size * 0.1, y_pos + box_size * 0.1))
        Rects.append((rectangle,birds_list[i]))

    return Rects

def tutorial(screen:pygame.Surface,clock):
    # telling towers
    dt = clock.tick(TICKS)/1000
    screen_width,screen_height=screen.get_size()
    Surface=pygame.surface.Surface(VIRTUAL_SIZE)
    player_data,left_list,_,Tower_left,Tower_right=Utils.helper.initialize(Surface,[(0.01*VIRTUAL_SIZE[0],0.20*VIRTUAL_SIZE[0]),(0.80*VIRTUAL_SIZE[0],0.99*VIRTUAL_SIZE[0])],Sizes,STATE)
    loop=True
    curr_bird=None
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                loop=False
            if event.type == pygame.KEYDOWN:
                loop=False
        generate_background(Surface)
        generate_mountains(Surface)
        pygame.draw.rect(Surface,BASE_COLOR,(0,VIRTUAL_SIZE[1]-BASE_LOC,VIRTUAL_SIZE[0],BASE_LOC))
        temp=pygame.Surface(VIRTUAL_SIZE,pygame.SRCALPHA)
        temp.fill("black")
        temp.set_alpha(192)
        Surface.blit(temp,(0,0))
        main_game.draw_tower(Tower_left,Surface)
        Utils.helper.display_zoomed(screen,Surface,0,0,1,True)
        text=FONTS["AngryBirds_32"].render("This is Your Tower", True, "black")
        rect=text.get_rect()
        pygame.draw.rect(screen,"orange",(0.1*screen_width-10,0.25*screen_height-10,rect[2]+20,rect[3]+20),border_radius=10)
        pygame.draw.rect(screen,"black",(0.1*screen_width-10,0.25*screen_height-10,rect[2]+20,rect[3]+20),border_radius=10,width=3)
        screen.blit(text,(0.1*screen_width,0.25*screen_height))
        pygame.display.flip()
        clock.tick(TICKS)
    loop =True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                loop=False
            if event.type == pygame.KEYDOWN:
                loop=False
        generate_background(Surface)
        generate_mountains(Surface)
        pygame.draw.rect(Surface,BASE_COLOR,(0,VIRTUAL_SIZE[1]-BASE_LOC,VIRTUAL_SIZE[0],BASE_LOC))
        main_game.draw_tower(Tower_left,Surface)
        temp=pygame.Surface(VIRTUAL_SIZE,pygame.SRCALPHA)
        temp.fill("black")
        temp.set_alpha(192)
        Surface.blit(temp,(0,0))
        main_game.draw_tower(Tower_right,Surface)
        Utils.helper.display_zoomed(screen,Surface,0,0,1,True)
        text=FONTS["AngryBirds_32"].render("This is Opponent's Tower", True, "black")
        rect=text.get_rect()
        pygame.draw.rect(screen,"orange",(0.65*screen_width-10,0.25*screen_height-10,rect[2]+20,rect[3]+20),border_radius=10)
        pygame.draw.rect(screen,"black",(0.65*screen_width-10,0.25*screen_height-10,rect[2]+20,rect[3]+20),border_radius=10,width=3)
        screen.blit(text,(0.65*screen_width,0.25*screen_height))
        pygame.display.flip()
        clock.tick(TICKS)
    loop = True
    rects=[]
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
               for rect,bird in rects:
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        curr_bird=bird
                        print(curr_bird)
                        loop= False
        generate_background(Surface)
        generate_mountains(Surface)
        pygame.draw.rect(Surface,BASE_COLOR,(0,VIRTUAL_SIZE[1]-BASE_LOC,VIRTUAL_SIZE[0],BASE_LOC))
        main_game.draw_tower(Tower_left,Surface)
        main_game.draw_tower(Tower_right,Surface)
        temp=pygame.Surface(VIRTUAL_SIZE,pygame.SRCALPHA)
        temp.fill("black")
        temp.set_alpha(192) 
        Surface.blit(temp,(0,0))
        Utils.helper.display_zoomed(screen,Surface,0,0,1,True)
        rects=display_final_choice(screen,True,left_list[:3],player_data)
        text=FONTS["AngryBirds_32"].render("Choose Bird by clicking on that bird", True, "black")
        rect=text.get_rect()
        pygame.draw.rect(screen,"orange",(0.05*screen_width-10,0.25*screen_height-10,rect[2]+20,rect[3]+20),border_radius=10)
        pygame.draw.rect(screen,"black",(0.05*screen_width-10,0.25*screen_height-10,rect[2]+20,rect[3]+20),border_radius=10,width=3)
        screen.blit(text,(0.05*screen_width,0.25*screen_height))
        pygame.display.flip()
        clock.tick(TICKS)
    loop=True
    RESIZED["LSLING"]=pygame.transform.scale_by(IMAGES["LSLING"],0.15)
    Left_Sling=slingshot((0.25*VIRTUAL_SIZE[0],VIRTUAL_SIZE[1]-0.15*IMAGES["LSLING"].get_size()[1]-195),RESIZED["LSLING"],(10,10),Surface.get_size()[1],True)
    while loop:
        mouse_posn = Utils.helper.screen_to_virtual(pygame.mouse.get_pos(), (screen_width, screen_height), VIRTUAL_SIZE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Left_Sling.enable(mouse_posn):
                    SOUND["SLINGSHOT"].set_volume(SETTINGS["Volume"]/100)
                    SOUND["SLINGSHOT"].play()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button==1 and Left_Sling.enabled and curr_bird:
                    SOUND["LAUNCH"].set_volume(SETTINGS["Volume"]/100)
                    SOUND["LAUNCH"].play()
                    loop=False
        generate_background(Surface)
        generate_mountains(Surface)
        pygame.draw.rect(Surface,BASE_COLOR,(0,VIRTUAL_SIZE[1]-BASE_LOC,VIRTUAL_SIZE[0],BASE_LOC))
        main_game.draw_tower(Tower_left,Surface)
        main_game.draw_tower(Tower_right,Surface)
        temp=pygame.Surface(VIRTUAL_SIZE,pygame.SRCALPHA)
        temp.fill("black")
        temp.set_alpha(64) 
        Surface.blit(temp,(0,0))
        Left_Sling.draw(Surface)
        text=FONTS["AngryBirds_32"].render("Pull sling shot by clicking left button and release it to launch", True, "black")
        temp=Left_Sling.image.get_rect()
        if Left_Sling.enabled:
            curr_bird.draw(Surface)
        rect=text.get_rect()
        curr_bird.update(dt,Surface)
        if Left_Sling.enabled:
            if mouse_posn[1]+Left_Sling.bird_size[1] > Left_Sling.screen_height -BASE_LOC:
                mouse_posn=(mouse_posn[0],Left_Sling.prev_mouse_posn[1])
            curr_bird.x,curr_bird.y=mouse_posn
            curr_bird.vx,curr_bird.vy=Left_Sling.update(mouse_posn)
            curr_bird.xm,curr_bird.ym=curr_bird.x / METER,curr_bird.y /METER
        Utils.helper.display_zoomed(screen,Surface,0,0,1,True)
        pygame.draw.rect(screen,"orange",(0.05*screen_width-10,0.15*screen_height-10,rect[2]+20,rect[3]+20),border_radius=10)
        pygame.draw.rect(screen,"black",(0.05*screen_width-10,0.15*screen_height-10,rect[2]+20,rect[3]+20),border_radius=10,width=3)
        screen.blit(text,(0.05*screen_width,0.15*screen_height))
        pygame.display.flip()
        clock.tick(TICKS)
    loop =True
    Hints = [
        "You can skip animations by pressing space",
        "If you play faboulously with a bird it accquires a special move", 
        "Launch your bird and press 's' to activate special move",
        "Destroy your opponent before he can!",
        "Let's meet our freinds"
        ]
    hint_index = 0
    loop = True
    while loop: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if hint_index + 1>=len(Hints):
                    loop= False
                else:hint_index += 1
        generate_background(Surface)
        generate_mountains(Surface)
        pygame.draw.rect(Surface, BASE_COLOR, (0, VIRTUAL_SIZE[1] - BASE_LOC, VIRTUAL_SIZE[0], BASE_LOC))
        main_game.draw_tower(Tower_left, Surface)
        main_game.draw_tower(Tower_right, Surface)
        temp = pygame.Surface(VIRTUAL_SIZE, pygame.SRCALPHA)
        temp.fill("black")
        temp.set_alpha(192)
        Surface.blit(temp, (0, 0))
        Utils.helper.display_zoomed(screen, Surface, 0, 0, 1, True)
        text = FONTS["AngryBirds_32"].render(Hints[hint_index], True, "black")
        rect = text.get_rect(center=(screen_width // 2, screen_height // 2))  
        pygame.draw.rect(screen, "orange", (rect.x - 10, rect.y - 10, rect.width + 20, rect.height + 20), border_radius=10)
        pygame.draw.rect(screen, "black", (rect.x - 10, rect.y - 10, rect.width + 20, rect.height + 20), border_radius=10, width=3)
        screen.blit(text, rect.topleft)
        pygame.display.flip()
        clock.tick(TICKS)

    Bird_index = 0
    loop = True
    Bird_name=["Red","Chuck","Blues","Bomb","Stella"]
    Bird_desc=[
        [
            "He is the de facto leader of the Angry Birds",
            "Red is Master of All trades",
            "You better not mess with berserker red"
        ],
        [
            "Chuck is very competitive and strives to prove his worth to his hero Red",
            "His fast speed and sharp beak can pierce anywood or anything",
            "Nobody knows how hes able to generate speed midair"
        ],
        [
            "The Blues are immature and mischievous due to their age",
            "Jay, Jake and Jim, collectively known as the Blues broke every vase in their house",
            "They usually dont split but nobody knows what happen what if they ..."
        ],
        [
            "Bomb is laid-back and fun-loving, often playing with the Blues",
            "Bomb got hard body which can destroy any rock",
            "Nobody ever suvived bomb's explosion"
        ],
        [
            "Stella thrives on freedom and excitement and is unafraid to make a scene to assert her autonomy.",
            "This cute little bird is a menace for her enemies",
            "Stella's ability to magically repair things is yet to be studied"
        ]
    ]
    while loop:
        screen_width,screen_height=screen.get_size()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if Bird_index+1 >= len(Bird_name):
                    loop=False
                else :Bird_index+=1
        generate_background(Surface)
        generate_mountains(Surface)
        pygame.draw.rect(Surface, BASE_COLOR, (0, VIRTUAL_SIZE[1] - BASE_LOC, VIRTUAL_SIZE[0], BASE_LOC))
        main_game.draw_tower(Tower_left, Surface)
        main_game.draw_tower(Tower_right, Surface)
        temp = pygame.Surface(VIRTUAL_SIZE, pygame.SRCALPHA)
        temp.fill("black")
        temp.set_alpha(192)
        Surface.blit(temp, (0, 0))
        Utils.helper.display_zoomed(screen, Surface, 0, 0, 1, True)

        text = FONTS["ShadowFight_48"].render(Bird_name[Bird_index], True, "black")
        rect = text.get_rect(center=(screen_width // 2, screen_height // 5))  
        pygame.draw.rect(screen, "orange", (rect.x - 10, rect.y - 10, rect.width + 20, rect.height + 20), border_radius=10)
        pygame.draw.rect(screen, "black", (rect.x - 10, rect.y - 10, rect.width + 20, rect.height + 20), border_radius=10, width=3)
        screen.blit(text, rect.topleft)
        for i,desc in enumerate(Bird_desc[Bird_index]):
            text = FONTS["AngryBirds_16"].render(desc,True,"black")
            rect = text.get_rect(topleft=(screen_width // 2, screen_height*2 // 5 + i * screen_height//10))  
            pygame.draw.rect(screen, "orange", (rect.x - 10, rect.y - 10, rect.width + 20, rect.height + 20), border_radius=10)
            pygame.draw.rect(screen, "black", (rect.x - 10, rect.y - 10, rect.width + 20, rect.height + 20), border_radius=10, width=3)
            screen.blit(text, rect.topleft)
        # image
        RESIZED[f"{Bird_name[Bird_index].upper()}"]=pygame.transform.smoothscale_by(SPRITE[f"{Bird_name[Bird_index].upper()}"][0],screen_height*0.6/IMAGES[f"{Bird_name[Bird_index].upper()}"].get_height())
        screen.blit(RESIZED[f"{Bird_name[Bird_index].upper()}"],(0.1*screen_width,0.3*screen_height))
        pygame.display.flip()
        clock.tick(TICKS)
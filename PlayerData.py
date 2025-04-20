import pygame
from Data import *
import Scenes.Game.background.background
from Scenes.UI.main_menu import *
from load import *
from Physics.config import * 
pygame.init()

def display_tower(screen:pygame.surface,curr,size):
    Blocks={
        1 : RESIZED["GLASS"],
        2 : RESIZED["WOOD"],
        3 : RESIZED["STONE"]
    }
    sprite_size=Blocks[1].get_size()

    for i in range(size[0]):
        for j in range(size[1]):
            posn=((screen.get_size()[0]-size[0]*sprite_size[0])//2+i*sprite_size[0],450-(j+1)*sprite_size[1])
            typeofblock=curr[j*size[0]+i]
            if 1<=typeofblock<=3:screen.blit(Blocks[typeofblock],posn)


def read_designs():
    Designs,Sizes=list(),list()
    with open("Data/Towers.txt","r") as file:
        for line in file:
            data = list(map(int,line.strip().split(",")))
            Sizes.append(data[0:2])
            Designs.append(data[2:])
    return Designs,Sizes
# Setup screen
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("Enter Player Name")

# Load assets
IMAGES, RESIZED ,SPRITE= load_images()
FONTS = load_fonts()

# Fonts & Colors
font = pygame.font.SysFont(None, 50)
input_font = pygame.font.SysFont(None, 60)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
Designs,Sizes=read_designs()
curr_index=0
mountain_x=0
def redraw_screen():
    screen_width, screen_height = screen.get_size()
    
    Scenes.Game.background.background.generate_background(screen)
    RESIZED["MOUNTAIN"] = pygame.transform.scale(
        IMAGES["MOUNTAIN"], (screen_width * 3, int(screen_height * 1.75))
    )
    screen.blit(RESIZED["MOUNTAIN"], (mountain_x, 0))
    pygame.draw.rect(screen, BASE_COLOR, (0, 450, screen_width, screen_height - 450))
    
    input_box.x = screen_width // 2 - 4*len(player_name)
    # === Label ===
    label_surface = FONTS["ShadowFight_32"].render("Enter Your Name:", True, (255, 215, 140))
    label_tower = FONTS["ShadowFight_48"].render("Choose Tower:" ,True, (255, 215, 140))
    screen.blit(label_tower,(0.02 * screen.get_size()[0],0.02 * screen.get_size()[1]))
    label_rect = label_surface.get_rect()
    label_rect.centery = input_box.centery
    label_rect.right = input_box.left - padding
    label_rect.x=20
    screen.blit(label_surface, label_rect)
    left_button.draw()
    right_button.draw()

    # === Input Box ===
    if active:
        wait+=1
        if (wait//30)%2:
            name_surface = FONTS["AngryBirds_32"].render(player_name + "I", True, "white")
            screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))
        else :
            name_surface = FONTS["AngryBirds_32"].render(player_name, True, "white")
            screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))
    else:       
        name_surface = FONTS["AngryBirds_32"].render(player_name, True, "white")
        screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))
# Input setup
active = False
box_width, box_height = 300, 60
padding = 20
input_box = pygame.Rect(0, 0, box_width, box_height) 
def scrollleft():
    global curr_index
    curr_index=len(Designs)-1 if curr_index==0 else curr_index-1
def scrollright():
    global curr_index
    curr_index=(curr_index+1)%len(Designs)

left_button=Button((0.2,0.4),0.05,RESIZED["LARROW"],screen,scrollleft,redraw_screen)
right_button=Button((0.75,0.4),0.05,RESIZED["RARROW"],screen,scrollright,redraw_screen)
clock = pygame.time.Clock()
running = True

def get_input(initial_input):
    global player_name,mountain_x
    wait=0
    player_name = initial_input
    active = False
    global running
    while running:
        screen_width, screen_height = screen.get_size()
        screen.fill(WHITE)
        RATIO= 0.45/ max(Sizes[curr_index][0],Sizes[curr_index][1])
        RESIZED["GLASS"]=pygame.transform.scale(IMAGES["GLASS"],(int(RATIO*screen_width),int(RATIO*screen_height)))    
        RESIZED["WOOD"]=pygame.transform.scale(IMAGES["WOOD"],(int(RATIO*screen_width),int(RATIO*screen_height)))
        RESIZED["STONE"]=pygame.transform.scale(IMAGES["STONE"],(int(RATIO*screen_width),int(RATIO*screen_height)))

        
        # Update input box position
        bottom_y = 450 + (screen_height - 450) // 2 - box_height // 2
        input_box.y = bottom_y
        input_box.w = box_width
        input_box.h = box_height

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                    if player_name==initial_input:player_name = ''
                else:
                    active = False
                left_button.check_click(event.pos)
                right_button.check_click(event.pos)
            elif event.type==pygame.KEYDOWN and not active:
                if event.key == pygame.K_RETURN:
                    active=True
                    if player_name==initial_input:player_name = ''
            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    print("Player Name:", player_name)
                    return player_name,curr_index
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 24:
                        player_name += event.unicode

        # === Draw background ===
        Scenes.Game.background.background.generate_background(screen)
        RESIZED["MOUNTAIN"] = pygame.transform.scale(
            IMAGES["MOUNTAIN"], (screen_width * 3, int(screen_height * 1.75))
        )
        screen.blit(RESIZED["MOUNTAIN"], (mountain_x, 0))

        # === Draw dark bottom rectangle ===
        pygame.draw.rect(screen, BASE_COLOR , (0, 450, screen_width, screen_height - 450))

        input_box.x = screen_width // 2 - 4*len(player_name)
        # === Label ===
        label_surface = FONTS["ShadowFight_32"].render("Enter Your Name:", True, (255, 215, 140))
        label_tower = FONTS["ShadowFight_48"].render("Choose Tower:" ,True, (255, 215, 140))
        screen.blit(label_tower,(0.02 * screen.get_size()[0],0.02 * screen.get_size()[1]))
        label_rect = label_surface.get_rect()
        label_rect.centery = input_box.centery
        label_rect.right = input_box.left - padding
        label_rect.x=20
        screen.blit(label_surface, label_rect)

        # === Input Box ===
        if active:
            wait+=1
            if (wait//30)%2:
                name_surface = FONTS["AngryBirds_32"].render(player_name + "I", True, "white")
                screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))
            else :
                name_surface = FONTS["AngryBirds_32"].render(player_name, True, "white")
                screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))
        else:       
            name_surface = FONTS["AngryBirds_32"].render(player_name, True, "white")
            screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

        # === Start Button ===
        # pygame.draw.rect(screen, GRAY, start_button)
        # start_text = font.render("Start", True, "white")
        # screen.blit(start_text, (start_button.x + 30, start_button.y + 10))
        left_button.draw()
        right_button.draw()
        
        display_tower(screen,Designs[curr_index],Sizes[curr_index])
        pygame.display.flip()
        clock.tick(60)
    return player_name,curr_index

if __name__=="__main__":
    mountain_x=0
    screen_width, screen_height = screen.get_size()
    Player1,Tower1=get_input("Player1")
    while running and mountain_x+screen_width*2-50>0:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                break
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    mountain_x=-2*screen_width+50
        Scenes.Game.background.background.generate_background(screen)
        RESIZED["MOUNTAIN"] = pygame.transform.scale(
            IMAGES["MOUNTAIN"], (screen_width * 3, int(screen_height * 1.75))
        )
        screen.blit(RESIZED["MOUNTAIN"], (mountain_x, 0))
        mountain_x-=10
        pygame.draw.rect(screen, BASE_COLOR, (0, 450, screen_width, screen_height - 450))
        pygame.display.flip()
        clock.tick(60)
    Player2,Tower2=get_input("Player2")
    print(Player1,":",Tower1)
    print(Player2,":",Tower2)

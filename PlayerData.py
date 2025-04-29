import pygame
from Data import *
import Scenes.Game.background.background
from Scenes.UI.main_menu import *
from Entities.Button import *
from load import *
from Physics.config import * 
import random
import leaderboard
pygame.init()
leaderboard.load_data()
BIRDS=[

]
BASE_LOC=200
def display_tower(screen:pygame.surface,curr,size):
    Blocks={
        1 : RESIZED["WOOD_4"],
        2 : RESIZED["GLASS_4"],
        3 : RESIZED["STONE_4"]
    }
    sprite_size=Blocks[2].get_size()
    for i in range(size[0]):
        for j in range(size[1]):
            posn=((screen.get_size()[0]-size[0]*sprite_size[0])//2+i*sprite_size[0],BASE_LOC-(j+1)*sprite_size[1])
            typeofblock=curr[j*size[0]+i]
            if 1<=typeofblock<=3:screen.blit(Blocks[typeofblock],posn)

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Enter Player Name")

# Load assets
IMAGES, RESIZED ,SPRITE= load_images()
FONTS = load_fonts()

Designs,Sizes=read_designs()
mountain_x=0
# Input setup
clock = pygame.time.Clock()

def get_player_data():
    global BASE_LOC
    running = True
    mountain_x=0
    def get_input(initial_input):
        global BASE_LOC
        nonlocal mountain_x,running
        BASE_LOC=screen.get_height() * 0.8
        active = False
        box_width, box_height = 300, 60
        padding = 20
        input_box = pygame.Rect(0, 0, box_width, box_height) 
        curr_index=0
        rating_rect = None
        Player=None
        def scrollleft():
            nonlocal curr_index
            curr_index=len(Designs)-1 if curr_index==0 else curr_index-1
        def scrollright():
            nonlocal curr_index
            curr_index=(curr_index+1)%len(Designs)
        def redraw_screen():
            screen_width, screen_height = screen.get_size() 
            screen.fill("orange")
            RESIZED["MOUNTAIN"] = pygame.transform.smoothscale(
                IMAGES["MOUNTAIN"], (screen_width * 2.5, screen_height * 2.5)
            )
            screen.blit(RESIZED["MOUNTAIN"], (mountain_x, -1.25*screen_height))
            pygame.draw.rect(screen, BASE_COLOR, (0, BASE_LOC, screen_width, screen_height - BASE_LOC))
            
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
        left_button=Button((0.2,0.4),0.05,RESIZED["LARROW"],screen,scrollleft,redraw_screen)
        right_button=Button((0.75,0.4),0.05,RESIZED["RARROW"],screen,scrollright,redraw_screen)
        wait=0
        player_name = initial_input
        active = False
        while running:
            BASE_LOC=screen.get_height() * 0.8
            screen_width, screen_height = screen.get_size()
            RATIO= 0.35/ max(Sizes[curr_index][0],Sizes[curr_index][1]) 
            RESIZED["WOOD_4"]=pygame.transform.smoothscale_by(IMAGES["WOOD_4"],RATIO * screen_width/IMAGES["WOOD_4"].get_width())
            RESIZED["GLASS_4"]=pygame.transform.smoothscale_by(IMAGES["GLASS_4"],RATIO * screen_width/IMAGES["GLASS_4"].get_width())
            RESIZED["STONE_4"]=pygame.transform.smoothscale_by(IMAGES["STONE_4"],RATIO * screen_width/IMAGES["STONE_4"].get_width())
            # Update input box position
            bottom_y = BASE_LOC + (screen_height - BASE_LOC) // 2 - box_height // 2
            input_box.y = bottom_y
            input_box.w = box_width
            input_box.h = box_height

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False,False

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
                        Player=leaderboard.get_player(player_name)
                        Player=leaderboard.add_player(player_name)
                        return player_name,curr_index
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                        Player=leaderboard.get_player(player_name)
                    else:
                        if len(player_name) < 16:
                            player_name += event.unicode
                            Player=leaderboard.get_player(player_name)
                            if len(player_name)==0:
                                Player=None

            # === Draw background ===
            screen.fill("orange")
            RESIZED["MOUNTAIN"] = pygame.transform.smoothscale(
                IMAGES["MOUNTAIN"], (screen_width * 2.5, screen_height * 2.5)
            )
            screen.blit(RESIZED["MOUNTAIN"], (mountain_x, -1.25*screen_height))

            # === Draw dark bottom rectangle ===
            pygame.draw.rect(screen, BASE_COLOR , (0, BASE_LOC, screen_width, screen_height))

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
            left_button.update(screen)
            right_button.update(screen)
            left_button.draw()
            right_button.draw()
            if Player is not None:
                rating_rect=(0.8*screen_width,input_box.y+10,0.1*screen_width,50)
                if Player.matches == 0 : color="grey"
                elif Player.rank == 1: color=(255,215,0)
                elif Player.rank == 2: color=(192,192,192)
                elif Player.rank == 3: color=(176,141,87)
                elif Player.rank < 10 : color="green"
                else :color="cyan"
                pygame.draw.rect(screen,color,rating_rect,border_radius=10)
                text=FONTS["AngryBirds_32"].render("TBD" if Player.matches==0 else str(Player.rating),True,"white")
                screen.blit(text,(rating_rect[0]+(rating_rect[2]-text.get_width())//2,rating_rect[1]+(rating_rect[3]-text.get_height())//2))
                if Player.matches > 0 :
                    rank_surface = FONTS["AngryBirds_16"].render(f"#{Player.rank}", True, "white")
                    screen.blit(rank_surface, (rating_rect[0], rating_rect[1] - 20))
                
            display_tower(screen,Designs[curr_index],Sizes[curr_index])
            pygame.display.flip()
            clock.tick(60)
        return player_name,curr_index
    
    screen_width, screen_height = screen.get_size()
    Player1,Tower1=get_input("Player1")
    if not Player1:
        return False
    global BASE_LOC
    while running and mountain_x+screen_width>0:
        screen_width, screen_height = screen.get_size()
        BASE_LOC=screen_height*0.8
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    mountain_x=-screen_width
        screen.fill("orange")
        RESIZED["MOUNTAIN"] = pygame.transform.smoothscale(
            IMAGES["MOUNTAIN"], (screen_width * 2.5, screen_height * 2.5)
        )
        screen.blit(RESIZED["MOUNTAIN"], (mountain_x, -1.25*screen_height))
        mountain_x += (-screen_width - mountain_x-10) * 0.05
        pygame.draw.rect(screen, BASE_COLOR, (0, BASE_LOC, screen_width, screen_height - BASE_LOC+100))
        pygame.display.flip()
        clock.tick(60)
    Player2,Tower2=get_input("Player2")
    if not Player2:return False
    with open("Data/lastgame.txt","w") as file:
        file.write(str([Player1,Player2,Tower1,Tower2])+"\n")
        nos=[1,2,3,4,5]
        random.shuffle(nos)
        file.write(str(nos)+"\n")
        random.shuffle(nos)
        file.write(str(nos)+"\n")
        file.write(str([(tile,100) for tile in Designs[Tower1]])+"\n")
        file.write(str([(tile,100) for tile in Designs[Tower2]])+"\n")
        file.write("True")
    # fade out 
    fade_out(screen,clock)
    return [Player1,Player2,Tower1,Tower2]

def fade_out(screen,clock):
    for i in range(32):
        temp=pygame.Surface(screen.get_size(),pygame.SRCALPHA)
        temp.fill("black")
        temp.set_alpha(8*i)
        screen.blit(temp,(0,0))
        pygame.display.flip()
        clock.tick(60)
if __name__=="__main__":
    output=print(get_player_data())
    print("========>",output)

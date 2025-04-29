import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from load import *
import pygame
import PlayerData
from Entities.Button import *
        
def yo():
    print("Yo has been implemented")
    return True

def quit():
    return 0

def update_logo(screen):
    screen_size=screen.get_size()
    img1=pygame.transform.scale(IMAGES["LOGO"],(int(0.6*screen_size[0]),int(0.6*screen_size[0]*IMAGES["LOGO"].get_height()/IMAGES["LOGO"].get_width())))
    img2=pygame.transform.scale(IMAGES["LOGO2"],(int(0.3*screen_size[0]),int(0.3*screen_size[0]*IMAGES["LOGO2"].get_height()/IMAGES["LOGO2"].get_width())))
    return img1,img2
def draw_logo(screen:pygame.Surface,img1:pygame.image,img2):
    screen_size=screen.get_size()
    screen.blit(img1,(0.2*screen_size[0],0.05*screen_size[1]))
    screen.blit(img2,(0.8*screen_size[0]-img2.get_width(),0.04*screen_size[1]+img1.get_height()))

def playgame():
    return 1
def newgame():return 2
def settings():return 3
def controls():return 4
def credit():return 5

def main_menu(screen):
    print("Entered main menu")
    screen_size=screen.get_size()
    Buttons=list()
    #Adding all 6 buttons at the relative position:
    Buttons.append(Button((0.15,0.4),0.3,IMAGES["NEW_GAME"],screen,playgame))
    Buttons.append(Button((0.55,0.4),0.3,IMAGES["LOAD_PREV"],screen,newgame))
    Buttons.append(Button((0.15,0.6),0.3,IMAGES["SETTINGS"],screen,settings))
    Buttons.append(Button((0.55,0.6),0.3,IMAGES["CONTROLS"],screen,controls))
    Buttons.append(Button((0.15,0.8),0.3,IMAGES["CREDITS"],screen,credit))
    Buttons.append(Button((0.55,0.8),0.3,IMAGES["QUIT"],screen,quit))
    # Buttons.append(Button((0.2,0.1),(0.3,0.15),IMAGES["NEW_GAME"],screen,yo))
    menu=True
    RESIZED["MAIN_BACKGROUND"]=pygame.transform.scale(IMAGES["MAIN_BACKGROUND"],screen.get_size())
    img1,img2=update_logo(screen)
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return False
            if event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                for button in Buttons:
                    clicked,output=button.check_click(mouse_pos)
                    if clicked: return output

            if event.type==pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                RESIZED["MAIN_BACKGROUND"]=pygame.transform.scale(IMAGES["MAIN_BACKGROUND"],screen.get_size())
                for button in Buttons:
                    button.update(screen)
                img1,img2=update_logo(screen)
                
                
        screen.blit(RESIZED["MAIN_BACKGROUND"],(0,0))
        for button in Buttons:
            button.draw()
        
        draw_logo(screen,img1,img2)
        pygame.display.flip()


if __name__=="__main__":
    import pygame
    import random 
    # Colors 
    COLORS = {
        "red": (255,0,0), "green": (0,255,0), "blue": (0,0,255), "white": (255,255,255),
        "black": (0,0,0), "yellow": (255,255,0), "pink": (255,192,203), "orange": (255,165,0),
        "violet": (138,43,226), "gray": (128,128,128), "cyan": (0,255,255), "magenta": (255,0,255)
    }
    BG_COLOR="blue"
    
    # STANDARD VARIABLES
    WINDOW_SIZE=(720,450)
    TICKS=10
    
    # INGAME VARIABLES
    screen=pygame.display.set_mode(WINDOW_SIZE,pygame.RESIZABLE | pygame.SCALED)
    pygame.display.set_caption("")
    clock=pygame.time.Clock()
    
    IMAGES,RESIZED,SPRITE=load_images()
    FONTS=load_fonts()
    
    game = True
    while game:
        clock.tick(TICKS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game = False
        #Game Calculations
    
        # Update Everything
    
        #Background 
        if not main_menu(screen):
            game=False
        pygame.display.flip()
    
    pygame.display.quit()
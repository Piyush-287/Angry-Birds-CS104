SETTINGS={
    "autozoom" : False,
    "zoom_speed" : 5,
    "offset_speed" : 3,
    "default_zoom" : 2,
    "autosave":True,
    "Super":True,
    "Music":False,
    "Volume":0.5
}
import pygame
import load
import Scenes.Game.background.background as background
pygame.init()
FONTS=load.load_fonts()
def save_settings():
    with open("Data/settings.txt","w") as file:
        for key,item in SETTINGS.items():
            file.write(str(item)+"\n")
def load_settings():
    with open("Data/settings.txt","r") as file:
        for key,item in SETTINGS.items():
            SETTINGS[key]=eval(file.readline())

def get_settings(screen:pygame.Surface,clock=pygame.time.Clock):
    load_settings()
    global FONTS
    screen_width,screen_height=screen.get_size()
    words=["Autozoom","Autosave","Super Birds","Music"]
    rendered=[]
    for word in words:
        text=FONTS["AngryBirds_256"].render(word,True,"white")
        rendered.append(pygame.transform.smoothscale_by(text,0.1*screen_height/text.get_height()))
    game=True
    target_x,x=list(),list()
    target_x.append(1.0 if SETTINGS["autozoom"] else 0.0)
    target_x.append(1.0 if SETTINGS["autosave"] else 0.0)
    target_x.append(1.0 if SETTINGS["Super"] else 0.0)
    target_x.append(1.0 if SETTINGS["Music"] else 0.0)
    x=target_x.copy()
    DRAG=False
    save_hover=False
    while game:
        screen_width,screen_height=screen.get_size()
        clock.tick(60)
        save_button=pygame.Surface((int(screen_width*0.1),int(screen_height*0.1)),pygame.SRCALPHA)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                load_settings()
                return 1
            if event.type==pygame.MOUSEBUTTONDOWN:
                button_rect = pygame.Rect(int(screen_width * 0.7), int(screen_height * 0.15),int(screen_width * 0.1), int(screen_height * 0.1))
                if button_rect.collidepoint(mouse_pos):
                    SETTINGS["autozoom"] = not SETTINGS["autozoom"]
                    target_x[0] = 1.0 if SETTINGS["autozoom"] else 0.0
                button_rect = pygame.Rect(int(screen_width * 0.7), int(screen_height * 0.27),int(screen_width * 0.1), int(screen_height * 0.1))
                if button_rect.collidepoint(mouse_pos):
                    SETTINGS["autosave"] = not SETTINGS["autosave"]
                    target_x[1] = 1.0 if SETTINGS["autosave"] else 0.0
                button_rect = pygame.Rect(int(screen_width * 0.7), int(screen_height * 0.39),int(screen_width * 0.1), int(screen_height * 0.1))
                if button_rect.collidepoint(mouse_pos):
                    SETTINGS["Super"] = not SETTINGS["Super"]
                    target_x[2] = 1.0 if SETTINGS["Super"] else 0.0
                button_rect = pygame.Rect(int(screen_width * 0.7), int(screen_height * 0.51),int(screen_width * 0.1), int(screen_height * 0.1))
                if button_rect.collidepoint(mouse_pos):
                    SETTINGS["Music"] = not SETTINGS["Music"]
                    target_x[3] = 1.0 if SETTINGS["Music"] else 0.0
                button_rect = pygame.Rect(int(screen_width * 0.5), int(screen_height * 0.51),int(screen_width * 0.1), int(screen_height * 0.1))
                if 0.69*screen_height<mouse_pos[1]<0.72*screen_height:
                    DRAG=True
                if save_hover:
                    save_settings()
                    return 1
            if event.type==pygame.MOUSEBUTTONUP:
                DRAG=False
        if DRAG and SETTINGS["Music"]:
            print("here")
            SETTINGS["Volume"]=min(100,max((mouse_pos[0]-0.5*screen_width)/(0.3*screen_width)*100,0))
            print(SETTINGS["Volume"])
        save_rect = pygame.Rect(int(0.45 * screen_width), int(0.75 * screen_height), int(0.1 * screen_width), int(0.1 * screen_height))
        if save_rect.collidepoint(mouse_pos):
            save_hover = True
        else:
            save_hover = False
        background.generate_background(screen)
        background.generate_mountains(screen)
        temp=pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)
        pygame.draw.rect(temp,"black",(int(screen_width*0.15),int(screen_height*0.1),int(screen_width*0.7),int(screen_height*0.8)),border_radius=int(screen_width*0.025))
        temp.set_alpha(128)
        screen.blit(temp,(0,0))
        for i,word in enumerate(rendered):
            screen.blit(word,(0.2*screen_width,(0.15+i*0.12)*screen_height))
            button_surface=pygame.Surface((int(screen_width*0.05+screen_height*0.1),int(screen_height*0.1)),pygame.SRCALPHA)
            x[i]+=(target_x[i]-x[i])*(0.1)
            pygame.draw.rect(button_surface,"white",(0,0,int(screen_width*0.1),int(screen_height*0.1)),border_radius=int(screen_height*0.05),width=5)
            pygame.draw.rect(button_surface,(0,0,0,0),(3,3,int(screen_width*0.1-6),int(screen_height*0.1-6)),border_radius=int(screen_height*0.05),width=3)
            pygame.draw.rect(button_surface,"white",(0,0,int(x[i]*screen_width*0.05+screen_height*0.1),int(screen_height*0.1)),border_radius=int(screen_height*0.05))
            pygame.draw.circle(button_surface,(0,0,0,0),(int(screen_height*0.05)+x[i]*screen_width*0.05,int(screen_height*0.05)),int(screen_height*0.05-3),width=3)
            screen.blit(button_surface,(int(screen_width*0.7),int(screen_height*0.15+i*screen_height*0.12)))
        if SETTINGS["Music"]:
            text=FONTS["AngryBirds_256"].render("Volume",True,"white")
            text=pygame.transform.smoothscale_by(text,0.1*screen_height/text.get_height())
            screen.blit(text,(0.2*screen_width,(0.65)*screen_height))
            pygame.draw.rect(screen,"white",(0.5*screen_width,0.7*screen_height,0.3*screen_width,0.01*screen_height),width=1)
            pygame.draw.rect(screen,"white",(0.5*screen_width,0.7*screen_height,0.3*screen_width*SETTINGS["Volume"]/100,0.01*screen_height))
            pygame.draw.circle(screen,"white",((0.5+0.3*SETTINGS["Volume"]/100)*screen_width,0.705*screen_height),10 if DRAG else 5)
        pygame.draw.rect(save_button,"white",(0,0,int(screen_width*0.1),int(screen_height*0.1)),border_radius=int(screen_height*0.02),width=5 if save_hover else 3)
        text=FONTS["AngryBirds_256"].render("SAVE",True,(255,255,255,0 if save_hover else 255))
        text=pygame.transform.smoothscale_by(text,0.08*screen_height/text.get_height())
        save_button.blit(text,((0.1*screen_width - text.get_width())//2,(0.1*screen_height - text.get_height())//2))
        screen.blit(save_button,(0.45*screen_width,0.75*screen_height))
        pygame.display.flip()


if __name__ == "__main__":
    screen=pygame.display.set_mode((1000,500),pygame.RESIZABLE)
    clock=pygame.time.Clock()
    IMAGES,RESIZED,SPRITE=load.load_images()
    get_settings(screen,clock)
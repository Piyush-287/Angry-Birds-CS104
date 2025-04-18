import pygame
pygame.font.init()
pygame.display.init()
IMAGES,RESIZED=dict(),dict()
FONTS=dict()
def load_images():
    global IMAGES,RESIZED
    with open("Assets/Images/Paths.txt","r") as file:
        for line in file:
            name,path,transparency = line.strip().split(",")
            IMAGES[name]=pygame.image.load(str("Assets/Images/" + path)).convert_alpha()
            IMAGES[name].set_alpha(256-(int(transparency)*255)//100)
            RESIZED[name]=IMAGES[name]
    print("Loaded Images")
    return [IMAGES,RESIZED]

def load_fonts():
    global FONTS
    with open("Assets/FONTS/Paths.txt","r") as file:
        for line in file:
            name,path,size = line.strip().split(",")
            FONTS[f"{name}_{size}"]=pygame.font.Font(str("Assets/Fonts/")+path,int(size))
    print("Loaded Fonts")
    return FONTS   


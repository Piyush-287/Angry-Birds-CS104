import pygame
pygame.font.init()
pygame.display.init()
IMAGES,RESIZED,SPRITE=dict(),dict(),dict()
FONTS=dict()
def load_images():
    global IMAGES,RESIZED
    with open("Assets/Images/Paths.txt","r") as file:
        for line in file:
            name,path,transparency,tile_size_x,tile_size_y = line.strip().split(",")
            tile_size_x,tile_size_y=int(tile_size_x),int(tile_size_y)
            IMAGES[name]=pygame.image.load(str("Assets/Images/" + path)).convert_alpha()
            IMAGES[name].set_alpha(256-(int(transparency)*255)//100)
            RESIZED[name]=IMAGES[name]
            if tile_size_x != 0:
                SPRITE[name] = []
                tilemap = IMAGES[name]
                map_width, map_height = tilemap.get_size()
                tile_width,tile_height= map_width//tile_size_x,map_height//tile_size_y
                for y in range(tile_size_y):
                    for x in range(tile_size_x):
                        rect = pygame.Rect(x * tile_width, y * tile_height, tile_width, tile_height)
                        tile = tilemap.subsurface(rect).copy()
                        SPRITE[name].append(tile)
    print("Loaded Images")
    return [IMAGES,RESIZED,SPRITE]

def load_fonts():
    global FONTS
    with open("Assets/FONTS/Paths.txt","r") as file:
        for line in file:
            name,path,size = line.strip().split(",")
            FONTS[f"{name}_{size}"]=pygame.font.Font(str("Assets/Fonts/")+path,int(size))
    print("Loaded Fonts")
    return FONTS   

def get_settings():
    SETTINGS={
    "autozoom" : True,
    "zoom_speed" : 5,
    "offset_speed" : 3,
    "default_zoom" : 2
    }
    return SETTINGS

def read_designs():
    Designs,Sizes=list(),list()
    with open("Data/Towers.txt","r") as file:
        for line in file:
            data = list(map(int,line.strip().split(",")))
            Sizes.append(data[0:2])
            Designs.append(data[2:])
    return Designs,Sizes
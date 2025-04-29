import pygame
GRAVITY    = 80
METER = 10 #per 100 inches
E = 0.1 # coefficint of restitution
FRICTION=0.8
BASE_COLOR= (24, 5, 1)
BASE_LOC=200
VIRTUAL_SIZE=(1920,1080)
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

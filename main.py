import pygame
import load
from Utils.config import *
screen=pygame.display.set_mode((960,540),pygame.RESIZABLE)
clock=pygame.time.Clock()
IMAGES,RESIZED,SPRITES=load.load_images()
import settings
FONTS=load.load_fonts()
SETTINGS=settings.load_settings(SETTINGS)
import Scenes.main_menu as menu
import main_game
import PlayerData
import tutorial
import leaderboard
pygame.init()
DESIGNS,SIZES=load.read_designs()
game=True
if SETTINGS["Music"]:
    pygame.mixer.music.load("Assets/Sound/bg_music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(SETTINGS["Volume"]/100)
while game:
    match menu.main_menu(screen):
        case 0:
            game=False
        case 1:
            PlayerData.fade_out(screen,clock)
            data=PlayerData.get_player_data(screen,clock)
            if data:
                PlayerData.fade_out(screen,clock)
                x=main_game.main_game(screen,clock)
                while x:
                    PlayerData.fade_out(screen,clock)
                    if x==2:data=PlayerData.get_player_data(screen,clock)
                    x=main_game.main_game(screen,clock)
        case 2:
            
            PlayerData.fade_out(screen,clock)
            x=main_game.main_game(screen,clock)
            while x:
                PlayerData.fade_out(screen,clock)
                if x==2:data=PlayerData.get_player_data(screen,clock)
                x=main_game.main_game(screen,clock)
        case 3:
            PlayerData.fade_out(screen,clock)
            settings.get_settings(SETTINGS,screen,clock)
            if not SETTINGS["Music"]:
                pygame.mixer.music.stop()
            elif pygame.mixer.get_busy():
                pygame.mixer.music.set_volume(SETTINGS["Volume"]/100)
            else :
                pygame.mixer.music.load("Assets/Sound/bg_music.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(SETTINGS["Volume"]/100)                
        case 4:
            tutorial.tutorial(screen,clock)
        case 5:
            leaderboard.show_leaderboard(screen,clock)
        case _:
            print("idk what you choosed")
pygame.quit()
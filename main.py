import pygame
import load
import Scenes.main_menu as menu
import main_game
import PlayerData
import settings
import tutorial
import leaderboard
pygame.init()

IMAGES,RESIZED,SPRITES=load.load_images()
FONTS=load.load_fonts()
SETTINGS=load.get_settings()
DESIGNS,SIZES=load.read_designs()
screen=pygame.display.set_mode((960,540),pygame.RESIZABLE)
clock=pygame.time.Clock()
game=True
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
            settings.get_settings(screen,clock)
        case 4:
            tutorial.tutorial(screen,clock)
        case 5:
            leaderboard.show_leaderboard(screen,clock)
        case _:
            print("idk what you choosed")
pygame.quit()
# Main File to run complete program. Currently under progress.
import pygame
import load
import Scenes.UI.main_menu as menu
import main_game
import PlayerData
import settings
pygame.init()

IMAGES,RESIZED,SPRITES=load.load_images()
FONTS=load.load_fonts()
SETTINGS=load.get_settings()
DESIGNS,SIZES=load.read_designs()
screen=pygame.display.set_mode((960,540),pygame.RESIZABLE)
clock=pygame.time.Clock()
game=True
while game:
    settings.load_settings()
    match menu.main_menu(screen):
        case 0:
            game=False
        case 1:
            PlayerData.fade_out(screen,clock)
            data=PlayerData.get_player_data()
            if data:
                PlayerData.fade_out(screen,clock)
                x=main_game.main_game(screen,clock)
                while x:
                    PlayerData.fade_out(screen,clock)
                    if x==2:data=PlayerData.get_player_data()
                    x=main_game.main_game(screen,clock)
        case 2:
            PlayerData.fade_out(screen,clock)
            x=main_game.main_game(screen,clock)
            while x:
                PlayerData.fade_out(screen,clock)
                if x==2:data=PlayerData.get_player_data()
                x=main_game.main_game(screen,clock)
        case 3:
            PlayerData.fade_out(screen,clock)
            settings.get_settings(screen,clock)
        case _:
            print("idk what you choosed")
pygame.quit()
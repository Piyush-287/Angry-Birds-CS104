# Main File to run complete program. Currently under progress.
import pygame
import load
import Scenes.UI.main_menu as menu
import main_game
import PlayerData
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
            data=PlayerData.get_player_data()
            if data:
                main_game.main_game(screen,clock,data)
        case _:
            print("idk what you choosed")
pygame.quit()
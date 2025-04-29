Playerlist = {}
RankedPlayerList = []

class Player():
    def __init__(self, name, rating=1000, matches=0, win=0, rank=len(Playerlist)+1):
        self.name = name
        self.rating = rating
        self.matches = matches
        self.win = win
        self.scalefactor = 30
        self.rank = rank

    def update(self, exp, score):
        self.matches += 1
        if score > 5:
            self.win += 1
        if self.matches > 3:
            self.scalefactor = 100
        self.rating += int(self.scalefactor * (score - exp))
def get_player(name):
    if name in Playerlist:
        return Playerlist[name]
    else :
        return Player(name)
def add_player(name):
    if name not in Playerlist:
        player = Player(name)
        Playerlist[name] = player
        insert(player)
    return Playerlist[name]

def insert(player):
    low, high = 0, len(RankedPlayerList)
    while low < high:
        mid = (low + high) // 2
        if player.rating > RankedPlayerList[mid].rating:
            high = mid
        else:
            low = mid + 1
    RankedPlayerList.insert(low, player)
    for i, p in enumerate(RankedPlayerList):
        p.rank = i + 1

def update_rating(player1: Player, player2: Player, score_player1):
    exp1 = 1 / (1 + 10 ** ((player2.rating - player1.rating) / 400))
    player1.update(exp1, score_player1)
    player2.update(1 - exp1, 1 - score_player1)
    reposition(player1)
    reposition(player2)
    save_data()

def reposition(player):
    RankedPlayerList.remove(player)
    insert(player)

def save_data():
    with open("Data/player.txt", "w") as file:
        for player in RankedPlayerList:
            file.write(str([player.name, player.rating, player.matches, player.win]) + "\n")

def load_data():
    with open("Data/player.txt", "r") as file:
        global Playerlist,RankedPlayerList
        RankedPlayerList=[]
        Playerlist={}
        lines = file.readlines()
        for i,line in enumerate(lines):
            name, rating, matches, win = eval(line.strip())
            player = Player(name, rating, matches, win,rank=i+1)
            Playerlist[name] = player
            insert(player)
import pygame
from Scenes.background import *
def show_leaderboard(screen: pygame.Surface, clock: pygame.time.Clock):
    load_data()
    TICKS = 60
    scroll_y = -70 #-(tile_height + tile_spacing)
    scroll_speed = 30
    running = True
    tile_height=50
    tile_height = 60
    tile_spacing = 10
    x_padding=30
    while running:
        screen_width, screen_height = screen.get_size()
        clock.tick(TICKS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running == False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  
                    scroll_y = min(scroll_y + scroll_speed, -(tile_height + tile_spacing))
                if event.button == 5:
                    if scroll_y > -((len(RankedPlayerList)+2)* (tile_height + tile_spacing) - 0.7*screen_height):
                        scroll_y -= scroll_speed

        screen.fill("orange") 
        generate_mountains(screen)

        # Header image
        RESIZED["LBD"] = pygame.transform.scale_by(IMAGES["LBD"], 0.1 * screen_height / IMAGES["LBD"].get_height())
        header_rect = RESIZED["LBD"].get_rect(center=(screen_width // 2, screen_height * 0.1))
        screen.blit(RESIZED["LBD"], header_rect)

        lb_top = int(0.27 * screen_height)
        lb_bottom = int(0.95 * screen_height)
        lb_height = lb_bottom - lb_top
        # Draw fixed header bar for leaderboard labels
        header_tile_rect = pygame.Rect(0, lb_top, screen_width , -tile_height)
        pygame.draw.rect(screen, "brown", header_tile_rect,width=1)
        pygame.draw.rect(screen, "black", header_tile_rect, width=1, border_radius=10)

        label_font = FONTS["AngryBirds_32"]
        label_spacing = 40
        label_right_x = header_tile_rect.right - 20
        if screen_width > 500:
            matches_label = label_font.render("Rating", True, "white")
            label_right_x -= matches_label.get_width()
            screen.blit(matches_label, (label_right_x, header_tile_rect.y + tile_height // 4))
            label_right_x -= label_spacing
        if screen_width > 800:
            win_label = label_font.render("Win%", True, "white")
            label_right_x -= win_label.get_width()
            screen.blit(win_label, (label_right_x, header_tile_rect.y + tile_height // 4))
            label_right_x -= label_spacing
        if screen_width > 1200:
            rating_label = label_font.render("Matches", True, "white")
            label_right_x -= rating_label.get_width()
            screen.blit(rating_label, (label_right_x, header_tile_rect.y + tile_height // 4))

        name_label = label_font.render("Rank - Name", True, "white")
        screen.blit(name_label, (header_tile_rect.x + 20, header_tile_rect.y + tile_height // 4))
        leaderboard_surface = pygame.Surface((screen_width, lb_height),pygame.SRCALPHA)
        leaderboard_surface.set_clip(leaderboard_surface.get_rect())
        y_start = scroll_y
        font = FONTS["ShadowFight_32"]
        for idx, player in enumerate(RankedPlayerList, start=1):
            tile_y = y_start + idx * (tile_height + tile_spacing)
            if tile_y > -tile_height and tile_y < lb_height:
                tile_rect = pygame.Rect(x_padding, tile_y, screen_width - 2 * x_padding, tile_height)
                pygame.draw.rect(leaderboard_surface, "orange", tile_rect, border_radius=10)
                pygame.draw.rect(leaderboard_surface, "black", tile_rect, border_radius=10, width=5)
                name_text = font.render(f"{idx}. {player.name}", True, (0, 0, 0))
                leaderboard_surface.blit(name_text, (tile_rect.x + 20, tile_rect.y + tile_height // 4))
                win_rate = (player.win / player.matches * 100) if player.matches > 0 else 0
                rating_text = font.render(str(player.rating).rjust(5), True, (0, 0, 0))
                win_text = font.render(f"{int(win_rate)}%", True, (0, 0, 0))
                matches_text = font.render(str(player.matches), True, (0, 0, 0))

                spacing = 40 

                right_x = tile_rect.right - 20  
                if screen_width > 500:
                    right_x -= rating_text.get_width()
                    leaderboard_surface.blit(rating_text, (right_x, tile_rect.y + tile_height // 4))
                if screen_width > 800:
                    right_x -= spacing + win_text.get_width()
                    leaderboard_surface.blit(win_text, (right_x, tile_rect.y + tile_height // 4))
                if screen_width > 1200:
                    right_x -= spacing + matches_text.get_width()
                    leaderboard_surface.blit(matches_text, (right_x, tile_rect.y + tile_height // 4))
        screen.blit(leaderboard_surface, (0, lb_top))
        pygame.display.flip()

if __name__=="__main__":
    WINDOW_SIZE=(1000,500)
    screen=pygame.display.set_mode(WINDOW_SIZE,pygame.RESIZABLE)
    pygame.display.set_caption("Leaderboard")
    clock=pygame.time.Clock()
    TICKS=10
    IMAGES,RESIZED,SPRITE=load_images()
    FONTS=load_fonts()
    show_leaderboard(screen,clock)
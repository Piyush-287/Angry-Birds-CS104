import pygame
import random 
import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    
def check(tower, width, height):
    stability = [['0' for _ in range(width)] for _ in range(height)]

    for x in range(width):
        if tower[0][x].type != 0:
            stability[0][x] = 'P'

    for y in range(1, height):
        for x in range(width):
            if tower[y][x].type == 0:
                continue
            if stability[y - 1][x] == 'P':
                stability[y][x] = 'P'
                continue
            left = x > 0 and stability[y][x - 1] == 'P'
            right = x < width - 1 and stability[y][x + 1] == 'P'
            if left and right:
                stability[y][x] = 'P'
                continue
            if left or right:
                stability[y][x] = 'T'
    visited = [[stability[y][x] != '0' for x in range(width)] for y in range(height)]
    return visited


def tower_check(Surface: pygame.Surface, tower: list[list]) -> None:
    height = len(tower)
    width = len(tower[0]) if height > 0 else 0
    stable = check(tower,width,height)
    for x in range(width):
        last_stable=-1
        for y in range(height-1,-1,-1):
            if stable[y][x]==True:
                last_stable=y
                break
        for y in range(last_stable+1,height):
            if tower[y][x].type != 0:
                last_stable += 1
                block_to_fall = tower[y][x]
                fall_distance = (y - last_stable) * block_to_fall.size[1]
                block_to_fall.target_posn = [
                    block_to_fall.posn[0],
                    block_to_fall.posn[1] + fall_distance
                ]
                block_to_fall.falling = True
                print(block_to_fall.posn,block_to_fall.target_posn)
                tower[last_stable][x], tower[y][x] = tower[y][x], tower[last_stable][x]
    return tower
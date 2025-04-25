import pygame
import random 
import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# import Entities.Birds as entity
def detect_line_circle_collision(circle : tuple,line: tuple,vel:pygame.Vector2):
    center : pygame.Vector2=circle[0]
    upadated_center : pygame.Vector2=circle[0]+vel 
    radius : float=circle[1]
    p1 : pygame.Vector2 = line[0]
    p2 : pygame.Vector2 = line[1]

    upadated_center_rel_p1=upadated_center-p1
    p2_rel_p1=p2-p1 # line

    k= upadated_center_rel_p1.dot(p2_rel_p1.normalize())
    if 0 < k <  p2_rel_p1.length() :
        if vel.cross(p1-center) * vel.cross(p2-center) <= 0 :
            k= ((center-p1)).dot(p2_rel_p1.normalize())
            chord_perp=((center-p1) - p2_rel_p1.normalize() * k)
            dist = chord_perp.length()
            correction = chord_perp.normalize() * (radius - dist)
            new_upadated_center = center + correction
            return True, (new_upadated_center, radius)

        chord_perp=(upadated_center_rel_p1 - p2_rel_p1.normalize() * k)
        dist = chord_perp.length()
        if dist < radius:
            if dist != 0:
                correction = chord_perp.normalize() * (radius - dist)
            else:
                correction = pygame.Vector2(0, -radius)
            new_upadated_center = upadated_center + correction
            return True, (new_upadated_center, radius)
    else : 
        return False
# def detect_line_circle_collision(circle: tuple, line: tuple, vel: pygame.Vector2):
#     center: pygame.Vector2 = circle[0]
#     updated_center: pygame.Vector2 = center + vel
#     radius: float = circle[1]
#     p1: pygame.Vector2 = line[0]
#     p2: pygame.Vector2 = line[1]

#     line_vec = p2 - p1
#     line_len = line_vec.length()

#     if line_len == 0:
#         return False  # Degenerate line

#     line_dir = line_vec.normalize()

#     # Project center onto line to find closest point
#     to_center = updated_center - p1
#     proj_len = to_center.dot(line_dir)
#     proj_point = p1 + proj_len * line_dir

#     # Check if projection is within the segment
#     within_segment = 0 <= proj_len <= line_len

#     if within_segment:
#         distance_vec = updated_center - proj_point
#         distance = distance_vec.length()

#         if distance < radius:
#             if distance != 0:
#                 correction = distance_vec.normalize() * (radius - distance)
#             else:
#                 # Pick a normal direction to correct if overlapping exactly
#                 normal = pygame.Vector2(-line_dir.y, line_dir.x)
#                 correction = normal * radius

#             corrected_center = updated_center + correction
#             return True, (corrected_center, radius)
#     else:
#         # Check endpoints
#         dist_p1 = (updated_center - p1).length()
#         if dist_p1 < radius:
#             correction = (updated_center - p1).normalize() * (radius - dist_p1)
#             return True, (updated_center + correction, radius)

#         dist_p2 = (updated_center - p2).length()
#         if dist_p2 < radius:
#             correction = (updated_center - p2).normalize() * (radius - dist_p2)
#             return True, (updated_center + correction, radius)

#     return False

# def detect_line_circle_collision(circle : tuple,line: tuple,vel:pygame.Vector2): 
#     curr_center : pygame.Vector2=circle[0]
#     radius      : int           =circle[1]

#     point_1     : pygame.Vector2=line[0]
#     point_2     : pygame.Vector2=line[1]

#     # case 1 : ball crossed line
#     # case 2 : ball currently on line 
#     # if we check crossing and just update that then in next round we can automatically check current status right so we dont need to update for next move
    
#     crel=curr_center-point_1
#     p2rel=point_2-point_1
#     horcomp=crel.dot(p2rel.normalize()) * p2rel.normalize()
#     if (vel.cross(point_1-curr_center) * vel.cross(point_2-curr_center) <= 0 or ((crel-horcomp).length() < radius )) and (crel.dot(p2rel) > 0 and (curr_center-point_2).dot(-p2rel) > 0) : # automatically covering zero case 
#         # need to move such that on next move just touches line all points in rel to p1
#         newcenter=point_1 + horcomp + radius * (crel-horcomp).normalize()
#         return True,(newcenter,radius)
#     else : 
#         return False
    
def update_line_circle_collision_velocity(vel: pygame.Vector2,angle: pygame.Vector2,e: float):
    '''
    Return updated velocity after collision with line 
    Args:
        vel (pygame.Vector2): Velocity of colliding ball
        angle (pygame.Vector2): angle of the line ( make sure used normalised version)
        e (float): Coefficient of Restitution

    Returns: 
        pygame.Vector2: The final velocity vector
    '''
    return (1+e) * (vel.dot(angle)) * angle - e *  vel

def update_lines_circle_collision(points: list,circle: tuple,circle_vel,e: float):
    for i in range(len(points)-1):
        detection=detect_line_circle_collision(circle,(points[i],points[i+1]),circle_vel)
        if detection:
            _ , circle= detection
            circle_vel=update_line_circle_collision_velocity(circle_vel,(points[i+1]-points[i]).normalize(),e)
            if circle_vel.length() < 1 :
                circle_vel=pygame.Vector2(0,0)
            return circle,circle_vel
    return circle,circle_vel

# if __name__ == "__main__":
#     from collections import deque
#     pygame.init()

#     # --- SCREEN SETUP ---
#     WIDTH, HEIGHT = 800, 600
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     pygame.display.set_caption("Ball + Line Collision Test")
#     clock = pygame.time.Clock()

#     # --- BALL PROPERTIES ---
#     ball_radius = 15
#     ball_pos = pygame.Vector2(100, 100)
#     ball_vel = pygame.Vector2(4, 3)
#     restitution = 0.9  # bounciness

#     # --- LINE SEGMENTS ---
#     line_points = [pygame.Vector2(WIDTH / 10 * i - 10, random.randint(400, HEIGHT)) for i in range(10)]
#     line_points.append(pygame.Vector2(WIDTH + 40, random.randint(400, HEIGHT)))

#     # --- FRAME HISTORY ---
#     frame_history = deque(maxlen=30)  # stores (ball_pos, ball_vel)
#     current_frame_index = -1
#     paused = False
#     step_mode = False

#     # --- GAME LOOP ---
#     running = True
#     while running:
#         screen.fill((30, 30, 30))

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE:
#                     paused = not paused
#                     if paused:
#                         step_mode = True
#                         current_frame_index = len(frame_history) - 1
#                     else:
#                         step_mode = False

#                 elif paused and event.key == pygame.K_LEFT:
#                     if current_frame_index > 0:
#                         current_frame_index -= 1

#                 elif paused and event.key == pygame.K_RIGHT:
#                     if current_frame_index < len(frame_history) - 1:
#                         current_frame_index += 1

#         if not paused:
#             # --- Simulation Advance ---
#             ball_pos += ball_vel
#             ball_vel += pygame.Vector2(0, 1)  # gravity

#             if ball_pos.x - ball_radius <= 0 or ball_pos.x + ball_radius >= WIDTH:
#                 ball_vel.x *= -1
#             if ball_pos.y - ball_radius <= 0 or ball_pos.y + ball_radius >= HEIGHT:
#                 ball_vel.y *= -1

#             (ball_pos, ball_radius), ball_vel = update_lines_circle_collision(
#                 line_points, (ball_pos, ball_radius), ball_vel, restitution
#             )

#             # Store frame
#             frame_history.append((ball_pos.copy(), ball_vel.copy()))
#             current_frame_index = len(frame_history) - 1

#         elif step_mode:
#             if 0 <= current_frame_index < len(frame_history):
#                 ball_pos, ball_vel = frame_history[current_frame_index]

#         # --- Draw Ball and Lines ---
#         pygame.draw.circle(screen, (0, 200, 255), ball_pos, ball_radius)
#         for i in range(len(line_points) - 1):
#             pygame.draw.line(screen, (255, 255, 0), line_points[i], line_points[i + 1], 4)

#         # Optional: show paused state
#         if paused:
#             font = pygame.font.SysFont(None, 36)
#             msg = font.render("PAUSED - ←/→ to step, SPACE to resume", True, (255, 255, 255))
#             screen.blit(msg, (20, 20))

#         pygame.display.flip()
#         clock.tick(60)

#     pygame.quit()
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
import pygame
import sys
import math

pygame.init()

screen_width, screen_height = 1000, 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("KAOOA")

star_size = 400
angle_increment = 144
dot_radius = 20
dots = []
dist_from_left = 40
crow_positions = [
    # (dist_from_left, screen_height // 2 - 200),
    (dist_from_left, screen_height // 2 - 150),
    (dist_from_left, screen_height // 2 - 100),
    (dist_from_left, screen_height // 2 - 50),
    (dist_from_left, screen_height // 2),
    (dist_from_left, screen_height // 2 + 50),
    (dist_from_left, screen_height // 2 + 100),
    (dist_from_left, screen_height // 2 + 150)
]
vulture_position = [(dist_from_left, screen_height // 2 - 200)]
#dot_positions=vulture_position.append(crow_positions)
selected_dot = None
dragging = False

colored_dots_positions = {
    "crows": [],
    "vulture": []
}

dot_occupancy_flags = {tuple(dot): False for dot in dots}

# Function to update dot positions in the dictionaries
def update_dot_positions():
    colored_dots_positions["crows"] = [tuple(dot) for dot in crow_positions]
    colored_dots_positions["vulture"] = [tuple(dot) for dot in vulture_position]

button_radius = 50
left_button_pos = (screen_width // 6, screen_height // 6)
right_button_pos = (5 * screen_width // 6, screen_height // 6)
left_button_color = (255, 255, 0)  # Yellow
right_button_color = (255, 0, 0)  # Red

font = pygame.font.Font(None, 80)
duration = 800

# Introduce two Boolean variables to track whose turn it is
vulture_turn = False
crow_turn = True

def display_message(message, x, y):
    text = font.render(message, True, (255,255,255))
    screen.blit(text, (x, y))
    pygame.display.flip()  # Update the display
    screen.fill((0,0,0))
    pygame.time.delay(duration)  # Delay for the specified duration in milliseconds

def draw_crows():
    # i = 0
    for dot in crow_positions:
        pygame.draw.circle(screen, (255, 255, 0), dot, dot_radius)
    for dot in vulture_position:
        pygame.draw.circle(screen,(255, 0, 0), dot, dot_radius)          

def draw_star(x, y, size):
    points = []
    points1 = []
    angle = math.radians(-90)
    angle1 = math.radians(90)
    for _ in range(10):
        radius = size / 2
        radius1 = radius * math.sin(math.radians(22.5))
        points.append((x + radius * math.cos(angle), y + radius * math.sin(angle)))
        points1.append((x + radius1 * math.cos(angle1), y + radius1 * math.sin(angle1)))
        angle += math.radians(angle_increment)
        angle1 += math.radians(angle_increment)
        x_corner = int(x + radius * math.cos(angle))
        y_corner = int(y + radius * math.sin(angle))
        x_middle = int(x + radius1 * math.cos(angle1))
        y_middle = int(y + radius1 * math.sin(angle1))
        dots.append([x_corner, y_corner])
        dots.append([x_middle, y_middle])
        
        pygame.draw.circle(screen, (255, 255, 255), (x_corner, y_corner), dot_radius)
        pygame.draw.circle(screen, (255, 255, 255), (x_middle, y_middle), dot_radius)
           
    pygame.draw.polygon(screen, (255, 255, 255), points, 1)

def update_dot_occupancy_flags():
    for dot in dots:
        if tuple(dot) in colored_dots_positions["crows"] or tuple(dot) in colored_dots_positions["vulture"]:
            dot_occupancy_flags[tuple(dot)] = True
        else:
            dot_occupancy_flags[tuple(dot)] = False    

cond_var = 0
cond_var1 = 0
crows_captured = 0
def check_crow_win():
    # Define the winning conditions
    winning_conditions = {
        0: [3, 5, 7, 9],
        1: [2, 4, 5, 6, 7, 8],
        2: [1, 5, 7, 9],
        3: [0, 4, 6, 7, 8, 9],
        4: [1, 3, 7, 9],
        5: [0, 1, 2, 6, 8, 9],
        6: [1, 3, 5, 9],
        7: [0, 1, 2, 3, 4, 8],
        8: [1, 3, 5, 7],
        9: [0, 2, 3, 4, 5, 6]
    }
    for key, positions in winning_conditions.items():
        # print(positions)
        # print(key)
        counter=0
        
        for pos in positions:
            for i in crow_positions:
                distance = math.sqrt((dots[pos][0] - i[0])**2 + (dots[pos][1] - i[1])**2)
                if distance <= dot_radius:  # threshold is your threshold value for considering two points close enough
                    counter += 1
                    break
                
        l=len(positions)       
        if counter==l:
            return True           
                    
            
            # print(dots[pos])
            # print(dot_occupancy_flags[tuple(dots[pos])])
    # Check if all positions in the winning condition are occupied by crows and vulture


    
    return False

while True:
    if cond_var1 == 0:
        display_message("Let's begin!", screen_width // 2.75, screen_height // 2)
        display_message("Crow turn", screen_width // 2.75, screen_height // 2)
        cond_var1 = 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x_dot=-1
                y_dot=-1
                poss=()
                if crow_turn:  # Only handle mouse events if it's the crow's turn
                    for i, dot_pos in enumerate(crow_positions):
                        if math.sqrt((event.pos[0] - dot_pos[0])**2 + (event.pos[1] - dot_pos[1])**2) <= dot_radius:
                            selected_dot = i
                            dragging = True        
                    for star_dot in dots:
                        distance = math.sqrt((event.pos[0] - star_dot[0])**2 + (event.pos[1] - star_dot[1])**2)
                        if distance <= dot_radius:
                            x_dot=star_dot[0]
                            y_dot=star_dot[1]
                            poss=star_dot
                            print(poss)
                            print("Dot placed on the star!")
                            update_dot_occupancy_flags()
                            
                            # Add your logic for handling dot placement on the star here
                            # For example, change color or perform other actions
                            break
                        
                    if check_crow_win():
                        display_message("Crows Win!", screen_width // 2.75, screen_height // 8)
                        pygame.quit()
                        sys.exit()    
                elif vulture_turn:  # Only handle mouse events if it's the crow's turn
                    for i, dot_pos in enumerate(vulture_position):
                        if math.sqrt((event.pos[0] - dot_pos[0])**2 + (event.pos[1] - dot_pos[1])**2) <= dot_radius:
                            selected_dot = i
                            dragging = True        
                    for star_dot in dots:
                        distance = math.sqrt((event.pos[0] - star_dot[0])**2 + (event.pos[1] - star_dot[1])**2)
                        if distance <= dot_radius:
                            x_dot=star_dot[0]
                            y_dot=star_dot[1]
                            poss=star_dot
                            print(poss)
                            
                            print("Dot placed on the star!")
                            update_dot_occupancy_flags()
                            # Add your logic for handling dot placement on the star here
                            # For example, change color or perform other actions
                            break
                        
                    for crow_pos in crow_positions[:]:  # Iterate over a copy of the list
                        if math.sqrt((event.pos[0] - crow_pos[0])**2 + (event.pos[1] - crow_pos[1])**2) <= dot_radius:
                            crow_positions.remove(crow_pos)
                            print(crows_captured)
                            crows_captured += 1
                            if crows_captured >= 4:
                                display_message("Vulture Wins!", screen_width // 2.75, screen_height // 8)
                                pygame.quit()
                                sys.exit()            
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging and selected_dot is not None:
                print(poss)
                if crow_turn:
                    # crow_positions[selected_dot] = (x_dot,y_dot)
                    crow_positions[selected_dot] = event.pos
                    # dot_x, dot_y = crow_positions[selected_dot]
                elif vulture_turn:
                    # vulture_position[selected_dot] = (x_dot,y_dot)
                    vulture_position[selected_dot] =event.pos
                    # dot_x, dot_y = vulture_position[selected_dot]
                        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if math.sqrt((event.pos[0] - left_button_pos[0])**2 + (event.pos[1] - left_button_pos[1])**2) <= button_radius:
                # Toggle turn variables
                vulture_turn = True
                crow_turn = False
                display_message("Vulture turn", screen_width // 2.75, screen_height // 20)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if math.sqrt((event.pos[0] - right_button_pos[0])**2 + (event.pos[1] - right_button_pos[1])**2) <= button_radius:
                # Toggle turn variables
                vulture_turn = False
                crow_turn = True
                display_message("Crow turn", screen_width // 2.75, screen_height // 20)
                
                        
                
                

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, left_button_color, left_button_pos, button_radius)
    pygame.draw.circle(screen, right_button_color, right_button_pos, button_radius)
    draw_star(screen_width // 2, screen_height // 2, star_size)
    draw_crows()

    pygame.display.flip()
    
    
    """
    
    0 -> 3,5,7,9
    1 -> 2,4,5,6,7,8
    2 -> 1,5,7,9
    3 -> 0,4,6,7,8,9
    4 -> 1,3,7,9
    5 -> 0,1,2,6,8,9
    6 -> 1,3,5,9
    7 -> 0,1,2,3,4,8
    8 -> 1,3,5,7
    9 -> 0,2,3,4,5,6
    
    
    
    """


   


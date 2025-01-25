import pygame
import random
from logo import logo_text

#initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 700, 500

# Create the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Defining colors for game

TEAL = (0, 128, 128)
PINK = (255, 0, 127)

BACKGROUND_COLOR = (0, 0, 0)

#TIMER for pickups
MIN_PICKUP_INTERVAL = 3000 # 3 secdods
MAX_PICKUP_INTERVAL = 5000 # 5 seconds
MAX_ACTIVE_PICKUPS = 5 # limit for max number of pickups at a time
battle_cube = None

# Brightness ajustment
def adjust_brightness(color, factor):
    #color (tuple) R G B colors
    #factor (float)1 for darker, 1 for lights

    #tuple (rgb) color
    return tuple(max(0, min(255, int(c * factor))) for c in color)

# Cube class definition

class Cube:
    def __init__(self, color, position, velocity):
        # initialize cube color, position, velocity, and starting health

        self.color = color
        self.position = position
        self.velocity = velocity
        self.health = 10
        print(f"initialized {color} cube at {position} with velocity {velocity}")

    def move(self):
        # Update cube position based on velocity
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        #check for wall collision and reverse direction if hit

        if self.position[0] <= 0 or self.position[0] + 50 >= WIDTH:
            self.velocity[0] *= -1 #reverse in X
            #print(f"{self.color} cube hit a verticle wall")

        if self.position[1] <= 0 or self.position[1] + 50 >= HEIGHT:
            self.velocity[1] *= -1 #reverse in y
            #print(f"{self.color} hit a horizontal wall.")
    def draw_health_bar(self):
        bar_width = 50
        bar_height = 5

        health_percentage = max(self.health, 0) / 10 # max health is 10

        current_width = int(bar_width * health_percentage)

        # Healthbar background
        pygame.draw.rect(screen, (50, 50, 50), (self.position[0], self.position[1] - 10, bar_width, bar_height))
        # Healthbar current
        pygame.draw.rect(screen, (0, 255, 0), (self.position[0], self.position[1] - 10, current_width, bar_height))
    
    def draw(self):

        # Draw outline for cube
        pygame.draw.rect(screen, (255, 255, 255), (*self.position, 50, 50), border_bottom_left_radius=3)

        # Draw cube 
        pygame.draw.rect(screen, self.color, (*self.position, 50, 50))

        self.draw_health_bar()
    
class Pickup:
    def __init__(self):
        self.size = 20
        self.position = [random.randint(0, WIDTH - self.size), random.randint(0, HEIGHT - self.size)]
        self.color = random.choice([TEAL, PINK]) 
        print(f"Pickup created at {self.position} with color {self.color}")

    def draw(self):
        pygame.draw.rect(screen, self.color, (*self.position, self.size, self.size)) 

    def is_collected_by(self, cube):
        if self.color != cube.color:
            return False
        cube_rect = pygame.Rect(*cube.position, 50, 50 )
        pickup_rect = pygame.Rect(*self.position, self.size, self.size)
        return cube_rect.colliderect(pickup_rect) 


# MAIN game loop

# Create Cube

cube1 = Cube(TEAL, [WIDTH // 3, HEIGHT // 3], [random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)])
cube2 = Cube(PINK, [2 * WIDTH // 3, 2 * HEIGHT // 3], [random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)])

# list for pickups
active_pickups = []


# Timer vars

last_pickup_time = pygame.time.get_ticks()
pickup_interval = random.randint(MIN_PICKUP_INTERVAL, MAX_PICKUP_INTERVAL)

# Cooldown for cube dmg

damage_cooldown = 500 #ms
cube1_last_damage = 0
cube2_last_damage = 0

running = True
while running:
    current_time = pygame.time.get_ticks()

    # check for event 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle Pickup / Despawn 

    if current_time - last_pickup_time >= pickup_interval and len(active_pickups) < MAX_ACTIVE_PICKUPS:
        new_pickup = Pickup()
        active_pickups.append(new_pickup)
        last_pickup_time = current_time # timer reset
        pickup_interval = random.randint(MAX_PICKUP_INTERVAL, MAX_PICKUP_INTERVAL) # new interval

    # Fill background
    screen.fill(BACKGROUND_COLOR)

    # Move and draw

    cube1.move()
    cube2.move()
    cube1.draw()
    cube2.draw()

    # Check for collision and handle dmg
    cube1_rect = pygame.Rect(*cube1.position, 50, 50)
    cube2_rect = pygame.Rect(*cube2.position, 50, 50)

    
    if cube1_rect.colliderect(cube2_rect):
        current_time = pygame.time.get_ticks()

        if battle_cube == cube1 and current_time - cube2_last_damage >= damage_cooldown:
            cube2.health -= 1
            cube2_last_damage = current_time
            print(f"cube2 takes damage! Health: {cube2.health}")
        elif battle_cube == cube2 and current_time - cube1_last_damage >= damage_cooldown:
            cube1.health -= 1
            cube1_last_damage = current_time
            print(f"cube1 takes damage! Health: {cube1.health}")

    if cube1.health <= 0:
        print("Game Over! Pink WINS!")
        running = False

    if cube2.health <= 0:
        print("Game Over! Teal WINS!")
        running = False

    # Check if either cube has picked up
    for pickup in active_pickups[:]:
        if pickup.is_collected_by(cube1):
            BACKGROUND_COLOR = adjust_brightness(cube1.color, 0.8)
            active_pickups.remove(pickup) # remove pickup from the list
            battle_cube = cube1
            print("cube1 is ready!")
            

        elif pickup.is_collected_by(cube2):
            BACKGROUND_COLOR = adjust_brightness(cube2.color, 0.8)
            active_pickups.remove(pickup)
            battle_cube = cube2
            print("cube2 is ready!")
            
    
    # draw all actives
    for pickup in active_pickups:
        pickup.draw()

    # Update display with changes
    pygame.display.flip()

pygame.quit()
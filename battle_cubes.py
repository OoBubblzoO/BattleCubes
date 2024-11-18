import pygame
import random
from logo import logo_text

#initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

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
    
    def draw(self):

        # Draw outline for cube
        pygame.draw.rect(screen, (255, 255, 255), (*self.position, 50, 50), border_bottom_left_radius=3)

        # Draw cube 
        pygame.draw.rect(screen, self.color, (*self.position, 50, 50))
    
    def attack(self, other):
        
        # Reduce health of other cube if background matches this cube's color
        if BACKGROUND_COLOR == self.color:
            other.health -= 1 

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

    # Check if either cube has picked up
    for pickup in active_pickups[:]:
        if pickup.is_collected_by(cube1):
            BACKGROUND_COLOR = cube1.color
            active_pickups.remove(pickup) # remove pickup from the list
            cube1.attack(cube2)

        elif pickup.is_collected_by(cube2):
            BACKGROUND_COLOR = cube2.color
            active_pickups.remove(pickup)
            cube2.attack(cube1)
    
    # draw all actives
    for pickup in active_pickups:
        pickup.draw()

    # Update display with changes
    pygame.display.flip()

pygame.quit()
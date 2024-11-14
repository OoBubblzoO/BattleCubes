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
PICKUP_VISIBLE_DURATION = 2000 # pickup visible duration

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
        self.visible = False
        self.color = None 

    def draw(self):
        if self.visible:
            pygame.draw.rect(screen, self.color, (*self.position, self.size, self.size)) 

    def reset(self):
        # Set pikcup to new location and assign color
        self.position = [random.randint(0, WIDTH - self.size), random.randint(0, HEIGHT - self.size)]
        self.color = random.choice([TEAL, PINK]) # choose color w choice
        print(f"Pickup appeared at {self.position} with color {self.color}")

    def is_collected_by(self, cube):
        if not self.visible or self.color != cube.color:
            return False
        cube_rect = pygame.Rect(*cube.position, 50, 50 )
        pickup_rect = pygame.Rect(*self.position, self.size, self.size)
        return cube_rect.colliderect(pickup_rect) 


# MAIN game loop

# Create Cube

cube1 = Cube(TEAL, [WIDTH // 3, HEIGHT // 3], [random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)])
cube2 = Cube(PINK, [2 * WIDTH // 3, 2 * HEIGHT // 3], [random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)])

pickup = Pickup()

# Timer vars

last_pickup_time = pygame.time.get_ticks()
pickup_interval = random.randint(MIN_PICKUP_INTERVAL, MAX_PICKUP_INTERVAL)
pickup_visible = False

running = True
while running:

    current_time = pygame.time.get_ticks()

    # Check for Pygame event 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle Pickup / Despawn 

    if not pickup.visible and current_time - last_pickup_time >= pickup_interval:
        pickup.reset()
        pickup.visible = True
        last_pickup_time = current_time
        pickup_interval = random.randint(MAX_PICKUP_INTERVAL, MAX_PICKUP_INTERVAL) # new interval

    # Fill background
    screen.fill(BACKGROUND_COLOR)

    # Move and draw

    cube1.move()
    cube2.move()
    cube1.draw()
    cube2.draw()

    # Check if either cube has picked up
    if pickup.visible:
        if pickup.is_collected_by(cube1):
            BACKGROUND_COLOR = cube1.color
            pickup.visible = False # hide pickup
            last_pickup_time = current_time # reset timer
            cube1.attack(cube2)

        elif pickup.is_collected_by(cube2):
            BACKGROUND_COLOR = cube2.color
            pickup.visible = False # hide pickup
            last_pickup_time = current_time # reset timer
            cube2.attack(cube1)
    pickup.draw()

    # Update display with changes
    pygame.display.flip()

pygame.quit()
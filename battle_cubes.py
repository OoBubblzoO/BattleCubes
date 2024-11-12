import pygame
import random

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
        self.position[0] += self.velocity[1]

        #check for wall collision and reverse direction if hit

        if self.position[0] <= 0 or self.position[0] >= WIDTH:
            self.velocity[0] *= -1 #reverse in X
        if self.position[1] <= 0 or self.position[1] >= HEIGHT:
            self.velocity[1] *= -1 #reverse in y
    
    def draw(self):
        # Draw cube 
        pygame.draw.rect(screen, self.color, (*self.position, 50, 50))
    
    def attack(self, other):
        
        # Reduce health of other cube if background matches this cube's color
        if BACKGROUND_COLOR == self.color:
            other.health -= 1 

# MAIN game loop

cube1 = Cube(TEAL, [100, 100], [random.randint(-5, 5), random.randint(-5, 5)])
cube2 = Cube(TEAL, [300, 300], [random.randint(-5, 5), random.randint(-5, 5)])

running = True
while running:

    # Check for Pygame event 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    # Move and draw

    cube1.move()
    cube2.move()
    cube1.draw()
    cube2.draw()

    # Update display with changes
    pygame.display.flip()

pygame.quit()
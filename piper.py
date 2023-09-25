import pygame
from random import randint
from math import sin

# Constants to determine the size of the screen
SCREEN_WIDTH  = 500
SCREEN_HEIGHT = 500

# Number of clams to draw at the beginning of the game (or when regenerating)
NUM_CLAMS = 10

# Amount the player should move with each key press
STEP = 50

# Frames-per-second for the game
FPS = 60

class Entity():
    """Base class for all game entities

    You should not ever explicitly create an Entity object, only its child classes should be instantiated.

    Attributes:
        rect: A pygame.Rect that describes the location and size of the entity
    """
    def __init__(self, x, y, width, height,):
        """Initialize an Entity

        Args:
            x, y: Initial x,y position for entity
            width: Width of entity's rectangle
            height: Height of entity's rectangle
        """
        self.rect = pygame.Rect(x, y, width, height)
    
    def get_x(self):
        """Return the current x-coordinate"""
        return self.rect.x
    
    def set_x(self, value):
        """Set the x-coordinate to value"""
        self.rect.x = value
    
    def shift_x(self, shift):
        """Shift the x-coordinate by shift (positively or negatively)"""
        self.rect.x += shift
    
    def get_y(self):
        """Return the current y-coordinate"""
        return self.rect.y
    
    def set_y(self, value):
        """Set the y-coordinate to value"""
        self.rect.y = value
    
    def shift_y(self, shift):
        """Shift the y-coordinate by shift (positively or negatively)"""
        self.rect.y += shift
        
    def collide(self, other):
        return self.rect.colliderect(other.rect)
    
class Character(Entity):
    """An entity that represents a character"""
    def render(self, screen):
        """Renders a picture of the character at the position of the entity if it is visible"""
        if self.visible:
            screen.blit(self.image, (self.get_x(), self.get_y()))

class Player(Character):
    """An entity representing the player

    Attributes:
        image: A png image of a piper that represents the player
        visible: A boolean that determines if the player should be visible or invisible
    """
    def __init__(self):
        """Initializes a player"""
        super().__init__(0, 0, 50, 50)
        self.image = pygame.image.load('assets/piper.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.visible = True

class Clam(Character):
    """An entity representing a clam

    Attributes:
        image: A png image of a clam that represents a clam
        visible: A boolean that determines if a clam should be visible or invisible
    """
    def __init__(self):
        """Initializes a clam"""
        super().__init__(randint(0.5*SCREEN_WIDTH,SCREEN_WIDTH-30),randint(0,SCREEN_HEIGHT-30),30,30)
        self.image = pygame.image.load('assets/clam.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.visible = True
           
class Wave(Entity):
    """An entity representing a wave"""
    def __init__(self):
        super().__init__(0.75*SCREEN_WIDTH,0,SCREEN_WIDTH,SCREEN_HEIGHT)
    
    def render(self, screen):
        """renders a blue rectangole at the location of the wave"""
        pygame.draw.rect(screen, (0, 0, 225), self.rect)
           
        


def play_game(max_time):
    """Main game function for Piper's adventure

    Args:
        max_time: Number of seconds to play for
    """
    
    # Initialize the pygame engine
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Arial',14)
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Piper's adventures")

    # Initialize Player, Wave and Clams
    player = Player()
    clams = []
    for _ in range(NUM_CLAMS):
        clams.append(Clam())
    wave = Wave()
        
    time  = 0
    score = 0

    # Main game loop
    while time < max_time:

        # Obtain any user inputs
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
          break

        # Screen origin (0, 0) is the upper-left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.shift_x(STEP)
            elif event.key == pygame.K_LEFT:
                player.shift_x(-STEP)
            elif event.key == pygame.K_UP:
                player.shift_y(-STEP)
            elif event.key == pygame.K_DOWN:
                player.shift_y(STEP)
        
        # Determine if Piper gathered more clams
        for clam in clams:
            if player.collide(clam) and clam.visible == True:
                score += 1
                clam.visible = False
        # Update the position of the wave
        wave.set_x((0.75 * SCREEN_WIDTH) - (0.25 * SCREEN_WIDTH * sin(time)))
        # When the wave has reached its peak create new clams
        if wave.get_x() < 0.51*SCREEN_WIDTH:
            clams = []
            for _ in range(NUM_CLAMS):
                clams.append(Clam())
        # If the piper touched the wave the game is over...
        if player.collide(wave):
            break
        # Draw all of the game elements
        screen.fill([255,255,255])
        player.render(screen)
        for clam in clams:
            clam.render(screen)
        wave.render(screen)
       
       
        # Render the current time and score
        text = font.render('Time = ' + str(round(max_time-time, 1)), True, (0, 0, 0))
        screen.blit(text, (10, 0.95*SCREEN_HEIGHT))
    
        text = font.render('Score = ' + str(score), True, (0, 0, 0))
        screen.blit(text, (10, 0.90*SCREEN_HEIGHT))

        # Render next frame
        pygame.display.update()
        clock.tick(FPS)

        # Update game time by advancing time for each frame
        time += 1.0/FPS

    print('Game over!')
    print('Score =', score)

    pygame.display.quit()
    pygame.quit()

if __name__ == "__main__":
    play_game(30)

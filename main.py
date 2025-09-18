import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports
import math
# Global Variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'
HEART='gallery/sprites/heart.png'
OBSTACLE='gallery/sprites/obstacle.png'
h_blit=True
o_blit=True
l=1
l1='gallery/sprites/l1.png'
l2='gallery/sprites/l2.png'
l3='gallery/sprites/l3.png'
score=0
def welcomeScreen():
    """
    Shows welcome images on the screen
    """

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0
    global h_blit
    global o_blit
    global l
    global score
    
    heart = pygame.image.load(HEART)
    heart_rect = heart.get_rect()

    object_size = 35
    xo, yo = SCREENWIDTH, random.randint(0, SCREENHEIGHT - object_size)
    object_image = pygame.image.load("gallery/sprites/obstacle.png")  
    object_image = pygame.transform.scale(object_image, (object_size, object_size))
    # Initial position
    xh, yh =random.randint(0, SCREENWIDTH - heart_rect.width), SCREENHEIGHT // 2 - heart_rect.height // 2
    
    # Set the vertical speed
    # Set up variables for oscillation
    amplitude = 100
    frequency = 0.05
    time = 0
   
    # Set up clock to control frame rate
    clock = pygame.time.Clock()

   

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -6 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        
        
        heartcollide(playerx,playery,xh,yh)
        obscollide(playerx,playery,xo,yo)
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest :
            return


        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()
            if l==0:
                score=0
                l=1

        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        if l==1:
            L1 = pygame.image.load(l1).convert_alpha()
            SCREEN.blit(L1, (SCREENWIDTH-100, 10))
        if l==2:
            L2 = pygame.image.load(l2).convert_alpha()
            SCREEN.blit(L2, (SCREENWIDTH-100, 10))
        if l==3:
            L3 = pygame.image.load(l3).convert_alpha()
            SCREEN.blit(L3, (SCREENWIDTH-100, 10))
        
        
        
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        if h_blit==True and l<3:

            xh += 5  # You can adjust the speed by changing this value

            # Oscillate the image vertically
            yh = SCREENHEIGHT // 2 - heart_rect.height // 2 + amplitude * math.sin(frequency * time)

            # If the image goes off the screen, reset its position
            if xh > SCREENWIDTH:
                xh = -heart_rect.width

            # Draw the image at the current position
            SCREEN.blit(heart, (xh, yh))

            # Update time for oscillation
            time += 1

        elif h_blit==False:
            xh, yh =random.randint(0, SCREENWIDTH - heart_rect.width), SCREENHEIGHT // 2 - heart_rect.height // 2
            h_blit=True

        if o_blit:
            # Move object from right to left
            xo -= 3

            # If the object reaches the left edge, reset its position
            if xo < -object_size:
                xo = SCREENWIDTH
                yo = random.randint(0, SCREENHEIGHT - object_size)

            # Draw the object (image)
            SCREEN.blit(object_image, (xo, yo))
   
        else:
            xo, yo = SCREENWIDTH, random.randint(0, SCREENHEIGHT - object_size)
            o_blit=True

        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
        
        
def obscollide(playerx,playery,xo,yo):
    global o_blit
    global l
    global score
    o =pygame.image.load(OBSTACLE)
    p=pygame.image.load(PLAYER)
    mask1 = pygame.mask.from_surface(o)
    mask2 = pygame.mask.from_surface(p)

    # Calculate the offset between the images
    offset = (playerx - xo, playery - yo)

    # Check for collision using masks
    if mask1.overlap(mask2, offset):
        if score>0:
            score=score-1
        o_blit=False


def heartcollide(playerx,playery,xh,yh):
    global h_blit
    global l
    h =pygame.image.load(HEART)
    p=pygame.image.load(PLAYER)
    mask1 = pygame.mask.from_surface(h)
    mask2 = pygame.mask.from_surface(p)

    # Calculate the offset between the images
    offset = (playerx - xh, playery - yh)

    # Check for collision using masks
    if mask1.overlap(mask2, offset):
        if l<3:
            l=l+1
        h_blit=False


def isCollide(playerx, playery, upperPipes, lowerPipes):
    global l
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        if l>0:
            l=l-1
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            if l>0:
                l=l-1
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            if l>0:
                l=l-1
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe






if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Fardia')
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 

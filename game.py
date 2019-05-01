Deneme1

import os
import random
import pygame
import time
pygame.init()

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png')]
walkUp = [pygame.image.load('U1.png'), pygame.image.load('U2.png'), pygame.image.load('U3.png'), pygame.image.load('U4.png')]
walkDown = [pygame.image.load('D1.png'), pygame.image.load('D2.png'), pygame.image.load('D3.png'), pygame.image.load('D4.png')]

# Defining the colors to be used for graphical elements.
bright_red = (255,0,0)
bright_green = (0,255,0)
white = (255,255,255)

# Setting up the display.
sc = pygame.image.load('keypad_screen.png')                  # Loading the image to be loaded for keypad background.
bg = pygame.image.load('bg.jpg')                             # Loading the background/level image.
pygame.display.set_caption("Project X")                      # Title of the display window.
height = 719                                                 # Height of the display window.
width = 1039                                                 # Width of the display window.
win = pygame.display.set_mode((height,width))                # Generating the display window.
clock = pygame.time.Clock()                                  # Later to be used for FPS.

#Loading assets for the main menu.
sp = pygame.image.load("sp.jpg")                             # Loading the image for the main menu background.
intro_sound = pygame.mixer.Sound("intro.wav")                # Loading the sound to be played in main menu.
gameDisplay = pygame.display.set_mode((width,height))        # Setting up the display for main menu.                    

# Loading the sounds to be played in keypad menu.
acgr = pygame.mixer.Sound("acgr.wav")
acdn = pygame.mixer.Sound("acdn.wav")
unlock = pygame.mixer.Sound("dr.wav")

# Defining the arrays that will hold interactable and uninteractable elements in the game.
walls = []                                                 
papers = []
computers = []
doors = []
papers = []


# Holds the level layout in a list of strings. As a door is unlocked,
# level design will change accordingly so that the player can move freely between unlocked areas.

level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWPCW WWWW W WWC WWWWWWWW",
    "W    Q    W R     WCWWWWWW",
    "WWW  W      W     W      W",
    "WWW  W      W     W      W",
    "WWW  WWWPP  WWW   WWWWWXWW",
    "WW   WWW   WWWW   WC     W",
    "W    WWWW  WWWW   W      W",
    "WWBWWWWWWWWWWWWWVWWWW    W",
    "W        W          WW  WW",
    "WWWWWWWWAWWWWWWWWWWLWW  WW",
    "WWWWWPCW WWW WWWW   WW  WW",
    "WWW      W   WWWW   WW  WW",
    "WWW      W          WW  WW",
    "WWW      WWW        WW  WW",
    "WWW      WWW        T    W",
    "WWW      WWW        W    W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWW",
    ]

def newlevel(level):
    # Defining  the class to hold the walls as rectangles.
    class Wall(object):
        
        def __init__(self, pos):
            walls.append(self)
            self.rect = pygame.Rect(pos[0], pos[1], 40, 40)
    
    # Defining  the class to hold the walls as rectangles.
    class Door(object):
        
        def __init__(self, pos):
            doors.append(self)
            self.rect = pygame.Rect(pos[0], pos[1], 40, 40)
        
    class Paper(object):
        
        def __init__(self, pos):
            papers.append(self)
            self.rect = pygame.Rect(pos[0], pos[1], 40, 40)
    # Generating the level while D is door, W is wall.
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
            elif col == 'A' or col == 'B' or col == 'Q' or col == 'V' or col == 'R' or col == 'L' or col == 'T' or col == 'X':
                Door((x, y))
            elif col == 'P':
                Paper((x,y))
            x += 40
        y += 40
        x = 0
        
def PaperBox():
    screen = pygame.display.set_mode([1039,719])
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, white)
    text_rect = text.get_rect()
    text_x = screen.get_width() / 2 - text_rect.width / 2
    text_y = screen.get_height() / 2 - text_rect.height / 2
    screen.blit(text, [text_x, text_y])
    pygame.display.flip()
    time.sleep(3)
    
    
#Defining the main loop.
def game_loop():
    gameExit = False
    pygame.mixer.Sound.fadeout(intro_sound,3000)             # As the game starts intro sound fades out for 3 seconds. 

    # Initializing pygame.
    os.environ["SDL_VIDEO_CENTERED"] = "1"                   # Centers the game window on display window.
    pygame.init()
    newlevel(level)
    
    # Defining  the class to hold the character as a rectangle.
    class Player(object):
        
        def __init__(self):
            self.rect = pygame.Rect(150, 600, 30, 40)       # Defining the starting position as x and y values; defining height, and width for the player.
        
        def move(self, dx, dy):                             # Defining movement.
            
            # Moving on each axis
            if dx != 0:
                self.move_single_axis(dx, 0)
            if dy != 0:
                self.move_single_axis(0, dy)
        
        def move_single_axis(self, dx, dy):                # Defining single axi movement.
            
            # Moving the character on x and y axises.
            self.rect.x += dx
            self.rect.y += dy

            # If there is a collision with a wall, stop.
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dx > 0: # Moving right; Hit the left side of the wall
                        self.rect.right = wall.rect.left
                    if dx < 0: # Moving left; Hit the right side of the wall
                        self.rect.left = wall.rect.right
                    if dy > 0: # Moving down; Hit the top side of the wall
                        self.rect.bottom = wall.rect.top
                    if dy < 0: # Moving up; Hit the bottom side of the wall
                        self.rect.top = wall.rect.bottom
                        
            for paper in papers:
                if self.rect.colliderect(paper.rect):
                    if dx > 0: # Moving right; Hit the left side of the paper
                        self.rect.right = paper.rect.left
                    if dx < 0: # Moving left; Hit the right side of the paper
                        self.rect.left = paper.rect.right
                    if dy > 0: # Moving down; Hit the top side of the paper
                        self.rect.bottom = paper.rect.top
                    if dy < 0: # Moving up; Hit the bottom side of the paper
                        self.rect.top = paper.rect.bottom
                        
                    if key[pygame.K_SPACE]:
                        PaperBox()
                        
            # If there is a collision with a locked door, stop.            
            for door in doors:
                if self.rect.colliderect(door.rect):
                    if dx > 0: # Moving right; Hit the left side of the door
                        self.rect.right = door.rect.left
                    if dx < 0: # Moving left; Hit the right side of the door
                        self.rect.left = door.rect.right
                    if dy > 0: # Moving down; Hit the top side of the door
                        self.rect.bottom = door.rect.top
                    if dy < 0: # Moving up; Hit the bottom side of the door
                        self.rect.top = door.rect.bottom
                    
                    # Using spacebar to interact with the doors when nearby
                    if key[pygame.K_SPACE]:
                        text = input()
                        if text == '1234':                                     # Checking for the correct input for the first door
                            pygame.mixer.Sound.play(acgr)                      # Playing the access granted sound
                            time.sleep(0.75)                                   # Letting the screen stay for 0.75 seconds
                            pygame.mixer.Sound.play(unlock)                    # Palying door unlock sound
                            self.rect = pygame.Rect(310, 360, 30, 30)          # Transporting the player to the other side of the door
                        elif text == '4321':
                            pygame.mixer.Sound.play(acgr)                      # Playing the access granted sound
                            time.sleep(0.75)                                   # Letting the screen stay for 0.75 seconds
                            pygame.mixer.Sound.play(unlock)                    # Palying door unlock sound# Checking for the correct input for the first door
                            self.rect = pygame.Rect(88, 290, 30, 30)
                        else:
                            pygame.mixer.Sound.play(acdn)
                        
    player = Player()                                                          # Load the player
    walkCount = 0
    direction = 0
    while not gameExit:
        clock.tick(30)                                                         # Setting the fps to 30 frames per second
        
        # To decide when to kill the main loop and quit the game.
        for event in pygame.event.get():                       
            if event.type == pygame.QUIT:
                gameExit = True
                
        # Move the player if an arrow key is pressed.
        key = pygame.key.get_pressed()
        
        if key[pygame.K_LEFT]:
            player.move(-7, 0)
            walkCount += 1  
        if key[pygame.K_RIGHT]:
            player.move(7, 0)
            walkCount += 1  
        if key[pygame.K_UP]:
            player.move(0, -7)
            walkCount += 1  
        if key[pygame.K_DOWN]:
            player.move(0, 7)
            walkCount += 1  

        # Drawing what needs to be displayed on the window: background image, and character.
        win.blit(bg, (0,0))
        direction_left = 0
        direction_right = 0
        direction_up = 0
        direction_down = 0
        if key[pygame.K_LEFT]:
            win.blit(walkLeft[walkCount % 4], (player.rect.x, player.rect.y))
            direction = 1
        elif key[pygame.K_RIGHT]:
            win.blit(walkRight[walkCount % 4], (player.rect.x, player.rect.y))
            direction = 2
        elif key[pygame.K_UP]:
            win.blit(walkUp[walkCount % 4], (player.rect.x, player.rect.y))
            direction = 3
        elif key[pygame.K_DOWN]:
            win.blit(walkDown[walkCount % 4], (player.rect.x, player.rect.y))
            direction = 4
        else: win.blit(walkDown[3], (player.rect.x, player.rect.y))
    
            
        if direction == 1:
            win.blit(walkLeft[walkCount % 4], (player.rect.x, player.rect.y))
        if direction == 2:
            win.blit(walkRight[walkCount % 4], (player.rect.x, player.rect.y))
        if direction == 3:
            win.blit(walkUp[walkCount % 4], (player.rect.x, player.rect.y))
        if direction == 4:
            win.blit(walkDown[walkCount % 4], (player.rect.x, player.rect.y))

        pygame.display.flip()                                      # Updating/Refreshing the screen each time.
        print(walkCount, walkCount//3)
        
        
# Defining the main menu activities.
def game_intro():

    intro = True
    pygame.mixer.Sound.play(intro_sound)                           # Play the previously defined intro sound.     
    
    # Defining the conditions to quit the game
    while intro:
        for event in pygame.event.get():         
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisplay.blit(sp, (0, 0))                               # background image is loaded.
        largeText = pygame.font.SysFont("consolas",115)            # font is selected.
        TextSurf, TextRect = text_objects("PROJECT X", largeText)  # Contents of what is going to be written.
        TextRect.center = ((width/2),(height/2))                   # Position of what is going to be written.
        gameDisplay.blit(TextSurf, TextRect)                       # Draws the previously described ontent on the screen. 

        button("START",300,450,100,50,0,bright_green,game_loop)    # Defining the button to start the game
        button("QUIT",600,450,100,50,0,bright_red,quitgame)        # Defining the button to quit the game

        pygame.display.update()                                    # Refreshing the display
     
# Function to prompt door keypad.     
def input():
    screen = pygame.display.set_mode((1039 , 719))                 # Setting up the display window for keyscreen
    win.blit(sc, (0,0))
    font = pygame.font.Font(None, 32)                              # Font is selected.                                    
    input_box = pygame.Rect(100, 100, 140, 32)                     # Setting up an input box.
    color_inactive = pygame.Color('lightskyblue3')                 # Defining colors
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''                                                      # Defining an empty statement for the keypad.
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the aPctive variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)
        if text.count('') == 5:
            return text

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

#Function to prompt the interactive buttons in main menu.
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("consolas",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

# Function to quit the game when QUIT button is pressed in main menu.
def quitgame():
    pygame.QUIT
    quit()

#game_intro()
game_loop()
quit()
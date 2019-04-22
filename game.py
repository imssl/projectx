import os
import random
import pygame
import time
pygame.init()
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
vec = pygame.math.Vector2
scale = 3
sp = pygame.image.load("sp.jpg")
height = 719                                              # Height of the display window
width = 1039                                                # Width of the display window
win = pygame.display.set_mode((height,width))              # Generating the display window    
pygame.display.set_caption("Project X")                    # Title of the display window
clock = pygame.time.Clock()                                # Later to be used for FPS
intro_sound = pygame.mixer.Sound("intro.wav")
gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('PROJECT X')
bg = pygame.image.load('bg.jpg')

# Setting up the display
pygame.display.set_caption("Project X")
win = pygame.display.set_mode((1039, 719))
clock = pygame.time.Clock()
walls = []
papers = []
computers = []
doors = []


# Holds the level layout in a list of strings.

level0 = []

level1 = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWPCW WWWW W WWC WWWWWWWW",
    "W         W       WCWWWWWW",
    "WWW  W      W     W      W",
    "WWW  W      W     W      W",
    "WWW  WWWPP  WWW   WWWWW WW",
    "WW   WWW   WWWW   WC     W",
    "W    WWWW  WWWW   W      W",
    "WW WWWWWWWWWWWWW WWWW    W",
    "W        W          WW  WW",
    "WWWWWWWWDWWWWWWWWWW WW  WW",
    "WWWWWPCW WWW WWWW   WW  WW",
    "WWW      W   WWWW   WW  WW",
    "WWW      W          WW  WW",
    "WWW      WWW        WW  WW",
    "WWW      WWW             W",
    "WWW      WWW        W    W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWW",
    ]

level2 = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWPCW WWWW W WWC WWWWWWWW",
    "W    D    W D     WCWWWWWW",
    "WWW  W      W     W      W",
    "WWW  W      W     W      W",
    "WWW  WWWPP  WWW   WWWWWDWW",
    "WW   WWW   WWWW   WC     W",
    "W    WWWW  WWWW   W      W",
    "WWDWWWWWWWWWWWWWDWWWW    W",
    "W        W          WW  WW",
    "WWWWWWWW WWWWWWWWWWDWW  WW",
    "WWWWWPCW WWW WWWW   WW  WW",
    "WWW      W   WWWW   WW  WW",
    "WWW      W          WW  WW",
    "WWW      WWW        WW  WW",
    "WWW      WWW        D    W",
    "WWW      WWW        W    W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWW",
    ]

def newlevel(level):
    # Nice class to hold a wall rect
    class Wall(object):
        
        def __init__(self, pos):
            walls.append(self)
            self.rect = pygame.Rect(pos[0], pos[1], 40, 40)
    
    # Nice class to hold a door rect
    class Door(object):
        
        def __init__(self, pos):
            doors.append(self)
            self.rect = pygame.Rect(pos[0], pos[1], 40, 40)
            
    # Parse the level string above. W = wall, E = exit
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
           # if col == "P":
           #     paper_rect = pygame.Rect(x, y, 40, 40)
           # if col == "C":
           #     computer_rect = pygame.Rect(x, y, 40, 40)
            elif col == "D":
                Door((x, y))
           #     door_rect = pygame.Rect(x, y, 40, 40)
            x += 40
        y += 40
        x = 0

def game_loop():
    nl= 0
    gameExit = False
    pygame.mixer.Sound.fadeout(intro_sound,3000)
    
    # Initialise pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    newlevel(level1)
    
    # Class for the player
    class Player(object):
        
        def __init__(self):
            self.rect = pygame.Rect(150, 600, 30, 30)
        
        def move(self, dx, dy):
            
            # Move each axis separately. Note that this checks for collisions both times.
            if dx != 0:
                self.move_single_axis(dx, 0)
            if dy != 0:
                self.move_single_axis(0, dy)
        
        def move_single_axis(self, dx, dy):
            
            # Move the rect
            self.rect.x += dx
            self.rect.y += dy

            # If you collide with a wall, move out based on velocity
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
                    
                    if key[pygame.K_SPACE]:
                        if input() == '1234':
                            self.rect = pygame.Rect(310, 360, 30, 30)
                            #newlevel(level2)
    
    player = Player() # Create the player
    while not gameExit:
        clock.tick(30)
        
        # To decide when to kill the main loop and quit the game.
        for event in pygame.event.get():                       
            if event.type == pygame.QUIT:
                gameExit = True
                
        # Move the player if an arrow key is pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-7, 0)
        if key[pygame.K_RIGHT]:
            player.move(7, 0)
        if key[pygame.K_UP]:
            player.move(0, -7)
        if key[pygame.K_DOWN]:
            player.move(0, 7)

        # Draw the scene
        win.blit(bg, (0,0))
        pygame.draw.rect(win, (255, 200, 0), player.rect)
        pygame.display.flip()

def game_intro():

    intro = True
    pygame.mixer.Sound.play(intro_sound)
    
    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisplay.fill(black)
        gameDisplay.blit(sp, (0, 0))
        largeText = pygame.font.SysFont("consolas",115)
        TextSurf, TextRect = text_objects("PROJECT X", largeText)
        TextRect.center = ((width/2),(height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("START",300,450,100,50,0,bright_green,game_loop)
        button("QUIT",600,450,100,50,0,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)

def input():
    screen = pygame.display.set_mode((1039 , 719))
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        #print(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
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

def quitgame():
    pygame.QUIT
    quit()

game_intro()
pygame.init()
pygame.QUIT
quit()
from random import randint
from math import cos, sin, atan, degrees, pi, sqrt
import pygame
pygame.font.init()




#---------------------------------------#
# Basic Constants and Setup             #
#---------------------------------------#

backDrop = pygame.image.load("dungeondrop.jpg")
cursor = pygame.image.load("target.png")
titleText = pygame.font.Font("8-BIT WONDER.ttf", 50)
HUDtext = pygame.font.Font("8-BIT WONDER.ttf", 20)
subtitleText = pygame.font.Font("8-BIT WONDER.ttf", 30)
basicText = pygame.font.Font("8-BIT WONDER.ttf", 20)
smallText = pygame.font.Font("8-BIT WONDER.ttf", 10)
bodyText = pygame.font.Font("8-BIT WONDER.ttf", 15)
pygame.init()
WIDTH = 800
HEIGHT= 600
MIDDLE = int(WIDTH/2.0)
TOP = 0
BOTTOM = HEIGHT
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))

Chamberwidth = []
Chamberheight = []

doors = []
bullets = []
enemies = []
ebullets = []
scorelist = [0]

widthMin = 60
widthMax = 80
heightMin = 40
heightMax = 60


sBoxX = 80
sBoxY = 400
sBoxW = 300
sBoxH = 100

iBoxX = 430
iBoxY = 400
iBoxW = 300
iBoxH = 100

bBoxX = 250
bBoxY = 450
bBoxW = 300
bBoxH = 75

name = "Player 1"

clock = pygame.time.Clock()
FPS = 30
bulletR = 7
#---------------------------------------#
# Colours                               #
#---------------------------------------#

WHITE = (255,255,255)
BLUE = (0,0,255)
RED =   (255,0,0)
BLACK = (  0,  0,  0)
ORANGE= (255, 144, 0)
GREEN = (0, 160, 50)
GREY = (100, 100, 100)
DARKER = (80, 80, 80)
DARKER2 = (60, 60, 60)
DARKER3 = (40, 40, 40)
MAHOGANY = (66,40,53)
outline = 0
xChange = 0
yChange = 0




#---------------------------------------#
# Class Definitions                     #
#---------------------------------------#


# Player
class player(object):

    """Main player, movement attributes"""
    
    def __init__(self, x, y, width, height, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.difX = self.x - ChamberX
        self.difY = self.x - ChamberY
        self.angle = 0
        self.hitBox = pygame.Rect(self.x,self.y,self.width,self.height)

    def draw(self,gameWindow,x,y):
        pygame.draw.rect(gameWindow, ORANGE, (x,y,30,50), 0)
        pygame.draw.rect(gameWindow, BLACK, (x,y,30,50), 2)
        self.difX = self.x - ChamberX
        self.difY = self.y - ChamberY

    def getAngle(self):
        oppa = 0    # oppa means opposite/adjacent.
        if mouseX == 0 and mouseY == 0:
            self.angle = 0        
        elif mouseX == 0 and mouseY > 0:
            self.angle = 90
        elif mouseX == 0 and mouseY < 0:
            self.angle = 270
        else:
            oppa = mouseY/mouseX
    
        atangent = atan(oppa)
    
        if mouseX >0:
            self.angle = degrees(atangent)
        elif mouseX < 0:
            self.angle = degrees(atangent)+180
        

# Bullets
class projectile(object):

    """Projectiles shot by all characters/sprites"""
    
    def __init__(self,x,y,r,colour, difX, difY, xspeed, yspeed):
        self.difX = difX
        self.difY = difY
        self.x = x
        self.y = y
        self.r = r
        self.colour = colour
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.hitBox = pygame.Rect(self.x-self.r,self.y-self.r,self.r*2,self.r*2)

    def update(self):
        self.hitBox = pygame.Rect(self.x-self.r,self.y-self.r,self.r*2,self.r*2)
        
    def draw(self, gameWindow):
        self.update()
        pygame.draw.circle(gameWindow, self.colour, (self.x, self.y), self.r, 0)
        
# Doors
class door(object):

    """Door that activates the next level when the player makes contact"""

    def __init__(self, index, orientation):
        self.index = index
        if self.index == 1:
            self.x = ChamberX - 39
            self.y = ChamberY + (Chamberheight[level]/2-50)
        elif self.index == 2:
            self.x = ChamberX + (Chamberwidth[level]-1)
            self.y = ChamberY + (Chamberheight[level]/2-50)
        elif self.index == 3:
            self.x = ChamberX + (Chamberwidth[level]/2-50)
            self.y = ChamberY - 39
        elif self.index == 4:
            self.x = ChamberX + (Chamberwidth[level]/2-50)
            self.y = ChamberY + (Chamberheight[level] - 1)
        self.orientation = orientation
        if self.orientation == "horizontal":
            self.height = 40
            self.width = 100
        elif self.orientation == "vertical":
            self.height = 100
            self.width = 40
        self.hitBox = pygame.Rect(self.x,self.y,self.width,self.height)
        

    def update(self):
        if self.index == 1:
            self.x = ChamberX - 39
            self.y = ChamberY + (Chamberheight[level]/2-50)
        elif self.index == 2:
            self.x = ChamberX + (Chamberwidth[level]-1)
            self.y = ChamberY + (Chamberheight[level]/2-50)
        elif self.index == 3:
            self.x = ChamberX + (Chamberwidth[level]/2-50)
            self.y = ChamberY - 39
        elif self.index == 4:
            self.x = ChamberX + (Chamberwidth[level]/2-50)
            self.y = ChamberY + (Chamberheight[level] - 1)
        self.hitBox = pygame.Rect(self.x,self.y,self.width,self.height)

    def draw(self,gameWindow):
        self.update()
        pygame.draw.rect(gameWindow, GREY, (self.x,self.y,self.width,self.height), 0)
        if self.index == 1:
            pygame.draw.rect(gameWindow, DARKER, (self.x+20,self.y,self.width/4,self.height), 0)
            pygame.draw.rect(gameWindow, DARKER2, (self.x+10,self.y,self.width/4,self.height), 0)
            pygame.draw.rect(gameWindow, DARKER3, (self.x,self.y,self.width/4,self.height), 0)
            if doorLock == True:
                pygame.draw.rect(gameWindow, RED, (self.x+35,self.y,5,100), 0)

        elif self.index == 2:
            pygame.draw.rect(gameWindow, DARKER, (self.x+10,self.y,self.width/4,self.height), 0)
            pygame.draw.rect(gameWindow, DARKER2, (self.x+20,self.y,self.width/4,self.height), 0)
            pygame.draw.rect(gameWindow, DARKER3, (self.x+30,self.y,self.width/4,self.height), 0)
            if doorLock == True:
                pygame.draw.rect(gameWindow, RED, (self.x,self.y,5,100), 0)

        elif self.index == 3:
            pygame.draw.rect(gameWindow, DARKER, (self.x,self.y+20,self.width,self.height/4), 0)
            pygame.draw.rect(gameWindow, DARKER2, (self.x,self.y+10,self.width,self.height/4), 0)
            pygame.draw.rect(gameWindow, DARKER3, (self.x,self.y,self.width,self.height/4), 0)
            if doorLock == True:
                pygame.draw.rect(gameWindow, RED, (self.x,self.y+35,100,5), 0)

            
        elif self.index == 4:
            pygame.draw.rect(gameWindow, DARKER, (self.x,self.y+10,self.width,self.height/4), 0)
            pygame.draw.rect(gameWindow, DARKER2, (self.x,self.y+20,self.width,self.height/4), 0)
            pygame.draw.rect(gameWindow, DARKER3, (self.x,self.y+30,self.width,self.height/4), 0)
            if doorLock == True:
                pygame.draw.rect(gameWindow, RED, (self.x,self.y,100,5), 0)
        

# Enemies
class enemy(object):
    
    """Enemy sprites"""

    def __init__(self, x, y, width, height, health, speed):
        self.x = ChamberX + x
        self.y = ChamberY + y
        self.width = width
        self.height = height
        self.speed = speed
        self.Xseperation = 10
        self.Yseperation = 10
        self.health = 10
        self.difX = self.x - ChamberX
        self.difY = self.y - ChamberY
        self.originX = self.x + 15
        self.originY = self.y + 25
        self.cdifX = WIDTH/2.0 - self.x + 15
        self.cdifY = HEIGHT/2.0 - self.y + 15
        self.EBxSpeed = 0
        self.EBySpeed = 0
        self.angle = 0
        self.shoot = True
        self.hitBox = pygame.Rect(self.x,self.y,self.width,self.height)
        
    def update(self):
        self.x = ChamberX + self.difX
        self.y = ChamberY + self.difY
        self.originX = self.x + 15
        self.originY = self.y + 25
        self.cdifX = (WIDTH/2.0 - self.originX) + 15
        self.cdifY = (HEIGHT/2.0 - self.originY) + 25
        self.hitBox = pygame.Rect(self.x,self.y,self.width,self.height)
    
    def draw(self, gameWindow):
        self.update()
        self.move()
        pygame.draw.rect(gameWindow, BLUE, (self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(gameWindow, BLACK, (self.x, self.y, self.width, self.height),2)
        self.drawHealth()


    def move(self):
        if character.difX > self.difX:
            self.difX = self.difX + self.speed
        elif character.difX < self.difX:
            self.difX = self.difX - self.speed
        elif character.difY > self.difY:
            self.difY = self.difY + self.speed
        elif character.difY < self.difY:
            self.difY = self.difY - self.speed

    def drawHealth(self):
        pygame.draw.rect(gameWindow, BLACK, (self.x, self.y+60, self.width, 5), 0)
        for i in range(self.health):
            pygame.draw.rect(gameWindow, GREEN, (self.x+(3*i), self.y+60, 3, 5), 0)
        
        
    def getAngle(self):
        eoppa = 0   # eoppa means enemy opposite/adjacent
        if self.cdifX == 0 and self.cdifY == 0:
            self.angle = 0        
        elif self.cdifX == 0 and self.cdifY > 0:
            self.angle = 90
        elif self.cdifX == 0 and self.cdifY < 0:
            self.angle = 270
        else:
            eoppa = self.cdifY/self.cdifX
    
        eatangent = atan(eoppa)
    
        if self.cdifX >0:
            self.angle = degrees(eatangent)
        elif self.cdifX < 0:
            self.angle = degrees(eatangent)+180




#---------------------------------------#
# Functions                             #
#---------------------------------------#


# Draw the title screen.
def titleGameWindow():
    clock.tick(60)
    pygame.event.clear()
    gameWindow.fill(BLACK)
    gameWindow.blit(backDrop, (-120,0))
    if gameOn == False and instructionPage == False:
        drawTitle()
        drawSub()
        drawStartBox()
        drawInstructionBox()
        drawHighScore()
        drawCredits()
    elif instructionPage == True:
        drawInstructionpage()
        drawBackBox()
        
    pygame.display.update()

# Redraw the game window (in-game)
def redrawGameWindow():
    clock.tick(60)
    pygame.event.clear()
    gameWindow.fill(BLACK)
    drawChamber(Chamberwidth[level],Chamberheight[level])
    for door in doors:
        door.draw(gameWindow)
    for bullet in bullets:
        bullet.draw(gameWindow)
    for bullet in ebullets:
        bullet.draw(gameWindow)
    character.draw(gameWindow,character.x,character.y)
    for i in enemies:
        i.draw(gameWindow)
    drawHUD()
    drawPointer()
    pygame.display.update()

# draw the end screen
def drawEndscreen():
    clock.tick(60)
    pygame.event.clear()
    gameWindow.fill(BLACK)
    gameOver = titleText.render("GAME OVER",1,WHITE)
    gameScore = subtitleText.render("Your Score",1,WHITE)
    endScore = subtitleText.render(str(score),1,RED)
    backMessage = subtitleText.render("Press space to go back", 1, WHITE)
    gameWindow.blit(gameOver, (170, 220))
    gameWindow.blit(gameScore, (240, 320))
    gameWindow.blit(endScore, (550, 320))
    gameWindow.blit(backMessage, (110, 390))
    pygame.display.update()



# Draw the title, subtitle text
def drawTitle():
    pygame.draw.rect(gameWindow, WHITE, (45,55,715,150),20)
    title = titleText.render("Dungeon Crawl",1,WHITE)
    gameWindow.blit(title, (85, 100))


def drawSub():
    subtitle = subtitleText.render("An Endless Roguelike", 1, WHITE)
    gameWindow.blit(subtitle, (130,250))

# Draw boxes for navigation
def drawStartBox():
    if mouseHoverS == True:
        pygame.draw.rect(gameWindow, WHITE, (sBoxX,sBoxY,sBoxW,sBoxH),0)
        startBoxOff = subtitleText.render("START", 1, BLACK)
        gameWindow.blit(startBoxOff, (sBoxX+80,sBoxY+30))
    elif mouseHoverS == False:
        pygame.draw.rect(gameWindow, WHITE, (sBoxX,sBoxY,sBoxW,sBoxH),10)
        startBoxOn = subtitleText.render("START", 1, WHITE)
        gameWindow.blit(startBoxOn, (sBoxX+80,sBoxY+30))

def drawInstructionBox():
    if mouseHoverI == True:
        pygame.draw.rect(gameWindow, WHITE, (iBoxX,iBoxY,iBoxW,iBoxH),0)
        instructionBoxOff = subtitleText.render("Controls", 1, BLACK)
        gameWindow.blit(instructionBoxOff, (iBoxX+40,iBoxY+30))
    elif mouseHoverI == False:
        pygame.draw.rect(gameWindow, WHITE, (iBoxX,iBoxY,iBoxW,iBoxH),10)
        instructionBoxOn = subtitleText.render("Controls", 1, WHITE)
        gameWindow.blit(instructionBoxOn, (iBoxX+40,iBoxY+30))

def drawBackBox():
    if mouseHoverB == True:
        pygame.draw.rect(gameWindow, WHITE, (bBoxX,bBoxY,bBoxW,bBoxH),0)
        backBoxOff = subtitleText.render("Back", 1, BLACK)
        gameWindow.blit(backBoxOff, (bBoxX+90,bBoxY+20))
    elif mouseHoverB == False:
        pygame.draw.rect(gameWindow, WHITE, (bBoxX,bBoxY,bBoxW,bBoxH),10)
        backBoxOn = subtitleText.render("Back", 1, WHITE)
        gameWindow.blit(backBoxOn, (bBoxX+90,bBoxY+20))



# Draw the instruction name
def drawInstructionpage():
    pygame.draw.rect(gameWindow, WHITE, (40,40,WIDTH-80,HEIGHT-80),10)
    instructionTitle = subtitleText.render("Controls", 1, WHITE)
    movementControls = subtitleText.render("W A S D", 1, RED)
    movementText = subtitleText.render("Move the character", 1, WHITE)
    aimControl = subtitleText.render("Mouse", 1, RED)
    aimText = subtitleText.render("Aim to shoot", 1, WHITE)
    shotControl = subtitleText.render("Left Click", 1, RED)
    shotText = subtitleText.render("Launch projectiles", 1, WHITE)
    gameWindow.blit(instructionTitle, (275,60))
    gameWindow.blit(movementControls, (100,130))
    gameWindow.blit(movementText, (160,180))
    gameWindow.blit(aimControl, (100,240))
    gameWindow.blit(aimText, (160,290))
    gameWindow.blit(shotControl, (100,350))
    gameWindow.blit(shotText, (160,400))

# Display the highest score.
def drawHighScore():
    highScore = max(scorelist)
    highScoreText = basicText.render("Current High Score  ", 1, WHITE)
    highScoreNumber = basicText.render(str(highScore), 1, RED)
    gameWindow.blit(highScoreText, (230,300))
    gameWindow.blit(highScoreNumber, (600,300))

# Draw the credits

def drawCredits():
    creditText = smallText.render("Jesse Liu    ICS2O 2018", 1, WHITE)
    gameWindow.blit(creditText, (10,580))


    
# Draw the play Area
def drawChamber(Chamberwidth,Chamberheight):
    pygame.draw.rect(gameWindow, MAHOGANY, (ChamberX,ChamberY,Chamberwidth,Chamberheight), 0)
    


# Draw the pointer for aim
def drawPointer():
    mouseX, mouseY = pygame.mouse.get_pos()
    gameWindow.blit(cursor, (mouseX-15,mouseY-15))

# Draw game info - health points, chamber level and info that the player needs.
def drawHUD():
    pygame.draw.rect(gameWindow, WHITE, (0,500,WIDTH,10),0)
    pygame.draw.rect(gameWindow, BLACK, (0,510,WIDTH,90),0)
    drawHealthBar()
    drawName()
    drawLevel()
    drawScore()

# Display the Chamber number
def drawLevel():
    leveltext = HUDtext.render("Chamber "+str(level),1,WHITE)
    gameWindow.blit(leveltext, (250, 520))

# Display the player's score in enemies killed
def drawScore():
    scoreText = HUDtext.render("Score "+str(score),1,WHITE)
    gameWindow.blit(scoreText, (250, 550))
    
# Draw the player's health bar
def drawHealthBar():
    pygame.draw.rect(gameWindow, RED, (20,550,200,30),0)
    pygame.draw.rect(gameWindow, GREEN, (20,550,20*character.health,30))

# Draw the name
def drawName():
    nametext = HUDtext.render(name,1,WHITE)
    gameWindow.blit(nametext, (20, 520))

# Distace function
def distance(x1,y1,x2,y2):
    dist = sqrt((x1-x2)**2+(y1-y2)**2)
    return dist



# Get a random enemy x and y for generation
def getenemyX():
    x = 10*randint(1,(Chamberwidth[level]-30)/10)
    return x

def getenemyY():
    y = 10*randint(1,(Chamberheight[level]-100)/10)
    return y

# Generate enemies.
def generateEnemies():
    if level/5 == 0:
        for i in range(2):
            enemies.append(enemy(getenemyX(),getenemyY(), 30, 50, 5, 2))
    elif level/5 == 1:
        for i in range(3):
            enemies.append(enemy(getenemyX(),getenemyY(), 30, 50, 5, 4))
    else:
        for i in range(4):
            enemies.append(enemy(getenemyX(),getenemyY(), 30, 50, 5, 8))





#---------------------------------------#
# Startup                               #
#---------------------------------------#
TitleScreen = True
Intro = False
mouseHoverS = False
mouseHoverI = False
mouseHoverB = False
instructionPage = False
endGame = False



#---------------------------------------#
# Title Loop                            #
#---------------------------------------#
while TitleScreen:
    mouseX, mouseY = pygame.mouse.get_pos()

    gameOn = False
    titleGameWindow()
   
    if mouseX > sBoxX and mouseX < sBoxX+sBoxW and mouseY > sBoxY and mouseY < sBoxY+sBoxH:
        mouseHoverS = True
    else:
        mouseHoverS = False

    if mouseX > iBoxX and mouseX < iBoxX+iBoxW and mouseY > iBoxY and mouseY < iBoxY+iBoxH:
        mouseHoverI = True
    else:
        mouseHoverI = False
    
    

    for event in pygame.event.get():    
        if mouseHoverI == True and event.type == pygame.MOUSEBUTTONDOWN :
            instructionPage = True
        elif mouseHoverS == True and event.type == pygame.MOUSEBUTTONDOWN:
            gameOn = True


#---------------------------------------#
# Instruction page loop                 #
#---------------------------------------#
    while instructionPage:
        mouseX, mouseY = pygame.mouse.get_pos()
        titleGameWindow()
        if mouseX > bBoxX and mouseX < bBoxX+bBoxW and mouseY > bBoxY and mouseY < bBoxY+bBoxH:
            mouseHoverB = True
        else:
            mouseHoverB = False
        for event in pygame.event.get():    
            if mouseHoverB == True and event.type == pygame.MOUSEBUTTONDOWN :
                instructionPage = False
            


    ## Generate the Starter Chamber.
    level = 0
    score = 0
    lastDoor = 0

    Chamberwidth.append((randint(55,70)*10))
    Chamberheight.append((randint(30,40)*10))
    ChamberX = WIDTH/2-15 - 10*((Chamberwidth[level]/10)/2)
    ChamberY = HEIGHT/2-15 - 10*((Chamberheight[level]/10)/2)

    ## Make instances of the character and doors, which are objects.

    character = player(WIDTH/2 - 15,HEIGHT/2 - 15,30,50,10)

    doors.append(door(1, "vertical"))
    doors.append(door(2, "vertical"))
    doors.append(door(3, "horizontal"))
    doors.append(door(4, "horizontal"))

    ## Ensure the first room has all open doors and begin the game.

    doorLock = False


    mouseX = 0 
    mouseY = 0


#---------------------------------------#
# Main Game Loop                        #
#---------------------------------------#
    
    while gameOn:
        redrawGameWindow()

        # Constantly get the mouse coordinates
        mouseX, mouseY = pygame.mouse.get_pos()

        # Update the mouse coordinates according to the player's center.
        mouseX = mouseX-WIDTH/2.0
        mouseY = mouseY-HEIGHT/2.0
        character.getAngle()

        # Get the angle for the enemies.
        for i in enemies:
            i.getAngle()



        for event in pygame.event.get():

            # Introduce new bullets when the mouse is pressed.
            if event.type == pygame.MOUSEBUTTONDOWN:
                differenceX = character.x+15 - ChamberX
                differenceY = character.y+25 - ChamberY
                BxSpeed = int(round(20*cos(character.angle*pi/180)))
                BySpeed = int(round(20*sin(character.angle*pi/180)))

                # Limit the player to 5 bullets total at a time.
                if len(bullets)<5:
                    bullets.append(projectile(character.x+15, character.y+25, bulletR, RED, differenceX, differenceY, BxSpeed,BySpeed))

        # Introduce the vertical and horizontal velocity for enemies' bullets.
        for v in enemies:
            v.EBxSpeed = int(round(5*cos(v.angle*pi/180)))
            v.EBySpeed = int(round(5*sin(v.angle*pi/180)))

        # Create bullets to be drawn.               
        if len(ebullets)<2:
            for b in enemies:
                ebullets.append(projectile(b.originX, b.originY, bulletR, BLUE, b.difX, b.difY, b.EBxSpeed,b.EBySpeed))
       

        keys = pygame.key.get_pressed()

        # Leave the game if the escape key is pressed.
        if keys[pygame.K_ESCAPE]:
            gameOn = False

        # Move the character inside the chamber.
        if keys[pygame.K_a] and not (character.x == ChamberX):          
            xChange = 10
            yChange = 0
        elif keys[pygame.K_d] and not (character.x+30 == ChamberX + Chamberwidth[level]):      
            xChange = -10
            yChange = 0
        elif keys[pygame.K_w] and not (character.y == ChamberY):  
            xChange = 0
            yChange = 10
        elif keys[pygame.K_s] and not (character.y+50 == ChamberY + Chamberheight[level]):
            xChange = 0
            yChange = -10
        else:
            xChange = 0
            yChange = 0

        # Shift the chamber to simulate relative movement
        ChamberX = ChamberX + xChange
        ChamberY = ChamberY + yChange


        # OBJECT COLLISION

        # Check for collisions between the player's bullets and the enemies. Take away health upon impact, eliminate bullets. 
        for a in range(len(enemies)):       
            lastIndex = len(bullets)-1      
            for j in range(lastIndex,-1,-1):
                if (bullets[j].hitBox).colliderect(enemies[a].hitBox):
                    enemies[a].health -= 1
                    bullets.pop(j)
                    
        # Check for collisions between the enemies' bullets and the player itself. Take away the player's health and eliminate bullets.
        ElastIndex = len(ebullets)-1 
        for i in range(ElastIndex,-1,-1):       
            if (ebullets[i].hitBox).colliderect(character.hitBox):
                character.health = character.health-1
                ebullets.pop(i)


        # If all enemies are eliminated, the player may advance to any door.
        if len(enemies) == 0:
            doorLock = False
        else:
            doorLock = True

        # Check for door collisions
        for i in doors:
            if doorLock == False:
                if (character.hitBox).colliderect(i.hitBox) and i.index == 1:
                    ChamberX = character.x - 10*((Chamberwidth[level]/10)-1)
                    Chamberwidth.append((randint(55,70)*10))
                    Chamberheight.append((randint(30,40)*10))
                    level = level+1
                    doorLock = True
                    generateEnemies()
                elif (character.hitBox).colliderect(i.hitBox) and i.index == 2:
                    ChamberX = character.x-10
                    Chamberwidth.append((randint(55,70)*10))
                    Chamberheight.append((randint(30,40)*10))
                    level = level+1
                    doorLock = True
                    generateEnemies()
                elif (character.hitBox).colliderect(i.hitBox) and i.index == 3:
                    ChamberY = character.y - 10*((Chamberheight[level]/10)+1)
                    Chamberwidth.append((randint(55,70)*10))
                    Chamberheight.append((randint(30,40)*10))
                    level = level+1
                    doorLock = True
                    generateEnemies()
                elif (character.hitBox).colliderect(i.hitBox) and i.index == 4:
                    ChamberY = character.y - 10
                    Chamberwidth.append((randint(55,70)*10))
                    Chamberheight.append((randint(30,40)*10))
                    level = level+1
                    doorLock = True
                    generateEnemies()

        # Move all the players' bullets.
        for bullet in bullets:
            if bullet.x >= ChamberX and bullet.x+bullet.r <= ChamberX+Chamberwidth[0] and bullet.y >= ChamberY and bullet.y+bullet.r <= ChamberY + Chamberheight[0]:
                bullet.difX = bullet.difX + bullet.xspeed
                bullet.difY = bullet.difY + bullet.yspeed
                bullet.x = ChamberX + bullet.difX
                bullet.y = ChamberY + bullet.difY
            else:
                bullets.pop(bullets.index(bullet))

        # Move the enemies'bullets.
        for bullet in ebullets:
            if bullet.x >= ChamberX and bullet.x+bullet.r <= ChamberX+Chamberwidth[0] and bullet.y >= ChamberY and bullet.y+bullet.r <= ChamberY + Chamberheight[0]:
                bullet.difX = bullet.difX + bullet.xspeed
                bullet.difY = bullet.difY + bullet.yspeed
                bullet.x = ChamberX + bullet.difX
                bullet.y = ChamberY + bullet.difY
            else:
                ebullets.pop(ebullets.index(bullet))

        
        # Check for any health depletions and take action where necessary.
        for i in enemies:
            if i.health <= 0:
                enemies.pop(enemies.index(i))
                score = score + 1

        if character.health <= 0:
            gameOn = False
            endGame = True
            scorelist.append(score)

    # Reset all lists.
    enemies = []
    bullets = []
    ebullets = []
    doors = []
    Chamberwidth = []
    Chamberheight = []
    

#---------------------------------------#
# End Loop                              #
#---------------------------------------#
    while endGame:
        drawEndscreen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            endGame = False
            
    

        
#---------------------------------------#    
pygame.quit()
print "Game Over! Thanks for playing!"


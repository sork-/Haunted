import pygame, sys, player, levels, monsters
from pygame.locals import *

gameStates = {0 : 'titleScreen',
              1 : 'map',
              2 : 'newGame',
              3 : 'loadGame'}

BLACK = (0, 0, 0)
TITLEFONTRED = (200, 20, 20)
WHITE = (255, 255, 255)




pygame.init()
FPS=30
fpsClock=pygame.time.Clock()


pygame.mixer.pre_init(44100, -16, 2, 2048)
DISPLAYSURF=pygame.display.set_mode((1280,720))
pygame.display.set_caption('Game')
player1 = player.hunter()
bulletList = pygame.sprite.Group()
baddieList = pygame.sprite.Group()
allSprites = pygame.sprite.Group()


allSprites.add(player1)



class cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.bitmap = pygame.image.load('assets/sprites/cursor.png')
        self.rect = self.bitmap.get_rect()
        
    def moveUp():
        self.rect.y += 64
    def moveDown():
        self.rect.y -= 64

def setGameState(number):
    global state
    state = gameStates[number]

def loadData():
    """This function will load saved data so the the player can
    continue where they left off"""
    pass     #Temporary
    return True
    

def exit_game():
    if state == 1:
        pass     #Once we figure out how to save game data, it will go here.
    pygame.quit()
    sys.exit()
        

def displayText(text, fontFile, fontSize, fontColor, backColor, center):
    font = pygame.font.Font(fontFile, fontSize)
    
    textSurfaceObj = font.render(text, False, fontColor, backColor)
    textRect = textSurfaceObj.get_rect()
    textRect.center = center
    DISPLAYSURF.blit(textSurfaceObj, textRect)
    

def showTitleScreen():
    DISPLAYSURF.fill(BLACK)
    displayText('Haunted', 'assets/ENDOR___.ttf', 80, TITLEFONTRED, BLACK, (640, 260))
    displayText('New Game', 'assets/thyssen.ttf', 20, WHITE, BLACK, (640, 530))
    displayText('Continue', 'assets/thyssen.ttf', 20, WHITE, BLACK, (640, 590))   
    
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == K_w and selector.rect.y == 584:
                selector.rect.y -= 64
            if event.key == K_s and selector.rect.y == 520:
                selector.rect.y += 64
            if event.key == K_RETURN:
                if selector.rect.y == 520:
                    state = setGameState(2)
                if selector.rect.y == 584:
                    state = setGameState(3)
            #If the player presses the escape key the game will exit
            if event.key == K_ESCAPE:
                exit_game()            
        if event.type == QUIT:
            exit_game()
            
        DISPLAYSURF.blit(selector.bitmap, selector.rect)
        pygame.display.update()
        

def showTerrain(grid):
    for row in range(12):
        for column in range(16):
            if grid[row][column] != 0:
                DISPLAYSURF.blit(levels.createTerrain(grid[row][column]), ((column * 64), (row * 64)))

def showPlayer():
    DISPLAYSURF.blit(player1.image, (player1.rect.x, player1.rect.y))
    
def showMenus():
    displayText('Score: ', 'assets/thyssen.ttf', 30, WHITE, BLACK, (1130, 650))
    displayText(str(score), 'assets/thyssen.ttf', 30, WHITE, BLACK, (1180, 650))
    
def updateBullets(spriteList):
    for e in spriteList:
        e.rect.x += e.xvelocity
        if e.rect.x > 1500:
            spriteList.remove(e)

def isTerrainPassable(newPlayerPositionX, newPlayerPositionY):
    if levels.level1Terrain[(newPlayerPositionY // 64)][(newPlayerPositionX // 64)] == 2:
        return False
    else:
        return True
    
#checks if the spot the player is moving too is walkable terrain, and if so
#moves the player there.
def mapEventCheck():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bulletList.add(player1.fireBullet())              
            if event.key == K_ESCAPE:
                exit_game()
        if event.type == QUIT:
            exit_game()
            
    keys = pygame.key.get_pressed()
    if keys[K_a] and isTerrainPassable(player1.rect.x, player1.rect.y + 20):
        player1.rect.x -= 5
    if keys[K_d] and isTerrainPassable(player1.rect.x + 50, player1.rect.y + 20):
        player1.rect.x += 5
    if keys[K_w] and isTerrainPassable(player1.rect.x + 30, player1.rect.y - 50):
        player1.rect.y -= 5
    if keys[K_s] and isTerrainPassable(player1.rect.x + 30, player1.rect.y + 20):
        player1.rect.y += 5
            
def updateMonsters(spriteList):
    if len(spriteList) < 1:
        spriteList.add(monsters.monster())
    for e in spriteList:
        e.rect.x += e.xvelocity
        if e.rect.x < -200:
            spriteList.remove(e)
            
def checkCollision(bullets, monstas):
    for b in bullets:
        for m in monstas:
            if abs(b.rect.x - m.rect.x) < 10 and abs(b.rect.y - m.rect.y) < 18:
                bullets.remove(b)
                monstas.remove(m)
                pygame.mixer.music.load('assets/Sound/ghostDie.xm')
                pygame.mixer.music.play(1, 0.0)                  
                return True
    for m in monstas:
        if abs(player1.rect.x + 40 - m.rect.x) < 5 and abs(player1.rect.y - m.rect.y) < 50:
            exit_game()        
                

        
       
    
state = setGameState(0)
state = 'titleScreen'
score = 0

while True:
    
    tick = 1
    selector = cursor()
    selector.rect.x = 570
    selector.rect.y = 520
    
    while state == 'titleScreen':
        if tick == 1:
            pygame.mixer.music.load('assets/Sound/05.xm')
            pygame.mixer.music.play(-1, 0.0)
            tick += 1
        showTitleScreen()
        
    while state == 'newGame':
        print("in newgame state")
        pygame.mixer.music.stop()
        state = 'map'
    
    while state == 'loadGame':
        loadData()
        state = 'titleScreen'
    
    while state == 'map':
        DISPLAYSURF.fill(BLACK)
        showTerrain(levels.level1Terrain)
        showPlayer()
        bulletList.draw(DISPLAYSURF)
        baddieList.draw(DISPLAYSURF)
        updateBullets(bulletList)
        updateMonsters(baddieList)
        if checkCollision(bulletList, baddieList):
            score += 1
        mapEventCheck()
        showMenus()
        pygame.display.update()
        fpsClock.tick(FPS)


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
DISPLAYSURF=pygame.display.set_mode((1280,720))
pygame.display.set_caption('Game')
player1 = player.hunter()
bulletList = pygame.sprite.Group()
baddieList = pygame.sprite.Group()
allSprites = pygame.sprite.Group()
score = 0

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
        

def displayText(text, fontFile, fontSize, fontColor, backColor, center):
    font = pygame.font.Font(fontFile, fontSize)
    
    textSurfaceObj = font.render(text, False, fontColor, backColor)
    textRect = textSurfaceObj.get_rect()
    textRect.center = center
    DISPLAYSURF.blit(textSurfaceObj, textRect)
    

def showTitleScreen():
    DISPLAYSURF.fill(BLACK)
    displayText('Hunted', 'assets/ENDOR___.ttf', 80, TITLEFONTRED, BLACK, (640, 260))
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
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
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
    displayText(score, 'assets/thyssen.ttf', 30, WHITE, BLACK, (1180, 650))
    
def updateBullets(spriteList):
    for e in spriteList:
        e.rect.x += e.xvelocity
        if e.rect.x > 1500:
            spriteList.remove(e)
        
def mapEventCheck():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_d:
                player1.rect.x += 20
            if event.key == K_a:
                player1.rect.x -= 20
            if event.key == K_w:
                player1.rect.y -= 20
            if event.key == K_s:
                player1.rect.y += 20
            if event.key == K_SPACE:
                bulletList.add(player1.fireBullet())        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
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
                score = score + 1;
        
       
    
state = setGameState(0)
state = 'titleScreen'

while True:
    
    selector = cursor()
    selector.rect.x = 570
    selector.rect.y = 520
    
    while state == 'titleScreen':
        showTitleScreen()
        
    while state == 'newGame':
        print("in newgame state")
        state = 'map'
    
    while state == 'loadGame':
        loadData()
    
    while state == 'map':
        DISPLAYSURF.fill(BLACK)
        showTerrain(levels.level1Terrain)
        showPlayer()
        showMenus()
        bulletList.draw(DISPLAYSURF)
        baddieList.draw(DISPLAYSURF)
        updateBullets(bulletList)
        updateMonsters(baddieList)
        checkCollision(bulletList, baddieList)
        mapEventCheck()
        pygame.display.update()             


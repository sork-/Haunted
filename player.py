import pygame
from pygame.locals import *



class hunter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([64,64], pygame.SRCALPHA, 32)
        self.image.blit(pygame.image.load('assets/sprites/hunter_base.png'), (0, 0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
    
    def fireBullet(self):
        newBullet = bullet()
        newBullet.rect.x = self.rect.x + 58
        newBullet.rect.y = self.rect.y + 39
        newBullet.xvelocity = 15
        pygame.mixer.music.load('assets/Sound/bulletFire.xm')
        pygame.mixer.music.play(1, 0.0)          
        return newBullet
        
    

class bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([64,64], pygame.SRCALPHA, 32)
        self.image.blit(pygame.image.load('assets/sprites/bullet.png'), (0, 0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.xvelocity = 0
        self.yvelocity = 0
        
        








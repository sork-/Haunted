import pygame, random
from pygame.locals import *


class monster(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([64,64], pygame.SRCALPHA, 32)
        self.image.blit(pygame.image.load('assets/sprites/cursor.png'), (0, 0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 1500
        self.rect.y = random.randrange(10, 600)
        self.xvelocity = -8
        
        
        
    
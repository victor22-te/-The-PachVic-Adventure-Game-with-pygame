import pygame
import random
from settings import directory
import state

class enemyCar(pygame.sprite.Sprite):
    def __init__(self, kind, lane):
        super().__init__()
        self.size = (50, 50)
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(directory + "\\sprites\\m1.png").convert_alpha(),self.size),180)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.kind = kind
        self.lane = lane

        if self.kind == 1:
            self.image = pygame.image.load(directory + "\\sprites\\m1.png").convert_alpha()
        elif self.kind == 2:
            self.image = pygame.image.load(directory + "\\sprites\\m2.jpg").convert_alpha()
        elif self.kind == 3:
            self.image = pygame.image.load(directory + "\\sprites\\m3.jpg").convert_alpha()
        elif self.kind == 4:
            self.image = pygame.image.load(directory + "\\sprites\\m1.png").convert_alpha()
        elif self.kind == 5:
            self.image = pygame.image.load(directory + "\\sprites\\m3.jpg").convert_alpha()
        elif self.kind == 6:
            self.image = pygame.image.load(directory + "\\sprites\\m1.png").convert_alpha()
            
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.lane
        self.rect.y = -100

    def moveForward(self):
        if self.rect.y < 650:
            self.rect.y += state.speed
        else:
            self.kill()

class thing(pygame.sprite.Sprite):
    def __init__(self, lane):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(directory + "\\sprites\\moneda.png").convert_alpha(), (50, 50))
        self.rect = self.image.get_rect()
        
        self.rect.y = -100
        self.rect.x = lane

    def moveForward(self):
        if self.rect.y < 650:
            self.rect.y += state.speed
        else:
           self.kill()

class kar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(directory + "\\sprites\\Nave2.jpg").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 400

    def moveRight(self, pixels):
        if self.rect.x < 550:
            self.rect.x += pixels
 
    def moveLeft(self, pixels):
        if self.rect.x > 200:
            self.rect.x -= pixels

class landscape(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = pygame.image.load(directory + "\\sprites\\levelBackground.png").convert_alpha()
        self.rect = self.image.get_rect() 
        self.rect.y = y

    def play(self):
        if self.rect.y < 500:
            self.rect.y += state.speed
        else:
            self.rect.y = -500

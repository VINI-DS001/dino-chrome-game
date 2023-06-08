import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange

main_folder = os.path.dirname(__file__)
images_folder = os.path.join(main_folder, 'images')
sounds_folder = os.path.join(main_folder, 'sounds')

WIDTH = 640
HEIGHT = 400

WHITE = (255,255,255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Dino Game')

sprite_sheet = pygame.image.load(os.path.join(images_folder, 'gameSpritesheet.png')).convert_alpha()

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dinosaur_images = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32,0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.dinosaur_images.append(img)
        self.list_index = 0
        self.image = self.dinosaur_images[self.list_index]
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT - 90) 
    def update(self):
        if self.list_index > 2:
            self.list_index = 0
        self.list_index += 0.25
        self.image = self.dinosaur_images[int(self.list_index)]

class Clouds(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = WIDTH - randrange(30, 300, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = WIDTH
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= 10

all_sprites = pygame.sprite.Group()
dino = Dino()
all_sprites.add(dino)

for i in range(4):
    cloud = Clouds()
    all_sprites.add(cloud)

frame_per_second = pygame.time.Clock()
while True:
    frame_per_second.tick(30)
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    all_sprites.draw(screen)
    all_sprites.update()

    pygame.display.flip()
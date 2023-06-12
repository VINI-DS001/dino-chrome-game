import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange

pygame.init()
pygame.mixer.init()

main_folder = os.path.dirname(__file__)
images_folder = os.path.join(main_folder, 'images')
sounds_folder = os.path.join(main_folder, 'sounds')

WIDTH = 640
HEIGHT = 400

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Dino Chrome Game')

sprite_sheet = pygame.image.load(os.path.join(images_folder, 'gameSpritesheet.png')).convert_alpha()

collision_sound = pygame.mixer.Sound(os.path.join(sounds_folder, 'deathSound.wav'))
collision_sound.set_volume(1)
bump = False

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.jmp_sound = pygame.mixer.Sound(os.path.join(sounds_folder, 'jumpSound.wav'))
        self.jmp_sound.set_volume(1)
        self.dinosaur_images = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.dinosaur_images.append(img)

        self.list_index = 0
        self.image = self.dinosaur_images[self.list_index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.initial_pos_y = HEIGHT - 64 - 96//2
        self.rect.center = [100, HEIGHT - 64]
        self.jmp = False

    def jump(self):
        self.jmp = True
        self.jmp_sound.play()

    def update(self):
        if self.jmp == True:
            if self.rect.y <= 200:
                self.jmp = False
            self.rect.y -= 20
        else:
            if self.rect.y < self.initial_pos_y:
                self.rect.y += 20
            else:
                self.rect.y = self.initial_pos_y

        if self.list_index > 2:
            self.list_index = 0
        self.list_index += 0.25
        self.image = self.dinosaur_images[int(self.list_index)]


class Clouds(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = WIDTH - randrange(30, 300, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = WIDTH
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= 10

class Floor(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - 64
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = WIDTH
        self.rect.x -= 10

class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (WIDTH, HEIGHT - 64)
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = WIDTH
        self.rect.x -= 10

all_sprites = pygame.sprite.Group()
dino = Dino()
all_sprites.add(dino)

for i in range(4):
    cloud = Clouds()
    all_sprites.add(cloud)

for i in range(640*2//64):
    floor = Floor(i)
    all_sprites.add(floor)

cactus = Cactus()
all_sprites.add(cactus)

obstacles_group = pygame.sprite.Group()
obstacles_group.add(cactus)

frame_per_second = pygame.time.Clock()
while True:
    frame_per_second.tick(30)
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if dino.rect.y != dino.initial_pos_y:
                    pass
                else:
                    dino.jump()
    collision = pygame.sprite.spritecollide(dino, obstacles_group, False, pygame.sprite.collide_mask)

    all_sprites.draw(screen)

    if collision and bump == False:
        collision_sound.play()
        bump = True

    if bump == True:
        pass
    else:
        all_sprites.update()

    pygame.display.flip()
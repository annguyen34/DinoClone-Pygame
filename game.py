import pygame
import sys
import os
import random

from pygame import rect
from pygame.constants import K_SPACE


pygame.init()

# HẰNG
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((1100, 600))
pygame.display.set_caption("Dino by AnNguyen")

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load('E:\Project\Python\Dinosaur\Assets\Dino\DinoRun1.png'),
           pygame.image.load('E:\Project\Python\Dinosaur\Assets\Dino\DinoRun2.png')]
JUMPING = pygame.image.load('E:\Project\Python\Dinosaur\Assets\Dino\DinoJump.png')
DUCKING = [pygame.image.load('E:\Project\Python\Dinosaur\Assets\Dino\DinoDuck1.png'),
           pygame.image.load('E:\Project\Python\Dinosaur\Assets\Dino\DinoDuck2.png')]

SMALL_CACTUS = [pygame.image.load('E:\Project\Python\Dinosaur\Assets\Cactus\SmallCactus1.png'),
                pygame.image.load('E:\Project\Python\Dinosaur\Assets\Cactus\SmallCactus2.png'),
                pygame.image.load('E:\Project\Python\Dinosaur\Assets\Cactus\SmallCactus3.png')]
LARGE_CACTUS = [pygame.image.load('E:\Project\Python\Dinosaur\Assets\Cactus\LargeCactus1.png'),
                pygame.image.load('E:\Project\Python\Dinosaur\Assets\Cactus\LargeCactus2.png'),
                pygame.image.load('E:\Project\Python\Dinosaur\Assets\Cactus\LargeCactus3.png')]

BIRD = [pygame.image.load('E:\Project\Python\Dinosaur\Assets\Bird\Bird1.png'),
        pygame.image.load('E:\Project\Python\Dinosaur\Assets\Bird\Bird2.png')]

CLOUD = pygame.image.load('E:\Project\Python\Dinosaur\Assets\Other\Cloud.png')

BG = pygame.image.load('E:\Project\Python\Dinosaur\Assets\Other\Track.png')
class Dino:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        # set img
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        # khủng long luôn luôn chạy
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        # khởi tạo hình ảnh
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        # Chạy nhảy cúi
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        # reset step
        if self.step_index >= 10:
            self.step_index = 0
        # xử lý
        if userInput[pygame.K_SPACE] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_duck:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
    # function chạy nhảy cúi

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel*4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    # vẽ img ra màn hình

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH+random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_Speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_Speed
        if self.rect.x < -SCREEN_WIDTH:
            Obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
        # self.rect.x=random.randint(1100,1200)


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300
        # self.rect.x=random.randint(1000,1500)


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0
        # self.rect.x=random.randint(800,900)

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global game_Speed, x_bg, y_bg, points, Obstacles
    Obstacles = []
    clock = pygame.time.Clock()
    player = Dino()
    cloud = Cloud()
    font = pygame.font.Font('freesansbold.ttf', 20)
    game_Speed = 14
    x_bg = 0
    y_bg = 380
    points = 0
    death_count = 0
    run = True

    def background():
        global x_bg, y_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_bg, y_bg))
        SCREEN.blit(BG, (image_width+x_bg, y_bg))
        if x_bg < -image_width:
            SCREEN.blit(BG, (image_width+x_bg, y_bg))
            x_bg = 0
        x_bg -= game_Speed

    def Score():
        global points, game_Speed
        points += 1
        if points % 100 == 0:
            game_Speed += 1  # update level
        text = font.render("Score: "+str(points), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 40)
        SCREEN.blit(text, text_rect)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        player.draw(SCREEN)
        player.update(userInput)
        if len(Obstacles) == 0:
            if random.randint(0, 2) == 0:
                Obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                Obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                Obstacles.append(Bird(BIRD))
        for i in Obstacles:
            i.draw(SCREEN)
            i.update()
            if player.dino_rect.colliderect(i.rect):
                pygame.time.delay(2000)
                death_count = 1
                menu(death_count)
                death_count = 0
        clock.tick(30)
        background()
        cloud.draw(SCREEN)
        cloud.update()
        Score()
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)
        if death_count == 0:
            text = font.render("Press any key to start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any key to restart", True, (0, 0, 0))
            score = font.render("Your Score: "+str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], ((SCREEN_WIDTH // 2 )- 35, (SCREEN_HEIGHT // 2) - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)

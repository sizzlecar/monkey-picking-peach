# -*- coding = utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
from random import randint

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

LEAF_IMAGE_PATH = "C:\\Users\\Administrator\\Desktop\\leaf.png"


# Player类 -- 继承自pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, initial_position):
        pygame.sprite.Sprite.__init__(self)  # ※ 父构造函数
        self.image = pygame.image.load(LEAF_IMAGE_PATH).convert_alpha()  # ※ 精灵图片Surface
        self.rect = self.image.get_rect()  # ※ 精灵图片的大小
        self.rect.topleft = initial_position  # ※ 精灵图片的位置

        self.speed = 6

    def update(self):
        self.rect.top += self.speed
        if self.rect.left > SCREEN_HEIGHT:
            self.kill()


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# 建立精灵组
group = pygame.sprite.Group()

while True:
    clock.tick(10)
    print(len(group.sprites()))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # 绘制背景
    screen.fill((255, 255, 255))

    # 不断往精灵组中添加精灵
    group.add(Player((randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT // 3))))

    # 将每个精灵更新后显示在Screen上
    group.update()
    group.draw(screen)

    pygame.display.update()

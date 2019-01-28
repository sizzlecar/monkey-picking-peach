import pygame
from pygame.locals import *
from sys import exit
import os

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = cur_path[:cur_path.find("monkey-picking-peach\\") + len("monkey-picking-peach\\")]  # 获取myProject，也就是项目的根路径
images_Path = os.path.abspath(root_path + 'images\\')  # 获取tran.csv文件的路径

# 初始化
pygame.init()

background_image = "C:\\Users\\Administrator\\Desktop\\tmpFile\\蝙蝠侠.jpg"
monkey_image = images_Path + "fugu.png"

# 新建窗口

screen = pygame.display.set_mode((800, 1000), 0, 32)

pygame.display.set_caption("猴子接苹果")

back_surface = pygame.image.load(background_image).convert()
monkey_surface = pygame.image.load(monkey_image).convert_alpha()

x, y = 0, 0
move_x, move_y = 0, 0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == KEYDOWN:
            # 键盘有按下？
            if event.key == K_LEFT:
                # 按下的是左方向键的话，把x坐标减一
                move_x = -1
            elif event.key == K_RIGHT:
                # 右方向键则加一
                move_x = 1
            elif event.key == K_UP:
                # 类似了
                move_y = -5
            elif event.key == K_DOWN:
                move_y = 1
        elif event.type == KEYUP:
            # 如果用户放开了键盘，图就不要动了
            move_x = 0
            move_y = 0

            # 计算出新的坐标
    x += move_x
    y += move_y
    screen.blit(back_surface, (0, 0))
    screen.blit(monkey_surface, (x, y))
    # 在新的位置上画图
    pygame.display.update()

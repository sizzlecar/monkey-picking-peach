import pygame
from sys import exit
from random import randint
import time
import os

# 定义窗口分辨率
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600

current_path = os.path.abspath(os.path.dirname(__file__))
root_path = current_path[:current_path.find("monkey-picking-peach\\") + len("monkey-picking-peach\\")] \
            + "resource\\images\\"
# 图片
BACKGROUND_IMAGE_PATH = root_path + "background.jpg"
MONKEY_IMAGE_PATH = root_path + "monkey.png"
APPLE_IMAGE_PATH = root_path + "apple.png"
JUMP_STATUS = False
OVER_FLAG = False
START_TIME = None
offset = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}

# 定义画面帧率
FRAME_RATE = 60

# 定义动画周期（帧数）
ANIMATE_CYCLE = 30

ticks = 0
clock = pygame.time.Clock()


# 猴子类
class Monkey(pygame.sprite.Sprite):
    # 苹果的数量
    apple_num = 0

    def __init__(self, mon_surface, monkey_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = mon_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = monkey_pos
        self.speed = 5

    # 控制猴子的移动
    def move(self, _offset):
        global JUMP_STATUS
        x = self.rect.left + _offset[pygame.K_RIGHT] - _offset[pygame.K_LEFT]
        y = self.rect.top + _offset[pygame.K_DOWN] - _offset[pygame.K_UP]
        if y < 0:
            self.rect.top = 0
            JUMP_STATUS = True
        elif y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
            JUMP_STATUS = False
        else:
            self.rect.top = y
            JUMP_STATUS = True

        if x < 0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x

    # 接苹果
    def picking_apple(self, app_group):

        # 判断接到几个苹果
        picked_apples = pygame.sprite.spritecollide(self, app_group, True)

        # 添加分数
        self.apple_num += len(picked_apples)

        # 接到的苹果消失
        for picked_apple in picked_apples:
            picked_apple.kill()


# 苹果类
class Apple(pygame.sprite.Sprite):
    def __init__(self, app_surface, apple_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = app_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = apple_pos
        self.speed = 1

    def update(self):
        global START_TIME
        if START_TIME is None:
            START_TIME = time.time()
        self.rect.top += (self.speed * (1 + (time.time() - START_TIME) / 40))
        if self.rect.top > SCREEN_HEIGHT:
            # 苹果落地游戏结束
            global OVER_FLAG
            OVER_FLAG = True
            self.kill()


# 初始化游戏
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("猴子接苹果")

# 载入图片
background_surface = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
monkey_surface = pygame.image.load(MONKEY_IMAGE_PATH).convert_alpha()
apple_surface = pygame.image.load(APPLE_IMAGE_PATH).convert_alpha()

# 创建猴子
monkey = Monkey(monkey_surface, (200, 500))

# 创建苹果组
apple_group = pygame.sprite.Group()

# 分数字体
score_font = pygame.font.SysFont("arial", 40)

# 主循环
while True:

    if OVER_FLAG:
        break

    # 控制游戏最大帧率
    clock.tick(FRAME_RATE)

    # 绘制背景
    screen.blit(background_surface, (0, 0))

    if ticks >= ANIMATE_CYCLE:
        ticks = 0

    # 产生苹果
    if ticks % 30 == 0:
        apple = Apple(apple_surface,
                      [randint(0, SCREEN_WIDTH - apple_surface.get_width()), -apple_surface.get_height()])
        apple_group.add(apple)

    # 控制苹果
    apple_group.update()

    # 绘制苹果组
    apple_group.draw(screen)

    # 绘制猴子
    screen.blit(monkey_surface, monkey.rect)
    ticks += 1

    # 接苹果
    monkey.picking_apple(apple_group)

    # 更新分数
    score_surface = score_font.render(str(monkey.apple_num), True, (0, 0, 255))
    screen.blit(score_surface, (620, 10))
    # 更新屏幕
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # 控制方向
        if event.type == pygame.KEYDOWN:
            if event.key in offset:
                if event.key == pygame.K_UP:
                    offset[event.key] = 80
                else:
                    offset[event.key] = monkey.speed
        elif event.type == pygame.KEYUP:
            if event.key in offset:
                offset[event.key] = 0

    # 移动猴子
    if JUMP_STATUS:
        offset[pygame.K_DOWN] = 5
        offset[pygame.K_UP] = 0
    monkey.move(offset)

# 游戏结束推出界面
score_surface = score_font.render(str(monkey.apple_num), True, (0, 0, 255))
over_surface = score_font.render(u"Game Over!", True, (0, 0, 255))
screen.blit(background_surface, (0, 0))
screen.blit(score_surface, (620, 10))
screen.blit(over_surface, (250, 270))

while True:

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

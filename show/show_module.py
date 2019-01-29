import pygame
from sys import exit
from random import randint
from logic.logic_module import SCREEN_HEIGHT, SCREEN_WIDTH, Monkey, Apple, offset, OVER_FLAG

# 定义画面帧率
FRAME_RATE = 60

# 定义动画周期（帧数）
ANIMATE_CYCLE = 30

ticks = 0
clock = pygame.time.Clock()

# 初始化游戏
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("猴子接苹果")

# 图片
ROOT_PATH = "C:\\Users\\Administrator\\Desktop\\tmpFile\\"
BACKGROUND_IMAGE_PATH = ROOT_PATH + "蝙蝠侠.jpg"
MONKEY_IMAGE_PATH = ROOT_PATH + "timg.jpg"
APPLE_IMAGE_PATH = ROOT_PATH + "leaf.png"

# 载入图片
background_surface = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
monkey_surface = pygame.image.load(MONKEY_IMAGE_PATH).convert_alpha()
apple_surface = pygame.image.load(APPLE_IMAGE_PATH).convert_alpha()

# 创建猴子
monkey = Monkey(monkey_surface, (200, 500))

# 创建苹果组
apple_group = pygame.sprite.Group()

# 主循环
while True:

    if OVER_FLAG:
        print('游戏结束!')
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
                    monkey.jump()
                else:
                    offset[event.key] = monkey.speed
        elif event.type == pygame.KEYUP:
            if event.key in offset:
                offset[event.key] = 0

    # 移动猴子
    monkey.move(offset)

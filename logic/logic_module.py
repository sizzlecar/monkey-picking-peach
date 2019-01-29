import pygame
import time

# 定义窗口分辨率
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 600
OVER_FLAG = False
START_TIME = None
offset = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}


# 猴子类
class Monkey(pygame.sprite.Sprite):
    # 苹果的数量
    apple_num = 0

    jump_height = 10

    def __init__(self, monkey_surface, monkey_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = monkey_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = monkey_pos
        self.speed = 5

    # 控制猴子的移动
    def move(self, _offset):
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        y = self.rect.top - self.jump_height
        if y < 0:
            self.rect.top = 0
        elif y > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top = y

        if x < 0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x

    def jump(self):
        y = self.rect.top - self.jump_height
        if y < 0:
            self.rect.top = 0
        elif y > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top = y

    # 接苹果
    def picking_apple(self, apple_group):

        # 判断接到几个苹果
        picked_apples = pygame.sprite.spritecollide(self, apple_group, True)

        # 添加分数
        self.apple_num += len(picked_apples)

        # 接到的苹果消失
        for picked_apple in picked_apples:
            picked_apple.kill()

        print('当前分数为:', self.apple_num)


# 苹果类
class Apple(pygame.sprite.Sprite):

    def __init__(self, apple_surface, apple_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = apple_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = apple_pos
        self.speed = 2

    def update(self):
        global START_TIME
        if START_TIME is None:
            START_TIME = time.time()
        self.rect.top += (self.speed * (1 + (time.time() - START_TIME) / 20))
        if self.rect.top > SCREEN_HEIGHT:
            # 苹果落地游戏结束
            global OVER_FLAG
            OVER_FLAG = True
            self.kill()
            print('游戏结束！')

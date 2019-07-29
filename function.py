import random
import pygame

# 游戏主窗口的矩形
SCREEN_RECT = pygame.Rect(0, 0, 480, 852)
# 设置事件id
CREATE_ENEMY_EVENT = pygame.USEREVENT + 1
FIRE_EVENT = pygame.USEREVENT + 2
# 敌机图片路径
enemy_path = "./plane/enemy1.png"
# 子弹图片路径
bullet_path = "./plane/bullet.png"
# 英雄图片路径
hero1_path = "./plane/hero1.png"
hero2_path = "./plane/hero2.png"
# 背景图片路径
background_path = "./plane/background.png"


class GamePlane(pygame.sprite.Sprite):
    """ 打飞机游戏的总类 """

    # 重写init方法
    def __init__(self, image_path, speed=2):
        # 调用父类的init方法，因为父类不是object类
        super().__init__()
        # 添加自己特用的实例属性
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.speed = speed

    # 重写更新方法
    def update(self):
        # 通过坐标，让图像动起来
        self.rect.y += self.speed


class Enemy(GamePlane):
    """ 敌机类 """

    # 重写init方法
    def __init__(self):
        # 调用父类中的init方法
        super().__init__(enemy_path)
        # 使速度随机
        self.speed = random.randint(1, 5)
        # 使位置随机
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
        self.rect.bottom = SCREEN_RECT.top

    # 重写update方法
    def update(self):
        super().update()
        if self.rect.top >= SCREEN_RECT.bottom:
            self.kill()


class Bullet(GamePlane):
    """ 子弹类 """

    # 重写init方法
    def __init__(self):
        # 调用父类的init方法
        super().__init__(bullet_path, -2)
        # 改变rect属性的参数
        self.rect.bottom = SCREEN_RECT.top

    # 重写update方法
    def update(self):
        super().update()
        if self.rect.bottom < SCREEN_RECT.top:
            self.kill()


class Hero(GamePlane):
    """ 英雄类 """

    # 重写init方法
    def __init__(self):
        # 调用父类的init方法
        super().__init__(hero1_path, 0)
        # 对英雄的起始位置进行重构
        # self.rect.bottom = SCREEN_RECT.bottom
        # self.centerx = SCREEN_RECT.centerx
        self.rect.center = SCREEN_RECT.center
        self.bullet_grp = pygame.sprite.Group()

    # 重构update方法
    def update(self):
        super().update()
        #检测上下左右边界问题
        if self.rect.left < SCREEN_RECT.left:
            self.rect.left = SCREEN_RECT.left
        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        if self.rect.top < SCREEN_RECT.top:
            self.rect.top = SCREEN_RECT.top
        if self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

    # 开火方法
    def fire(self):
        # 创建一个子弹实例
        bullet = Bullet()
        # 把这个子弹放到飞机的顶部
        # bullet.rect.bottom = self.rect.top + 1
        # bullet.rect.centerx = self.rect.centerx
        bullet.rect.bottom = self.rect.y - 10
        bullet.rect.centerx = self.rect.centerx
        # 创建一个子弹精灵组，把子弹放进组中
        self.bullet_grp.add(bullet)

    # 飞机移动方法
    def move(self, direct):
        if direct == "right":
            self.rect.right += 5
        if direct == "left":
            self.rect.left -= 5
        if direct == "up":
            self.rect.top -= 5
        if direct == "down":
            self.rect.bottom += 5


class Backgroud(GamePlane):
    """ 背景类 """

    # 重写init的方法
    def __init__(self, is_alternative=False):
        super().__init__(background_path)
        # 判断是不是备胎图像，是的话重写rect参数
        if is_alternative:
            self.rect.bottom = SCREEN_RECT.top

    # 重写update方法
    def update(self):
        super().update()
        # 判断背景图片是否移出了游戏主窗口
        if self.rect.top >= SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.top


# ---------------------------------------------------------------------#

class PlaneGame(object):
    # 重写初始化函数，使其成为游戏初始化函数
    def __init__(self):
        # 创建一个游戏主窗口
        self.screen = pygame.display.set_mode((480, 852))
        # 创建一个游戏时钟
        self.clock = pygame.time.Clock()
        # 创建一个英雄
        self.hero = Hero()
        # 创建一个英雄组，并把相关英雄放进组中
        self.hero_grp = pygame.sprite.Group()
        self.hero_grp.add(self.hero)
        # 创建一个敌机
        self.enemy = Enemy()
        # 创建一个敌机组，并把相关敌机放进组中
        self.enemy_grp = pygame.sprite.Group()
        self.enemy_grp.add(self.enemy)
        # 创建两个背景
        self.background_1 = Backgroud(True)
        self.background_2 = Backgroud()
        # 创建一个背景组，并把相关背景放进组中
        self.background_grp = pygame.sprite.Group()
        self.background_grp.add(self.background_1, self.background_2)
        # 设置定时器，并把相关事件与定时器相关联
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        # pygame.time.set_timer(FIRE_EVENT, 200)

    # 键盘事件监听
    def key_listen(self):
        # 获得键盘按键按下的列表
        key = pygame.key.get_pressed()
        # 判断哪个按键按下了
        if key[pygame.K_RIGHT]:
            self.hero.move("right")
        if key[pygame.K_LEFT]:
            self.hero.move("left")
        if key[pygame.K_DOWN]:
            self.hero.move("down")
        if key[pygame.K_UP]:
            self.hero.move("up")
        if key[pygame.K_SPACE]:
            self.hero.fire()
    # 其他事件监听
    def event_listen(self):
        # 遍历事件列表
        for event in pygame.event.get():
            # 判断是否退出
            if event.type == pygame.QUIT:
                self.game_quit()
            # 判断是否创造敌机
            if event.type == CREATE_ENEMY_EVENT:
                enemy_bak = Enemy()
                self.enemy_grp.add(enemy_bak)
            # 判断是否开火
            # if event.type == FIRE_EVENT:
            #     # bullet = Bullet()
            #     # self.hero.bullet_grp.add(bullet)
            #     self.hero.fire()
    # 检测碰撞
    def check_collide(self):
        dic =pygame.sprite.groupcollide(self.hero.bullet_grp, self.enemy_grp, True, True)
        print(dic)
        list = pygame.sprite.spritecollide(self.hero, self.enemy_grp, True)
        if len(list) > 0:
            self.hero.kill()
            self.game_quit()
    # 更新所有精灵组位置
    def update_sprites(self):
        self.enemy_grp.update()
        self.hero_grp.update()
        self.background_grp.update()
        self.hero.bullet_grp.update()


    # 所有精灵组都绘制成涂层
    def draw_sprites(self):
        self.background_grp.draw(self.screen)
        self.hero_grp.draw(self.screen)
        self.enemy_grp.draw(self.screen)
        self.hero.bullet_grp.draw(self.screen)
    # 退出游戏
    def game_quit(self):
        pygame.quit()
        exit()

    # 图像变换
    def image_switch(self, image_path, sprite):
        # 加载图像
        sprite.image = pygame.image.load(image_path)
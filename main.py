import pygame
import function


def main():
    game = function.PlaneGame()

    num = 0
    while True:
        # 设置游戏帧数
        game.clock.tick(60)
        # 图像变更
        if num % 2 == 0:
            game.image_switch(function.hero1_path, game.hero)
        else:
            game.image_switch(function.hero2_path, game.hero)
        # 监听事件
        game.key_listen()
        game.event_listen()
        # 碰撞检测
        game.check_collide()
        # 更新精灵位置
        game.update_sprites()
        # 绘制精灵涂层
        game.draw_sprites()
        # 显示内容
        pygame.display.update()
        # 计数器
        num = num + 1

if __name__ == '__main__':

    main()

from MainMap import MainMap
from MapLoader import MapLoader
import time
import pygame
from StartMenu import StartMenu
from GuiElements import *
from MenuElements import HelpButton
import sys
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.Channel(0).play(pygame.mixer.Sound('data/sounds/wind.wav'), -1)
pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/sounds/fire.wav'), -1)
pygame.mixer.Channel(2).play(pygame.mixer.Sound('data/sounds/step.wav'), -1)
pygame.mixer.Channel(3).play(pygame.mixer.Sound('data/sounds/background.wav'), -1)
screen = pygame.display.set_mode(SCREEN_SIZE, (pygame.FULLSCREEN | pygame.DOUBLEBUF))

def main():
    pygame.mixer.Channel(0).set_volume(0.1)
    pygame.mixer.Channel(1).set_volume(0.2)
    pygame.mixer.Channel(2).set_volume(0)
    pygame.mixer.Channel(3).set_volume(0.3)

    # Убираем курсор, так как есть свой
    pygame.mouse.set_visible(False)

    # Запускаем начальное окно
    StartMenu(screen)

    # Когда начальное окно закрылось загружаем карту
    level = MainMap('world.tmx', MapLoader())

    # Создание игрока
    level.player.health = 100
    level.player.temperature = 100
    level.player.wood = 2

    # Панель состояния игрока
    heath_hud = HealthHUD(level.player)

    # Кнопка помощи
    help_button = HelpButton()
    help_button.x = screen.get_width() - 100
    help_button.y = 50
    help_button.func = level.info_window.open

    # Открываем окно помощи
    level.info_window.open()

    # Делаем костер около игрока вечно горящим, до тех пор, пока не пользователь не закроет окно
    # с инструкциями
    level.objects[(294, 332)].time = 500
    level.objects[(294, 332)].endless = True
    level.info_window.func = lambda: setattr(level.objects[(294, 332)], 'endless', False)

    # Немного усиливаем звук ветра
    pygame.mixer.Channel(0).set_volume(0.2)

    clock = pygame.time.Clock()
    running = True
    while running:
        # Если здоровье падает до нуля, перезапускаем игру
        if level.player.health <= 0:
            return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # Нажатие на клетку
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    level.click_listener(event.pos)
        help_button.update()

        # Отрисовка элементов
        screen.fill((0, 0, 0))
        level.update(screen)
        heath_hud.render(screen)
        help_button.render(screen)
        screen.blit(compass, (SCREEN_WIDTH - compass.get_width(), SCREEN_HEIGHT - compass.get_height()))

        #  Убираем курсор если окно не в фокусе
        if pygame.mouse.get_focused():
            screen.blit(pointer, (pygame.mouse.get_pos()))
        pygame.display.update()
        clock.tick(FPS)



while main():
    pass
pygame.quit()


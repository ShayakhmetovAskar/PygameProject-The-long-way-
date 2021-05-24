import os
import sys

import pygame

pygame.init()
# Размеры экрана
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
SCALE = SCREEN_WIDTH / 1920
pygame.quit()
# Размер одной клетки в декартовой система
TILE_SIZE = 32
MAPS_DIR = 'data/maps'
IMAGES_DIR = 'data/images'
# Разрешение отрисовки
RENDER_SIZE = RENDER_WIDTH, RENDER_HEIGHT = (560, 315)
FPS = 30


def load_image(name):
    fullname = os.path.join(IMAGES_DIR, name)
    if not os.path.isfile(fullname):
        print(f'Файл "{fullname}" не найден')
        sys.exit()
    im = pygame.image.load(fullname)
    return im


# Курсор
pointer = pygame.transform.scale(load_image('gui\\pointer.png'), (24, 34))

# Компас (в углу экрана)
compass = pygame.transform.scale(load_image('compass.png'), (72, 72))


# Перевод из декартовых в изометрические координаты
def to_isometric(x, y):
    return (x - y), (x + y) // 2


# Перевод из изометрических в декартовы координаты
def to_cartesian(x, y):
    return (x + 2 * y) // 2, (2 * y - x) // 2

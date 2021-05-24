import os
from Constants import *
from MapBase import Map
from Entity import *
from TextWindow import TextWindow
import pygame

# Уровень из главного меню
class MenuMap(Map):
    def __init__(self, name, map_loader):
        super().__init__(name, map_loader)
        # смещение камеры
        self.ofx = 0
        self.ofy = 0

    def set_object(self, tile_id, x, y, z):
        # Костер
        if tile_id == 151:
            self.objects[(x, y)] = Fire(x * TILE_SIZE, y * TILE_SIZE, z)

    def render_object(self, tile_id, screen, x, y, coords):
        # Если текстура - костер: нарисовать огонь
        if tile_id == 151:
            self.objects[(x, y)].render(screen, coords)

    def update(self, screen):
        # Звук костра
        pygame.mixer.Channel(1).set_volume(0.2)
        # Отрисовка
        self.render(screen)

    def tile_clicked(self, tile_pos, tile_id):
        pass

    def render_player(self, screen, x, y, z):
        pass

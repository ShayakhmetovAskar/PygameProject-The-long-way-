import pygame
from Constants import *
from MenuElements import *


# Окно, которое можно показывать во время игры содержит в себе текст и кнопку закрыти
class Window:
    def __init__(self):

        # Открыто ли окно
        self.opened = False
        # Тескт, который нужно вывести
        self.text_size = int(26 * SCREEN_HEIGHT // 1080)
        with open('data/rules.txt', encoding='utf8') as rules:
            self.text = rules.read()

        # Рамка окна
        self.frame = BigFrame()
        self.frame.align_center()

        # Кнопка закрытия
        self.button = Button()
        self.button.align_center()
        self.button.y += self.frame.image.get_height() // 2 - self.button.image.get_height()
        self.button.func = self.close

        # Текст
        self.button_text = Text('Ок', size=50)
        self.button_text.align_center()
        self.button_text.y += self.frame.image.get_height() // 2 - self.button.image.get_height()

        self.func = lambda: None  # Функция, которую можно привязать к кнопке закрытия

    # Отрисовка
    def render(self, screen):
        # Обновление состояния кнопки
        self.button.update()
        if self.opened:
            self.frame.render(screen)
            self.button.render(screen)
            self.render_text(self.text, (self.frame.x + 150, self.frame.y + 100),
                             pygame.font.Font(None, self.text_size), screen)
            self.button_text.render(screen)

    # Отрисовка многострочного текста
    def render_text(self, text, pos, font, screen, color=pygame.Color('grey')):
        lines = [line.split() for line in text.splitlines()]
        space = font.size(' ')[0]
        right_bound = self.frame.x + self.frame.image.get_width() - 150
        x, y = pos
        for line in lines:
            for word in line:
                word_surf = font.render(word, 1, color)
                w_w, w_h = word_surf.get_size()
                screen.blit(word_surf, (x, y))
                # Если слово не вмещается в строку, переносим на следующую иначе добавляем пробел
                if x + w_w + space >= right_bound:
                    x = pos[0]
                    y += w_h
                else:
                    x += w_w + space
            x = pos[0]
            y += w_h

    # Функция открытия
    def open(self):
        self.opened = True

    # Функция закрытия, привязана к кнопке
    def close(self):
        if self.opened:
            self.func()
            self.func = lambda: None
            self.opened = False

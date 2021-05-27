import pygame
from Constants import *
from GuiElements import *


# Окно, которое можно показывать во время игры содержит в себе текст и кнопку закрытия
class TextWindow:
    def __init__(self):
        self.opened = False

        # Текст
        self.text = ''
        self.size = 24

        # Рамка окна
        self.frame = BigFrame()
        self.frame.align_center()

        # Кнопка закрытия
        self.button = Button1('Закрыть')
        self.button.align_center()
        self.button.set_pos(self.button.frame.x,
                            self.frame.image.get_height() - self.button.frame.image.get_height())
        self.button.func = self.close

        self.func = lambda: None  # Функция, которую можно привязать к кнопке закрытия
        self.font = pygame.font.SysFont('Arial', int(self.size * SCALE))

    # Отрисовка
    def render(self, screen: pygame.Surface):
        if self.opened:
            # Обновление состояния кнопки
            self.button.update()
            self.frame.render(screen)
            self.button.render(screen)
            self.render_text(self.text, [self.frame.x, self.frame.y],
                            self.font, screen)

    # Отрисовка многострочного текста
    def render_text(self, text, pos, font, screen, color=pygame.Color('grey')):
        lines = [line.split() for line in text.splitlines()]
        margin = int(self.frame.image.get_width() * 0.1)
        space = font.size(' ')[0]
        right_bound = self.frame.x + self.frame.image.get_width() - margin
        pos[0] += margin
        pos[1] += margin
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
        self.dy = 0
        self.opened = True

    def set_text(self, text):
        self.text = text

    # Функция закрытия, привязана к кнопке
    def close(self):
        if self.opened:
            self.func()
            self.func = lambda: None
            self.opened = False

from Constants import *
import pygame

# Изображения элементов графического интерфейса
images = {
    'Frame1': pygame.transform.scale(load_image('gui\\frame1.png'),
                                     (SCREEN_WIDTH // 4, round(SCREEN_HEIGHT / 1.5))),
    'Frame2': pygame.transform.scale(load_image('gui\\frame2.png'),
                                     (SCREEN_WIDTH // 3, SCREEN_WIDTH // 15)),
    'BigFrame': pygame.transform.scale(load_image('gui\\frame1.png'),
                                       (round(SCREEN_WIDTH * 0.8), round(SCREEN_HEIGHT * 0.9))),
    'Button': pygame.transform.scale(load_image('gui\\button.png'),
                                     (SCREEN_WIDTH // 5, SCREEN_WIDTH // 15)),
    'ButtonSelected': pygame.transform.scale(load_image('gui\\button_selected.png'),
                                             (SCREEN_WIDTH // 5, SCREEN_WIDTH // 15)),
    'ButtonPressed': pygame.transform.scale(load_image('gui\\button_pressed.png'),
                                            (SCREEN_WIDTH // 5, SCREEN_WIDTH // 15)),
    'ButtonHelp': load_image('gui\\button_question.png')
}


# Базовый класс для элементов графического интерфейса
class MenuObject:
    def __init__(self, image: pygame.Surface, x=0, y=0):
        self.image = image
        self.x = x
        self.y = y

    # Выравнивание по центру экрана
    def align_center(self):
        self.x = SCREEN_WIDTH // 2 - self.image.get_width() // 2
        self.y = SCREEN_HEIGHT // 2 - self.image.get_height() // 2

    # Отрисовка
    def render(self, screen: pygame.Surface):
        screen.blit(self.image, (self.x, self.y))


# Просто рамка
class Frame1(MenuObject):
    def __init__(self, x=0, y=0):
        super().__init__(images['Frame1'], x, y)


# Просто рамка 2
class Frame2(MenuObject):
    def __init__(self, x=0, y=0):
        super().__init__(images['Frame2'], x, y)


# Большая рамка
class BigFrame(MenuObject):
    def __init__(self, x=0, y=0):
        super().__init__(images['BigFrame'], x, y)


# Кнопка
class Button(MenuObject):
    def __init__(self, x=0, y=0):
        # Изображения кнопки в разных состояниях
        self.image_def = images['Button']
        self.image_pressed = images['ButtonPressed']
        self.image_selected = images['ButtonSelected']
        # Нажата ли кнопка
        self.pressed = False
        # Что выполнить при нажатии
        self.func = lambda: None
        super().__init__(self.image_def, x, y)

    # Обновление кнопки
    def update(self):
        x_, y_ = pygame.mouse.get_pos()
        # Если курсор находится над кнопкой
        if self.x <= x_ < self.x + self.image.get_width() \
                and self.y <= y_ < self.y + self.image.get_height():
            # Если в это время нажата левая кнопка мыши
            if pygame.mouse.get_pressed()[0]:
                # Меняем изображение на нажатую кнопку
                self.image = self.image_pressed
                self.pressed = True
            else:
                self.image = self.image_selected
                # Если кнопка нажата, но кнопка отжата, значит было совершено нажатие на кнопку
                if self.pressed:
                    self.func()
                self.pressed = False
        else:
            self.image = self.image_def
            self.pressed = False


# Кнопка помощи
class HelpButton(Button):
    def __init__(self):
        super().__init__()
        self.image_def = images['ButtonHelp']
        self.image_selected = images['ButtonHelp']
        self.image_pressed = images['ButtonHelp']


# Текст
class Text(MenuObject):
    def __init__(self, text, size=16, x=0, y=0):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.SysFont('', size)
        surface = self.font.render(self.text, True, (210, 125, 44))
        super().__init__(surface, x, y)

    def set_text(self, text):
        self.text = text
        self.image = self.font.render(self.text, True, (210, 125, 44))
        y_ = self.y
        self.align_center()
        self.y = y_

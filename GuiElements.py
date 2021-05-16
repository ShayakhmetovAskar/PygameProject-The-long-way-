from Constants import *


class HealthHUD:
    def __init__(self, player):
        self.player = player

        # Белая полупрозрачная рамка
        self.frame = pygame.Surface((SCREEN_WIDTH // 5, SCREEN_HEIGHT // 5))
        self.frame.set_alpha(150)
        self.frame.fill((255, 255, 255))

        # Полоса здоровья
        self.health_frame = pygame.transform.scale(load_image('hud\\Healthbar.png'),
                                                   (SCREEN_WIDTH // 6, SCREEN_WIDTH // 24))
        self.health_scale = pygame.transform.scale(load_image('hud\\Healthbar scale.png'),
                                                   (SCREEN_WIDTH // 6, SCREEN_WIDTH // 24))

        # Полоса теплоты
        self.thermometer_frame = pygame.transform.scale(load_image('hud\\thermometer frame.png'),
                                                        (SCREEN_WIDTH // 6,
                                                         int(SCREEN_WIDTH // 45.75)))
        self.thermometer_scale = pygame.transform.scale(load_image('hud\\thermometer scale.png'),
                                                        (SCREEN_WIDTH // 6,
                                                         int(SCREEN_WIDTH // 45.75)))

    def render(self, screen):
        screen.blit(self.frame, (0, 0))
        screen.blit(self.health_frame, (SCREEN_WIDTH // 60, SCREEN_HEIGHT // 70))

        health_width = int(self.player.health / 100 * self.health_scale.get_width() * 0.75 +
                           0.25 * self.health_scale.get_width())
        screen.blit(self.health_scale, (SCREEN_WIDTH // 60, SCREEN_HEIGHT // 70),
                    (0, 0, health_width, self.health_scale.get_height()))

        temp_width = int(self.player.temperature / 100 * self.thermometer_scale.get_width())
        screen.blit(self.thermometer_frame, (
            SCREEN_WIDTH // 60, SCREEN_HEIGHT // 70 + int(self.health_frame.get_height() * 1.25)))
        screen.blit(self.thermometer_scale, (
            SCREEN_WIDTH // 60, SCREEN_HEIGHT // 70 + int(self.health_frame.get_height() * 1.25)),
                    (0, 0, temp_width, self.thermometer_scale.get_height()))


class InventoryHud:
    def __init__(self, player):
        self.player = player


# Отображение показателей на экране
class HUD:
    def __init__(self, player):
        # Класс персонажа, откуда будут браться данные
        self.player = player

        # Белая полупрозрачная рамка
        self.frame = pygame.Surface((SCREEN_WIDTH // 5, SCREEN_HEIGHT // 4))
        self.frame.set_alpha(150)
        self.frame.fill((255, 255, 255))

        # Фон полосы здоровья
        self.health_frame = pygame.Surface((SCREEN_WIDTH // 5 - 20, 20))
        self.health_frame.fill((50, 50, 50))
        self.health_frame.set_alpha(128)

        # Полоса здоровья
        self.health = pygame.Rect((11, SCREEN_HEIGHT * 4 // 5 + 21, SCREEN_WIDTH // 5 - 22, 18))

        # Фон полосы теплоты
        self.cold_frame = pygame.Surface((SCREEN_WIDTH // 5 - 20, 20))
        self.cold_frame.fill((50, 50, 50))
        self.cold_frame.set_alpha(128)

        # Полоса теплоты
        self.cold = pygame.Rect((11, SCREEN_HEIGHT * 4 // 5 + 61, SCREEN_WIDTH // 5 - 22, 18))

    def render(self, screen: pygame.Surface):
        # Расчет длин полос состояний
        self.health = pygame.Rect((11, SCREEN_HEIGHT * 4 // 5 + 21,
                                   (SCREEN_WIDTH // 5 - 22) * self.player.health // 100, 18))
        self.cold = pygame.Rect((11, SCREEN_HEIGHT * 4 // 5 + 61,
                                 (SCREEN_WIDTH // 5 - 22) * self.player.temperature // 100, 18))

        # Количество поленьев в инвентаре
        text_wood = pygame.font.Font(None, 30).render(f'Поленьев в инвентаре: {self.player.wood}',
                                                      True, (70, 70, 70))

        # Количество собранных деталей
        text_parts = pygame.font.Font(None, 30).render(f'Деталей собрано: {self.player.parts} из 7',
                                                       True, (70, 70, 70))

        # Последовательная отрисовка элементов на экране
        screen.blit(self.frame, (0, SCREEN_HEIGHT * 3 // 4))
        screen.blit(self.health_frame, (10, SCREEN_HEIGHT * 4 // 5 + 20))
        pygame.draw.rect(screen, (200, 0, 0), self.health)
        screen.blit(self.cold_frame, (10, SCREEN_HEIGHT * 4 // 5 + 61))
        pygame.draw.rect(screen, (0, 0, 150), self.cold)

        screen.blit(text_wood, (10, SCREEN_HEIGHT * 4 // 5 + 100))

        screen.blit(text_parts, (10, SCREEN_HEIGHT * 4 // 5 + 140))


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
    def __init__(self, text, size=30, x=0, y=0):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.SysFont('', int(size * SCALE))
        print(text, int(size * SCALE))
        surface = self.font.render(self.text, True, (210, 125, 44))
        super().__init__(surface, x, y)

    def set_text(self, text):
        self.text = text
        self.image = self.font.render(self.text, True, (210, 125, 44))
        y_ = self.y
        self.align_center()
        self.y = y_


class Button1:
    def __init__(self, text=''):
        # Изображения кнопки в разных состояниях
        self.image_def = images['Button']
        self.image_pressed = images['ButtonPressed']
        self.image_hover = images['ButtonSelected']
        self.frame = MenuObject(self.image_def)
        self.text = Text(text, size=50)
        self.pressed = False
        self.func = lambda: None

    def set_text(self, text, size=50):
        self.text = Text(text=text, size=size)

    def update(self):
        x_, y_ = pygame.mouse.get_pos()
        # Если курсор находится над кнопкой
        if self.frame.x <= x_ < self.frame.x + self.frame.image.get_width() \
                and self.frame.y <= y_ < self.frame.y + self.frame.image.get_height():
            # Если в это время нажата левая кнопка мыши
            if pygame.mouse.get_pressed()[0]:
                # Меняем изображение на нажатую кнопку
                self.frame.image = self.image_pressed
                self.pressed = True
            else:
                self.frame.image = self.image_hover
                if self.pressed:
                    self.func()
                self.pressed = False
        else:
            self.frame.image = self.image_def
            self.pressed = False

    def align_center(self):
        self.frame.align_center()
        self.text.align_center()

    def render(self, screen):
        self.frame.render(screen)
        self.text.render(screen)

    def set_pos(self, x, y):
        self.frame.x = x
        self.frame.y = y
        self.text.x = x + int((self.frame.image.get_width() - self.text.image.get_width()) // 2)
        self.text.y = y + int((self.frame.image.get_height() - self.text.image.get_height()) // 2)

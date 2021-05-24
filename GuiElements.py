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
                                                        (int(SCREEN_WIDTH // 6),
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


class InventoryHUD:
    def __init__(self, player):
        self.player = player
        self.frame = pygame.Surface((SCREEN_WIDTH // 7, SCREEN_HEIGHT // 10))
        self.frame.set_alpha(150)
        self.frame.fill((255, 255, 255))

        self.wood = pygame.transform.scale(load_image('hud\\wood-pile.png'),
                                           (SCREEN_HEIGHT // 13, SCREEN_HEIGHT // 13))
        self.wood_am = -100

        self.boat_parts = pygame.transform.scale(load_image('hud\\paper-boat.png'),
                                                 (SCREEN_HEIGHT // 13, SCREEN_HEIGHT // 13))
        self.boat_parts_am = -100

    def render(self, screen):
        margin = int((self.frame.get_height() - self.wood.get_height()) / 2)
        screen.blit(self.frame, (0, SCREEN_HEIGHT - self.frame.get_height()))
        screen.blit(self.wood, (margin, SCREEN_HEIGHT - self.frame.get_height() + margin))
        screen.blit(self.boat_parts, (
            margin * 2 + self.wood.get_width(), SCREEN_HEIGHT - self.frame.get_height() + margin))
        if self.wood_am != self.player.wood:
            self.wood_am = self.player.wood
            self.wood_text = Text(str(self.player.wood), 35)
            self.wood_text.x = margin + self.wood.get_width() // 8
            self.wood_text.y = SCREEN_HEIGHT - self.frame.get_height() + margin + self.wood.get_height() // 20
        if self.boat_parts_am != self.player.parts:
            self.boat_parts_am = self.player.parts
            self.boat_parts_text = Text(f'{str(self.player.parts)}/9')
            self.boat_parts_text.x = margin * 2 + self.wood.get_width() + self.boat_parts.get_width() // 8
            self.boat_parts_text.y = SCREEN_HEIGHT - self.frame.get_height() + margin + self.boat_parts.get_height() // 20
        self.wood_text.render(screen)
        self.boat_parts_text.render(screen)


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
    'ButtonHelp': load_image('gui\\button_question.png'),
    'ButtonMap': pygame.transform.scale(load_image('gui\\map_button.png'),
                                        (SCREEN_WIDTH // 20, SCREEN_WIDTH // 20)),
    'ButtonMapHover': pygame.transform.scale(load_image('gui\\map_button_hover.png'),
                                             (SCREEN_WIDTH // 20, SCREEN_WIDTH // 20)),
    'ButtonMapPressed': pygame.transform.scale(load_image('gui\\map_button_pressed.png'),
                                               (SCREEN_WIDTH // 20, SCREEN_WIDTH // 20)),
    'ButtonPause': pygame.transform.scale(load_image('gui\\pause_button.png'),
                                          (SCREEN_WIDTH // 20, SCREEN_WIDTH // 20)),
    'ButtonPauseHover': pygame.transform.scale(load_image('gui\\pause_button_hover.png'),
                                               (SCREEN_WIDTH // 20, SCREEN_WIDTH // 20)),
    'ButtonPausePressed': pygame.transform.scale(load_image('gui\\pause_button_pressed.png'),
                                                 (SCREEN_WIDTH // 20, SCREEN_WIDTH // 20)),

    'ButtonTextWindow': pygame.transform.scale(load_image('gui\\text_window_button.png'),
                                               (SCREEN_WIDTH // 20, SCREEN_WIDTH // 20)),
    'ButtonTextWindowHover': pygame.transform.scale(load_image('gui\\text_window_button_hover.png'),
                                                    (SCREEN_WIDTH // 20, SCREEN_WIDTH // 20)),
    'ButtonTextPressed': pygame.transform.scale(load_image('gui\\text_window_button_pressed.png'),
                                                (SCREEN_WIDTH // 20, SCREEN_WIDTH // 20)),
}


# Базовый класс для элементов интерфейса
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


# Текст
class Text(MenuObject):
    def __init__(self, text, size=30, x=0, y=0):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.SysFont('', int(size * SCALE))
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
        self.set_pos(self.frame.x, self.frame.y)

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


class SmallButton(Button1):
    def __init__(self, img_def, img_hov, img_prs):
        super().__init__()
        self.image_def = images[img_def]
        self.image_pressed = images[img_prs]
        self.image_hover = images[img_hov]
        self.frame = MenuObject(self.image_def)


# Текст, появляющийся при наведении курсора на объекты
class Hint:
    def __init__(self):
        self.frame = pygame.Surface((0, 0))
        self.frame.set_alpha(128)
        self.text = Text('')

    def set_text(self, text):
        self.text.set_text(text)
        self.frame = pygame.transform.scale(self.frame,
                                            (int(self.text.image.get_width() * 1.2),
                                             int(self.text.image.get_height() * 1.1)))

    def render(self, screen, pos):
        screen.blit(self.frame, (pos[0] - self.frame.get_width(), pos[1]))
        screen.blit(self.text.image,
                    (pos[0] + int(self.text.image.get_width() * 0.1) - self.frame.get_width(),
                     pos[1] + int(self.text.image.get_height() * 0.05)))

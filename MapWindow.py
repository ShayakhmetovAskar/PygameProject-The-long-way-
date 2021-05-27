from GuiElements import *


# Окно с картой местности
class MapWindow:
    def __init__(self, map_image):

        self.opened = False
        # Рамка окна
        self.frame = BigFrame()
        self.frame.align_center()

        # Кнопка закрытия
        self.button = Button1('Закрыть')
        self.button.align_center()
        self.button.set_pos(self.button.frame.x,
                            self.frame.image.get_height() - self.button.frame.image.get_height())
        self.button.func = self.close

        # Сама карта
        self.map =MenuObject(load_image(f'map_schemes\\{map_image}'))
        height = int(self.frame.image.get_height() * 0.9)
        width = int(self.map.image.get_width() / self.map.image.get_height() * height)
        self.map.image = pygame.transform.scale(self.map.image, (width, height))
        self.map.align_center()

        self.func = lambda: None  # Функция, которую можно привязать к кнопке закрытия

    # Отрисовка
    def render(self, screen):
        if self.opened:
            self.button.update()
            self.frame.render(screen)
            self.map.render(screen)
            self.button.render(screen)

    def open(self):
        self.opened = True

    # Функция закрытия, привязана к кнопке
    def close(self):
        if self.opened:
            self.func()
            self.func = lambda: None
            self.opened = False

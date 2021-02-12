from math import sin, cos, pi

from Map2 import *
from MapLoader import MapLoader
from MenuElements import *


# Стартовое окно игры
class StartMenu:
    def __init__(self, screen: pygame.Surface):
        clock = pygame.time.Clock()

        # Камера в начальном экране крутится по эллипсу
        self.angle = 0  # Текущий угол
        self.Rx = 80  # Радиус по горизонтали
        self.Ry = 30  # Радиус по вертикали

        # Для стартового окна есть отдельная карта
        self.level = Map('start_menu.tmx', MapLoader())

        # Бесконечный костер
        for fire in self.level.objects.values():
            if type(fire) == Fire:
                fire.time = 100000

        # Начальное смещение камеры
        self.ofx = -9 * 32
        self.ofy = -12 * 32

        # Рамки, интерфейса и их выравнивание
        self.frame1 = Frame1()
        self.frame1.align_center()
        self.frame2 = Frame2()
        self.frame2.align_center()
        self.frame1.y += self.frame2.image.get_height() // 2
        self.frame2.y -= self.frame1.image.get_height() // 2

        # Название игры
        self.text_frame1_title = Text('The long way', 100)
        self.text_frame1_title.align_center()
        self.text_frame1_title.y -= self.frame1.image.get_height() // 2

        # Кнопка "Начать игру"
        self.button_start = Button()
        self.button_start.align_center()
        self.button_start.y = self.frame1.y + self.frame1.image.get_height() // 6
        self.text_start = Text('Начать игру', 60)
        self.text_start.align_center()
        self.text_start.y = \
            self.frame1.y + self.frame1.image.get_height() // 6 + \
            self.button_start.image.get_height() // 3
        self.text_start_pressed = Text('Начать игру', 55)
        self.text_start_pressed.align_center()
        self.text_start_pressed.y = \
            self.frame1.y + self.frame1.image.get_height() // 6 + \
            self.button_start.image.get_height() // 3

        # Кнопка "Выйти"
        self.button_exit = Button()
        self.button_exit.align_center()
        self.button_exit.y = \
            self.frame1.y + self.frame1.image.get_height() * 9 // 10 - \
            self.button_exit.image.get_height()
        self.text_quit = Text('Выйти', 60)
        self.text_quit.align_center()
        self.text_quit.y = \
            self.frame1.y + self.frame1.image.get_height() * 9 // 10 + \
            self.button_exit.image.get_height() // 3 - self.button_exit.image.get_height()
        self.text_quit_pressed = Text('Выйти', 55)
        self.text_quit_pressed.align_center()
        self.text_quit_pressed.y = \
            self.frame1.y + self.frame1.image.get_height() * 9 // 10 + \
            self.button_exit.image.get_height() // 3 - self.button_exit.image.get_height()

        # Установка действий на кнопки
        self.button_exit.func = self.exit
        self.button_start.func = self.start

        self.running = True
        while self.running:
            self.camera_moving()
            for event in pygame.event.get():
                # Выход из программы при закрытии окна
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Анимация огня
            for fire in self.level.objects.values():
                if type(fire) == Fire:
                    fire.update()

            # Обновления состояний кнопок
            self.button_start.update()
            self.button_exit.update()

            # Отртисовка уровня
            screen.fill((0, 0, 0))
            self.level.render(screen)

            # Затемнение фона, путем наложения полупрозрачного прямоугольника на экран
            s = pygame.Surface(screen.get_size())
            s.set_alpha(128)
            s.fill((0, 0, 0))
            screen.blit(s, (0, 0))

            # Отрисовка интерфейса поверх уровня
            self.frame1.render(screen)
            self.frame2.render(screen)
            self.text_frame1_title.render(screen)
            self.button_start.render(screen)
            self.button_exit.render(screen)

            # Уменьшение текста при нажатии на кнопку
            if self.button_start.pressed:
                self.text_start_pressed.render(screen)
            else:
                self.text_start.render(screen)

            if self.button_exit.pressed:
                self.text_quit_pressed.render(screen)
            else:
                self.text_quit.render(screen)

            # Отрисовка курсора
            if pygame.mouse.get_focused():
                screen.blit(pointer, (pygame.mouse.get_pos()))

            pygame.display.update()
            clock.tick(FPS)

    # Движение камеры по кругу
    def camera_moving(self):
        self.angle += 3
        if self.angle == 360 * 8:
            self.angle = 0
        self.level.ofx = self.ofx - round(cos(self.rad(self.angle / 8)) * self.Rx)
        self.level.ofy = self.ofy - round(sin(self.rad(self.angle / 8)) * self.Ry)

    # Градусы в радианы
    def rad(self, angle):
        return pi / 180 * angle

    # Выход из программы
    def exit(self):
        pygame.quit()
        sys.exit()

    # Начало игры
    def start(self):
        self.running = False

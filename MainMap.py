import os
from Constants import *
from GuiElements import SmallButton, Button1, Text, Frame2, Frame1
from MapBase import Map
from Entity import *
from TextWindow import TextWindow
import pygame

from MapWindow import MapWindow


class MainMap(Map):

    def __init__(self, name, map_loader):
        super().__init__(name, map_loader)
        # Горизотальное и вертикальное смещение камеры (в декартовой системе координат)
        self.ofx = -258 * TILE_SIZE
        self.ofy = -300 * TILE_SIZE

        self.paused = False

        # Игрок
        self.player = Player(291 * TILE_SIZE, 331 * TILE_SIZE, 2)

        with open('data/texts/box_found.txt', encoding='utf8') as file:
            text = file.read()
            self.box_texts = iter(text.splitlines())


        # Окно с текстом
        self.text_window = TextWindow()
        self.text_window.opened = False
        with open('data/texts/rules.txt', encoding='utf8') as file:
            text = file.read()
            self.text_window.set_text(text)

        self.text_window1 = TextWindow()
        self.text_window1.size = 50
        self.text_window1.opened = False
        self.text_window1.set_text('')

        # Окно с картой
        self.map_window = MapWindow('test.png')
        self.map_window.opened = False

        # Кнопка паузы
        self.btn_pause = SmallButton('ButtonPause', 'ButtonPauseHover', 'ButtonPausePressed')
        self.btn_pause.set_pos(SCREEN_WIDTH - int(self.btn_pause.frame.image.get_width() * 1.2),
                               int(self.btn_pause.frame.image.get_height() * 0.2))
        self.btn_pause.func = lambda: setattr(self, 'paused', True)

        # Кнопка карты
        self.btn_map = SmallButton('ButtonMap', 'ButtonMapHover', 'ButtonMapPressed')
        self.btn_map.set_pos(SCREEN_WIDTH - int(self.btn_map.frame.image.get_width() * 1.2),
                             int(
                                 self.btn_map.frame.image.get_height() * 0.2) + self.btn_pause.frame.image.get_height())
        self.btn_map.func = lambda: self.map_window.open()

        # Кнопка окна с текстом
        self.btn_text_window = SmallButton('ButtonTextWindow', 'ButtonTextWindowHover',
                                           'ButtonTextPressed')
        self.btn_text_window.set_pos(
            SCREEN_WIDTH - int(self.btn_text_window.frame.image.get_width() * 1.2),
            int(
                self.btn_map.frame.image.get_height() * 0.2) + self.btn_map.frame.image.get_height() + self.btn_pause.frame.image.get_height())
        self.btn_text_window.func = lambda: self.text_window.open()

    def set_object(self, tile_id, x, y, z):
        # Если клетка костер - прикрепляем к нему объект огня
        if tile_id == 151:
            self.objects[(x, y)] = Fire(x * TILE_SIZE, y * TILE_SIZE, z)
        # Если клетка сундук - прикрепляем к нему объект сундука
        if tile_id == 145 or tile_id == 147 or tile_id == 161 or tile_id == 177:
            self.objects[(x, y)] = Chest(x * TILE_SIZE, y * TILE_SIZE, z,
                                         self.textures[tile_id],
                                         self.textures[tile_id + 1])

    def render_object(self, tile_id, screen, x, y, coords):
        # Если текстура - костер: нарисовать огонь
        if tile_id == 151:
            self.objects[(x, y)].render(screen, coords)
        elif tile_id == 145 or tile_id == 147 or tile_id == 161 or tile_id == 177:
            self.objects[(x, y)].render(screen, coords)

    def render_player(self, screen, x, y, z):
        if (x, y, z) == self.player.tile_coods():
            self.player.render(screen, (self.player.x + self.ofx, self.player.y + self.ofy))

    def update_player(self):
        # Обновление счетчка цикла анимации игрока
        self.player.update()
        # Анимация игрока по направлению движения
        self.player.walk()

        # Смещение по горизонтали и вертикали и скорость
        dx, dy = 0, 0

        speed = self.player.speed
        if pygame.key.get_pressed()[pygame.K_m]:
            speed = 20

        if pygame.key.get_pressed()[pygame.K_w]:
            dy = -speed
        if pygame.key.get_pressed()[pygame.K_s]:
            dy = speed
        if pygame.key.get_pressed()[pygame.K_a]:
            dx = -speed
        if pygame.key.get_pressed()[pygame.K_d]:
            dx = speed

        if dx and dy:
            # Движение вверх-вниз (в изометрических (экранных) координатах)
            if dx > 0 and dy < 0 or dx < 0 and dy > 0:
                dx = round(speed / 2) if dx > 0 else round(-speed / 2)
                dy = round(speed / 2) if dy > 0 else round(-speed / 2)
            # Движение влево-вправо (в изометрических (экранных) координатах)
            else:
                dx = speed if dx > 0 else -speed
                dy = speed if dy > 0 else -speed
        # Направление движения в изометрических (экранных) координатах
        dir_x, dir_y = 0, 0

        if dx < 0:
            dir_x = -1
        elif dx > 0:
            dir_x = 1

        if dy < 0:
            dir_y = -1
        elif dy > 0:
            dir_y = 1

        if dx or dy:
            self.player.walking = True
            # Проверяем на столкновение будущуюю точку игрока
            if not self.check_collisions(self.player.x + dx, self.player.y + dy, self.player.z):
                self.player.x += dx
                self.player.y += dy

            # Если будущая точка сталкивается с объектом, проверяем на столкновение точку без
            # смещения по одной из осей. Таким образом игрок не останавливается у преграды при
            # диагональном движении
            elif not self.check_collisions(self.player.x + dx, self.player.y,
                                           self.player.z) and dx:
                self.player.x += dx
                dir_y = 0
            elif not self.check_collisions(self.player.x, self.player.y + dy,
                                           self.player.z) and dy:
                self.player.y += dy
                dir_x = 0
            else:
                self.player.walking = False
            # Устанавливаем направление движения игрока.
            self.player.direction_x, self.player.direction_y = dir_x, dir_y

        # Если кнопки на нажаты, то игрок не двигается
        else:
            self.player.walking = False

    def render(self, screen: Surface):
        super().render(screen)
        self.btn_map.render(screen)
        self.btn_text_window.render(screen)
        self.btn_pause.render(screen)
        if self.map_window.opened:
            self.map_window.render(screen)
        if self.text_window.opened:
            self.text_window.render(screen)
        if self.text_window1.opened:
            self.text_window1.render(screen)

    def update(self, screen):

        if self.paused:
            self.pause(screen)
        # Получение координат курсора
        m_pos = pygame.mouse.get_pos()

        # Расстояние до ближайшего костра
        fire_dist = 1000
        for obj in self.objects.values():
            if type(obj) == Fire:
                # Если курсор находится на клетке с костром, то на следующей отрисовке выводим
                # полосу состояния костра
                obj.selected = \
                    (obj.x // TILE_SIZE, obj.y // TILE_SIZE) == self.tile_pos(m_pos)
                # Находим расстояние до ближайшего костра
                if obj.time > 0:
                    fire_dist = min(fire_dist, self.nearness(self.player.x, self.player.y, obj.x - 3,
                                                             obj.y - 16))
                # Обновление костра (Анимация, Уменьшение времени горения)
                obj.update()

        # Если до ближайшего костра меньше 50 пикселей (в декартовой системе)
        # греем игрока, иначе охлаждаем
        if fire_dist < 100:
            self.player.heat()
        else:
            self.player.freeze()

        # Громкость звука костра 1 при расстоянии меньше 150, иначе линейно уменьшается до 0
        # в зависимости от расстояния
        if fire_dist < 150:
            fire_volume = 1
        else:
            fire_volume = max(0, -149 + -1 / 150 * fire_dist + (150 + 1))
        pygame.mixer.Channel(1).set_volume(fire_volume)

        # Звуки шага
        if self.player.walking:
            pygame.mixer.Channel(2).set_volume(0.3)
        else:
            pygame.mixer.Channel(2).set_volume(0)

        # Обновление параметров
        self.update_player()
        self.btn_map.update()
        self.btn_text_window.update()
        self.btn_pause.update()
        # Движение камеры
        self.move_camera()

        # Отрисовка
        self.render(screen)

    # Плавное движение камеры. Изменение смещения зависит от дальности игрока от центра экрана.
    # Камера начинает двигаться только, когда игрок отходит на некоторое расстояние от центра.
    def move_camera(self):
        if self.player.x + self.ofx < self.iso_x_center - 20:
            self.ofx += (self.iso_x_center - self.player.x - self.ofx) // 20
        elif self.player.x + self.ofx > self.iso_x_center + 20:
            self.ofx += (self.iso_x_center - self.player.x - self.ofx) // 30
        if self.player.y + self.ofy < self.iso_y_center - 10:
            self.ofy += (self.iso_y_center - self.player.y - self.ofy) // 20
        elif self.player.y + self.ofy > self.iso_y_center + 10:
            self.ofy += (self.iso_y_center - self.player.y - self.ofy) // 20

    def tile_clicked(self, tile_pos, tile_id):
        if self.nearness(self.player.x, self.player.y, TILE_SIZE * tile_pos[0] - self.iso_of[0],
                         TILE_SIZE * tile_pos[1] - self.iso_of[1]) >= 64:
            return
        if tile_id == 151:
            if self.player.use_wood():
                self.objects[tile_pos].add_time(200)
                # Звук бросания в костер
                self.player.throw_sound.play()
        # Нажатие на клетку с дровами
        elif tile_id == 149 or tile_id == 150:
            if self.player.add_wood():
                # Звук поднятия предмета
                self.player.pick_up_sound.play()
        # Нажатие на клетку с сундуком
        elif tile_id == 145 or tile_id == 147 or tile_id == 161 or tile_id == 177:
            if not self.objects[tile_pos].opened:
                self.text_window1.set_text(next(self.box_texts))
                self.text_window1.open()

                self.player.add_part()
                self.objects[tile_pos].open()
                # Проигрывается звук открытия
                self.player.open_sound.play()
        elif tile_id == 229:
            with open('data/texts/speed_boost.txt', encoding='utf8') as file:
                self.text_window1.set_text(file.read())
            self.text_window1.open()
            self.player.speed = 4

        elif tile_id == 231:
            with open('data/texts/temperature_boost.txt', encoding='utf8') as file:
                self.text_window1.set_text(file.read())
            self.text_window1.open()
            self.player.delta_temperature = -0.01


        # Лодка
        elif tile_id in [296, 297, 298]:
            if self.player.parts >= 7:
                self.text_window.text_size = 60
                with open('data/texts/ending.txt', encoding='utf8') as file:
                    text = file.read()
                self.text_window.text = text
                self.text_window.button.set_text('Выйти из игры')
                self.text_window.button.func = self.exit
                self.text_window.open()

    def pause(self, screen: Surface):
        background = screen.copy()
        clock = pygame.time.Clock()
        # Рамки, интерфейса и их выравнивание
        frame1 = Frame1()
        frame1.align_center()
        frame2 = Frame2()
        frame2.align_center()
        frame1.y += frame2.image.get_height() // 2
        frame2.y -= frame1.image.get_height() // 2

        text_frame1_title = Text(text='Пауза', size=100)
        text_frame1_title.align_center()
        text_frame1_title.y -= frame1.image.get_height() // 2

        button_continue = Button1('Продолжить')
        button_continue.align_center()
        button_continue.set_pos(
            button_continue.frame.x,
            frame1.y + frame1.image.get_height() // 6
        )
        button_continue.func = lambda: setattr(self, 'paused', False)

        button_exit = Button1()
        button_exit.set_text('Выйти (прогресс будет утерян)', size=25)
        button_exit.align_center()
        button_exit.set_pos(
            button_exit.frame.x,
            frame1.y + frame1.image.get_height() * 9 // 10 - button_exit.frame.image.get_height() - button_exit.frame.image.get_height()
        )
        button_exit.func = quit
        # Затемнение фона
        s = pygame.Surface(screen.get_size())
        s.set_alpha(128)
        s.fill((0, 0, 0))
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            screen.blit(background, (0, 0))
            screen.blit(s, (0, 0))
            button_continue.update()
            button_exit.update()
            frame1.render(screen)
            frame2.render(screen)
            text_frame1_title.render(screen)
            button_continue.render(screen)
            button_exit.render(screen)
            # Отрисовка курсора
            if pygame.mouse.get_focused():
                screen.blit(pointer, (pygame.mouse.get_pos()))
            pygame.display.update()
            clock.tick(FPS)

    def game_over(self, screen, ):
        clock = pygame.time.Clock()
        background = screen.copy()
        self.text_window.set_text('Замерз.')
        self.text_window.button.set_text('Выйти в меню')
        self.text_window.button.func = lambda: setattr(self, 'paused', False)
        self.text_window.open()
        self.paused = True
        s = pygame.Surface(screen.get_size())
        s.set_alpha(128)
        s.fill((0, 0, 0))
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            screen.blit(background, (0, 0))
            screen.blit(s, (0, 0))
            self.text_window.render(screen)
            if pygame.mouse.get_focused():
                screen.blit(pointer, (pygame.mouse.get_pos()))
            pygame.display.update()
            clock.tick(FPS)

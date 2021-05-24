from random import choice
from Constants import *
from GuiElements import SmallButton, Button1, Text, Frame2, Frame1, Hint
from MapBase import Map
from Entity import *
from TextWindow import TextWindow
import pygame
from MapWindow import MapWindow


class MainMap(Map):

    def __init__(self, name, map_loader):
        super().__init__(name, map_loader)
        # Начальное смещение камеры (в декартовой системе координат)
        self.ofx = -258 * TILE_SIZE
        self.ofy = -300 * TILE_SIZE

        self.paused = False

        # Игрок
        self.player = Player(291 * TILE_SIZE, 331 * TILE_SIZE, 2)

        # Текст, выводящийся при нахождении деталей
        with open('data/texts/box_found.txt', encoding='utf8') as file:
            text = file.read()
            self.box_texts = iter(text.splitlines())

        # Окно с текстом
        self.text_window = TextWindow()
        self.text_window.opened = False
        # Выводим правила игры
        with open('data/texts/rules.txt', encoding='utf8') as file:
            text = file.read()
            self.text_window.set_text(text)

        # Второе окно с текстом
        self.text_window1 = TextWindow()
        self.text_window1.opened = False
        self.text_window1.set_text('')
        self.text_window1.size = 50

        # Окно с картой
        self.map_window = MapWindow('map.png')
        self.map_window.opened = False

        # Кнопка паузы
        self.btn_pause = SmallButton('ButtonPause', 'ButtonPauseHover', 'ButtonPausePressed')
        self.btn_pause.set_pos(SCREEN_WIDTH - int(self.btn_pause.frame.image.get_width() * 1.2),
                               int(self.btn_pause.frame.image.get_height() * 0.2))
        self.btn_pause.func = lambda: setattr(self, 'paused', True)

        # Кнопка карты
        self.btn_map = SmallButton('ButtonMap', 'ButtonMapHover', 'ButtonMapPressed')
        self.btn_map.set_pos(SCREEN_WIDTH - int(self.btn_map.frame.image.get_width() * 1.2),
                             int(self.btn_map.frame.image.get_height() * 0.2) + self.btn_pause.frame.image.get_height())
        self.btn_map.func = lambda: self.map_window.open()

        # Кнопка открывающая окно с правилами
        self.btn_text_window = SmallButton('ButtonTextWindow', 'ButtonTextWindowHover',
                                           'ButtonTextPressed')
        self.btn_text_window.set_pos(
            SCREEN_WIDTH - int(self.btn_text_window.frame.image.get_width() * 1.2),
            int(
                self.btn_map.frame.image.get_height() * 0.2) + self.btn_map.frame.image.get_height() + self.btn_pause.frame.image.get_height())
        self.btn_text_window.func = lambda: self.text_window.open()

        # Подсказка при наведении на объекты
        self.hint = Hint()

    # Прикрепление объектов к определенным клеткам
    def set_object(self, tile_id, x, y, z):
        # Пламя костра
        if tile_id == 151:
            self.objects[(x, y)] = Fire(x * TILE_SIZE, y * TILE_SIZE, z)
        # Ящик с инструментами
        if tile_id == 145 or tile_id == 147 or tile_id == 161 or tile_id == 177:
            self.objects[(x, y)] = Chest(x * TILE_SIZE, y * TILE_SIZE, z, self.textures[tile_id], self.textures[tile_id + 1])
        # Монументы
        if tile_id == 229 or tile_id == 231:
            self.objects[(x, y)] = Monument(x * TILE_SIZE, y * TILE_SIZE, z)

    # Отрисовка объектов
    def render_object(self, tile_id, screen, x, y, coords):
        if tile_id == 151:
            self.objects[(x, y)].render(screen, coords)
        elif tile_id == 145 or tile_id == 147 or tile_id == 161 or tile_id == 177:
            self.objects[(x, y)].render(screen, coords)

    # Отрисовка игрока
    def render_player(self, screen, x, y, z):
        if (x, y, z) == self.player.tile_coods():
            self.player.render(screen, (self.player.x + self.ofx, self.player.y + self.ofy))

    def update_player(self):
        self.player.update()
        # Анимация игрока по направлению движения
        self.player.walk()
        # Смещение по горизонтали и вертикали и скорость
        dx, dy = 0, 0
        speed = self.player.speed
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
            # Проверяем на столкновение следующую координату игрока
            if not self.check_collisions(self.player.x + dx, self.player.y + dy, self.player.z):
                self.player.x += dx
                self.player.y += dy

            # Если точка сталкивается с объектом, проверяем на столкновение точку без
            # смещения по одной из осей. Так персонаж не будет останавливаться перед препятствием
            # при движении по диагонали
            elif not self.check_collisions(self.player.x + dx, self.player.y, self.player.z) and dx:
                self.player.x += dx
                dir_y = 0
            elif not self.check_collisions(self.player.x, self.player.y + dy, self.player.z) and dy:
                self.player.y += dy
                dir_x = 0
            else:
                self.player.walking = False
            # Устанавливаем направление движения игрока.
            self.player.direction_x, self.player.direction_y = dir_x, dir_y

        # Если кнопки на нажаты, то игрок не двигается
        else:
            self.player.walking = False

    # Отрисовка всех кнопок, окон, подсказок
    def render(self, screen: Surface):
        super().render(screen)
        self.btn_map.render(screen)
        self.btn_text_window.render(screen)
        self.btn_pause.render(screen)
        self.tile_hover(screen, pygame.mouse.get_pos())
        self.map_window.render(screen)
        self.text_window.render(screen)
        self.text_window1.render(screen)

    def update(self, screen):
        if self.paused:
            self.pause(screen)

        m_pos = pygame.mouse.get_pos()
        fire_dist = 5000  # Расстояние до ближайшего костра
        monument_dist = 5000  # Расстояние до ближайшего монумента
        for obj in self.objects.values():
            if type(obj) == Fire:
                # Если курсор находится на клетке с костром, рисуем полосу времени
                obj.selected = (obj.x // TILE_SIZE, obj.y // TILE_SIZE) == self.tile_pos(m_pos)
                # Находим расстояние до ближайшего костра
                if obj.time > 0:
                    fire_dist = min(fire_dist, self.nearness(self.player.x, self.player.y, obj.x - 3, obj.y - 16))
                # Обновление костра (Анимация, Уменьшение времени горения)
                obj.update()
            if type(obj) == Monument and obj.active:
                monument_dist = min(monument_dist, self.nearness(self.player.x, self.player.y, obj.x, obj.y))

        # Если до ближайшего костра меньше 50 пикселей (в декартовой системе)
        # греем игрока, иначе охлаждаем
        if fire_dist < 100:
            self.player.heat()
        else:
            self.player.freeze()

        # Громкость звука костра = 1 на расстоянии меньше 150, иначе плавно уменьшается до 0 в зависимости от расстояния
        if fire_dist < 150:
            fire_volume = 1
        else:
            fire_volume = max(0, -149 + -1 / 150 * fire_dist + (150 + 1))
        pygame.mixer.Channel(1).set_volume(fire_volume)

        # Громкость очень страшной музыки монумента
        pygame.mixer.Channel(4).set_volume(max(0, 1 - monument_dist / 1500))

        # Звук ходьбы
        if self.player.walking:
            pygame.mixer.Channel(2).set_volume(0.3)
        else:
            pygame.mixer.Channel(2).set_volume(0)

        # Обновление всех элементов
        self.update_player()
        self.btn_map.update()
        self.btn_text_window.update()
        self.btn_pause.update()

        # Следование камеры за игроком
        self.move_camera()

        # Отрисовка
        self.render(screen)

    # Плавное движение камеры
    def move_camera(self):
        if self.player.x + self.ofx < self.iso_x_center - 20:
            self.ofx += (self.iso_x_center - self.player.x - self.ofx) // 30
        elif self.player.x + self.ofx > self.iso_x_center + 20:
            self.ofx += (self.iso_x_center - self.player.x - self.ofx) // 30
        if self.player.y + self.ofy < self.iso_y_center - 10:
            self.ofy += (self.iso_y_center - self.player.y - self.ofy) // 30
        elif self.player.y + self.ofy > self.iso_y_center + 10:
            self.ofy += (self.iso_y_center - self.player.y - self.ofy) // 30

    # События при нажатии на экран
    def tile_clicked(self, tile_pos, tile_id):
        # Персонаж должен быть достаточно близок к объекту
        if self.nearness(self.player.x, self.player.y, TILE_SIZE * tile_pos[0] - self.iso_of[0],
                         TILE_SIZE * tile_pos[1] - self.iso_of[1]) >= 64:
            return
        # Костер
        if tile_id == 151:
            if self.player.use_wood():
                self.objects[tile_pos].add_time(250)
                self.player.throw_sound.play()
        # Дрова
        elif tile_id == 149 or tile_id == 150:
            if self.player.add_wood():
                choice([self.player.wood_sound1, self.player.wood_sound2]).play()
        # Ящики с деталями
        elif tile_id == 145 or tile_id == 147 or tile_id == 161 or tile_id == 177:
            if not self.objects[tile_pos].opened:
                self.text_window1.set_text(next(self.box_texts))
                self.text_window1.open()
                self.player.add_part()
                self.objects[tile_pos].open()
                self.player.open_sound.play()

        # Монумент скорости
        elif tile_id == 229:
            if self.objects[tile_pos].active:
                with open('data/texts/speed_boost.txt', encoding='utf8') as file:
                    self.text_window1.set_text(file.read())
                self.text_window1.open()
                self.player.magic_sound.play()
                self.player.speed = 4
                self.objects[tile_pos].active = False
        # Монумент температуры
        elif tile_id == 231:
            if self.objects[tile_pos].active:
                with open('data/texts/temperature_boost.txt', encoding='utf8') as file:
                    self.text_window1.set_text(file.read())
                self.text_window1.open()
                self.player.magic_sound.play()
                self.player.delta_temperature = -0.01
                self.objects[tile_pos].active = False

        # Лодка
        elif tile_id in [296, 297, 298]:
            if self.player.parts >= 9:
                self.text_window.text_size = 60
                with open('data/texts/ending.txt', encoding='utf8') as file:
                    text = file.read()
                self.player.delta_temperature = 0
                self.player.temperature += 1
                self.text_window.text = text
                self.text_window.button.set_text('Выйти из игры')
                self.text_window.button.func = self.exit
                self.text_window.open()
            else:
                self.text_window1.text_size = 60
                with open('data/texts/not_enough_parts.txt', encoding='utf8') as file:
                    text = file.read()
                self.text_window1.text = text
                self.text_window1.open()

    # Текст всплывающий при наведении на объекты
    def tile_hover(self, screen, pos):
        tile_pos = self.tile_pos(pos)
        tile_id = self.map[2][tile_pos[1]][tile_pos[0]]
        # Дрова
        if tile_id == tile_id == 149 or tile_id == 150:
            self.hint.set_text('Охапка дров')
        # Ящики с деталями
        elif tile_id == 145 or tile_id == 147 or tile_id == 161 or tile_id == 177:
            self.hint.set_text('Ящик с деталями')
        # Костер
        elif tile_id == 151:
            text = 'Костер'
            if self.objects[tile_pos].time:
                text += f' (осталось {int(self.objects[tile_pos].time / 15)}с)'
            else:
                text += ' (потух)'
            self.hint.set_text(text)
        # Монументы
        elif tile_id == 229 or tile_id == 231:
            self.hint.set_text('Мистический монумент')
        # Лодка
        elif tile_id in [296, 297, 298]:
            self.hint.set_text('Сломанная лодка')
        # Снеговики
        elif tile_id in [1357, 1358, 1359]:
            self.hint.set_text('Снеговик (смешной)')
        # Вышки
        elif tile_id == 545:
            self.hint.set_text('Охотничья вышка')
        else:
            # При зажатии кнопки j всплывает id клетки
            if pygame.key.get_pressed()[pygame.K_j]:
                self.hint.set_text(str(tile_id))
            else:
                return
        self.hint.render(screen, pos)

    # Окно паузы
    def pause(self, screen: Surface):
        background = screen.copy()
        clock = pygame.time.Clock()
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
            if pygame.mouse.get_focused():
                screen.blit(pointer, (pygame.mouse.get_pos()))
            pygame.display.update()
            clock.tick(FPS)

    # gg((
    def game_over(self, screen, ):
        clock = pygame.time.Clock()
        background = screen.copy()
        with open('data/texts/gameover.txt', encoding='utf8') as file:
            text = file.read()
            self.text_window.set_text(text)
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

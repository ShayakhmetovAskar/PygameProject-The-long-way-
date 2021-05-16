import os
from Constants import *
from MapBase import Map
from Entity import *
from InfoWindow import Window
import pygame


class MainMap(Map):

    def __init__(self, name, map_loader):
        super().__init__(name, map_loader)

        # Горизотальное и вертикальное смещение камеры (в декартовой системе координат)
        self.ofx = -258 * TILE_SIZE
        self.ofy = -300 * TILE_SIZE

        # Игрок
        self.player = Player(291 * TILE_SIZE, 331 * TILE_SIZE, 2)

        # Окно с текстом
        self.info_window = Window()
        self.info_window.opened = False

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

        speed = 2
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
                dx = 1 if dx > 0 else -1
                dy = 1 if dy > 0 else -1
            # Движение влево-вправо (в изометрических (экранных) координатах)
            else:
                dx = 2 if dx > 0 else -2
                dy = 2 if dy > 0 else -2

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

    def update(self, screen):

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
            self.player.set_delta_temperature(0.050)
        else:
            self.player.set_delta_temperature(-0.025)

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

        # Обновление параметров игрока
        self.update_player()
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
                self.player.add_part()
                self.objects[tile_pos].open()
                # Проигрывается звук открытия
                self.player.open_sound.play()

        # Лодка
        elif tile_id in [296, 297, 298]:
            if self.player.parts >= 7:
                self.info_window.text_size = 60
                with open('data/ending.txt', encoding='utf8') as file:
                    text = file.read()
                self.info_window.text = text
                self.info_window.button_text.set_text('Выйти из игры')
                self.info_window.button.func = self.exit
                self.info_window.open()

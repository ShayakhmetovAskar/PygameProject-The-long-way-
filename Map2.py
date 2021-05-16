import os
from Constants import *
from Entity import *
from InfoWindow import Window
import pygame


def load_image(name):
    fullname = os.path.join(IMAGES_DIR, name)
    if not os.path.isfile(fullname):
        print(f'Файл "{fullname}" не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Map:
    def __init__(self, name, map_loader):

        # Центр экрана в изометрических координатах
        self.iso_x_center = (RENDER_WIDTH + 2 * RENDER_HEIGHT) // 4
        self.iso_y_center = (-RENDER_WIDTH + 2 * RENDER_HEIGHT) // 4

        # Разрезание большой текстуры на отдельные
        self.textures = self.slice_texture('snowplains_tileset_final.png', 16, 95, (64, 32))
        # Разрезание карты коллизий
        self.colliders = self.slice_texture('Colliders.png', 16, 95, (32, 32))

        # Горизотальное и вертикальное смещение камеры (в декартовой системе координат)
        self.ofx = -258 * TILE_SIZE
        self.ofy = -300 * TILE_SIZE

        # Изометрическое смещение центра клетки
        self.iso_of = to_isometric(TILE_SIZE // 2, TILE_SIZE // 2)

        # Игрок
        self.player = Player(291 * TILE_SIZE, 331 * TILE_SIZE, 2)

        # Модуль, отвечающий за загрузку карт
        self.loader = map_loader
        # Динамические объекты игры
        self.objects = {}
        # Карта, ширина и высота карты (в блоках), количество слоев
        self.map, self.width, self.height, self.layers = self.set_map(name)

        # Окно информации
        self.info_window = Window()
        self.info_window.opened = False

    # Загрузка карты
    def set_map(self, name):  # Загрузка карты и объектов
        map_, width, height, layers = self.loader.map_load(MAPS_DIR + '/' + name)
        for z in range(layers):
            for y in range(height):
                for x in range(width):
                    tile_id = map_[z][y][x]
                    # Если клетка костер - прикрепляем к нему объект огня
                    if tile_id == 151:
                        self.objects[(x, y)] = Fire(x * TILE_SIZE, y * TILE_SIZE, z)
                    # Если клетка сундук - прикрепляем к нему объект сундука
                    if tile_id == 145 or tile_id == 147 or tile_id == 161 or tile_id == 177:
                        self.objects[(x, y)] = Chest(x * TILE_SIZE, y * TILE_SIZE, z,
                                                     self.textures[tile_id],
                                                     self.textures[tile_id + 1])

        return map_, width, height, layers

    # Функция разрезает изображение на заданное количество текстур
    def slice_texture(self, name, width, height, size):
        texture = load_image(name)
        textures_list = [pygame.Surface([64, 32], pygame.SRCALPHA, 32).convert_alpha()]
        for y in range(height):
            for x in range(width):
                textures_list.append(
                    texture.subsurface((x * size[0], y * size[1], size[0], size[1])))
        return textures_list

    def render(self, screen: Surface):
        # Холст с разшением (RENDER_WIDTH, RENDER_HEIGHT)
        # Для рендера в пониженном разрешение (увеличивает производительность)
        tmp = pygame.Surface(RENDER_SIZE)
        # Отрисовка начинается с нижних слоев
        for z in range(self.layers):
            # Далее отрисовываются только видимые тайлы
            for y in range(max(0, -self.ofy // TILE_SIZE - (
                    self.tile_pos((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))[1] -
                    self.tile_pos((SCREEN_WIDTH, 0))[1]) - 4),
                           min(self.width - 1, (RENDER_HEIGHT - self.ofy) // TILE_SIZE + 4)):
                for x in range(max(0, -self.ofx // TILE_SIZE - 4),
                               min(self.height - 1, (RENDER_WIDTH - self.ofx) // TILE_SIZE + 4)):
                    if (x, y, z) == self.player.tile_coods():
                        self.player.render(tmp, (self.player.x + self.ofx, self.player.y + self.ofy))

                    tile_id = self.map[z][y][x]  # порядковый номер тайла по заданным координатам

                    # Не отрисовываем пустоту и барьер
                    # (барьер невидим в игре, но отображается в редакторе карт)
                    if tile_id != 0 and tile_id != 448:
                        # Изометрические коордаты для отрисовки на экране
                        coords = to_isometric(x * TILE_SIZE + self.ofx, y * TILE_SIZE + self.ofy)
                        if coords[0] + 2 * TILE_SIZE < 0 or coords[
                            0] - 2 * TILE_SIZE > SCREEN_WIDTH or \
                                coords[1] + 2 * TILE_SIZE < 0 or coords[
                            1] - 2 * TILE_SIZE > SCREEN_HEIGHT:
                            continue

                        # Отрисовка текстуры
                        tmp.blit(self.textures[self.map[z][y][x]], coords)

                        # Если текстура - костер: нарисовать огонь
                        if tile_id == 151:
                            self.objects[(x, y)].render(tmp, coords)
                        elif tile_id == 145 or tile_id == 147 or tile_id == 161 or tile_id == 177:
                            self.objects[(x, y)].render(tmp, coords)

                        # Если нажать кнопку h - будет показан процесс отрисовки
                        if pygame.key.get_pressed()[pygame.K_h]:
                            screen.blit(pygame.transform.scale(tmp, (1920, 1080)), (0, 0))
                            pygame.display.flip()

        # Растягиваем вышеобъявленный холст и отрисовываем его на экране
        screen.blit(pygame.transform.scale(tmp, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        self.info_window.render(screen)

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
            # Устанавливаем направление движения игрока. Это пригодится для анимирования на следующем
            # кадре
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

    def check_collisions(self, x, y, z):
        # Проверка на столкновение прилежащих к игроку пикселей
        # Проверяем не конкретную точку, а квадратную область
        for dy in range(32, 40):
            for dx in range(16, 22):
                # Координаты проверяемой точки
                coords = (x + dx) // TILE_SIZE, (y + dy) // TILE_SIZE

                # Смещение точки относительно левого верхнего угла клетки
                offset_x = (x + dx) - (x + dx) // 32 * 32
                offset_y = (y + dy) - (y + dy) // 32 * 32

                # Клетка на карте коллизий на уровне ног и головы персонажа
                collider_bottom = self.colliders[self.map[z - 1][coords[1]][coords[0]]]
                collider_up = self.colliders[self.map[z][coords[1]][coords[0]]]

                # Если точка на карте коллизий имеет цвет то столкновение есть
                # (На карте коллизий красным цветом обозначены непроходимые области текстур)
                if collider_bottom.get_at((offset_x, offset_y))[0] or \
                        collider_up.get_at((offset_x, offset_y))[0]:
                    return True
        return False

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

    # Нахождение расстояния между двумя точками
    def nearness(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    # Определение клетки по изометрическим координатам.
    def tile_pos(self, pos):
        # Так как смещения заданы в декартовых координатай, надо конвертировать их в изометрические
        iso_ofx, iso_ofy = to_isometric(self.ofx, self.ofy)

        # Коэффициенты разрешения. Разрешение отрисовки может отличаться от разрешения экрана
        k_x = RENDER_WIDTH / SCREEN_WIDTH
        k_y = RENDER_HEIGHT / SCREEN_HEIGHT
        # Находим координаты мыши в декартовой системе
        cart_x, cart_y = to_cartesian(pos[0] * k_x - iso_ofx - 30, pos[1] * k_y - iso_ofy)
        return int(cart_x // TILE_SIZE), int(cart_y // TILE_SIZE)

    # Действия при нажатии на клетки поля
    def click_tile(self, pos):
        # Нахождение координат клетки
        tile_pos = self.tile_pos(pos)
        # Нахождение id (типа) клетки
        tile_id = self.map[2][tile_pos[1]][tile_pos[0]]
        # Расстояние от игрока до центра нажатой клетки
        if self.nearness(self.player.x, self.player.y, TILE_SIZE * tile_pos[0] - self.iso_of[0],
                         TILE_SIZE * tile_pos[1] - self.iso_of[1]) < 64:
            # Нажатие на клетку костра
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

            elif tile_id in [296, 297, 298]:
                if self.player.parts >= 7:
                    self.info_window.text_size = 60
                    with open('data/ending.txt', encoding='utf8') as file:
                        text = file.read()
                    self.info_window.text = text
                    self.info_window.button_text.set_text('Выйти из игры')
                    self.info_window.button.func = self.exit
                    self.info_window.open()

    def exit(self):
        pygame.quit()
        sys.exit()

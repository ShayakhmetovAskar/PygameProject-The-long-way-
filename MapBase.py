import os
from abc import abstractmethod

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

        # Изометрическое смещение центра клетки
        self.iso_of = to_isometric(TILE_SIZE // 2, TILE_SIZE // 2)

        # Горизотальное и вертикальное смещение камеры (в декартовой системе координат)
        self.ofx = 0 * TILE_SIZE
        self.ofy = 0 * TILE_SIZE

        # Динамические объекты
        self.objects = {}

        # Модуль, отвечающий за загрузку карт
        self.loader = map_loader
        # Карта, ширина и высота карты (в блоках), количество слоев
        self.map, self.width, self.height, self.layers = self.set_map(name)

    # Загрузка карты
    def set_map(self, name):  # Загрузка карты и объектов
        map_, width, height, layers = self.loader.map_load(MAPS_DIR + '/' + name)
        for z in range(layers):
            for y in range(height):
                for x in range(width):
                    tile_id = map_[z][y][x]
                    self.set_object(tile_id, x, y, z)
        return map_, width, height, layers

    @abstractmethod
    def set_object(self, tile_id, x, y, z):
        pass

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
                    self.render_player(tmp, x, y, z)  # Отрисовка игрока
                    tile_id = self.map[z][y][x]  # порядковый номер тайла по заданным координатам

                    # Не отрисовываем пустоту и барьер
                    # (барьер невидим в игре, но отображается в редакторе карт)
                    if tile_id != 0 and tile_id != 448:
                        # Изометрические коордаты для отрисовки на экране
                        coords = to_isometric(x * TILE_SIZE + self.ofx, y * TILE_SIZE + self.ofy)
                        # Не отрисовываем тайлы, которые не видны на экране
                        if coords[0] + 2 * TILE_SIZE < 0 or coords[0] - 2 * TILE_SIZE > SCREEN_WIDTH or \
                                coords[1] + 2 * TILE_SIZE < 0 or coords[1] - 2 * TILE_SIZE > SCREEN_HEIGHT:
                            continue

                        # Отрисовка текстуры
                        tmp.blit(self.textures[self.map[z][y][x]], coords)

                        self.render_object(tile_id, tmp, x, y, coords)

                        # Если нажать кнопку h - будет показан процесс отрисовки
                        if pygame.key.get_pressed()[pygame.K_h]:
                            screen.blit(pygame.transform.scale(tmp, (1920, 1080)), (0, 0))
                            pygame.display.flip()

        # Растягиваем временный холст и отрисовываем его на экране
        screen.blit(pygame.transform.scale(tmp, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

    @abstractmethod
    def render_object(self, tile_id, screen, x, y, coords):
        pass

    @abstractmethod
    def render_player(self, screen, x, y, z):
        pass

    def update(self, screen):
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
    def click_listener(self, pos):
        # Нахождение координат клетки
        tile_pos = self.tile_pos(pos)
        # Нахождение id клетки
        tile_id = self.map[2][tile_pos[1]][tile_pos[0]]

        self.tile_clicked(tile_pos, tile_id)

    @abstractmethod
    def tile_clicked(self, tile_pos, tile_id):
        pass

    def exit(self):
        pygame.quit()
        sys.exit()
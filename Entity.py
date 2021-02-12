from Constants import *
from pygame import Surface, transform


# Функция разрезает изображение на заданное количество текстур
def slice_texture(name, width, height, size):
    texture = load_image(name)
    textures_list = []
    for y in range(height):
        for x in range(width):
            textures_list.append(
                texture.subsurface((x * size[0], y * size[1], size[0], size[1])))
    return textures_list


# Изображения анимации огня
fire_images = [transform.scale(load_image(f'fire/00{i // 10}{i % 10}.png'), (80, 128)) for i in
               range(1, 31)]

# Изображения анимации персонажа
player_images = [transform.scale(im, (32, 32)) for im in
                 slice_texture('character.png', 9, 8, (56, 65))]


# Базовый класс для игровых сущностей
class Entity:
    def __init__(self, image: Surface, x, y, z):
        self.image = image
        self.x = x
        self.y = y
        self.z = z


# Класс персонажа
class Player(Entity):
    def __init__(self, x, y, z):
        super().__init__(player_images[63], x, y, z)

        # Звук бросания предмета в костер
        self.throw_sound = pygame.mixer.Sound('data/sounds/throw_in_fire.wav')
        # Звук открытия сундука
        self.open_sound = pygame.mixer.Sound('data/sounds/chest_open.wav')
        self.open_sound.set_volume(0.3)
        # Звук поднятия предмета
        self.pick_up_sound = pygame.mixer.Sound('data/sounds/pick_up.wav')
        self.pick_up_sound.set_volume(0.3)

        # Показатели персонажа
        self.health = 100  # Здоровье
        self.temperature = 100  # Температура
        self.wood = 2  # Количество топлива в инвентаре
        self.parts = 0  # Количество собранных деталей

        # Направления движения
        self.direction_x = 1
        self.direction_y = 1

        # Счетчик цикла анимации
        self.cycle = 0
        # Счетчик простоя и скорость анимации
        self.counter, self.freq = 0, 2

        # Границы анимаций
        self.border1, self.border2 = 0, 0
        # Ходит ли персонаж
        self.walking = False

        # размеры изображения персонажа
        self.w = self.image.get_width()
        self.h = self.image.get_height()

    # Обновление изображения персонажа для анимирования
    def update(self):
        if not self.counter:
            if not self.walking:
                self.image = player_images[self.border2 - 1]
                return
            self.cycle -= 1
            if self.cycle < self.border1:
                self.cycle = self.border2 - 1
            self.image = player_images[self.cycle]
        self.counter += 1
        if self.counter >= self.freq:
            self.counter = 0

    # Изменение цикла анимации (зависит от направления движения)
    def walk(self):
        if not self.walking:
            return
        if self.direction_x == 1 and self.direction_y == 0:
            self.border1, self.border2 = 63, 72
        elif self.direction_x == -1 and self.direction_y == 0:
            self.border1, self.border2 = 0, 9
        elif self.direction_x == 0 and self.direction_y == 1:
            self.border1, self.border2 = 45, 54
        elif self.direction_x == 0 and self.direction_y == -1:
            self.border1, self.border2 = 18, 27
        elif self.direction_x == 1 and self.direction_y == 1:
            self.border1, self.border2 = 54, 62
        elif self.direction_x == -1 and self.direction_y == 1:
            self.border1, self.border2 = 36, 45
        elif self.direction_x == 1 and self.direction_y == -1:
            self.border1, self.border2 = 27, 36
        elif self.direction_x == -1 and self.direction_y == -1:
            self.border1, self.border2 = 9, 18
        self.cycle = self.border2 - 1 if self.cycle < self.border1 or self.cycle >= self.border2 \
            else self.cycle

    # Координаты, на которых находится персонаж
    def tile_coods(self):
        return (self.x + 20 * TILE_SIZE // 32) // TILE_SIZE, (
                self.y + 38 * TILE_SIZE // 32) // TILE_SIZE, self.z

    # Изменение температуры персонажа
    def set_delta_temperature(self, dt):
        self.temperature += dt
        if self.temperature < 0:
            self.temperature = 0
            self.health -= 0.1
        elif self.temperature > 100:
            self.temperature = 100

    # Добавление топлива в инвентарь
    def add_wood(self):
        if self.wood < 10:
            self.wood += 1
            return True
        return False

    # Использование топлива из инвентаря
    def use_wood(self) -> bool:
        if self.wood > 0:
            self.wood -= 1
            return True
        return False

    # Добавление ресурса в инвентарь
    def add_part(self):
        self.parts += 1
        if self.parts == 7:
            pass

    # Отрисовка персонажа
    def render(self, screen: Surface, coords):
        screen.blit(self.image, to_isometric(*coords))


# Класс пламени
class Fire(Entity):
    def __init__(self, x, y, z):
        super().__init__(fire_images[0], x, y, z)
        # Бесконечный костер
        self.endless = False
        # Сколько осталось пламени гореть
        self.time = 0
        # Цикл анимации
        self.cycle = 0
        # Счетчик простоя и скорость анимации
        self.counter, self.freq = 0, 2
        # Наведена ли мышь на костер
        self.selected = False
        # Размеры изображения
        self.w, self.h = self.image.get_size()

    # Обновление изображения пламени
    def update(self):
        if not self.counter:
            if self.time == 0:
                if self.cycle >= len(fire_images) - 1:
                    return
            else:
                if self.cycle >= 20:
                    self.cycle = 10
                if not self.endless:
                    self.time -= 1
            self.cycle += 1
            self.image = fire_images[self.cycle]
        self.counter += 1
        if self.counter >= self.freq:
            self.counter = 0

    # Добавление времени горения
    def add_time(self, time):
        if self.time == 0:
            self.cycle = 0
        self.time += time
        # Ограничение на время горения
        if self.time > 2000:
            self.time = 2000

    # Отрисовка
    def render(self, screen: Surface, coords):
        screen.blit(self.image, (coords[0] - 9, coords[1] - 105))
        # Если мышь наведена на костер, рисуется полоса времени горения
        if self.selected:
            # Серый прозрачный фон полосы
            bg = pygame.Surface((60, 5))
            bg.set_alpha(128)
            bg.fill((90, 90, 90))
            screen.blit(bg, (coords[0] + 3, coords[1] - 30))
            # Оранжевая полоса времени
            bar = pygame.Surface((max(0, self.time // 33), 5))
            bar.set_alpha(128)
            bar.fill((255, 51, 0))
            screen.blit(bar, (coords[0] + 3, coords[1] - 30))


# Класс сундука
class Chest(Entity):
    def __init__(self, x, y, z, im_closed, im_open):
        # Был ли сундук открыт
        self.opened = False

        # Изображение открытого сундука и закртытого
        self.im_open = im_open
        self.im_closed = im_closed

        super().__init__(im_closed, x, y, z)

    # Действие при открытии сундука
    def open(self, function=lambda: None):  # function - функция, исполняемая при открытии
        # Исполняем внешнюю функцию
        function()
        # Сундук теперь был открыт
        self.opened = True
        # Картинка заменяется на открытый сундук
        self.image = self.im_open

    # Отрисовка изображения
    def render(self, screen: Surface, coords):
        screen.blit(self.image, coords)

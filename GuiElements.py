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

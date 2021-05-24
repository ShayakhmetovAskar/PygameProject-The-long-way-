from MainMap import MainMap
from MapLoader import MapLoader
import time
from StartMenu import StartMenu
from GuiElements import *

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.Channel(0).play(pygame.mixer.Sound('data/sounds/wind.wav'), -1)
pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/sounds/fire.wav'), -1)
pygame.mixer.Channel(2).play(pygame.mixer.Sound('data/sounds/step.wav'), -1)
pygame.mixer.Channel(3).play(pygame.mixer.Sound('data/sounds/background.wav'), -1)
pygame.mixer.Channel(4).play(pygame.mixer.Sound('data/sounds/monument.wav'), -1)
screen = pygame.display.set_mode(SCREEN_SIZE, (pygame.FULLSCREEN | pygame.DOUBLEBUF))


def main():
    pygame.mixer.Channel(0).set_volume(0.1)
    pygame.mixer.Channel(1).set_volume(0.2)
    pygame.mixer.Channel(2).set_volume(0)
    pygame.mixer.Channel(3).set_volume(0.3)
    pygame.mixer.Channel(4).set_volume(0)

    pygame.mouse.set_visible(False)

    # Запускаем главное меню
    StartMenu(screen)

    # Загружаем игру, когда главное меню закрылось
    level = MainMap('world.tmx', MapLoader())

    level.player.health = 100
    level.player.temperature = 100
    level.player.wood = 2

    # Панели состояния игрока
    heath_hud = HealthHUD(level.player)
    inv_hud = InventoryHUD(level.player)

    # Открываем окно с правилами
    level.text_window.open()

    pygame.mixer.Channel(0).set_volume(0.2)

    clock = pygame.time.Clock()
    running = True
    while running:
        start = time.time()
        # Если здоровье падает до нуля открываем окно game_over
        if level.player.health <= 0:
            level.game_over(screen)
            return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # Нажатие на клетку
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    level.click_listener(event.pos)

        # Отрисовка элементов
        level.update(screen)
        heath_hud.render(screen)
        inv_hud.render(screen)
        screen.blit(compass, (SCREEN_WIDTH - compass.get_width(), SCREEN_HEIGHT - compass.get_height()))

        #  Убираем курсор если окно не в фокусе
        if pygame.mouse.get_focused():
            screen.blit(pointer, (pygame.mouse.get_pos()))
        pygame.display.update()
        framerate = 1 / (time.time() - start)
        clock.tick(FPS)


while main():
    pass
pygame.quit()

import pygame as pg
import random
import time

# Иниацилизация 
pg.init()

class Target:
    # Конструктор
    def __init__(self, pos:tuple, size:tuple, color:tuple, timer:float):
        self.rect = pg.rect.Rect(pos[0], pos[1], size[0], size[1])
        self.color = color
        self.timer = timer
        self.is_alive = True
        self.font = pg.font.SysFont('arial', 16)

    # Функция обновленя
    def update(self):
        if self.is_alive:
            if self.timer <= 0:
                is_alive = False
                self.rect.x = 0
                self.rect.y = 0
                self.rect.width = 0
                self.rect.height = 0
            else:
                self.timer -= 0.1

    # Функция отрисовки
    def draw(self):
        if self.is_alive:
            pg.draw.rect(window, self.color, self.rect)

            text = self.font.render(str(round(self.timer, 1)), False, (0, 0, 0))
            window.blit(text, (self.rect.x + self.rect.width/2 - text.get_width()/2, self.rect.y + self.rect.height/2 - text.get_height()/2))

# Создание часов
clock = pg.time.Clock()

# Создание шрифта
my_font = pg.font.SysFont('arial', 50)

# Создание окна
window = pg.display.set_mode()
pg.display.set_caption('Попади в квадрат!')

# Настройки окна
ww, wh = window.get_width(), window.get_height()
fps = 10

# Цикл приложения
is_app = True
while is_app:
    # Создание переменнной с режимом игры
    game_mode = 0

    # Окрашивание окна
    window.fill((0, 0, 0))

    # Создание заглавка
    text = my_font.render('Выберите сложность игры', False, (255, 255, 255), (50, 50, 50))
    text_rect = text.get_rect()
    text_rect.x = (ww - text_rect.width)/2
    text_rect.y = wh / 5 - text_rect.height/2

    # Создание кнопки легкого уровня сложности 
    button_easy = my_font.render('Легкий', False, (255, 255, 255), (100, 100, 100))
    button_easy_rect = button_easy.get_rect()
    button_easy_rect.x = (ww - button_easy_rect.width)/2
    button_easy_rect.y = wh / 5 * 2 - button_easy_rect.height / 2
    
    # Создание кнопки легкого уровня сложности 
    button_medium = my_font.render('Средний', False, (255, 255, 255), (100, 100, 100))
    button_medium_rect = button_medium.get_rect()
    button_medium_rect.x = (ww - button_medium_rect.width)/2
    button_medium_rect.y = wh / 5 * 3  - button_medium_rect.height / 2
    
    # Создание кнопки легкого уровня сложности 
    button_hard = my_font.render('Сложный', False, (255, 255, 255), (100, 100, 100))
    button_hard_rect = button_hard.get_rect()
    button_hard_rect.x = (ww - button_hard_rect.width)/2
    button_hard_rect.y = wh / 5 * 4 - button_hard_rect.height / 2

    # Отоброжение текста и кнопак
    window.blit(text, text_rect)
    window.blit(button_easy, button_easy_rect)
    window.blit(button_medium, button_medium_rect)
    window.blit(button_hard, button_hard_rect)

    # Обработка событий
    for event in pg.event.get():
        # Обработка выхода из игры
        if event.type == pg.QUIT:
            is_app = False

        # Обработка нажатий клавиши
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                is_app = False

        # Обработка нажатий мышки
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button_easy_rect.collidepoint(event.pos):
                    game_mode = 1
                    target_size = int(ww * 30 / 1280)
                    target_timer = 2
                elif button_medium_rect.collidepoint(event.pos):
                    game_mode = 2
                    target_size = int(ww * 20 / 1280)
                    target_timer = 1.5
                elif button_hard_rect.collidepoint(event.pos):
                    game_mode = 3
                    target_size = int(ww * 10 / 1280)
                    target_timer = 1

    # Начало игры
    if game_mode != 0: 
        # Создание игрока
        player_score = 0

        # Игрвой цикл
        is_game = True
        while is_game:
            # Создание мишени
            target = Target((random.randint(0, ww-target_size), random.randint(0, wh-target_size)), (target_size, target_size), (255, 255, 0), target_timer)

            # Цикл раунда
            is_round = True
            while is_round:
                # Закрашишивание окна
                window.fill((0, 0, 0))

                # Отрисовка количества очков
                score = my_font.render(str(player_score), False, (255, 255, 255))
                window.blit(score, ((ww-score.get_width())/2, 0))

                # Отрисовка оставлегося времени
                left_time = my_font.render(str(round(target.timer, 1)), False, (255, 255, 255))
                window.blit(left_time, ((ww-left_time.get_width())/2, wh-left_time.get_height()))

                # Обновление и отрисвка мишени
                target.draw()
                target.update()
                
                # Обработка событий
                for event in pg.event.get():
                    # Обработка выхода из игры
                    if event.type == pg.QUIT:
                        is_app = False
                        is_game = False
                        is_round = False

                    # Обработка нажатий клавиши
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            is_game = False
                            is_round = False
                            game_mode = 0

                    # Обработка нажатий мышки
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1 or event.button == 3:
                            if target.rect.collidepoint(event.pos):
                                player_score += 1
                            else:
                                player_score -= 1

                            is_round = False

                # Вырубание игры если время мишени истекло
                if target.timer <= 0 and is_round:
                    is_round = False
                    player_score -= 1

                # Обновление окна
                pg.display.update()
                clock.tick(fps)

    # Обновление окна
    pg.display.update()
    clock.tick(fps)
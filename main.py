import pygame as pg
import random
import time

# Иниацилизация 
pg.init()

# Создание окна
window = pg.display.set_mode()
pg.display.set_caption('Попади в квадрат!')

# Настройки окна
WW, WH = window.get_width(), window.get_height()
FPS = 10

class Target:
    # Конструктор
    def __init__(self, pos:tuple, size:int, color:tuple, timer:float):
        self.rect = pg.rect.Rect(pos[0], pos[1], size, size)
        self.color = color
        self.timer = timer
        self.is_alive = True
        self.font = pg.font.SysFont('arial', int((size-size*0.75) * WW / 1280))

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
my_font = pg.font.SysFont('arial', int(50 * WW / 1280))

# Переменная с цветом мишени
target_color = [255, 255, 0]

# Переменная с выбранным режимом изменения цвета мишени
target_change_color = 0

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
    text_rect.x = (WW - text_rect.width)/2
    text_rect.y = WH / 5 - text_rect.height/2

    # Создание кнопки легкого уровня сложности 
    button_easy = my_font.render('Легкий', False, (255, 255, 255), (100, 100, 100))
    button_easy_rect = button_easy.get_rect()
    button_easy_rect.x = (WW - button_easy_rect.width)/2
    button_easy_rect.y = WH / 5 * 2 - button_easy_rect.height / 2
    
    # Создание кнопки легкого уровня сложности 
    button_medium = my_font.render('Средний', False, (255, 255, 255), (100, 100, 100))
    button_medium_rect = button_medium.get_rect()
    button_medium_rect.x = (WW - button_medium_rect.width)/2
    button_medium_rect.y = WH / 5 * 3  - button_medium_rect.height / 2
    
    # Создание кнопки легкого уровня сложности 
    button_hard = my_font.render('Сложный', False, (255, 255, 255), (100, 100, 100))
    button_hard_rect = button_hard.get_rect()
    button_hard_rect.x = (WW - button_hard_rect.width)/2
    button_hard_rect.y = WH / 5 * 4 - button_hard_rect.height / 2

    # Отоброжение текста и кнопак
    window.blit(text, text_rect)
    window.blit(button_easy, button_easy_rect)
    window.blit(button_medium, button_medium_rect)
    window.blit(button_hard, button_hard_rect)

    # Отоброжение цвета кубика
    pg.draw.rect(window, target_color, (WW/4*3-WW/20, WH/2-WH/20, WW/10, WH/10))

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
                    target_size = int(WW * 30 / 1280)
                    target_timer = 2
                elif button_medium_rect.collidepoint(event.pos):
                    game_mode = 2
                    target_size = int(WW * 20 / 1280)
                    target_timer = 1.5
                elif button_hard_rect.collidepoint(event.pos):
                    game_mode = 3
                    target_size = int(WW * 10 / 1280)
                    target_timer = 1

    # Обработка нажатых клавиш
    keys = pg.key.get_pressed()

    if keys[pg.K_r]:
        target_change_color = 0
    elif keys[pg.K_g]:
        target_change_color = 1
    elif keys[pg.K_b]:
        target_change_color = 2

    elif keys[pg.K_UP]:
        if target_color[target_change_color] <= 250:
            target_color[target_change_color] += 5

    elif keys[pg.K_DOWN]:
        if target_color[target_change_color] >= 5:
            target_color[target_change_color] -= 5

    elif keys[pg.K_1]:
        target_color = [255, 0, 0]
    elif keys[pg.K_2]:
        target_color = [0, 255, 0]
    elif keys[pg.K_3]:
        target_color = [0, 0, 255]
    elif keys[pg.K_4]:
        target_color = [255, 255, 0]
    elif keys[pg.K_5]:
        target_color = [255, 255, 255]

    # Начало игры
    if game_mode != 0: 
        # Создание игрока
        player_score = 0

        # Игрвой цикл
        is_game = True
        while is_game:
            # Создание мишени
            target = Target((random.randint(0, WW-target_size), random.randint(0, WH-target_size)), target_size, target_color, target_timer)

            # Цикл раунда
            is_round = True
            while is_round:
                # Закрашишивание окна
                window.fill((0, 0, 0))

                # Отрисовка количества очков
                score = my_font.render(str(player_score), False, (255, 255, 255))
                window.blit(score, ((WW-score.get_width())/2, 0))

                # Отрисовка оставлегося времени
                left_time = my_font.render(str(round(target.timer, 1)), False, (255, 255, 255))
                window.blit(left_time, ((WW-left_time.get_width())/2, WH-left_time.get_height()))

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
                clock.tick(FPS)

    # Обновление окна
    pg.display.update()
    clock.tick(FPS)
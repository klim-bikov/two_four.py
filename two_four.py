from logics import *
import pygame
import sys
from database import get_best, cur, insert_result

GAMERS_DB = get_best()


def draw_top_gamers():
    font_top = pygame.font.SysFont('Verdana', 20)
    font_gamers = pygame.font.SysFont('Verdana', 20)
    text_heading = font_top.render('Best tries: ', True, COLOR_TEXT)
    screen.blit(text_heading, (300, 2))
    for index, gamer in enumerate(GAMERS_DB):
        name, score = gamer
        s = f'{index + 1}. {name} - {score}'
        text_gamer = font_gamers.render(s, True, COLOR_TEXT)
        screen.blit(text_gamer, (270, 25 + 24 * index))
        print(index + 1, name, score)


def draw_interface(score, delta=0):
    pygame.draw.rect(screen, WHITE, TITLE_REC)
    font = pygame.font.SysFont('stxingkai', 70)
    font_score = pygame.font.SysFont('Verdana', 40)
    font_score_value = pygame.font.SysFont('simsun', 40)
    font_delta = pygame.font.SysFont('simsun', 32)
    text_score = font_score.render('Score: ', True, COLOR_TEXT)
    text_score_value = font_score_value.render(f'{score}', True, COLOR_TEXT)
    screen.blit(text_score, (20, 13))
    screen.blit(text_score_value, (155, 19))
    if delta > 0:
        text_delta = font_delta.render(f'+{delta}', True, COLOR_TEXT)
        screen.blit(text_delta, (155, 65))
    pretty_print(mas)
    draw_top_gamers()
    for row in range(BLOCKS):
        for column in range(BLOCKS):
            value = mas[row][column]
            text = font.render(f'{value}', True, BLACK)
            w = column * SIZE_BLOCK + MARGIN * (column + 1)
            h = row * SIZE_BLOCK + MARGIN * (row + 1) + SIZE_BLOCK
            pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCK, SIZE_BLOCK))
            if value != 0:
                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCK - font_w) / 2
                text_y = h + (SIZE_BLOCK - font_h) / 2
                screen.blit(text, (text_x, text_y))


COLOR_TEXT = (255, 127, 0)
COLORS = {
    0: (130, 130, 130),
    2: (255, 255, 255),
    4: (255, 255, 128),
    8: (255, 255, 0),
    16: (255, 235, 255),
    32: (255, 235, 128),
    64: (255, 235, 0),
    128: (255, 100, 50),
    256: (150, 255, 128),
    512: (255, 128, 128),
    1024: (150, 255, 128),
    2048: (255, 128, 128)
}
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (130, 130, 130)

BLOCKS = 4
SIZE_BLOCK = 110
MARGIN = 10
WIDTH = BLOCKS * SIZE_BLOCK + (BLOCKS + 1) * MARGIN
HEIGHT = WIDTH + SIZE_BLOCK
TITLE_REC = pygame.Rect(0, 0, WIDTH, SIZE_BLOCK)

SUB_COLOR = (245, 242, 157)
SUB_PARAMS = (0, 0, 490, 600)


def init_const():
    global score, mas
    mas = [[0, 0, 0, 0] for _ in range(4)]
    score = 0
    empty = get_empty_list(mas)
    random.shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = get_index_from_number(random_num1)
    x2, y2 = get_index_from_number(random_num2)
    insert_2_or_4(mas, x1, y1)
    insert_2_or_4(mas, x2, y2)


score = None
mas = None
init_const()
USERNAME = None

print(get_empty_list(mas))
pretty_print(mas)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')


def draw_intro():
    img2048 = pygame.image.load('intro.webp.png')
    font_welcome = pygame.font.SysFont('Verdana', 50)
    text_welcome = font_welcome.render('Welcome!', True, WHITE)
    name = 'Введите имя'
    is_find_name = False

    while not is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == 'Введите имя':
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) >= 2:
                        global USERNAME
                        USERNAME = name
                        is_find_name = True
                        break

        screen.fill(SUB_COLOR)
        text_name = font_welcome.render(name, True, WHITE)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center
        pygame.draw.rect(screen, SUB_COLOR, SUB_PARAMS)
        screen.blit(pygame.transform.scale(img2048, [200, 200]), [145, 60])
        screen.blit(text_welcome, (125, 340))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(BLACK)


def draw_game_over():
    global USERNAME, mas
    img2048 = pygame.image.load('intro.webp.png')
    font_end = pygame.font.SysFont('Verdana', 50)
    font_score = pygame.font.SysFont('Verdana', 40)
    text_end = font_end.render('Game Over!', True, WHITE)
    text_score = font_score.render(f'Сумма очков: {score}', True, WHITE)
    best_score = GAMERS_DB[0][1]
    if score > best_score:
        text = 'Рекорд побит!'
    else:
        text = f'Рекорд: {best_score}'
    text_record = font_score.render(text, True, WHITE)
    insert_result(USERNAME, score)
    make_decision = False
    while not make_decision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    make_decision = True
                    init_const()
                elif event.key == pygame.K_RETURN:
                    USERNAME = None
                    make_decision = True
                    init_const()
        pygame.draw.rect(screen, SUB_COLOR, SUB_PARAMS)
        screen.blit(pygame.transform.scale(img2048, [200, 200]), [145, 60])
        screen.blit(text_end, (90, 290))
        screen.blit(text_score, (45, 380))
        screen.blit(text_record, (45, 460))
        pygame.display.update()
    screen.fill(BLACK)


def game_loop():
    global score, mas
    draw_interface(score)
    pygame.display.update()
    is_btn_click = False
    while is_zero_in_mas(mas) or can_move(mas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT:
                    mas, delta = move_left(mas)
                    is_btn_click = True
                elif event.key == pygame.K_RIGHT:
                    mas, delta = move_right(mas)
                    is_btn_click = True
                elif event.key == pygame.K_UP:
                    mas, delta = move_up(mas)
                    is_btn_click = True
                elif event.key == pygame.K_DOWN:
                    mas, delta = move_down(mas)
                    is_btn_click = True
                score += delta
                if is_zero_in_mas(mas) and is_btn_click:
                    empty = get_empty_list(mas)
                    random.shuffle(empty)
                    random_num = empty.pop()
                    x, y = get_index_from_number(random_num)
                    insert_2_or_4(mas, x, y)
                    print(f'Мы заполнили элемент под номером {random_num}')
                    is_btn_click = False
                draw_interface(score, delta)
                pygame.display.update()
        print(USERNAME)


while True:
    if USERNAME is None:
        draw_intro()
    game_loop()
    draw_game_over()
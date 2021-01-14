import os
import sys

import pygame

f = open('scoreboard.txt', 'r')
x = f.read()
rec = x.split('\n')
f.close()

level = 1
hp = 8
score = 0

size = WIDTH, HEIGHT = 1100, 700
FPS = 60


def load_image(name, transform=False):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    if transform:
        image = pygame.transform.scale(pygame.image.load(fullname), (50, 50))
    else:
        image = pygame.image.load(fullname)
    return image


tile_images = {
    'wall': load_image('wall.bmp', True),
    'empty': load_image('pol.bmp', True),
    'coin': load_image('coin.png'),
    'exit': load_image('exit.bmp', True),
    'trap': load_image('trap.png')
}
player_image = load_image('DM.png', False)
hp_full = load_image('heart_full.png', False)
hp_half = load_image('heart_half.png', False)

tile_width = tile_height = 50

# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'x':
                Tile('trap', x, y)
            elif level[y][x] == '/':
                Tile('exit', x, y)
            elif level[y][x] == '0':
                Tile('coin', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global level
    global hp
    global score
    font = pygame.font.Font(None, 50)
    text = font.render("Cave game!", True, (100, 255, 100))
    text_x = (width // 2 - text.get_width() // 2)  # 453
    text_y = (height // 2 - text.get_height() // 2) - 150  # 182
    text_w = text.get_width()  # 195
    text_h = text.get_height()  # 36
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)

    font = pygame.font.Font(None, 50)
    text = font.render("Продолжить", True, (100, 255, 100))
    text_x = (width // 2 - text.get_width() // 2)  # 451
    text_y = (height // 2 - text.get_height() // 2) - 90  # 243
    text_w = text.get_width()  # 198
    text_h = text.get_height()  # 35
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)

    font = pygame.font.Font(None, 50)
    text = font.render("Начать новую игру", True, (100, 255, 100))
    text_x = (width // 2 - text.get_width() // 2)  # 389
    text_y = (height // 2 - text.get_height() // 2) - 30  # 303
    text_w = text.get_width()  # 323
    text_h = text.get_height()  # 35
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)

    font = pygame.font.Font(None, 50)
    text = font.render("Выход", True, (100, 255, 100))
    text_x = (width // 2 - text.get_width() // 2)  # 490
    text_y = (height // 2 - text.get_height() // 2) + 30  # 363
    text_w = text.get_width()  # 120
    text_h = text.get_height()  # 34
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)

    intro_text = ["Cave game", "",
                  "Правила игры",
                  "Вы находитнсь в лабиринте,",
                  "в лабиринте есть ловушки и золото,",
                  "за золото вы",
                  "получаете очки, ",
                  "ловушки наносят вам урон,",
                  "при получении ",
                  "критического урона вы",
                  "погибаете, при выходе из лабиринта,",
                  "попадают в список рекордов.",
                  "Сохранения происходят каждый уровень"]

    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    font1 = pygame.font.Font(None, 30)
    text_coord2 = 500
    records1 = []
    for i in rec:
        records1.append(i)

    records = ['РЕКОРДЫ!']
    for i in range(len(records1)):
        records1[i] = int(records1[i])
    records1 = sorted(records1, reverse=True)
    for i in range(5):
        if records1[i] == 0:
            pass
        else:
            records.append(records1[i])
    for line in records:
        line = str(line)
        string_rendered2 = font1.render(line, 1, pygame.Color('white'))
        intro_rect2 = string_rendered2.get_rect()
        text_coord2 += 10
        intro_rect2.top = text_coord2
        intro_rect2.x = 10
        text_coord2 += intro_rect2.height
        screen.blit(string_rendered2, intro_rect2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos_x = int(event.pos[0])
                pos_y = int(event.pos[1])
                if (pos_x >= 480 and pos_x <= 480 + 140) and (pos_y >= 353 and pos_y <= 353 + 54):
                    terminate()
                if (pos_x >= 379 and pos_x <= 379 + 343) and (pos_y >= 293 and pos_y <= 293 + 55):
                    f = open('save.txt', 'w')
                    f.write('0' + '\n')
                    level = 1
                    hp = 8
                    score = 0
                    f.close()
                    return

                if (pos_x >= 431 and pos_x <= 431 + 239) and (pos_y >= 233 and pos_y <= 233 + 55):
                    f = open('save.txt', 'r')
                    x = f.read()
                    if x[0] != '0':
                        level = int(x[0])
                        hp = int(x[2])
                        score = int(x[4:-1])
                    else:
                        f.close()
                        f = open('save.txt', 'w')
                        f.write('0' + '\n')
                        level = 1
                        hp = 8
                        score = 0
                        f.close()

                    return

        pygame.display.flip()
        clock.tick(FPS)


def pause():
    global level
    global hp
    global score
    screen.fill('black')
    font = pygame.font.Font(None, 50)
    text = font.render("Cave game!", True, (100, 255, 100))
    text_x = (width // 2 - text.get_width() // 2)  # 453
    text_y = (height // 2 - text.get_height() // 2) - 150  # 182
    text_w = text.get_width()  # 195
    text_h = text.get_height()  # 36
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)

    font = pygame.font.Font(None, 50)
    text = font.render("Продолжить", True, (100, 255, 100))
    text_x = (width // 2 - text.get_width() // 2)  # 451
    text_y = (height // 2 - text.get_height() // 2) - 90  # 243
    text_w = text.get_width()  # 198
    text_h = text.get_height()  # 35
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)

    font = pygame.font.Font(None, 50)
    text = font.render("Выход", True, (100, 255, 100))
    text_x = (width // 2 - text.get_width() // 2)  # 490
    text_y = (height // 2 - text.get_height() // 2) - 30  # 363
    text_w = text.get_width()  # 120
    text_h = text.get_height()  # 34
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos_x = int(event.pos[0])
                pos_y = int(event.pos[1])
                if (pos_x >= 480 and pos_x <= 480 + 140) and (pos_y >= 293 and pos_y <= 293 + 55):
                    terminate()

                if (pos_x >= 431 and pos_x <= 431 + 239) and (pos_y >= 233 and pos_y <= 233 + 55):
                    f = open('save.txt', 'r')
                    x = f.read()
                    if x[0] != '0':
                        level = int(x[0])
                        hp = int(x[2])
                        score = int(x[4:-1])
                    else:
                        f.close()
                        f = open('save.txt', 'w')
                        f.write('0' + '\n')
                        level = 1
                        hp = 8
                        score = 0
                        f.close()

                    return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся круг 25')
    size = width, height = 1100, 700
    screen = pygame.display.set_mode(size)
    running = True
    where = ''
    screen.fill('black')
    clock = pygame.time.Clock()
    player, level_x, level_y = generate_level(load_level('lev1.txt'))
    level_map = load_level('lev1.txt')

    start_screen()
    if level == 1:
        player, level_x, level_y = generate_level(load_level('lev1.txt'))
        level_map = load_level('lev1.txt')
    elif level == 2:
        player, level_x, level_y = generate_level(load_level('lev2.txt'))
        level_map = load_level('lev2.txt')
    elif level == 3:
        player, level_x, level_y = generate_level(load_level('lev3.txt'))
        level_map = load_level('lev3.txt')
    elif level == 4:
        player, level_x, level_y = generate_level(load_level('lev4.txt'))
        level_map = load_level('lev4.txt')
    elif level == 5:
        player, level_x, level_y = generate_level(load_level('lev5.txt'))
        level_map = load_level('lev5.txt')
    flag2 = False
    flag3 = False
    flag4 = False
    flag5 = False
    coin = pygame.mixer.Sound('data\coin.wav')
    vika = pygame.mixer.Sound('data\\vika.mp3')
    dmg = pygame.mixer.Sound('data\\dmg.wav')
    game_over = pygame.mixer.Sound('data\\game over.wav')
    pygame.mixer.music.load('data\\music.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.2)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if level_map[player.pos_y][player.pos_x - 1] == '.':
                        lst = list(level_map[player.pos_y])
                        lst[player.pos_x - 1] = '@'
                        lst[player.pos_x] = '.'
                        level_map[player.pos_y] = ''.join(lst)
                        player.pos_x = player.pos_x - 1
                    elif level_map[player.pos_y][player.pos_x - 1] == 'x':
                        lst = list(level_map[player.pos_y])
                        lst[player.pos_x - 1] = '@'
                        lst[player.pos_x] = '.'
                        level_map[player.pos_y] = ''.join(lst)
                        player.pos_x = player.pos_x - 1
                        hp -= 1
                        dmg.play()
                    elif level_map[player.pos_y][player.pos_x - 1] == '0':
                        lst = list(level_map[player.pos_y])
                        lst[player.pos_x - 1] = '@'
                        lst[player.pos_x] = '.'
                        level_map[player.pos_y] = ''.join(lst)
                        player.pos_x = player.pos_x - 1
                        score += 10
                        coin.play()
                    elif level_map[player.pos_y][player.pos_x - 1] == '/':
                        lst = list(level_map[player.pos_y])
                        lst[player.pos_x - 1] = '@'
                        lst[player.pos_x] = '.'
                        level_map[player.pos_y] = ''.join(lst)
                        player.pos_x = player.pos_x - 1
                        score += 50
                        level += 1
                elif event.key == pygame.K_RIGHT:
                    if level_map[player.pos_y][player.pos_x + 1] == '.':
                        lst = list(level_map[player.pos_y])
                        lst[player.pos_x + 1] = '@'
                        lst[player.pos_x] = '.'
                        level_map[player.pos_y] = ''.join(lst)
                        player.pos_x = player.pos_x + 1
                    elif level_map[player.pos_y][player.pos_x + 1] == 'x':
                        lst = list(level_map[player.pos_y])
                        lst[player.pos_x + 1] = '@'
                        lst[player.pos_x] = '.'
                        level_map[player.pos_y] = ''.join(lst)
                        player.pos_x = player.pos_x + 1
                        hp -= 1
                        dmg.play()
                    elif level_map[player.pos_y][player.pos_x + 1] == '0':
                        lst = list(level_map[player.pos_y])
                        lst[player.pos_x + 1] = '@'
                        lst[player.pos_x] = '.'
                        level_map[player.pos_y] = ''.join(lst)
                        player.pos_x = player.pos_x + 1
                        score += 10
                        coin.play()
                    elif level_map[player.pos_y][player.pos_x + 1] == '/':
                        lst = list(level_map[player.pos_y])
                        lst[player.pos_x + 1] = '@'
                        lst[player.pos_x] = '.'
                        level_map[player.pos_y] = ''.join(lst)
                        player.pos_x = player.pos_x + 1
                        score += 50
                        level += 1
                elif event.key == pygame.K_UP:
                    if level_map[player.pos_y - 1][player.pos_x] == '.':
                        lstOT = list(level_map[player.pos_y])
                        lstTO = list(level_map[player.pos_y - 1])
                        lstOT[player.pos_x] = '.'
                        lstTO[player.pos_x] = '@'
                        level_map[player.pos_y] = ''.join(lstOT)
                        level_map[player.pos_y - 1] = ''.join(lstTO)
                        player.pos_y = player.pos_y - 1
                    elif level_map[player.pos_y - 1][player.pos_x] == 'x':
                        lstOT = list(level_map[player.pos_y])
                        lstTO = list(level_map[player.pos_y - 1])
                        lstOT[player.pos_x] = '.'
                        lstTO[player.pos_x] = '@'
                        level_map[player.pos_y] = ''.join(lstOT)
                        level_map[player.pos_y - 1] = ''.join(lstTO)
                        player.pos_y = player.pos_y - 1
                        hp -= 1
                        dmg.play()
                    elif level_map[player.pos_y - 1][player.pos_x] == '0':
                        lstOT = list(level_map[player.pos_y])
                        lstTO = list(level_map[player.pos_y - 1])
                        lstOT[player.pos_x] = '.'
                        lstTO[player.pos_x] = '@'
                        level_map[player.pos_y] = ''.join(lstOT)
                        level_map[player.pos_y - 1] = ''.join(lstTO)
                        player.pos_y = player.pos_y - 1
                        score += 10
                        coin.play()
                    elif level_map[player.pos_y - 1][player.pos_x] == '/':
                        lstOT = list(level_map[player.pos_y])
                        lstTO = list(level_map[player.pos_y - 1])
                        lstOT[player.pos_x] = '.'
                        lstTO[player.pos_x] = '@'
                        level_map[player.pos_y] = ''.join(lstOT)
                        level_map[player.pos_y - 1] = ''.join(lstTO)
                        player.pos_y = player.pos_y - 1
                        score += 50
                        level += 1
                elif event.key == pygame.K_DOWN:
                    if level_map[player.pos_y + 1][player.pos_x] == '.':
                        lstOT = list(level_map[player.pos_y])
                        lstTO = list(level_map[player.pos_y + 1])
                        lstOT[player.pos_x] = '.'
                        lstTO[player.pos_x] = '@'
                        level_map[player.pos_y] = ''.join(lstOT)
                        level_map[player.pos_y + 1] = ''.join(lstTO)
                        player.pos_y = player.pos_y + 1
                    elif level_map[player.pos_y + 1][player.pos_x] == 'x':
                        lstOT = list(level_map[player.pos_y])
                        lstTO = list(level_map[player.pos_y + 1])
                        lstOT[player.pos_x] = '.'
                        lstTO[player.pos_x] = '@'
                        level_map[player.pos_y] = ''.join(lstOT)
                        level_map[player.pos_y + 1] = ''.join(lstTO)
                        player.pos_y = player.pos_y + 1
                        hp -= 1
                        dmg.play()
                    elif level_map[player.pos_y + 1][player.pos_x] == '0':
                        lstOT = list(level_map[player.pos_y])
                        lstTO = list(level_map[player.pos_y + 1])
                        lstOT[player.pos_x] = '.'
                        lstTO[player.pos_x] = '@'
                        level_map[player.pos_y] = ''.join(lstOT)
                        level_map[player.pos_y + 1] = ''.join(lstTO)
                        player.pos_y = player.pos_y + 1
                        coin.play()
                        score += 10
                    elif level_map[player.pos_y + 1][player.pos_x] == '/':
                        lstOT = list(level_map[player.pos_y])
                        lstTO = list(level_map[player.pos_y + 1])
                        lstOT[player.pos_x] = '.'
                        lstTO[player.pos_x] = '@'
                        level_map[player.pos_y] = ''.join(lstOT)
                        level_map[player.pos_y + 1] = ''.join(lstTO)
                        player.pos_y = player.pos_y + 1
                        score += 50
                        level += 1
                elif event.key == pygame.K_ESCAPE:
                    pause()

        # в главном игровом цикле
        # изменяем ракурс камеры
        if level == 2 and flag2 == False:
            level_map = load_level('lev2.txt')
            player, level_x, level_y = generate_level(load_level('lev2.txt'))
            flag2 = True

            f = open('save.txt', 'w')
            f.write(str(level) + '\n')
            f.write(str(hp) + '\n')
            f.write(str(score) + '\n')
            f.close()
        if level == 3 and flag3 == False:
            level_map = load_level('lev3.txt')
            player, level_x, level_y = generate_level(load_level('lev3.txt'))
            flag3 = True

            f = open('save.txt', 'w')
            f.write(str(level) + '\n')
            f.write(str(hp) + '\n')
            f.write(str(score) + '\n')
            f.close()
        if level == 4 and flag4 == False:
            level_map = load_level('lev4.txt')
            player, level_x, level_y = generate_level(load_level('lev4.txt'))
            flag4 = True

            f = open('save.txt', 'w')
            f.write(str(level) + '\n')
            f.write(str(hp) + '\n')
            f.write(str(score) + '\n')
            f.close()
        if level == 5 and flag5 == False:
            level_map = load_level('lev5.txt')
            player, level_x, level_y = generate_level(load_level('lev5.txt'))
            flag5 = True

            f = open('save.txt', 'w')
            f.write(str(level) + '\n')
            f.write(str(hp) + '\n')
            f.write(str(score) + '\n')
            f.close()
        if level == 6:
            f = open('save.txt', 'w')
            f.write('0' + '\n')
            rec.append(str(score))
            f1 = open('scoreboard.txt', 'a')
            f1.write('\n' + str(score))
            level = 1
            hp = 8
            score = 0
            f.close()
            level_map = load_level('lev1.txt')
            player, level_x, level_y = generate_level(load_level('lev1.txt'))
            flag2 = False
            flag3 = False
            flag4 = False
            flag5 = False
            vika.play()
            screen.fill('black')
            start_screen()
        player, x, y = generate_level(level_map)

        all_sprites.draw(screen)
        all_sprites.update()
        all_sprites = pygame.sprite.Group()

        font = pygame.font.Font(None, 50)
        text = font.render(str(score), True, (100, 255, 100))
        text_x = width - 80
        text_y = 20
        text_w = text.get_width()
        text_h = text.get_height()

        if hp == 1:
            screen.blit(hp_half, (10, 10))
        elif hp == 2:
            screen.blit(hp_full, (10, 10))
        elif hp == 3:
            screen.blit(hp_full, (10, 10))
            screen.blit(hp_half, (20, 10))
        elif hp == 4:
            screen.blit(hp_full, (10, 10))
            screen.blit(hp_full, (20, 10))
        elif hp == 5:
            screen.blit(hp_full, (10, 10))
            screen.blit(hp_full, (20, 10))
            screen.blit(hp_half, (30, 10))
        elif hp == 6:
            screen.blit(hp_full, (10, 10))
            screen.blit(hp_full, (20, 10))
            screen.blit(hp_full, (30, 10))
        elif hp == 7:
            screen.blit(hp_full, (10, 10))
            screen.blit(hp_full, (20, 10))
            screen.blit(hp_full, (30, 10))
            screen.blit(hp_half, (40, 10))
        elif hp == 8:
            screen.blit(hp_full, (10, 10))
            screen.blit(hp_full, (20, 10))
            screen.blit(hp_full, (30, 10))
            screen.blit(hp_full, (40, 10))
        elif hp == 0:
            f = open('save.txt', 'w')
            f.write('0' + '\n')
            level = 1
            hp = 8
            score = 0
            game_over.play()
            f.close()
            level_map = load_level('lev1.txt')
            player, level_x, level_y = generate_level(load_level('lev1.txt'))
            flag2 = False
            flag3 = False
            flag4 = False
            flag5 = False
            screen.fill('black')
            start_screen()

        screen.blit(text, (text_x, text_y))

        pygame.display.flip()
        screen.fill('white')
        clock.tick(FPS)
    pygame.quit()

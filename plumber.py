# Made by Group 12
# --- Plumber ---

import pygame, math, random

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.mixer.init()
pygame.init()
random.seed(8)
myfont = pygame.font.SysFont("comicsans", 40)
screen_h = 800
screen_w = 700
block_side = 70

rx = 70
ry = 150

win = pygame.display.set_mode((screen_h, screen_w))
pygame.display.set_caption("Plumber")
icon = pygame.image.load("Assets/VAB.jpg")
pygame.display.set_icon(icon)
# background image
start = pygame.image.load("Assets/begin.png")
outlet_im = pygame.image.load("Assets/wylot.png")
start_menu = pygame.image.load("Assets/bg_img.jpg")
start_menu = pygame.transform.scale(start_menu, (screen_h, screen_w))
# ảnh các khối
elbow_image = [pygame.image.load('Assets/UR.png'), pygame.image.load('Assets/BR.png'), \
                 pygame.image.load('Assets/BL.png'), pygame.image.load('Assets/UL.png')]
pipe_image = [pygame.image.load('Assets/poziom.png'), pygame.image.load('Assets/pion.png')]
rock_image = [pygame.image.load('Assets/rock.png')]
# hình ảnh nút
start_button = pygame.image.load("Assets/st_bt.png")
start_button = pygame.transform.scale(start_button, (196, 66))
# kích thước nút (tất cả chúng đều có cùng kích thước)
button = start_button.get_size()  # (width, height)
next_button = pygame.image.load("Assets/next_bt.png")
next_button = pygame.transform.scale(next_button, (196, 66))
quit_button = pygame.image.load("Assets/ex_bt.png")
quit_button = pygame.transform.scale(quit_button, (196, 66))
menu_button = pygame.image.load("Assets/menu_bt.png")
menu_button = pygame.transform.scale(menu_button, (196, 66))
restart_button = pygame.image.load("Assets/rst_bt.png")
restart_button = pygame.transform.scale(restart_button, (196, 66))
lv_complete_button = pygame.image.load("Assets/lv_complete.png")
lv_complete_button = pygame.transform.scale(lv_complete_button, (250, 250))
all_lv_complete_button = pygame.image.load("Assets/all_lv_complete.png")
all_lv_complete_button = pygame.transform.scale(all_lv_complete_button, (250, 250))
gameover_button = pygame.image.load("Assets/gameover.png")
gameover_button = pygame.transform.scale(gameover_button, (250, 250))

music_button = [pygame.transform.scale(pygame.image.load("Assets/volume.png"), (button)), pygame.transform.scale(pygame.image.load("Assets/mute.png"), (button))]




# âm thanh
rotationSound = pygame.mixer.Sound("Assets/click.wav")
music = pygame.mixer.music.load("Assets/music.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)  # lặp lại âm thanh nhiều lần

isMusic = True


class level():
    def __init__(self, block, width, height):
        self.block = block
        self.width = width
        self.height = height
        self.size = height * width


class pipe(object):
    def __init__(self, size, picture, up, down, left, right, option, position):
        self.size = size
        self.picture = picture
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.position = position
        self.image = self.picture[position]
        self.option = option  # option- 1 elbow, 2 pipe, 3 rock

    def draw(self, place, win):
        if (place // sideX == place / sideX):
            i = pos // sideX
        else:
            i = place // sideX + 1
        j = place - (i - 1) * sideX
        x = (j - 1) * block_side + rx
        y = (i - 1) * block_side + ry
        win.blit(self.image, (x, y))

    def connection(self, place):
        inlet = []
        if (place // sideX == place / sideX):  # nó nằm ở cột cuối cùng
            i = place // sideX
        else:
            i = place // sideX + 1
        j = place - (i - 1) * sideX

        if (self.right == True):
            if (j < sideX):  # j< sideX
                inlet.append(place + 1)  # place + 1
            else:
                inlet.append(0)

        if (self.up == True):
            if (i > 1):
                inlet.append(place - sideX)  # place - sideX
            else:
                inlet.append(0)

        if (self.left == True):
            if (j > 1):
                inlet.append(place - 1)  # place -1
            else:
                inlet.append(0)

        if (self.down == True):
            if (i < sideY):
                inlet.append(place + sideX)  # place + sideX
            else:
                inlet.append(0)

        if (len(inlet) == 0):
            inlet.append(0)
            inlet.append(0)

        return (i, j, inlet[0], inlet[1])

    def inlet(self):
        return (self.up, self.down, self.left, self.right)

    def rotation(self):  # xoay 90 độ sang phải
        new_position = (self.position + 1) % len(self.picture)
        self.position = new_position
        self.image = self.picture[new_position]
        temp = self.right
        self.right = self.up
        self.up = self.left
        self.left = self.down
        self.down = temp

    def startPosition(self, new_position):
        if not (new_position == self.position):
            if (self.option == 1):
                self.up = 1
                self.down = 0
                self.right = 1
                self.left = 0
            elif (self.option == 2):
                self.up = 0
                self.down = 0
                self.right = 1
                self.left = 1
            else:
                self.up = 0
                self.down = 0
                self.right = 0
                self.left = 0

            self.position = new_position % len(self.picture)
            self.image = self.picture[self.position]
            for i in range(1, self.position + 1):
                temp = self.right
                self.right = self.up
                self.up = self.left
                self.left = self.down
                self.down = temp


def orCombined(block):  # block is an array with all elbows and pipes
    global wLevel
    size = len(block)
    ile = 1
    pos = 1
    if (block[0].left == True and block[size - 1].right == True):
        pos = 1

        outlet_old = 0
        check = True
    else:
        check = False
        return False

    while check:
        ile += 1

        (o, u, wlot1, wlot2) = block[pos - 1].connection(pos)
        if (wlot1 == outlet_old):  # có một kết nối giữa các khối
            if (wlot2 == False):  # nó đi ra khỏi bảng
                if (pos == size):  # chúng ta đang ở khối cuối cùng
                    return True  # kiểm tra xem nó có cống bên phải không
                else:
                    return False

            else:
                outlet_old = pos
                pos = wlot2  # przechodzimy do klocka do którego woda popłynie

        elif (wlot2 == outlet_old):
            if (wlot1 == False):  # nó đi ra khỏi bảng
                if (pos == size):  # đang ở khối cuối cùng
                    return True  # kiểm tra xem nó có cống bên phải không
                else:
                    return False

            else:
                outlet_old = pos
                pos = wlot1  # chúng ta đi đến khối nơi nước sẽ chảy

        else:
            return False  # tức là hai khối đã thử nghiệm không có kết nối


def updateLevel():
    global wLevel
    wLevel += 1
    (size, block, sideX, sideY) = selectLevel(wLevel)
    return (size, block, sideX, sideY)


def selectLevel(wLevel):
    random.seed(8)
    if (wLevel == 0):
        for k in levele[0].block:
            k.startPosition(random.randint(0, 6))

    elif (wLevel == 1):

        for k in levele[1].block:
            k.startPosition(random.randint(0, 6))
    elif (wLevel == 2):

        for k in levele[2].block:
            k.startPosition(random.randint(0, 6))
    elif (wLevel == 3):

        for k in levele[3].block:
            k.startPosition(random.randint(0, 6))

    elif (wLevel == 4):

        for k in levele[4].block:
            k.startPosition(random.randint(0, 6))

    elif (wLevel == 5):

        for k in levele[5].block:
            k.startPosition(random.randint(0, 6))

    level = levele[wLevel]
    size = level.size
    block = level.block
    sideX = level.width
    sideY = level.height
    return (size, block, sideX, sideY)


def Menu(intro=False):
    global isMusic
    global block, sideX, sideY, size, t0, wLevel
    isMenu = True
    while isMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isMenu = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if (screen_h / 2 - button[0] / 2 < pos[0] < (screen_h / 2 + button[0] / 2)):

                    # trở lại trò chơi chưa?
                    if (intro == False):
                        if ((screen_w / 2 - 1.5 * button[1]) < pos[1] < (screen_w / 2 - button[1] / 2)):
                            isMenu = False

                    # hoặc bắt đầu lại từ đầu
                    if ((screen_w / 2 - button[1] / 2) < pos[1] < (screen_w / 2 + button[1] / 2)):
                        isMenu = False
                        wLevel = 0
                        (size, block, sideX, sideY) = selectLevel(0)
                        t0 = pygame.time.get_ticks()

                        # bật/tắt nhạc
                    if ((screen_w / 2 + button[1] / 2) < pos[1] < (screen_w / 2 + 1.5 * button[1])):
                        if isMusic == True:
                            pygame.mixer.music.pause()
                            isMusic = False
                        else:
                            pygame.mixer.music.unpause()
                            isMusic = True
                    if ((screen_w / 2 + 1.5 * button[1]) < pos[1] < (screen_w / 2 + 2.5 * button[1])):
                        pygame.quit()

        win.fill((0, 0, 0))  # đặt nền màn hình
        win.blit(start_menu, (0, 0))

        # hiển thị các nút trên màn hình

        win.blit(start_button, (screen_h / 2 - button[0] / 2, screen_w / 2 - button[1] / 2))
        win.blit(music_button[isMusic], (screen_h / 2 - button[0] / 2, screen_w / 2 + button[1] / 2))
        win.blit(quit_button, (screen_h / 2 - button[0] / 2, screen_w / 2 + 1.5 * button[1]))
        pygame.display.update()

    # thông báo sau khi thắng 1 lv


def announcement():
    global wLevel, sideX, sideY, size, block, t0
    isPause = True
    while isPause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isPause = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if ((screen_w - button[0] - 20) < pos[0] < (screen_w - 20)):
                    # tiếp tục chơi
                    if (300 - 2 * button[1] < pos[1] < 300 - button[1]):
                        isPause = False
                        if wLevel < ileLeveli - 1:  # Có nhiều cấp độ cao hơn để chơi
                            (size, block, sideX, sideY) = updateLevel()
                            t0 = pygame.time.get_ticks()

                        # czy menu
                    if (300 - button[1] < pos[1] < 300):
                        isPause = False
                        Menu()

        win.blit(lv_complete_button, (275, 400))
        win.blit(next_button, (screen_w - button[0] - 20, 300 - 2 * button[1]))
        win.blit(menu_button, (screen_w - button[0] - 20, 300 - button[1]))
        pygame.display.update()


def endTime():
    global wLevel, sideX, sideY, size, block, t0
    isPause = True
    while isPause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isPause = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if ((screen_w - button[0] - 20) < pos[0] < (screen_w - 20)):
                    # powtarzam level
                    if (300 - 2 * button[1] < pos[1] < 300 - button[1]):
                        isPause = False
                        (size, block, sideX, sideY) = selectLevel(wLevel)
                        t0 = pygame.time.get_ticks()
                        # czy menu
                    if (300 - button[1] < pos[1] < 300):
                        isPause = False
                        Menu()

        win.blit(gameover_button, (275, 400))
        win.blit(restart_button, (screen_w - button[0] - 20, 300 - 2 * button[1]))
        win.blit(menu_button, (screen_w - button[0] - 20, 300 - button[1]))
        pygame.display.update()


def victory():
    global wLevel, sideX, sideY, size, block, t0
    isPause = True
    while isPause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isPause = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if ((screen_w - button[0] - 20) < pos[0] < (screen_w - 20)):
                    # idz do menu
                    if (300 - button[1] < pos[1] < 300):
                        isPause = False
                        Menu(intro=True)


        win.blit(all_lv_complete_button, (275, 400))

        win.blit(menu_button, (screen_w - button[0] - 20, 300 - button[1]))
        pygame.display.update()


# ----------------tạo các khối khác nhau ở vị trí 0-----------------------------------
# ống cong
kol1 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol2 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol3 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol4 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol5 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol6 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol7 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol8 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol9 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol10 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol11 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol12 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol13 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol14 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol15 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol16 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol17 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol18 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol19 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol20 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol21 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol22 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol23 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol24 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol25 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
kol26 = pipe(block_side, elbow_image, 1, 0, 0, 1, 1, 0)  # up-right
# đường ống
r1 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r2 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r3 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r4 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r5 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r6 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r7 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r8 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r9 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r10 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r11 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # pnằm ngang
r12 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r13 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r14 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r15 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r16 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r17 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
r18 = pipe(block_side, pipe_image, 0, 0, 1, 1, 2, 0)  # nằm ngang
# rock
p1 = pipe(block_side, rock_image, 0, 0, 0, 0, 3, 0)  # rock
p2 = pipe(block_side, rock_image, 0, 0, 0, 0, 3, 0)  # rock
p3 = pipe(block_side, rock_image, 0, 0, 0, 0, 3, 0)  # rock
p4 = pipe(block_side, rock_image, 0, 0, 0, 0, 3, 0)  # rock
p5 = pipe(block_side, rock_image, 0, 0, 0, 0, 3, 0)  # rock
p6 = pipe(block_side, rock_image, 0, 0, 0, 0, 3, 0)  # rock
p7 = pipe(block_side, rock_image, 0, 0, 0, 0, 3, 0)  # rock
p8 = pipe(block_side, rock_image, 0, 0, 0, 0, 3, 0)  # rock
p9 = pipe(block_side, rock_image, 0, 0, 0, 0, 3, 0)  # rock
p10 = pipe(block_side, rock_image, 0, 0, 0, 0, 3, 0)  # rock

# ----------------tạo cấp độ --------------------------------
block1 = [kol1, kol2, p1, \
           kol3, r1, kol4, \
           kol5, kol6, kol7]
level1 = level(block1, 3, 3)
# tiếp theo
block2 = [kol1, kol2, r1, kol3, \
           kol4, kol5, kol6, kol7, \
           r2, r3, kol8, r4]
level2 = level(block2, 4, 3)
# tiếp theo
block3 = [r1, kol1, p1, kol2, p2, \
           kol3, kol4, p3, kol5, kol6, \
           kol7, r2, r3, kol8, r4, \
           r5, p4, r6, p5, kol9]
level3 = level(block3, 5, 4)
# tiếp theo
block4 = [kol1, kol2, kol3, p1, \
           r1, r2, kol4, kol5, \
           kol6, kol7, kol8, kol9, \
           kol10, r3, kol11, kol12, \
           kol13, r4, r5, r6]
level4 = level(block4, 4, 5)
# tiếp theo
block5 = [kol1, kol2, kol3, kol4, kol5, \
           r1, kol6, kol7, kol8, kol9, \
           kol10, kol11, kol12, r2, r3, \
           kol13, kol14, p1, kol15, kol16]

level5 = level(block5, 5, 4)

# tiếp theo
block10 = [r1, kol1, kol2, r2, kol3, \
            kol4, kol5, kol6, kol7, kol8, \
            p1, kol9, p2, kol10, kol11, \
            kol12, kol13, kol14, kol15, kol16, \
            kol17, kol18, kol19, kol20, kol21, \
            kol22, r3, r4, kol23, p3, \
            p4, r5, r6, kol24, r7]
level10 = level(block10, 5, 7)

# ----tất cả các cấp trong danh sách--------------
levele = [level1, level2, level3, level5, level4, level10]

# ----giá trị ban đầu -------------------------------

# size - number of blocks, sideX sideY- dimensions of the board, block - list of blocks on the board
(size, block, sideX, sideY) = selectLevel(0)
time = 30
ileLeveli = len(levele)

run = True
ile_click = 0
n1 = 0  # vị trí của khối được nhấp trong danh sách các khối từ cấp độ hiện tại

isMenu = True
wLevel = 0
t0 = pygame.time.get_ticks()


# ---------vòng lặp trò chơi-------------------
while run:

    if isMenu == True:
        Menu(intro=True)
        t0 = pygame.time.get_ticks()
        isMenu = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            if rx < pos[0] < rx + sideX * block_side:
                if ry < pos[1] < ry + sideY * block_side:
                    j = ((pos[0] - rx) // block_side + 1)
                    i = ((pos[1] - ry) // block_side + 1)
                    n1 = (i - 1) * sideX + j
                    block[n1 - 1].rotation()
                    rotationSound.play()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        Menu()
        isMenu = False

    win.fill((0, 0, 0))  # đặt nền màn hình
    win.blit(start, (0, 0))
    for pos in range(1, size + 1):
        block[pos - 1].draw(pos, win)

    label = myfont.render(" Level " + str(wLevel + 1), 1, (255, 255, 255))
    win.blit(label, (screen_w / 2 - 50, 30))

    t1 = math.floor((pygame.time.get_ticks() - t0) / 1000)
    if time - t1 >= 10:
        label = myfont.render(" Time: " + str(time - t1), 1, (255, 255, 255))
    elif time - t1 >= 0:
        label = myfont.render(" Time: " + str(time - t1), 1, (255, 0, 0))
    else:
        label = myfont.render(" Time Over!!! ", 1, (255, 0, 0))
    win.blit(label, (screen_w / 2 + 150, 30))

    win.blit(outlet_im, (sideX * block_side + rx, (sideY - 1) * block_side + ry))

    pygame.display.update()  # hiển thị mọi thứ trên màn hình

    if orCombined(block) == True:
        if wLevel < ileLeveli - 1:
            announcement()  # chọn chơi tiếp hay chơi lại từ đầu
        else:
            victory()
    elif time - t1 < 0:
        endTime()

pygame.quit()

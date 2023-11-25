import numpy as np
import os
from colorama import Fore
from colorama import Style
from copy import deepcopy
import pygame, sys
from pygame.locals import *
from tkinter import *
import random
from tkinter import messagebox
import astar
import bfs
import player as pl

screen_width = 800
screen_height = 500

moves = 0

TIME_OUT = 190

clock = pygame.time.Clock()
FPS = 30  # Đặt FPS theo mong muốn của bạn

# os.getcwd(): trả về biểu diễn chuỗi thư mục đang làm việc hiện tại

current_file_path  = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

path_board = os.path.join(current_file_path, 'Testcases')
path_checkpoint = os.path.join(current_file_path, 'Checkpoints')

#window = Tk()
#window.title('quay lai')
#window.geometry('20x20')


#window.mainloop()


def get_boards():
    os.chdir(path_board)
    list_boards = []

    # Lấy danh sách tất cả các file với phần mở rộng ".txt"
    files = [file for file in os.listdir() if file.endswith(".txt")]

    # Sắp xếp danh sách file theo số xuất hiện trong tên file
    sorted_files = sorted(files, key=lambda x: int(''.join(filter(str.isdigit, x))))

    for file in sorted_files:
        file_path = os.path.join(path_board, file)
        print(file_path)
        board = get_board(file_path)
        list_boards.append(board)
        print(board)

    return list_boards

def get_check_points():
    os.chdir(path_checkpoint)
    list_check_point = []
    
    # Lấy danh sách các tệp tin .txt và sắp xếp chúng
    file_list = sorted([file for file in os.listdir() if file.endswith(".txt")], key=lambda x: int(x.split('.')[0]))

    for file in file_list:
        file_path = f"{path_checkpoint}\{file}"
        print(file_path)
        check_point = get_pair(file_path)
        list_check_point.append(check_point)
    
    return list_check_point

def format_row(row):
    random_grass = ['0', '1', '2', '3']
    random_wall = ['#']
    for i in range(len(row)):
        if row[i] == '1':
            row[i] = random.choice(random_wall)
        elif row[i] == 'p':
            row[i] = '@'
        elif row[i] == 'b':
            row[i] = '$'
        elif row[i] == 'c':
            row[i] = '%'
        elif row[i] == 'g':
            row[i] = random.choice(random_grass)

def format_check_points(check_points):
    result = []
    for check_point in check_points:
        result.append((check_point[0], check_point[1]))
    return result

def get_board(path):
    result = np.loadtxt(f"{path}", dtype=str, delimiter=',')
    for row in result:
        format_row(row)
    return result

def get_pair(path):
    result = np.loadtxt(f"{path}", dtype=int, delimiter=',')
    return result

maps = get_boards()
check_points = get_check_points()

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Sokoban')
clock = pygame.time.Clock()
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR = (255, 102, 51)
BLACK = (255, 255, 255)

#assets_path = os.getcwd() + "\\..\\Assets"
#os.chdir(assets_path)

current_file_path  = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
Asset_path = os.path.join(current_file_path, 'Assets')
os.chdir(Asset_path)

player = pygame.image.load(os.getcwd() + '\\horngirl.png')
wall = pygame.image.load(os.getcwd() + '\\Wood_Block_Tall.png')
wall1 = pygame.image.load(os.getcwd() + '\\Wall_Block_Tall.png')
box = pygame.image.load(os.getcwd() + '\\star.png')
point = pygame.image.load(os.getcwd() + '\\RedSelector.png')
space = pygame.image.load(os.getcwd() + '\\Plain_Block.png')
grass = pygame.image.load(os.getcwd() + '\\Grass_Block.png')
truepoint = pygame.image.load(os.getcwd() + '\\Selector.png')
tree1 = pygame.image.load(os.getcwd() + '\\Tree_Tall.png')
tree2 = pygame.image.load(os.getcwd() + '\\Tree_Ugly.png')
rock = pygame.image.load(os.getcwd() + '\\Rock.png')

solved = pygame.image.load(os.getcwd() + '\\star_solved.png')

orginal_menu = pygame.image.load(os.getcwd() + '\\home.png')
menu = pygame.transform.scale(orginal_menu, (screen_width, screen_height))

orginal_btnPlay = pygame.image.load(os.getcwd() + '\\btnPlay1.png')
btnPlay = pygame.transform.scale(orginal_btnPlay, (200, 100))

btnMainMenu = pygame.image.load(os.getcwd() + '\\mainMenu.png')
btnPlayer = pygame.image.load(os.getcwd() + '\\btnPlayer.png')
btnBFS = pygame.image.load(os.getcwd() + '\\btn_BFS.png')
btnAStar = pygame.image.load(os.getcwd() + '\\btnAstar.png')
btnLeft = pygame.image.load(os.getcwd() + '\\left.png')
btnRight = pygame.image.load(os.getcwd() + '\\right.png')
btnreStart = pygame.image.load(os.getcwd() + '\\reStart.png')

arrow_left = pygame.image.load(os.getcwd() + '\\arrow_left.png')
arrow_right = pygame.image.load(os.getcwd() + '\\arrow_right.png')
init_background = pygame.image.load(os.getcwd() + '\\home1.png')
loading_background = pygame.image.load(os.getcwd() + '\\background.png')
notfound_background = pygame.image.load(os.getcwd() + '\\background.png')
found_background = pygame.image.load(os.getcwd() + '\\background.png')

def renderMap(board):
    width = len(board[0])
    height = len(board)
    cell_width = 50  # Kích thước mới theo chiều rộng
    cell_height = 50  # Kích thước mới theo chiều cao

    # indent_x = (screen_width - width * cell_width) / 2.0
    # indent_y = (screen_height - height * cell_height) / 2.0

    indent_x = (screen_width - 450)
    indent_y = (screen_height - 450)

    true_points = []
    for check_point in check_points[mapNumber]:
        true_points.append((check_point[0], check_point[1]))

    # print(true_points)

    for i in range(height):
        for j in range(width):
            screen.blit(space, (j * cell_width + indent_x, i * cell_height + indent_y))
            if board[i][j] == '#':
                screen.blit(wall, (j * cell_width + indent_x, i * cell_height + indent_y))
            elif board[i][j] == '!':
                screen.blit(wall1, (j * cell_width + indent_x, i * cell_height + indent_y))
            elif board[i][j] == '$':
                if (i, j) in true_points:
                    screen.blit(truepoint, (j * cell_width + indent_x, i * cell_height + indent_y))
                    screen.blit(box, (j * cell_width + indent_x, i * cell_height + indent_y))
                else: 
                    screen.blit(box, (j * cell_width + indent_x, i * cell_height + indent_y))
            elif board[i][j] == '.':
                screen.blit(point, (j * cell_width + indent_x, i * cell_height + indent_y))
            elif board[i][j] == '@':
                if (i, j) in true_points:
                    screen.blit(point, (j * cell_width + indent_x, i * cell_height + indent_y))
                    screen.blit(player, (j * cell_width + indent_x, i * cell_height + indent_y))
                else: 
                    screen.blit(player, (j * cell_width + indent_x, i * cell_height + indent_y))
            elif board[i][j] == '%':
                screen.blit(point, (j * cell_width + indent_x, i * cell_height + indent_y))
            elif board[i][j] == '0':
                screen.blit(grass, (j * cell_width + indent_x, i * cell_height + indent_y))
            elif board[i][j] == '1':
                screen.blit(grass, (j * cell_width + indent_x, i * cell_height + indent_y))
                screen.blit(tree1, (j * cell_width + indent_x, i * cell_height + indent_y))
            elif board[i][j] == '2':
                screen.blit(grass, (j * cell_width + indent_x, i * cell_height + indent_y))
                screen.blit(tree2, (j * cell_width + indent_x, i * cell_height + indent_y))
            elif board[i][j] == '3':
                screen.blit(grass, (j * cell_width + indent_x, i * cell_height + indent_y))
                screen.blit(rock, (j * cell_width + indent_x, i * cell_height + indent_y))
mapNumber = 0
algorithm = "Player"
sceneState = "begin"
loading = False

def sokoban():
    running = True
    global sceneState # biến tham chiếu
    global loading
    global algorithm
    global list_board
    global mapNumber
    global moves
    moves = 0
    stateLenght = 0
    currentState = 0
    global list_board_win

    while running:
        clock.tick(FPS)
        if sceneState == "begin":
            screen.blit(menu, (0, 0))
            # Tải hình ảnh
            image_rect = btnPlay.get_rect()
            image_x = (screen_width - image_rect.width) // 2
            image_y = (screen_height - image_rect.height) // 2
            image_rect.topleft = (image_x, image_y + 40)
            screen.blit(btnPlay, image_rect)

            # mapSize = pygame.font.Font('gameFont1.ttf', 20)
            # mapText = mapSize.render("Design by Group 7", True, WHITE)
            # mapRect = mapText.get_rect(center=(screen_width // 2, screen_height - 50))
            # screen.blit(mapText, mapRect)

        elif sceneState == "init":
            screen.blit(init_background, (0, 0))
            # mainMenu_rect.topleft = (0, 0)
            resized_btnMainMenu = pygame.transform.scale(btnMainMenu, (50, 50))
            mainMenu_rect = resized_btnMainMenu.get_rect(topleft=(0, 0))
            screen.blit(resized_btnMainMenu, (0, 0))

            resized_btnLeft = pygame.transform.scale(btnLeft, (50, 50))
            btnLeft_rect = resized_btnLeft.get_rect(topleft=(55, 100))
            screen.blit(resized_btnLeft, (55, 100))

            resized_btnRight = pygame.transform.scale(btnRight, (50, 50))
            btnRight_rect = resized_btnRight.get_rect(topleft=(230, 100))
            screen.blit(resized_btnRight, (230, 100))

            resized_btnGiveUp = pygame.transform.scale(btnreStart,  (50, 50))
            btnGiveUp_rect = resized_btnGiveUp.get_rect(topleft=(750, 0))
            screen.blit(resized_btnGiveUp, (750, 0))

            resized_btnPlayer = pygame.transform.scale(btnPlayer, (100, 50))
            btnPlayer_rect = resized_btnPlayer.get_rect(topleft=(120, 150)) 
            screen.blit(resized_btnPlayer, (120, 150))

            resized_btnBFS = pygame.transform.scale(btnBFS, (100, 50))
            btnBFS_rect = resized_btnBFS.get_rect(topleft=(120, 200))
            screen.blit(resized_btnBFS, (120, 200))

            resized_btnAStar = pygame.transform.scale(btnAStar, (100, 50))
            btnAStar_rect = resized_btnAStar.get_rect(topleft=(120, 250))
            screen.blit(resized_btnAStar, (120, 250))

            # screen.blit(resized_btnMainMenu, (0, 0))
            if 0 <= mapNumber < len(maps):
                initGame(maps[mapNumber])
            else:
                # Đặt mapNumber về giá trị hợp lệ nếu nó vượt quá
                mapNumber = 0
                initGame(maps[mapNumber])

        if sceneState == "executing":
            list_check_point = check_points[mapNumber]
            # Chọn giữa người dùng chơi và máy chơi
            if algorithm == "Player":
                print("Player")
                list_board = maps[mapNumber]
            elif algorithm == "AStar":
                print("AStar")
                loadingGame()
                list_board = astar.AStar_Search(maps[mapNumber], list_check_point)
            else:
                print("BFS")
                list_board = bfs.BFS_search(maps[mapNumber], list_check_point)

            if len(list_board) > 0:
                sceneState = "playing"
                stateLenght = len(list_board[0])
                currentState = 0
            else:
                sceneState = "end"
                found = False
        
        if sceneState == "end":
            if algorithm == "Player":
                foundGame(list_board)
            else:
                foundGame(list_board[0][stateLenght - 1])
        
        if sceneState == "loading":
            loadingGame()
            sceneState = "executing"

        if sceneState == "playing":
            clock.tick(4)
            if(algorithm == "Player"):
                new_list_board = pl.Player(list_board, list_check_point, pygame)
                list_board = new_list_board
                if list_board == True:
                    sceneState = "end"
                    list_board = list_board_win
                    found = True
                else:
                    renderMap(list_board)
                    list_board_win = list_board
            if (algorithm == "AStar"):
                renderMap(list_board[0][currentState])
                currentState = currentState + 1
                # sceneState = "init"
            if (algorithm == "BFS"):
                renderMap(list_board[0][currentState])
                currentState = currentState + 1
            if currentState == stateLenght:
                sceneState = "end"
                found = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and sceneState == "begin":
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if image_rect.collidepoint(mouse_x, mouse_y):
                    sceneState = "init"
                    print(sceneState)
                    print(image_rect)
            elif event.type == pygame.MOUSEBUTTONDOWN and sceneState == "playing":
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if btnGiveUp_rect.collidepoint(mouse_x, mouse_y):
                    sceneState = "init"
            elif event.type == pygame.MOUSEBUTTONDOWN and sceneState == "init":
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if btnPlayer_rect.collidepoint(mouse_x, mouse_y):
                    print(btnPlayer_rect)
                    sceneState = "executing"
                    algorithm = "Player"
                    print(sceneState)
                elif mainMenu_rect.collidepoint(mouse_x, mouse_y):
                    sceneState = "begin"
                elif btnBFS_rect.collidepoint(mouse_x, mouse_y):
                    sceneState = "executing"
                    algorithm = "BFS"
                elif btnAStar_rect.collidepoint(mouse_x, mouse_y):
                    sceneState = "executing"
                    algorithm = "AStar"
                elif btnLeft_rect.collidepoint(mouse_x, mouse_y):
                    if mapNumber > 0:
                        mapNumber = mapNumber - 1
                    else:
                        mapNumber = len(maps) - 1
                elif btnRight_rect.collidepoint(mouse_x, mouse_y):
                    if mapNumber < len(maps) - 1:
                        mapNumber = mapNumber + 1
                    else:
                        mapNumber = 0

        pygame.display.update()
    pygame.quit()

def initGame(map):

    mapSize = pygame.font.Font('gameFont.ttf', 50)
    mapText = mapSize.render("Lv." + str(mapNumber + 1), True, COLOR)
    mapRect = mapText.get_rect(center=(170, 130))
    screen.blit(mapText, mapRect)

    renderMap(map)



def loadingGame():
    screen.blit(loading_background, (0, 0))

    fontLoading_1 = pygame.font.Font('gameFont.ttf', 40)
    text_1 = fontLoading_1.render('LOADING...', True, WHITE)
    text_rect_1 = text_1.get_rect(center=(320, 320))
    screen.blit(text_1, text_rect_1)

def foundGame(map):
    global mapNumber
    global sceneState
    global moves
    stateLength = len(list_board[0])

    # Check if the list is not empty and the index is within the valid range
    if list_board and 0 <= stateLength - 1 < len(list_board[0]):
        print(stateLength)
        # Lấy kích thước của ảnh "solved"
        solved_width, solved_height = solved.get_size()

        # Tính toán vị trí để đặt ảnh "solved" ở giữa màn hình
        solved_x = (screen_width - solved_width) // 2
        solved_y = (screen_height - solved_height) // 2

        renderMap(map)
        screen.blit(solved, (solved_x, solved_y))
        pygame.display.flip()

        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting_for_key = False

        mapNumber += 1
        sceneState = 'init'
        print(mapNumber)
        print(stateLength)


def notfoundGame():
    screen.blit(notfound_background, (0, 0))
    font_2 = pygame.font.Font('gameFont.ttf', 20)
    text_2 = font_2.render('Press Enter to continue.', True, WHITE)
    text_rect_2 = text_2.get_rect(center=(320, 600))
    screen.blit(text_2, text_rect_2)


def main():
    sokoban()

if __name__ == "__main__":
     main()


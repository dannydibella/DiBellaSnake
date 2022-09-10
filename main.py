import random
import tkinter as tk
from tkinter import *
import time


# Class for each location on the board as an object
class Spot:
    bomb = False
    flag = False
    hidden = True
    num_bombs_touching = 0

    def __init__(self, bomb, flag, hidden, num_bobs_touching):
        self.bomb = bomb
        self.flag = flag
        self.hidden = hidden
        self.num_bombs_touching = num_bobs_touching

    def __int__(self):
        self.bomb = False
        self.flag = False
        self.hidden = True
        self.num_bombs_touching = 0


# Other variables
bomb_percentage = 0.2
first_click_happened = False
playing = False
board_length = 20
square_length = 35
board_width = board_length * square_length + 4
board_height = board_length * square_length + 4
squares_left = 0

# Initialize board
board = []
hold = []
for r in range(0, board_length):
    for c in range(0, board_length):
        hold.append(Spot(False, False, True, 0))
    board.append(hold)
    hold = []
squares_left = len(board) * len(board[0]) - (int(len(board) * len(board[0]) * bomb_percentage))

# Main
main = Tk()
canvas = Canvas(main, width=board_width, height=board_height)
canvas.pack()

# Draw grid
row = 0
col = 0
for r in board:
    for c in r:
        canvas.create_line(col * square_length + 3, 0, col * square_length + 3, board_height)
        canvas.create_line(0, row * square_length + 3, board_width, row * square_length + 3)
        canvas.create_rectangle(row * square_length + 3, col * square_length + 3,
                                row * square_length + square_length + 3, col * square_length + square_length + 3,
                                fill='white')
        col += 1
    row += 1
    col = 0
canvas.create_line(board_width, 0, board_width, board_height)
canvas.create_line(0, board_height, board_width, board_height)


# Draw a bomb
def add_bomb(bx, by):
    canvas.create_oval(bx, by, bx + square_length, by + square_length, fill='red')


# Switch a flag
def switch_flag(fx, fy):
    if board[fx][fy].flag:
        canvas.create_rectangle(fx * square_length + 3, fy * square_length + 3,
                                fx * square_length + square_length + 3, fy * square_length + square_length + 3,
                                fill='white')
    else:
        canvas.create_rectangle(fx * square_length + 3, fy * square_length + 3,
                                fx * square_length + square_length + 3, fy * square_length + square_length + 3,
                                fill='yellow')
    board[fx][fy].flag = not board[fx][fy].flag


# Add bombs to board
def add_bombs_to_board():
    for num in range(int(len(board) * len(board[0]) * bomb_percentage)):
        not_finished = True
        while not_finished:
            x = random.randint(0, board_length-1)
            y = random.randint(0, board_length-1)
            if not board[x][y].bomb:
                board[x][y].bomb = True
                not_finished = False


add_bombs_to_board()


# Add non bomb values to board
def add_values_to_board():
    row = 0
    col = 0
    for r in board:
        for c in r:
            if not board[row][col].bomb:
                sum = 0
                for w in range(-1, 2):
                    for h in range(-1, 2):
                        if 0 <= row + w <= board_length-1 and 0 <= col + h <= board_length-1 and board[row + w][col + h].bomb:
                            sum += 1
                board[row][col].num_bombs_touching = sum
            col += 1
        row += 1
        col = 0


add_values_to_board()


def game_over():
    global playing
    playing = False
    start = time.time()
    end = start + 2
    clock = start
    while clock < end:
        clock = time.time()
    display_board()


def display_board():
    row = 0
    col = 0
    for r in board:
        for c in r:
            if c.hidden:
                reveal_square(row, col)
            col += 1
        row += 1
        col = 0


def game_won():
    global playing
    playing = False
    start = time.time()
    end = start + 2
    clock = start
    while clock < end:
        clock = time.time()
    reset_game()


# Reveal the selected location on the board
def reveal_square(xcor, ycor):
    global squares_left
    if board[xcor][ycor].bomb:
        if playing:
            game_over()
        else:
            add_bomb(xcor * square_length + 3, ycor * square_length + 3)
            board[xcor][ycor].hidden = False
    elif board[xcor][ycor].num_bombs_touching > 0:
        if playing:
            canvas.create_rectangle(xcor * square_length + 3, ycor * square_length + 3,
                                    xcor * square_length + square_length + 3, ycor * square_length + square_length + 3,
                                    fill='light green')
            canvas.create_text(xcor * square_length + square_length/2 + 3, ycor * square_length + square_length/2 + 3,
                               font=("Arial", 12), fill="black", text=str(board[xcor][ycor].num_bombs_touching))
        board[xcor][ycor].hidden = False
        squares_left -= 1
        if squares_left == 0 and playing:
            game_won()
    else:
        if playing:
            canvas.create_rectangle(xcor * square_length + 3, ycor * square_length + 3,
                                    xcor * square_length + square_length + 3, ycor * square_length + square_length + 3,
                                    fill='light green')
        board[xcor][ycor].hidden = False
        squares_left -= 1
        for w in range(-1, 2):
            for h in range (-1, 2):
                if 0 <= xcor + w <= board_length-1 and 0 <= ycor + h <= board_length-1 and board[xcor + w][ycor + h].hidden:
                    reveal_square(xcor + w, ycor + h)
        if squares_left == 0 and playing:
            game_won()


def first_click():
    for num in range(1, int((board_length-1)/2)):
        for w in range(-num, num+1):
            for h in range(-num, num+1):
                if board[int((board_length - 1)/2) + w][int((board_length - 1)/2) + h].num_bombs_touching == 0 and \
                        not board[int((board_length - 1)/2) + w][int((board_length - 1)/2) + h].bomb:
                    reveal_square(int((board_length - 1)/2) + w, int((board_length - 1)/2) + h)
                    return


# Left mouse click
def on_left_click(event):
    global first_click_happened
    global playing
    if not first_click_happened:
        playing = True
        first_click_happened = True
        first_click()
    else:
        x = int(event.x / square_length)
        y = int(event.y / square_length)
        if not board[x][y].flag:
            reveal_square(x, y)


canvas.bind("<Button-1>", on_left_click)


# Right mouse click
def on_right_click(event):
    x = int(event.x / square_length)
    y = int(event.y / square_length)
    if board[x][y].hidden:
        switch_flag(x, y)


canvas.bind("<Button-2>", on_right_click)


# Keyboard bindings
def reset_game():
    global playing
    global first_click_happened
    global squares_left
    playing = False
    first_click_happened = False
    row = 0
    col = 0
    for r in board:
        for c in r:
            c.hidden = True
            c.flag = False
            c.bomb = False
            c.num_bombs_touching = 0
            canvas.create_rectangle(row * square_length + 3, col * square_length + 3,
                                    row * square_length + square_length + 3, col * square_length + square_length + 3,
                                    fill='white')
            col += 1
        row += 1
        col = 0
    add_bombs_to_board()
    add_values_to_board()
    squares_left = len(board) * len(board[0]) - (int(len(board) * len(board[0]) * bomb_percentage))


reset_button = tk.Button(text="Reset", command=reset_game)
reset_button.pack()

# Game loop
while True:
    main.update()
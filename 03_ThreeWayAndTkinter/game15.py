from tkinter import *
from random import randint
'''GLOBALS'''
srow = 3
scol = 3
can_win = False
'''-------'''


def swap(self, a, b):
    self[a][b], self[srow][scol] = self[srow][scol], self[a][b]


def press_handler(button):
    global srow, scol
    gi = button.grid_info()
    i = gi['row']
    j = gi['column']
    # print("press_handler :", i, j, "and srow and scol", srow, scol)
    if srow == i and (scol - j == 1 or scol - j == -1) or scol == j and (srow - i == 1 or srow - i == -1):
        swap(ButtonString, i, j)
        srow = i
        scol = j
        print_board(ButtonString)
    else:
        pass


def scramble():
    global can_win, choice
    can_win = False
    global ButtonString, srow, scol
    numberr = 0
    for i in range(4):
        for j in range(4):
            numberr += 1
            obj = Button(board_bot, width=4, height=4, text=str(numberr))
            obj.configure(command=lambda button=obj: press_handler(button))
            ButtonString[i][j] = obj
    ButtonString[3][3] = Label(board_bot, width=4, height=4)
    srow = 3
    scol = 3
    print_board(ButtonString)
    if choice.get() == 'Super Easy':
        iterations = 10
    elif choice.get() == 'Easy':
        iterations = 100
    elif choice.get() == 'Medium':
        iterations = 500
    elif choice.get() == 'Hard':
        iterations = 1000
    for i in range(iterations):
        num = randint(1, 4)
        if num == 1 and scol <= 2:
            ButtonString[srow][scol + 1].invoke()
        elif num == 1 and scol == 3:
            ButtonString[srow][scol - 1].invoke()
        if num == 2 and scol >= 1:
            ButtonString[srow][scol - 1].invoke()
        elif num == 2 and scol == 0:
            ButtonString[srow][scol + 1].invoke()
        if num == 3 and srow >= 1:
            ButtonString[srow - 1][scol].invoke()
        elif num == 3 and srow == 0:
            ButtonString[srow + 1][scol].invoke()
        if num == 4 and srow <= 2:
            ButtonString[srow + 1][scol].invoke()
        elif num == 4 and srow == 3:
            ButtonString[srow - 1][scol].invoke()
    can_win = True


def print_board(board):
    global can_win
    for a in range(4):
        for b in range(4):
            board[a][b].grid(row=a, column=b, sticky="NEWS")
    if can_win:
        # print("game starts")
        flag = True
        check_num = 1
        for i in range(4):
            for j in range(4):
                # print(ButtonString[i][j]['text'])
                if ButtonString[i][j]['text'] != str(check_num) and check_num != 16:
                    flag = False
                    break
                check_num += 1
            else:
                continue
            break
        if flag:
            # print("we win")
            win_window()
            can_win = False


def win_window():
    def win_handler():
        new.invoke()
        win_screen.destroy()
    win_screen = Tk()
    win_screen.title("Win Screen")
    WinLabel = Label(win_screen, width=30, height=1, text="You Win! Congratulations!")
    WinButton = Button(win_screen, width=15, height=1,
                       text="Restart the Game!", command=win_handler)
    WinLabel.pack(expand=1, pady=10)
    WinButton.pack(expand=1, pady=10)
    win_screen.mainloop()


root = Tk()
root.title("15 GAME")
menu_top = LabelFrame(text="Menu")
board_bot = LabelFrame(text="Board")
new = Button(menu_top, width=5, height=1, text="New", command=scramble)
exit = Button(menu_top, width=5, height=1, text="Exit", command=root.destroy)

choice = StringVar()
optionlist = ('Super Easy', 'Easy', 'Medium', 'Hard')
choice.set(optionlist[0])
dropMenu = OptionMenu(menu_top, choice, *optionlist)
# gi = button.grid_info()
# i = gi['row']
# j = gi['column']
# print("press_handler :", i, j, "and srow and scol", srow, scol)


ButtonString = []
number = 0
for i in range(4):
    collist = []
    for j in range(4):
        number += 1
        obj = Button(board_bot, width=4, height=4, text=str(number))
        obj.configure(command=lambda button=obj: press_handler(button))
        collist.append(obj)
    ButtonString.append(collist)
ButtonString[3][3] = Label(board_bot, width=4, height=4)

menu_top.pack(expand=1, fill=X)
board_bot.pack(expand=1, fill=BOTH)

board_bot.rowconfigure(0, weight=1)
board_bot.rowconfigure(1, weight=1)
board_bot.rowconfigure(2, weight=1)
board_bot.rowconfigure(3, weight=1)
board_bot.columnconfigure(0, weight=1)
board_bot.columnconfigure(1, weight=1)
board_bot.columnconfigure(2, weight=1)
board_bot.columnconfigure(3, weight=1)

menu_top.rowconfigure(0, weight=1)
menu_top.rowconfigure(1, weight=1)
menu_top.columnconfigure(0, weight=1)

new.grid(column=0, row=0, pady=5, padx=10, sticky="WS")
exit.grid(column=1, row=0, pady=10, padx=10, sticky="WS")
dropMenu.grid(columnspan=2, pady=5, padx=10, sticky="NEWS")


print_board(ButtonString)
print_board(ButtonString)
root.mainloop()

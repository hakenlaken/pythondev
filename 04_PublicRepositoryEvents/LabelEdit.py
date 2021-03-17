import tkinter as tk
# from tkinter import ttk
# from itertools import product


class LabelEdit(tk.Label):
    '''Making "Entry"-like Label '''
    # ttk.Style().configure('white/black.TLabel', foreground='white',
    #                      background='black', highlightcolor="white")
    # ttk.Style().configure('green/black.TFrame', height=20, foreground='green', background='black')

    def __init__(self, master=None, **kwargs):
        self.S = tk.StringVar()
        self.S.set("click me or tab TO Check")
        super().__init__(master, font=("Courier", 20),
                         cursor="xterm",
                         foreground='white',
                         background='black',
                         relief="ridge",
                         anchor="w",
                         takefocus=True,
                         textvariable=self.S,
                         highlightthickness=1,
                         highlightcolor='lightblue',
                         # style='white/black.TLabel',
                         ** kwargs)

        self.FrameUnder = tk.Frame(self,
                                   height=20,
                                   bg="lightgreen",
                                   # style='green/black.TFrame',
                                   width=1)
        self.sym_width = 12
        self.cur_pos = 0
        self.shift = 0
        self.move()

        def change_color():
            current_color = self.FrameUnder["background"]
            next_color = "lightgreen" if current_color == "yellow" else "yellow"
            self.FrameUnder.config(background=next_color)
            self.master.after(3000, change_color)

        change_color()
        self.create_handlers()

    def create_handlers(self):
        '''Create all Handlers for LabelEdit'''
        def mouse_handler(event):
            self.focus()
            self.cur_pos = event.x // self.sym_width
            self.shift = 0
            # print(self.cur_pos)
            self.move()
            # print(self.FrameUnder.place_info() == {})
        self.bind('<Button-1>', mouse_handler)

        def key_handler(event):
            cur_S = self.S.get()
            if event.keysym == 'Tab':
                self.move()
                return
            if self.FrameUnder.place_info() == {}:
                return
            elif event.keysym in ('Left', 'KP_Left'):
                self.shift = self.shift - 1
                self.move()
            elif event.keysym in ('Right', 'KP_Right'):
                self.shift = self.shift + 1
                self.move()
            elif event.keysym == 'BackSpace':
                self.S.set(cur_S[:max(self.change_pos - 1, 0)] + cur_S[self.change_pos:])
                self.shift = self.shift - 1
                self.move()
            elif event.keysym == 'Delete':
                self.S.set(cur_S[:self.change_pos] + cur_S[self.change_pos + 1:])
            elif event.keysym == 'Home':
                self.cur_pos = 0
                self.shift = 0
                self.move()
            elif event.keysym == 'End':
                self.cur_pos = len(cur_S)
                self.shift = 0
                self.move()
            elif event.char:
                self.S.set(cur_S[:self.change_pos] + event.char + cur_S[self.change_pos:])
                self.shift = self.shift + 1
                self.move()
                self.focus_get()
        self.bind('<Any-Key>', key_handler)

    def move(self):
        self.change_pos = self.cur_pos
        # print(self.change_pos)
        self.change_pos += self.shift
        if self.change_pos < 0:
            self.change_pos = 0
        lenS = len(self.S.get())
        # print(lenS)
        if self.change_pos > lenS:
            self.change_pos = lenS
        # print(self.change_pos)
        self.FrameUnder.place(x=self.sym_width * self.change_pos, y=2)


class Application(tk.Frame):
    '''Sample tkinter application class'''

    def __init__(self, master=None, title="<application>", **kwargs):
        '''Create root window with frame, tune weight and resize'''
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()

    def create_widgets(self):
        '''Create all the widgets'''
        self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)
        self.LabelEdit_unit = LabelEdit(self)
        # self.LabelEdit_unit.grid(column=0, sticky="WE")
        self.LabelEdit_unit.pack(expand=1, fill='x')
        self.Quit = tk.Button(self, text="Quit", command=self.master.quit,
                              highlightcolor='lightblue')
        # self.Quit.grid(row=1, column=0, sticky="E")
        self.Quit.pack(expand=1, anchor='se')
        self.Quit.focus()
        # self.LabelEdit_unit.focus()


app = Application(title="LabelEdit")
app.mainloop()

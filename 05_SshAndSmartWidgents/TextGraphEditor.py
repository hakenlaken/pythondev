'''
Tkinter skeleton app
'''
import tkinter as tk
from itertools import product
import re


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
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        '''Create all the widgets'''


class App(Application):
    def create_widgets(self):
        super().create_widgets()

        self.canvas = tk.Canvas(self, bg='black')
        self.startpress = False
        self.Motion = False
        self.oval = 0
        self.oval_width = 3
        self.oval_outline = "pink"
        self.oval_fill = "forestgreen"

        self.T = tk.Text(self, bg='black')
        self.T.tag_config('SyntaxChecker', foreground='red')

        self.Q = tk.Button(self, text="Quit", command=self.master.quit)
        self.clearB = tk.Button(self, text="Clear", command=self.ClearHandler)
        self.drawB = tk.Button(self, text="DrawText", command=self.DrawTextHandler)

        self.canvas.bind("<Button-1>", self.OvalStart)
        self.canvas.bind("<B1-Motion>", self.OvalMotion)
        self.canvas.bind("<ButtonRelease-1>", self.OvalRelease)

        self.canvas.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="NEWS")
        self.T.grid(row=0, column=4, rowspan=4, columnspan=4, sticky="NEWS")
        self.Q.grid(row=4, column=0, sticky="NEWS")
        self.Q.grid(row=4, column=0, sticky="NEWS")
        self.clearB.grid(row=4, column=1, sticky="NEWS")
        self.drawB.grid(row=4, column=3, sticky="NEWS")

    def OvalStart(self, event):
        self.startpress = True
        self.starting_pos = [event.x, event.y]
        self.cur_pos = [event.x, event.y]
        oval_list = self.canvas.find_overlapping(*self.starting_pos, *self.cur_pos)
        if oval_list:
            self.oval = oval_list[-1]
        else:
            self.oval = 0
        if self.oval:
            self.Motion = True
        else:
            self.oval = self.canvas.create_oval((*self.starting_pos, *self.cur_pos), width=self.oval_width,
                                                outline=self.oval_outline, fill=self.oval_fill)
        self.cur_pos = self.canvas.coords(self.oval)

    def OvalMotion(self, event):
        if self.startpress and self.Motion:
            self.canvas.move(self.oval, event.x -
                             self.starting_pos[0], event.y - self.starting_pos[1])
            self.starting_pos[0], self.starting_pos[1] = event.x, event.y
        elif self.startpress and not(self.Motion):
            self.canvas.coords(
                self.oval, *self.starting_pos, event.x, event.y)

    def OvalRelease(self, event):
        if self.Motion:
            self.re_pattern = "<{start1},{start2},{end1},{end2}".format(start1=int(self.cur_pos[0]), start2=int(
                self.cur_pos[1]), end1=int(self.cur_pos[2]), end2=int(self.cur_pos[3]))
            self.re_search = self.T.search(self.re_pattern, '1.0')
            if self.re_search:
                self.new_pos = self.canvas.coords(self.oval)
                self.T.delete(self.re_search[0] + '.0 linestart',
                              str(int(self.re_search[0]) + 1) + '.0 linestart')
                self.T.insert(self.re_search[0] + '.0 linestart', 'oval<{start1},{start2},{cur1},{cur2},width={w},outline="{o}",fill="{f}">\n'.format(
                    start1=int(self.new_pos[0]), start2=int(self.new_pos[1]), cur1=int(self.new_pos[2]), cur2=int(self.new_pos[3]), w=self.oval_width, o=self.oval_outline, f=self.oval_fill))
        else:
            self.canvas.coords(self.oval, (*self.starting_pos, event.x, event.y))
            self.T.insert(tk.END, 'oval<{start1},{start2},{cur1},{cur2},width={w},outline="{o}",fill="{f}">\n'.format(
                start1=self.starting_pos[0], start2=self.starting_pos[1], cur1=event.x, cur2=event.y, w=self.oval_width, o=self.oval_outline, f=self.oval_fill))

        self.startpress = False
        self.Motion = False

    def ClearHandler(self):
        for i in self.canvas.find_all():
            self.canvas.delete(i)
        self.T.delete('1.0', 'end')

    def DrawTextHandler(self):
        # draw_coords, draw_width, draw_outline, draw_fill = ()
        for i in self.canvas.find_all():
            self.canvas.delete(i)
        self.lines = self.T.get('0.0', 'end').split('\n')
        for i, line in enumerate(self.lines):
            # draw_coords, draw_width, draw_outline, draw_fill = re.findall(r"<(.*),width=(.*),outline=\"(.*)\",fill=\"(.*)\"", line)[0]
            # print(draw_coords.split(','), draw_width, draw_outline, draw_fill, type(draw_coords), type(draw_width), type(draw_outline))
            if len(line):
                try:
                    draw_coords, draw_width, draw_outline, draw_fill = re.findall(
                        r"<(.*),width=(.*),outline=\"(.*)\",fill=\"(.*)\">", line)[0]
                    draw_coords = draw_coords.split(',')
                    self.canvas.create_oval(int(draw_coords[0]), int(draw_coords[1]), int(draw_coords[2]), int(draw_coords[3]), width=int(draw_width),
                                            outline=draw_outline, fill=draw_fill)
                except:
                    self.T.tag_add('SyntaxChecker', str(i + 1) +
                                   '.0 linestart', str(i + 1) + '.0 lineend')
                else:
                    self.T.tag_remove('SyntaxChecker', str(i + 1) +
                                      '.0 linestart', str(i + 1) + '.0 lineend')


app = App(title="Editor")
app.mainloop()

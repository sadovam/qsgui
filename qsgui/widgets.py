import tkinter as tk
from tkinter import ttk
from tkinter import X, Y, BOTH, END, VERTICAL, HORIZONTAL

class Widget:
    def __init__(self, expand=False):
        self.tkw = None
        self.expand = expand
        self.tag = ''
        self.commands = {}
        
    def add_command(self, name, command):
        self.commands[name] = lambda _: command(self)
        if self.tkw:
            self.tkw.bind(name, self.commands[name])
            
    def _build(self):
        if self.commands:
            for name, command in self.commands.items():
                self.tkw.bind(name, self.commands[name])


# ===========================
class Box(Widget):
    def __init__(self, expand=False, orient=Y):
        self.side, self.direct = ("top", X) if orient == Y else ("left", Y)
        super().__init__(expand)
        self.widgets = []
    
    def _create_tk(self, parent):
        self.tkw = ttk.Frame(parent.tkw)
    
    def _build(self):
        super()._build()
        if self.widgets:
            self._add(self.widgets)
        
    def _add(self, widgets):
        for w in widgets:
            w._create_tk(self)
            w.tkw.pack(side=self.side, 
                       fill=BOTH if w.expand else self.direct,
                       expand=w.expand)
            w._build()
        
    def append(self, *widgets):
        l = len(self.widgets)
        for w in widgets:
            if type(w) is str:
                w = Label(text=w)
            self.widgets.append(w)
        if self.tkw:
            self._add(self.widgets[l:])
            
    def __getitem__(self, index):
        return self.widgets[index]

        
class Scroll(Box):
    def __init__(self, direct=BOTH, expand=False):
        super().__init__(expand)
        self.direct = direct
        
    def _build(self):
        if self.direct == Y or self.direct == BOTH:
            self.yscrollbar = ttk.Scrollbar(self.tkw, orient='vertical')
            self.yscrollbar.grid(row=0, column=1, sticky='news')
        if self.direct == X or self.direct == BOTH:
            self.xscrollbar = ttk.Scrollbar(self.tkw, orient='horizontal')
            self.xscrollbar.grid(row=1, column=0, sticky='news')
        self.tkw.grid_rowconfigure(0, weight=1)
        self.tkw.grid_columnconfigure(0, weight=1)
        super()._build()
    
    def _add(self, widget):
        if len(widget) > 0:
            widget = widget[0]
        widget._create_tk(self)
        
        widget.tkw.grid(row=0, column=0, sticky="nsew")
        if self.direct == Y or self.direct == BOTH:
            self.yscrollbar.configure(command=widget.tkw.yview)
            widget.tkw.configure(yscrollcommand=self.yscrollbar.set)
        if self.direct == X or self.direct == BOTH:
            self.xscrollbar.configure(command=widget.tkw.xview)
            widget.tkw.configure(xscrollcommand=self.xscrollbar.set)
        widget._build()

class MainWindow(Box):
    def __init__(self, title="New QSGui Application"):
        super().__init__()
        self.tk = tk.Tk()
        self.tk.title(title)
        self.tkw = ttk.Frame(self.tk)
        self.tkw.pack(expand=True, fill=BOTH)
        self._build()
        
    def run(self):
        self.tk.mainloop()

class Grid(Box):
    def __init__(self, width=2, expand=False):
        self._width = width
        super().__init__(expand)
        self.x = 0
        self.y = 0
        
    def _create_tk(self, parent):
        self.parent = parent
        self.tkw = ttk.Frame(parent.tkw)
    
    def _add(self, widgets):
        for w in widgets:
            w._create_tk(self)
            w.tkw.grid(row=self.y, column=self.x, sticky='news')
            if w.expand:
                self.tkw.grid_rowconfigure(self.y, weight=1)
            self.tkw.grid_columnconfigure(self.x, weight=1)
            self.x += 1
            if self.x >= self._width:
                self.x = 0
                self.y += 1
            w._build()

class Split(Widget):
    def __init__(self, expand=False, orient=Y):
        self.orient = VERTICAL if orient == Y else HORIZONTAL
        super().__init__(expand)
        self.widgets = []
    
    def __getitem__(self, index):
        return self.widgets[index]
    
    def _create_tk(self, parent):
        self.tkw = ttk.PanedWindow(parent.tkw, orient=self.orient)
    
    def _build(self):
        super()._build()
        if self.widgets:
            self._add(self.widgets)
    
    def _add(self, widgets):
        for w in widgets:
            w._create_tk(self)
            weight = 1 if w.expand else 0
            self.tkw.add(w.tkw, weight=weight)
            w._build()
        
    def append(self, *widgets):
        l = len(self.widgets)
        for w in widgets:
            if type(w) is str:
                w = Label(text=w)
            self.widgets.append(w)
        if self.tkw:
            self._add(self.widgets[l:])


# ==========================

class Label(Widget):
    def __init__(self, text="", expand=False):
        super().__init__(expand)
        self._text = text
        self._color = ('', '')
        
    def _create_tk(self, parent):
        self.tkw = ttk.Label(parent.tkw, text=self.text, anchor=tk.CENTER)
        
    @property
    def text(self):
        if self.tkw:
            return self.tkw['text']
        return self._text
        
    @text.setter
    def text(self, text):
        self._text = text
        if self.tkw:
            self.tkw['text'] = text
            
    @property
    def color(self):
        if self.tkw:
            return self.tkw['foreground'], self.tkw['background']
        return self._color
        
    @color.setter
    def color(self, color):
        self._color = color
        if self.tkw:
            self.tkw['foreground'] = color[0] 
            self.tkw['background'] = color[1]


class Entry(Widget):
    def __init__(self, text="", expand=False):
        super().__init__(expand)
        self._text = text
        self._changes_cmd = None
        self._return_cmd = None
        
    def _create_tk(self, parent):
        self.tkw = ttk.Entry(parent.tkw)
    
    def _build(self):
        self.tkw.insert(END, self._text)
        if self._changes_cmd:
            self.tkw.bind("<KeyRelease>", self._changes_cmd)
        if self._return_cmd:
            self.tkw.bind("<Return>", self._return_cmd)
        super()._build()
        
    @property
    def text(self):
        if self.tkw:
            return self.tkw.get()
        return self._text
        
    @text.setter
    def text(self, text):
        self._text = text
        if self.tkw:
            self.tkw.delete(0, END)
            self.tkw.insert(END, text)
            
    @property
    def return_cmd(self):
        return self._return_cmd
        
    @return_cmd.setter
    def return_cmd(self, command):
        self._return_cmd = lambda _: command(self)
        if self.tkw:
            self.tkw.bind("<Return>", self._return_cmd)
            
    @property
    def changes_cmd(self):
        return self._changes_cmd
        
    @changes_cmd.setter
    def changes_cmd(self, command):
        self._changes_cmd = lambda _: command(self)
        if self.tkw:
            self.tkw.bind("<KeyRelease>", self._changes_cmd)
        

class Text(Widget):
    def __init__(self, text="", width=20, height=5, expand=False):
        super().__init__(expand)
        self._text = text
        self._changes_cmd = None
        self._width = width
        self._height = height
        
    def _create_tk(self, parent):
        self.tkw = tk.Text(parent.tkw, width=self._width, height=self._height)
    
    def _build(self):
        self.tkw.insert(END, self._text)
        if self._changes_cmd:
            self.tkw.bind("<KeyRelease>", self._changes_cmd)
        super()._build()
        
    @property
    def text(self):
        if self.tkw:
            return self.tkw.get(1.0, END).strip()
        return self._text
        
    @text.setter
    def text(self, text):
        self._text = text
        if self.tkw:
            self.tkw.delete(1.0, END)
            self.tkw.insert(1.0, text)
            
    @property
    def changes_cmd(self):
        return self._changes_cmd
        
    @changes_cmd.setter
    def changes_cmd(self, command):
        self._changes_cmd = lambda _: command(self)
        if self.tkw:
            self.tkw.bind("<KeyRelease>", self._changes_cmd)

class Button(Widget):
    def __init__(self, text="", command=None, expand=False):
        super().__init__(expand)
        self._text = text
        self._command = lambda: command(self)
        
    def _create_tk(self, parent):
        width = len(self.text) + 2
        self.tkw = ttk.Button(parent.tkw, text=self.text, 
                              command=self._command,
                              width=width)
    
    @property
    def text(self):
        if self.tkw:
            return self.tkw['text']
        return self._text
        
    @text.setter
    def text(self, text):
        self._text = text
        if self.tkw:
            self.tkw['text'] = text
            
    @property
    def command(self):
        if self.tkw:
            return self.tkw['command']
        return self._command
        
    @command.setter
    def command(self, command):
        self._command = lambda: command(self)
        if self.tkw:
            self.tkw['command'] = command


class Check(Widget):
    def __init__(self, text="", state=False, command=None, expand=False):
        super().__init__(expand)
        self._text = text
        self._command = lambda: command(self)
        self._variable = tk.BooleanVar()
        self._variable.set(state)
        
    def _create_tk(self, parent):
        self.tkw = ttk.Checkbutton(parent.tkw, text=self.text, 
                                   variable=self._variable, 
                                   command=self._command)
    
    @property
    def state(self):
        return self._variable.get()
        
    @state.setter
    def state(self, state):
        self._variable.set(state)
        
    @property
    def text(self):
        if self.tkw:
            return self.tkw['text']
        return self._text
        
    @text.setter
    def text(self, text):
        self._text = text
        if self.tkw:
            self.tkw['text'] = text
            
    @property
    def command(self):
        if self.tkw:
            return self.tkw['command']
        return self._command
        
    @command.setter
    def command(self, command):
        self._command = lambda: command(self)
        if self.tkw:
            self.tkw['command'] = command


class ComboBox(Widget):
    def __init__(self, values=(), expand=False):
        self._values = values
        super().__init__(expand)
        
    def _create_tk(self, parent):    
        self.tkw = ttk.Combobox(parent.tkw, values=self._values, state='readonly')
        
    
class Table(Widget):
    def __init__(self, columns=(), expand=False):
        self.columns = columns
        self._select_cmd = None
        super().__init__(expand)
        
    def _create_tk(self, parent):
        self.tkw = ttk.Treeview(parent.tkw, columns=self.columns, show='headings')
    
    def _build(self):
        if self._select_cmd:
            self.tkw.bind("<<TreeviewSelect>>", self._select_cmd)
        super()._build()
    
    def add(self, item):
        self.tkw.insert("", END, item[0], values=item)
        
    def get_select_key(self):
        sel = self.tkw.selection()
        if sel:
            return sel[0]
        return None
        
    @property
    def select_cmd(self):
        return self._select_cmd
        
    @select_cmd.setter
    def select_cmd(self, command):
        self._select_cmd = lambda _: command(self)
        if self.tkw:
            self.tkw.bind("<<TreeviewSelect>>", self._select_cmd)
X = 0
Y = 1
BOTH = 2


class Widget:
    def __init__(self, name) -> None:
        self._name = name
        self.template = f"<{self._name}>%s</{self._name}>"

    def make(self):
        print(self)


class Label(Widget):
    def __init__(self, text='--') -> None:
        super().__init__('Label')
        self.text = text

    def __str__(self):
        return self.template % self.text

class Button(Widget):
    def __init__(self, text="--", command=None) -> None:
        super().__init__('Button')
        self.text = text
        self.command = command

    def invoke(self):
        self.command()


class Container(Widget):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.widgets = []

    def add(self, *widgets: Widget):
        for w in widgets:
            self.widgets.append(w)
            w.make()


class Box(Container):
    def __init__(self, direction=Y) -> None:
        super().__init__('Box')
        self.direction = direction

    def __str__(self) -> str:
        endl = '\n' if self.direction else ''
        res = ''

        for w in self.widgets:
            res += str(w) + endl

        return self.template % res


class App(Box):
    def __init__(self, title='New Application') -> None:
        super().__init__()
        self.title = title

    def __str__(self) -> str:
        return '_-' + self.title + '-_\n' + super().__str__()
    
    def run(self):
        self.make()
        print("App runing...") 


if __name__ == '__main__':
    app = App("Hello!")
    lbl1 = Label("AAAAAA AA")
    lbl2 = Label("BBB")
    box1 = Box(direction=X)
    box1.add(lbl1)
    box1.add(lbl2)
    # print(box1)
    lbl3 = Label("SDAAAA AA")
    lbl4 = Label("BBB KKK")
    box2 = Box()
    box2.add(lbl3)
    box2.add(lbl4)
    # print(box2)
    app.add(box1)
    app.add(box2)
    app.run()

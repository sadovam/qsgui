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
    def __init__(self, text='--', name='Label') -> None:
        super().__init__(name)
        self.text = text

    def __str__(self):
        return self.template % self.text

class Button(Label):
    def __init__(self, text="--", command=None) -> None:
        super().__init__(text, 'Button')
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
    def __init__(self, direction=Y, name='Box') -> None:
        super().__init__(name)
        self.direction = direction

    def __str__(self) -> str:
        endl = '\n' if self.direction else ''
        res = ''

        for w in self.widgets:
            res += str(w) + endl

        return self.template % res


class App(Box):
    def __init__(self, title='New Application') -> None:
        super().__init__(name='App')
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
    box1.add(lbl1, lbl2)
    lbl3 = Label("SDAAAA AA")
    lbl4 = Label("BBB KKK")
    box2 = Box()
    box2.add(lbl3, lbl4)
    app.add(box1)
    app.add(box2)
    def change_lbl1():
        lbl1.text = '1234567'
    btn1 = Button("press me", change_lbl1)
    box2.add(btn1)

    app.run()

    btn1.invoke()
    app.make()

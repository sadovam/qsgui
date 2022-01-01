from qsgui.widgets import *

root = MainWindow()
    
hbox = Box(expand=True, orient=X)
text = "Quite Simple Gui\n Application"
l = Label(text, expand=True)
hbox.append("Hello world", l)

def set_state(w):
    l.text = '  %s %s' % (w.text, w.state)

grid = Grid(3, expand=True)
for i in range(13):
    grid.append(Check(text="chk %s" % i, command=set_state, state=True))
grid.append(Label("111", expand=True), "222", "333", Label("www", expand=True))

vbox = Box()
lbls = list([Label("label #%s" % i) for i in range(4)])
entry = Entry("some text")
txt = Text(expand=True)
scroll = Scroll(expand=True, direct=Y)
scroll.append(txt)
vbox.append(*lbls, entry, scroll)

def l0chg(w):
    lbls[0].text = w.text

def l1chg(w):
    lbls[1].text = w.text

def l2chg(w):
    lbls[2].text = txt.text
    w.text = entry.text

def l3chg(w):
    lbls[3].text = w.text
    
txt.changes_cmd = l3chg
entry.return_cmd = l0chg
entry.changes_cmd = l1chg
but = Button("Press me")
but.command = l2chg
vbox.append(but)
split = Split(expand=True, orient=X)
split.append(hbox, grid, vbox, Table(expand=True, columns=("12345", "67890")))
root.append(split) 
cb = ComboBox(values=("123", "qwer", "bnvh76"))
vbox.append(cb)   
    
root.run()

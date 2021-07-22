#!usr/bin/python

import urwid
import os

#os.system('keepsync')
menupad=5

def keyHandler(k):
    # TODO why is this slow?
    if k == 'j':
        os.system("2>/dev/null 1>/dev/null ydotool key Down")
    elif k == 'k':
        os.system("2>/dev/null 1>/dev/null ydotool key Up")
    elif k == 'q':
        raise urwid.ExitMainLoop()


def getTerminalSize():
    #import shlex
    import struct
    #import platform
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])


termSize = getTerminalSize()
tw = termSize[0]
th = termSize[1]


def buttonTextLength(padding):
    maxlen = tw*0.5
    maxlen = maxlen - 10 - (padding * 2)
    return int(maxlen)


class CustomButton(urwid.Button):
    button_left = urwid.Text('|')
    button_right = urwid.Text('|')


class Note:
    def __init__(self, number, title, content):
        self.number = number
        self.title = title
        self.content = content


def getTitle(n):
    if len(n.title) > buttonTextLength(menupad):
        resp = n.title[0:buttonTextLength(menupad)]
    else:
        resp = n.title
    return resp


path = "/home/dave/notes/"
dirNotes = os.popen("ls /home/dave/notes/").read().split()

noteList = []
urwidTexts = []

for filename in dirNotes:
    with open(path + filename, "r+") as file:
        note = Note(filename[0:2], filename[3:], file.read())
        noteList.append(note)

for item in noteList:
    box = urwid.Filler(urwid.Text(item.content), 'top')
    urwidTexts.append(box)


def choiceMade(b, c):
    for i in noteList:
        if i.title == c:
            newNote = urwid.Padding(urwid.Filler(urwid.Text(i.content), 'top'))
            cols.contents[1] = (newNote, cols.options())


def makeMenu(options):
    optboxcontent = []
    for o in map(getTitle, options):
        button = CustomButton(o)
        urwid.connect_signal(button, 'click', choiceMade, o)
        optboxcontent.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(optboxcontent))


menu = urwid.Padding(makeMenu(noteList), left=menupad, right=menupad)

noteWindow = urwid.Padding(urwidTexts[0])

cols = urwid.Columns(
                     [menu,noteWindow],
                     dividechars=10,
                     focus_column=None,
                     min_width=20,
                     box_columns=None
)
urwid.MainLoop(cols,
               palette=[('reversed', 'bold', 'dark red')],
               unhandled_input=keyHandler).run()

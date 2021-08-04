from tkinter import *
import NewMenu
import MapMaker


class MainMenu:
    def __init__(self, Master):
        self._master = Master
        self._master.title("Spudnick Map Maker")
        self._frame = Frame(self._master)

        self._lblTitle = Label(self._frame, text="Spudnick Map Maker")
        self._lblTitle.pack()

        self._btnNew = Button(self._frame, text="New Map", command=self.new)
        self._btnNew.pack()

        self._btnOpen = Button(self._frame, text="Open Map file", command=self.open)
        self._btnOpen.pack()

        self._frame.pack()

        mainloop()

    def new(self):
        self._frame.destroy()
        NewMenu.NewMenu(self._master)

    def open(self):
        self._frame.destroy()
        MapMaker.MapMaker(self._master, 0, 0)

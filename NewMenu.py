from tkinter import *
import MapMaker


class NewMenu:
    def __init__(self, Master):
        self._master = Master
        self._master.title("Spudnick Map Maker")
        self._frame = Frame(self._master)

        self._lblTitle = Label(self._frame, text="Spudnick Map Maker")
        self._lblTitle.grid(row=0, columnspan=2)

        self._lblNumRows = Label(self._frame, text="Number of rows")
        self._lblNumRows.grid(row=1, column=0)

        self._lblNumCols = Label(self._frame, text="Number of Columns")
        self._lblNumCols.grid(row=1, column=1)

        self._sbNumRows = Spinbox(self._frame, from_=1, to=100)
        self._sbNumRows.grid(row=2, column=0)

        self._sbNumCols = Spinbox(self._frame, from_=1, to=100)
        self._sbNumCols.grid(row=2, column=1)

        self._btnCreate = Button(self._frame, text="Create Map", command=self.openMapMaker)
        self._btnCreate.grid(row=3, columnspan=2)

        self._frame.pack()
        mainloop()

    def openMapMaker(self):
        rows = int(self._sbNumRows.get())
        cols = int(self._sbNumCols.get())
        self._frame.destroy()
        MapMaker.MapMaker(self._master, rows, cols)
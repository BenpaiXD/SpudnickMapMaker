import os
from tkinter import *
from functools import partial
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from PIL import Image, ImageTk


# from tkinter.ttk import *


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
        MapMaker(self._master, rows, cols)


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
        NewMenu(self._master)

    def open(self):
        self._frame.destroy()
        MapMaker(self._master, 0, 0)


class MapMaker:
    def __init__(self, master, rows, cols):
        self._master = master
        self._rows = rows
        self._cols = cols
        self._photos = imageList(r'venv\GroundTiles')
        self._tileIndex = len(self._photos) - 1
        self._multiTileStage = 0
        self._multiTileIndex = None

        self._menu = Menu(self._master)
        self._master.config(menu=self._menu)

        self._fileMenu = Menu(self._menu)
        self._menu.add_cascade(label='File', menu=self._fileMenu)
        self._fileMenu.add_command(label="New", command=self.new)
        self._fileMenu.add_command(label="Open", command=self.open)
        self._fileMenu.add_command(label="Save As", command=self.save)


        # left frame set up
        self._frameLeft = Frame(self._master)

        self._lblMode = Label(self._frameLeft, text="Chose Mode")
        self._lblMode.grid(row=0, columnspan=2)

        self._mode = IntVar()

        self._rbSingle = Radiobutton(self._frameLeft, text="Single Tile", variable=self._mode, value=0)
        self._rbSingle.grid(row=1, sticky="W")

        self._rbMulti = Radiobutton(self._frameLeft, text="Multi Tile", variable=self._mode, value=1)
        self._rbMulti.grid(row=2, sticky="W")

        self._rbRemoveRow = Radiobutton(self._frameLeft, text="Remove Row", variable=self._mode, value=2)
        self._rbRemoveRow.grid(row=3, sticky="W")

        self._rbRemoveCol = Radiobutton(self._frameLeft, text="Remove Column", variable=self._mode, value=3)
        self._rbRemoveCol.grid(row=4, sticky="W")

        self._rbAddRow = Radiobutton(self._frameLeft, text="Add Row", variable=self._mode, value=4)
        self._rbAddRow.grid(row=5, sticky="W")

        self._AB = IntVar()
        self._rbAbove = Radiobutton(self._frameLeft, text="Above", variable=self._AB, value=0)
        self._rbAbove.grid(row=5, column=1, sticky="W")

        self._rbBelow = Radiobutton(self._frameLeft, text="Below", variable=self._AB, value=1)
        self._rbBelow.grid(row=6, column=1, sticky="W")

        self._rbAddCol = Radiobutton(self._frameLeft, text="Add Column", variable=self._mode, value=5)
        self._rbAddCol.grid(row=7, sticky="W")

        self._LR = IntVar()
        self._rbLeft = Radiobutton(self._frameLeft, text="Left", variable=self._LR, value=0)
        self._rbLeft.grid(row=7, column=1, sticky="W")

        self._rbRight = Radiobutton(self._frameLeft, text="Right", variable=self._LR, value=1)
        self._rbRight.grid(row=8, column=1, sticky="W")

        self._lblTile = Label(self._frameLeft, image=self._photos[-1])
        self._lblTile.grid(row=9)

        self._lblComment = Label(self._frameLeft, text="H:14 W:24")
        self._lblComment.grid(row=10)

        self._frameLeft.grid(row=0, column=0)


        # right frame set up
        self._frameRight = Frame(self._master)

        self._mapCanvas = Canvas(self._frameRight)
        self._mapFrame = Frame(self._mapCanvas)
        self._vsb = Scrollbar(self._frameRight, orient="vertical", command=self._mapCanvas.yview)
        self._hsb = Scrollbar(self._frameRight, orient="horizontal", command=self._mapCanvas.xview)
        self._mapCanvas.configure(yscrollcommand=self._vsb.set, xscrollcommand=self._hsb.set)

        self._vsb.pack(side="right", fill="y")
        self._hsb.pack(side="bottom", fill="x")
        self._mapCanvas.pack(side="left", fill="both", expand=True)
        self._mapCanvas.create_window((4, 4), window=self._mapFrame, anchor="nw")

        self._mapFrame.bind("<Configure>", self.onFrameConfigure)

        self._frameRight.grid(row=0, column=1, columnspan=5)

        self._mapArray = []
        self._buttonMap = []

        # Bottom frame set up
        self._frameBottom = Frame(self._master)

        self._btnTiles = []

        for i in range(len(self._photos)):
            self._btnTiles.append(Button(self._frameBottom, image=self._photos[i], command=partial(self.select, i)))
            self._btnTiles[i].grid(row=0, column=i)

        # self._btnTiles[2].config(command=lambda: self.select(2))

        self._frameBottom.grid(row=1, column=0, columnspan=2)

        if self._rows == 0:
            self.open()
        else:
            self.mapSetup()

        # window size change
        self._master.bind("<Configure>", self.onFrameConfigure)

        mainloop()

    def mapSetup(self, lines=None):
        self._mapArray = []
        self._buttonMap = []

        # loop to set up tile placement
        for i in range(self._rows):
            arr = []
            buttonArr = []
            if lines is not None:
                lines[i] = lines[i].split()
            for j in range(self._cols):
                if lines is None:
                    arr.append(14)
                    buttonArr.append(Button(self._mapFrame, text=str(14), image=self._photos[-1], borderwidth=0,
                                            command=partial(self.tileChange, i, j)))
                else:
                    arr.append(int(lines[i][j]))
                    buttonArr.append(Button(self._mapFrame, text=int(lines[i][j]), image=self._photos[int(lines[i][j])], borderwidth=0,
                                         command=partial(self.tileChange, i, j)))

                buttonArr[j].grid(row=i, column=j)

            self._mapArray.append(arr)
            self._buttonMap.append(buttonArr)

    def onFrameConfigure(self, event):
        self._mapCanvas.configure(scrollregion=self._mapCanvas.bbox("all"))
        self._frameRight.config(width=(self._master.winfo_width() - self._frameLeft.winfo_width()), height=(self._master.winfo_height() - self._frameBottom.winfo_height()))

    def select(self, i):
        self._lblTile.config(image=self._photos[i])
        self._tileIndex = i

    def new(self):
        self._frameLeft.destroy()
        self._frameBottom.destroy()
        self._frameRight.destroy()
        self._menu.destroy()
        NewMenu(self._master)

    def open(self):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))

        if filename == "":
            self.new()
        else:
            mapFile = open(filename, "r")

            self._rows = 0
            self._cols = 0
            lines = mapFile.readlines()
            for line in lines:
                if line == "|\n":
                    break
                self._rows += 1

            lines = lines[:self._rows]

            self._cols = len(lines[0].split())

            self.mapSetup(lines)

            self._frameRight.grid(row=0, column=1)
            mapFile.close()

            print(len(self._buttonMap))
            print(len(self._photos))

    def save(self):
        file = asksaveasfile(mode='w', defaultextension=".txt")
        if file is None:
            return

        for array in self._mapArray:
            for tile in array:
                if tile < 10:
                    file.write("0" + str(tile) + " ")
                else:
                    file.write(str(tile) + " ")
            file.write("\n")
        file.write("|\n")

    def tileChange(self, i, j):
        # single tile change mode
        if self._mode.get() == 0:
            self._buttonMap[i][j].config(image=self._photos[self._tileIndex])
            self._mapArray[i][j] = self._tileIndex
            self._multiTileStage = 0

        # multi tile change mode
        elif self._mode.get() == 1:
            if self._multiTileStage == 0:
                self._multiTileIndex = (i, j)
                self._multiTileStage = 1
            else:
                for i2 in range(min(self._multiTileIndex[0], i), max(self._multiTileIndex[0], i) + 1):
                    for j2 in range(min(self._multiTileIndex[1], j), max(self._multiTileIndex[1], j) + 1):
                        self._buttonMap[i2][j2].config(image=self._photos[self._tileIndex])
                        self._mapArray[i2][j2] = self._tileIndex
                self._multiTileStage = 0

        # remove row mode
        elif self._mode.get() == 2:
            self._mapArray.pop(i)
            for button in self._buttonMap[i]:
                button.destroy()
            self._buttonMap.pop(i)
            self._rows -= 1

            for i2 in range(i, self._rows):
                for j2 in range(self._cols):
                    self._buttonMap[i2][j2].grid(row=i2)
                    self._buttonMap[i2][j2].config(command=partial(self.tileChange, i2, j2))

        # remove column mode
        elif self._mode.get() == 3:
            for i2 in range(0, self._rows):
                self._mapArray[i2].pop(j)
                self._buttonMap[i2][j].destroy()
                self._buttonMap[i2].pop(j)
            self._cols -= 1

            for i2 in range(self._rows):
                for j2 in range(j, self._cols):
                    self._buttonMap[i2][j2].grid(column=j2)
                    self._buttonMap[i2][j2].config(command=partial(self.tileChange, i2, j2))

        # add row mode
        elif self._mode.get() == 4:
            numRow = []
            btnRow = []

            for i2 in range(len(self._mapArray[0])):
                numRow.append(len(self._photos) - 1)
                btnRow.append(
                    Button(self._mapFrame, text=str(len(self._photos) - 1), image=self._photos[-1], borderwidth=0,
                           command=partial(self.tileChange, i + self._AB.get(), i2)))
                # btnRow[i2].grid(row=i + self._AB.get(), column=i2)
            self._mapArray.insert(i + self._AB.get(), numRow)
            self._buttonMap.insert(i + self._AB.get(), btnRow)
            self._rows += 1

            for i2 in range(self._rows):
                for j2 in range(self._cols):
                    self._buttonMap[i2][j2].grid(row=i2, column=j2)
                    self._buttonMap[i2][j2].config(command=partial(self.tileChange, i2, j2))

        # add column mode
        elif self._mode.get() == 5:
            for i2 in range(len(self._mapArray)):
                self._mapArray[i2].insert(j + self._LR.get(), len(self._photos) - 1)
                self._buttonMap[i2].insert(j + self._LR.get(), Button(self._mapFrame, text=str(len(self._photos) - 1),
                                                                      image=self._photos[-1], borderwidth=0,
                                                                      command=partial(self.tileChange, i2,
                                                                                      j + self._LR.get())))
            self._cols += 1

            for i2 in range(self._rows):
                for j2 in range(self._cols):
                    self._buttonMap[i2][j2].grid(row=i2, column=j2)
                    self._buttonMap[i2][j2].config(command=partial(self.tileChange, i2, j2))


def imageList(directory):
    lst = []
    ID = 0
    for file in os.listdir(directory):

        if file.endswith(".jpg") or file.endswith(".png"):
            lst.append(PhotoImage(file=os.path.join(directory, file)))
            ID += 1

    return lst


def scale(spriteList, width, height):
    for i in range(len(spriteList)):
        spriteList[i] = (spriteList[i], (width, height))
    return spriteList


def main():
    root = Tk()
    MainMenu(root)


if __name__ == '__main__':
    main()

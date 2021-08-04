import os
from tkinter import *
import MainMenu


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
    MainMenu.MainMenu(root)


if __name__ == '__main__':
    main()

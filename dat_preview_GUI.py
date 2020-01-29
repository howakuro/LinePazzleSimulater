from tkinter import *
from tkinter import ttk, font
from functools import partial
import numpy as np
import puzzle as pz

import pickle
import os

if __name__ == '__main__':
	# tkinter 設定
	root = Tk()
	root.title("dat preview GUI")
	root.geometry("480x460")
	root.minsize(480, 460)
	root.mainloop()
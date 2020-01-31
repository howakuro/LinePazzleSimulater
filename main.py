from tkinter import *
from tkinter import ttk, font
from src import Game_Record
from src import Game_View
from src import Record_View
from src import puzzle

import os

if __name__ == '__main__':
    # 実行環境パス
    file_dir = os.path.dirname(os.path.abspath(__file__))

    # dat 初期化
    dat_file = Game_Record(file_dir)

    # 疑似環境呼び出し
    env = puzzle.Touhou_Line_Pazzle()
    field = env.get_board_GUI().flatten()

    # tkinter 設定
    root = Tk()
    root.title("Touhou Line Puzzle Simulator")
    root.geometry("480x470")
    root.minsize(480, 480)
    root.maxsize(480, 480)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    record_view = Record_View(root, dat_file)
    game_view = Game_View(root, env, dat_file)

    game_view.set_move_btn_change_frame(record_view.frame)
    game_view.set_move_btn_event(record_view.update_tree)
    record_view.set_back_btn_change_frame(game_view.frame)

    root.mainloop()
from tkinter import *
from tkinter import ttk, font
from functools import partial
from src.game_record import Game_Record

class Record_View():
    def __init__(self, root, dat_file):
      # datファイル保持
      self.dat_file = dat_file
      # treeview作成
      self.frame  = ttk.Frame(root)
      self.tree = ttk.Treeview(self.frame)
      self.header_list    = ["Number", "Score", "Tile"]
      
      data_index     = (1,2,3)
      self.tree["column"] = data_index
      self.tree["show"]   = "headings"
      
      for i in data_index:
        self.tree.heading(i, text=self.header_list[i-1])
        self.tree.column(i, width=100, anchor=CENTER)
      
      self.update_tree()
      
      # 戻るボタン作成
      back_btn = Button(self.frame, text="戻る", command=self.back_btn_action)
      back_btn.pack()
      self.tree.pack(fill=BOTH, expand=1)
      
      self.frame.grid(row=0, column=0, sticky="nsew")

    def set_back_btn_change_frame(self, frame):
      self.back_btn_change_frame = frame

    def update_tree(self):
      self.tree.delete(*self.tree.get_children())
      for i, (score, tile) in enumerate(self.dat_file.data):
        self.tree.insert("", "end", values=(str(i+1), str(score), str(tile)))

    def back_btn_action(self):
      self.back_btn_change_frame.tkraise()
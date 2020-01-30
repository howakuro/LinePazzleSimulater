from tkinter import *
from tkinter import ttk, font
from functools import partial
import numpy as np
from decimal import Decimal, ROUND_HALF_UP

import csv
import pickle
import os

"""
game_recordsに保存されているdatファイル群の解析を出力するプログラム。

"ID"            : ファイル名
"MAX_SCORE"     : 最大スコア
"MAX_TILE"      : 最小スコア
"AVERAGE_SCORE" : 平均スコア
"AVERAGE_TILE"  : 平均最大タイル
"PLAY_NUM"      : プレイ回数

各ヘッダ部分をクリックすることで昇順・降順ソートを交互に行う。

CSV出力ボタン
  現在表示されている表をgame_records/game_records.csvに保存する。

最小回数変換ボタン
  「game_recordsの中でのプレイ最小回数」分のデータを
  各game_recordの先頭から抽出したデータに変更する。
"""

class DataImport():
	def __init__(self):
		self.now_directory    = os.path.dirname(os.path.abspath(__file__))
		self.data_folder_name = "game_records"
		self.data_folder_path = os.path.join(self.now_directory, self.data_folder_name)
		self.csv_name         = "game_records.csv"
		self.csv_path         = os.path.join(self.data_folder_path, self.csv_name)
		self.data_list        = []
		self.header_list      = ["ID", "MAX_SCORE", "MAX_TILE", "AVERAGE_SCORE", "AVERAGE_TILE", "PLAY_NUM"]
		self.print_round      = '0.1'
		self.sort_reverse     = False
		self.sort_key         = "ID"
		self.min_num          = float('inf')
		self.min_flag         = False
		
		if os.path.isdir(self.data_folder_path):
			for i in os.listdir(self.data_folder_path):
				p = os.path.join(self.data_folder_path, i)
				name, ext = os.path.splitext(i)
				if ext != ".dat": continue
				with open(p, 'rb') as f:
					data = pickle.load(f)
					m_score, m_tile = np.max(data, axis=0)
					a_score, a_tile = np.average(data, axis=0)
					data_dict                  = {}
					data_dict["ID"]            = name.upper()
					data_dict["DATA"]          = data
					data_dict["MAX_SCORE"]     = m_score
					data_dict["MAX_TILE"]      = m_tile
					data_dict["AVERAGE_SCORE"] = float(Decimal(str(a_score)).quantize(Decimal(self.print_round), rounding=ROUND_HALF_UP))
					data_dict["AVERAGE_TILE"]  = float(Decimal(str(a_tile)).quantize(Decimal(self.print_round), rounding=ROUND_HALF_UP))
					data_dict["PLAY_NUM"]      = len(data)
					self.data_list.append(data_dict)
		
		if self.data_list:
			self.min_num = min([i["PLAY_NUM"] for i in self.data_list])
		
		for i in self.data_list:
			data_min = i["DATA"][:self.min_num]
			m_score, m_tile = np.max(data_min, axis=0)
			a_score, a_tile = np.average(data_min, axis=0)
			i["BACK_MAX_SCORE"]     = m_score
			i["BACK_MAX_TILE"]      = m_tile
			i["BACK_AVERAGE_SCORE"] = float(Decimal(str(a_score)).quantize(Decimal(self.print_round), rounding=ROUND_HALF_UP))
			i["BACK_AVERAGE_TILE"]  = float(Decimal(str(a_tile)).quantize(Decimal(self.print_round), rounding=ROUND_HALF_UP))
	
	def search(self, ID):
		#IDで検索を掛ける関数
		for data_dict in self.data_list:
			if data_dict["ID"] == str(ID):
				return data_dict
		return None
	
	def research_data(self):
		self.min_flag = not(self.min_flag)
		for i in self.data_list:
			i["BACK_MAX_SCORE"]    , i["MAX_SCORE"]     = i["MAX_SCORE"]     , i["BACK_MAX_SCORE"]
			i["BACK_MAX_TILE"]     , i["MAX_TILE"]      = i["MAX_TILE"]      , i["BACK_MAX_TILE"]
			i["BACK_AVERAGE_SCORE"], i["AVERAGE_SCORE"] = i["AVERAGE_SCORE"] , i["BACK_AVERAGE_SCORE"]
			i["BACK_AVERAGE_TILE"] , i["AVERAGE_TILE"]  = i["AVERAGE_TILE"]  , i["BACK_AVERAGE_TILE"]
	
	def sort_list(self, head):
		if self.sort_key == head:
			self.sort_reverse = not(self.sort_reverse)
			self.data_list    = sorted(self.data_list, key=lambda x:x[head], reverse=self.sort_reverse)
		else :
			self.sort_reverse = False
			self.sort_key     = head
			self.data_list    = sorted(self.data_list, key=lambda x:x[head], reverse=self.sort_reverse)
	
	def export_csv(self):
		with open(self.csv_path, "w", newline="") as f:
			writer = csv.writer(f, delimiter=",")
			writer.writerow([self.header_list[i] for i in list(range(len(self.header_list)))])
			for i in range(len(self.data_list)):
				writer.writerow([dat_db.data_list[i][j] for j in dat_db.header_list])

def header_action(dat_db, head, tree):
	dat_db.sort_list(head)
	update_tree(tree, dat_db)

def min_btn_action(dat_db, tree):
	dat_db.research_data()
	update_tree(tree, dat_db)

def update_tree(tree, dat_db):
	tree.delete(*tree.get_children())
	for i in range(len(dat_db.data_list)):
		tree.insert("", "end", values=[dat_db.data_list[i][j] for j in dat_db.header_list])

def Abstract_Data_View(root, dat_db):
	# treeview作成
	frame  = ttk.Frame(root)
	tree   = ttk.Treeview(frame)
	
	data_index     = tuple(range(1, len(dat_db.header_list)+1))
	tree["column"] = data_index
	tree["show"]   = "headings"
	
	for i in data_index:
		cmd = partial(header_action, dat_db, dat_db.header_list[i-1], tree)
		tree.heading(i, text=dat_db.header_list[i-1], command=cmd)
		tree.column(i, width=100, anchor=CENTER)
	
	for i in range(len(dat_db.data_list)):
		tree.insert("", "end", values=[dat_db.data_list[i][j] for j in dat_db.header_list])
	
	# csv生成ボタン作成
	csv_btn = Button(frame, text="CSV出力", command=dat_db.export_csv)
	
	# 最小回数一致ボタン作成
	cmd = partial(min_btn_action, dat_db, tree)
	min_btn = Button(frame, text="最小回数変換", command=cmd)
	
	csv_btn.pack()
	min_btn.pack()
	tree.pack(fill=BOTH, expand=1)
	return frame, tree

def Detail_Data_View(root, dat_db, back_func):
	# treeview作成
	frame  = ttk.Frame(root)
	tree   = ttk.Treeview(frame)
	
	header_list    = ["Number", "Score", "Tile"]
	data_index     = (1,2,3)
	tree["column"] = data_index
	tree["show"]   = "headings"
	
	for i in data_index:
		tree.heading(i, text=header_list[i-1])
		tree.column(i, width=100, anchor=CENTER)
	
	# 戻るボタン作成
	back_btn = Button(frame, text="戻る", command=back_func)
	
	back_btn.pack()
	tree.pack(fill=BOTH, expand=1)
	return frame, tree

def tree_selection_event(event, dat_db=None, abs_tree=None, det_tree=None, det_frame=None):
	det_tree.delete(*det_tree.get_children())
	data = dat_db.search(abs_tree.set(abs_tree.selection()[0])["1"])
	for i, (score, tile) in enumerate(data["DATA"]):
		tag = "Min" if i < dat_db.min_num else ""
		det_tree.insert("", "end", values=(str(i+1), str(score), str(tile)), tags=(tag, ))
	det_tree.tag_configure("Min", background="cyan")
	det_frame.tkraise()

def back_btn_action(abs_frame):
	abs_frame.tkraise()

if __name__ == '__main__':
	# tkinter 設定
	root = Tk()
	root.title("dat preview GUI")
	root.geometry("640x480")
	root.minsize(640, 480)
	root.grid_rowconfigure(0, weight=1)
	root.grid_columnconfigure(0, weight=1)
	
	# データ取得
	dat_db = DataImport()
	
	# frame作成
	abs_frame, abs_tree = Abstract_Data_View(root, dat_db)
	det_frame, det_tree = Detail_Data_View(root, dat_db, partial(back_btn_action, abs_frame))
	
	# イベント設定
	cmd = partial(tree_selection_event, dat_db=dat_db, abs_tree=abs_tree, det_tree=det_tree, det_frame=det_frame)
	abs_tree.bind('<<TreeviewSelect>>', cmd)
	
	# 配置設定
	abs_frame.grid(row=0, column=0, sticky="nsew")
	det_frame.grid(row=0, column=0, sticky="nsew")
	abs_frame.tkraise()
	
	root.mainloop()

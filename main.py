from tkinter import *
from tkinter import ttk, font
from functools import partial
import numpy as np
import puzzle as pz

import pickle
import os

bg_color = ["light cyan",
            "gray85",
            "dark orange",
            "khaki1",
            "plum2",
            "SteelBlue3",
            "chartreuse2",
            "RosyBrown3",
            "cyan2",
            "VioletRed2"
]

class Game_Record():
	def __init__(self):
		os.chdir(os.path.dirname(os.path.abspath(__file__)))
		self.path = os.path.join(os.getcwd(), "game_record.dat")
		self.can_write = True
		self.data = []
		if os.path.isfile(self.path): #ファイルが存在するときファイル読み込み
			with open(self.path, 'rb') as f:
				self.data = pickle.load(f)

	def get_max_record(self):
		max_score, max_tile = np.max(self.data, axis=0)
		return maxscore, maxtile

	def get_play_count(self):
		return len(self.data)

	def can_write_reset(self):
		self.can_write= True

	def write_check(self, done):
		return self.can_write and done

	def write_record(self, env):
		field = env.get_board_GUI().flatten()
		total_score = env.total_score
		max_tile = np.max(field)
		self.data.append([total_score, max_tile])
		with open(self.path, 'wb') as f:
			pickle.dump(self.data , f)
		self.can_write = False

def game_over_check(label_list):
	field = env.get_board_GUI().flatten()
	return label_list[field.size+2]['text'] == "GAME OVER"

def update_label(env, label_list, done, dat_file):
	field = env.get_board_GUI().flatten()
	for i in range(field.size):
		label_list[i]['text']  = str("" if field[i]==0 else field[i])
		label_list[i]['bg']    = bg_color[field[i]%10]
	have_tile = 0 if env.have_tile == None else env.have_tile
	label_list[field.size]['text'] = str("" if have_tile == 0 else have_tile)
	label_list[field.size]['bg']   = bg_color[have_tile%10]
	label_list[field.size+1]['text'] = str(env.total_score)
	label_list[field.size+2]['text'] = "GAME OVER" if done else ""
	label_list[field.size+3]['text'] = str(dat_file.get_play_count())

def btn_action(env, label_list, i, dat_file):
	if not game_over_check(label_list): 
		_, _, done, _ = env.step(i)
		update_label(env, label_list, done, dat_file)
		if dat_file.write_check(done):
			dat_file.write_record(env)

def btn_reset(env, label_list ,dat_file):
	if game_over_check(label_list): 
		env.reset()
		done = False
		update_label(env, label_list, done, dat_file)
		dat_file.can_write_reset()

if __name__ == '__main__':
	# dat 初期化
	dat_file = Game_Record()

	# tkinter 設定
	root = Tk()
	root.title("Touhou Line Puzzle Simulator")
	root.geometry("360x510")
	root.minsize(360, 510)
	
	tilefont  = font.Font(size=30)
	btnfont   = font.Font(size=15)
	scorefont = font.Font(size=20)
	
	field_frame = ttk.Frame(
		root,
		height=480,
		width=640,
		relief='sunken',
		borderwidth=5
	)

	record_frame = ttk.Frame(
		root
	)

	score_frame = ttk.Frame(
		record_frame
	)

	play_count_frame = ttk.Frame(
		record_frame
	)
	
	# 疑似環境呼び出し
	env = pz.Touhou_Line_Pazzle()
	field = env.get_board_GUI().flatten()
	
	# ラベル変更用リスト
	label_list = []
	
	# フィールド用ラベル記述
	for i in range(field.size):
		text = str("" if field[i]==0 else field[i])
		lab = Label(field_frame, text=text, fg="black", bg=bg_color[field[i]%10], font=tilefont)
		lab.grid(row=i//env.width+1, column=i%env.width, sticky=W+E)
		label_list.append(lab)
	
	# ホールド用ラベル記述
	lab = Label(field_frame, text=str("" if env.have_tile == None else env.have_tile), fg="black", bg=bg_color[field[i]%10], font=tilefont)
	lab.grid(row=env.height+2, column=env.width//2, sticky=W+E)
	label_list.append(lab)
	
	# スコア用ラベル記述
	lab = Label(score_frame, text="SCORE", font=scorefont)
	lab.pack(side="top")
	lab = Label(score_frame, text="0", font=scorefont)
	lab.pack(side="top")
	label_list.append(lab)

	# GAMEOVER用ラベル記述
	gameover_lab = Label(root, text="", font=scorefont)
	label_list.append(gameover_lab)

	# プレイ回数用ラベル記述
	play_count = dat_file.get_play_count()
	lab = Label(play_count_frame, text="PLAYCOUNT", font=scorefont)
	lab.pack(side="top")
	lab = Label(play_count_frame, text=str(play_count), font=scorefont)
	lab.pack(side="top")
	label_list.append(lab)
	
	# リセットボタン記述
	cmd = partial(btn_reset, env, label_list, dat_file)
	reset_btn = Button(root, text="リセット", command=cmd, font=btnfont)
	
	# 選択ボタン記述
	for i in range(5):
		cmd = partial(btn_action, env, label_list, i, dat_file)
		btn = Button(field_frame, text="選択", command=cmd, font=btnfont)
		btn.grid(row=env.height+3, column=i, sticky=W+E)
	
	score_frame.pack(side="left", padx=20)
	play_count_frame.pack(side="right", padx=20)
	record_frame.pack()
	field_frame.pack()
	gameover_lab.pack()
	reset_btn.pack()
	root.mainloop()
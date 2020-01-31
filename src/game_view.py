from tkinter import *
from tkinter import ttk, font
from functools import partial
from src.game_record import Game_Record
import src.puzzle as pz

class Game_View():
    def __init__(self, root, env, dat_file):
        # 背景色宣言
        self.bg_color = [
            "light cyan",
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

        # フォント宣言
        self.tilefont  = font.Font(size=30)
        self.btnfont   = font.Font(size=15)
        self.scorefont = font.Font(size=20)

        # ラベル変更用リスト
        self.label_list = []

        #GameViewメインフレーム
        self.frame = ttk.Frame(
            root
        )

        #各種内部フレーム
        field_frame = ttk.Frame(
            self.frame,
            height=480,
            width=640,
            relief='sunken',
            borderwidth=5
        )

        record_frame = ttk.Frame(self.frame)
        score_frame = ttk.Frame(record_frame)
        play_count_frame = ttk.Frame(record_frame)
        high_score_frame = ttk.Frame(record_frame)

        footer_frame = ttk.Frame(self.frame)
        
        # フィールド用ラベル記述
        field = env.get_board_GUI().flatten()
        for i in range(field.size):
            text = str("" if field[i]==0 else field[i])
            lab = Label(field_frame, text=text, fg="black", bg=self.bg_color[field[i]%10], font=self.tilefont)
            lab.grid(row=i//env.width+1, column=i%env.width, sticky=W+E)
            self.label_list.append(lab)
        
        # ホールド用ラベル記述
        lab = Label(field_frame, text=str("" if env.have_tile == None else env.have_tile), fg="black", bg=self.bg_color[field[i]%10], font=self.tilefont)
        lab.grid(row=env.height+2, column=env.width//2, sticky=W+E)
        self.label_list.append(lab)
        
        # スコア用ラベル記述
        lab = Label(score_frame, text="SCORE", font=self.scorefont)
        lab.pack(side="top")
        lab = Label(score_frame, text="0", font=self.scorefont)
        lab.pack(side="top")
        self.label_list.append(lab)

        # GAMEOVER用ラベル記述
        gameover_lab = Label(footer_frame, text="", font=self.scorefont)
        self.label_list.append(gameover_lab)

        # プレイ回数用ラベル記述
        play_count = dat_file.get_play_count()
        lab = Label(play_count_frame, text="PLAYCOUNT", font=self.scorefont)
        lab.pack(side="top")
        lab = Label(play_count_frame, text=str(play_count), font=self.scorefont)
        lab.pack(side="top")
        self.label_list.append(lab)

        # ハイスコア用ラベル記述
        high_score, _ = dat_file.get_max_record()
        lab = Label(high_score_frame, text="HIGH SCORE", font=self.scorefont)
        lab.pack(side="top")
        lab = Label(high_score_frame, text=str(high_score), font=self.scorefont)
        lab.pack(side="top")
        self.label_list.append(lab)

        # リセットボタン記述
        cmd = partial(self.btn_reset, env, dat_file)
        reset_btn = Button(footer_frame, text="リセット", command=cmd, font=self.btnfont)

        # 移動ボタン記述
        move_btn = Button(record_frame, text="スコア表示", command=self.move_btn, font=self.btnfont)
        
        # 選択ボタン記述
        for i in range(5):
            cmd = partial(self.btn_action, env, i, dat_file)
            btn = Button(field_frame, text="選択", command=cmd, font=self.btnfont)
            btn.grid(row=env.height+3, column=i, sticky=W+E)
        
        # record_frame
        score_frame.pack(pady=5)
        play_count_frame.pack(pady=5)
        high_score_frame.pack(pady=5)
        move_btn.pack(pady=5)
        
        # footer_frame
        gameover_lab.pack(pady=5)
        reset_btn.pack(pady=5)
        
        # self.frame
        field_frame.grid(row=0, column=0, padx=5, pady=5)
        footer_frame.grid(row=1, column=0)
        record_frame.grid(row=0, column=1, sticky="n")

        # root
        self.frame.grid(row=0, column=0, sticky="nsew")

    def set_move_btn_change_frame(self, frame):
        self.move_btn_change_frame = frame
    
    def set_move_btn_event(self, move_btn_event):
        self.move_btn_event = move_btn_event
    
    def move_btn(self):
        self.move_btn_event()
        self.move_btn_change_frame.tkraise()

    def btn_action(self, env, i, dat_file):
        if not self.game_over_check(env): 
            _, _, done, _ = env.step(i)
            self.update_label(env, done, dat_file)
            if dat_file.write_check(done):
                dat_file.write_record(env)

    def btn_reset(self, env, dat_file):
        if self.game_over_check(env): 
            env.reset()
            done = False
            self.update_label(env, done, dat_file)
            dat_file.can_write_reset()
    
    def update_label(self, env, done, dat_file):
        field = env.get_board_GUI().flatten()
        max_score, _ = dat_file.get_max_record()
        for i in range(field.size):
            self.label_list[i]['text']  = str("" if field[i]==0 else field[i])
            self.label_list[i]['bg']    = self.bg_color[field[i]%10]
        have_tile = 0 if env.have_tile == None else env.have_tile
        self.label_list[field.size]['text'] = str("" if have_tile == 0 else have_tile)
        self.label_list[field.size]['bg']   = self.bg_color[have_tile%10]
        self.label_list[field.size+1]['text'] = str(env.total_score)
        self.label_list[field.size+2]['text'] = "GAME OVER" if done else ""
        self.label_list[field.size+3]['text'] = str(dat_file.get_play_count())
        self.label_list[field.size+4]['text'] = str(max_score)

    def game_over_check(self, env):
        field = env.get_board_GUI().flatten()
        return self.label_list[field.size+2]['text'] == "GAME OVER"
    

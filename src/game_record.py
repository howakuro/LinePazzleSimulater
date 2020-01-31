import pickle
import os
import numpy as np
class Game_Record():
    def __init__(self, path):
        self.path = os.path.join(path, "game_record.dat")
        self.can_write = True
        self.data = []
        if os.path.isfile(self.path): #ファイルが存在するときファイル読み込み
            with open(self.path, 'rb') as f:
                self.data = pickle.load(f)

    def get_max_record(self):
        if len(self.data) == 0:
            return 0, 0
        else:
            max_score, max_tile = np.max(self.data, axis=0)
            return max_score, max_tile

    def get_average_record(self):
        if len(self.data) == 0:
            return 0, 0
        else:
            average_score, average_tile = np.average(self.data, axis=0)
            return average_score, average_tile

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
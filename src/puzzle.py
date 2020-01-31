import numpy as np
import gym
from gym.spaces import Box, Discrete, Dict
from gym.utils import seeding
from gym.spaces import Space

class Tile(Space):
    """
    タイルを示すgymのspace記述。
    本クラスはOpenAIGymのgym.spaces.Space
    クラスの記述に従う。
    
    Attributes
    ----------
    possible_types : tupple of type
        Tile空間のデータが取りえる型を明示するリスト

    low : int
        Tile空間の数値パネルにおける最小値

    high : str
        Tile空間の数値パネルにおける最大値
    """
    def __init__(self):
        self.possible_types =  (None, int)
        self.low = 0
        self.high = "inf"
    
    
    def contains(self, x):
        if not isinstance(x, (int, None)):
            return False
        return True
    
    def sample(self):
        pass

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def __contains__(self, x):
        return self.contains(x)

    def to_jsonable(self, sample_n):
        return sample_n
    
    def __repr__(self):
        return "Tile()"

class Touhou_Line_Pazzle(gym.Env):
    """
    English : This Environment is reproduction environment of Touhou_Pazzle.
    Japanese: 東方ラインパズルの再現環境
    
    Attributes
    ----------
    board : ndarray of int
        Japanese : ゲームの盤面
        English  : This is the Board of this game.

    have_tile : int or None 
        Japanese : プレーヤーが持っているタイルの種類。
                   数字タイルならint型の数値、
                   何も持っていないならNoneが格納される。
        English  : This is the type of tile that the player has.
                   If this is type of int, Player have number tile.
                   Also, if this is type of None, Player haven't the number tile.

    now_max_num : int
        Japanese : 現在の盤面の最大の数字タイルの数字
        English  : The largest number tile on the current board have number.
    before_shoot_colomn : int
        前回所持したタイルを発射した列番号

    next_tile_colomn : int
        NEXTタイルが積まれる予定の列

    next_tile : int
        NEXTタイルの種類
    
    tiles_probability : ndarray of float
        ゲームプレイ中の数字の出現確率SSS
            tiles_probability[0] : 1の出現確率
            tiles_probability[1] : 2の出現確率
            tiles_probability[2] : 3～盤面の最大値-1の数字の出現確率

    start_tiles_probability : ndarray of float 
        ゲームの初期化時に利用する1と2出現確率 
            start_tiles_probability[0] : 1の出現確率
            start_tiles_probability[0] : 2の出現確率

    
    """
    

    def __init__(self):
        #OpenAIGym general Attribute
        self.metadata = {'render.modes': ["human","ansi"]}
        self.reward_range = (-float('inf'), float('inf')) 
        self.action_space = Discrete(5) 
        self.observation_space = Dict({ 
                                        "board":Box(0, 1000, shape=(5, 5), dtype = np.int),
                                        "have_tile":Tile(), 
                                        "next_tile_colomn": Discrete(5),
                                        "next_tile":Tile()
                                    })
        
        #一回の学習を通して使用する変数
        self.now_episode_max_tile = None

        #Environment specific attributes
        self.width = 5
        self.height = 5
        self.board = np.zeros((self.height,self.width), dtype = np.int)
        self.have_tile = None 
        self.now_max_num = None
        self.before_shoot_colomn = None
        self.next_tile_colomn = None
        self.next_tile = None
        self.tiles_probability = np.array([0.5, 0.3, 0.2], dtype = np.float)
        self.start_tiles_probability = np.array([0.7, 0.3], dtype = np.float)
        self.reset()

        #reward関数関連
        self.total_score = 0
        
    def set_board(self,board):
        self.board = np.copy(board)
    
    def get_board(self):
        return np.copy(board)
    
    def get_board_GUI(self):
        next_board = np.zeros(self.width, dtype=int)
        next_board[self.next_tile_colomn] = self.next_tile
        return np.concatenate([[next_board], self.board])

    def reset(self):
       self.board = self._init_board()
       self.now_max_num = np.max(self.board)
       self.now_episode_max_tile = np.max(self.board)
       self.total_score = 0
       self._next_tile_lottery(mode = "start")
       obs = {
                "board":np.copy(self.board), 
                "have_tile":self.have_tile, 
                "next_tile_colomn":self.next_tile_colomn, 
                "next_tile":self.next_tile
              }
       return obs


    def step(self, action):
        done = False
        score = 0
        if self.have_tile == None:
            moved = self._get_tile(action)
        else:
            moved = True
            tile_over_flow_push = self._next_tile_push() 
            tile_over_flow_shoot,score = self._shoot(action)
            done = tile_over_flow_shoot or tile_over_flow_push 
            self.before_shoot_colomn = action
            self.now_max_num = np.max(self.board)
            self.total_score += score 

            self._next_tile_lottery()
        obs = {
                "board":np.copy(self.board), 
                "have_tile":self.have_tile, 
                "next_tile_colomn":self.next_tile_colomn, 
                "next_tile":self.next_tile
              }
        info ={
                "total_score": self.total_score
              }
        
        reward = self._reward(done, moved, score)
        return obs, reward, done, info

    def render(self, mode='human'):
        if mode == "human":
            board = np.zeros((6,5),dtype = np.int)
            nexts = np.zeros(5, dtype = np.int)
            nexts[self.next_tile_colomn] = self.next_tile
            board[0] = nexts
            for i, row in enumerate(self.board):
                board[i+1] = row
            print(board)
            print(f"have:{self.have_tile}\n")

    def close(self):
        pass
    
    def _init_board(self):
        """
        盤面の初期化

        Returns
        -------
        board : ndarray dtype=int shape=(5, 5)
            ゲームの盤面
        """
        board = np.zeros((5, 5), dtype = np.int)
        for y in range(2):
            for x in range(5):
                tile_lottery = np.random.choice([1, 2], p = self.start_tiles_probability)
                board[y][x] = tile_lottery
        return board

    def _next_tile_lottery(self,mode = "playing"):
        """
        次に盤面に配置されるタイルの抽選
        """
        can_push_colomn = np.arange(5)
        if mode == "playing":
            can_push_colomn = np.any(self.board == 0, axis=0)
            can_push_colomn[self.before_shoot_colomn] = False
            can_push_colomn = np.where(can_push_colomn==True)[0]
            if np.all(can_push_colomn==False):
                can_push_colomn =[self.before_shoot_colomn] 
    
        self.next_tile_colomn = np.random.choice(can_push_colomn)
        if self.now_max_num > 2:
            next_tile = np.random.choice([1, 2, 3], p = self.tiles_probability)
            if next_tile != 3:
                self.next_tile = next_tile
            else:
                self.next_tile = 3 if self.now_max_num == 3 else np.random.randint(3, self.now_max_num + 1) 
        else:
            self.next_tile = np.random.choice([1, 2], p = self.start_tiles_probability)
    
    def _get_tile(self, get_colomn):
        """
        指定した列の先頭のタイルを取り出す
        """
        for y in range(5)[::-1]:
            if self.board[y][get_colomn] == 0:
                continue
            self.have_tile = self.board[y][get_colomn]
            self.board[y][get_colomn] = 0
            break
        if self.have_tile == None:
            return False
        else:
            return True
        
    def _score(self, input, last):
      """
      発射したときの獲得スコアの計算
      """
      return np.sum(2**np.arange(last-input) * np.arange(input,last)**3)

    def _shoot(self, shoot_colomn):
        """
        指定した列にタイルを発射して統合する

        Returns
        -------
        tile_over_flow : bool
            タイルが列から溢れているか否か
        """
        shoot_tile = self.have_tile
        start_shoot_tile = shoot_tile
        tile_over_flow = False
        self.have_tile = None
        for y in range(5)[::-1]:
            if self.board[y][shoot_colomn] == 0:#空白マス
                if y == 0:#一番上の行までタイルがなかった場合
                    self.board[y][shoot_colomn] =  shoot_tile
                continue
            if self.board[y][shoot_colomn] != shoot_tile:#隣接するタイルが違う数字を持つ場合
                if y + 1 < 5:#タイルが溢れていない場合
                    self.board[y + 1][shoot_colomn] = shoot_tile
                else:#タイルが溢れている場合
                    tile_over_flow = True
                return tile_over_flow, self._score(start_shoot_tile, shoot_tile)
            elif self.board[y][shoot_colomn] == shoot_tile:#隣接するタイルが同じ数字を持つ場合
                self.board[y][shoot_colomn] += 1
                shoot_tile = self.board[y][shoot_colomn]
                if y + 1 < 5:#下から２番目の列までの処理
                    self.board[y + 1][shoot_colomn] =  0
        return tile_over_flow, self._score(start_shoot_tile, shoot_tile)


    
    def _next_tile_push(self):
        """
        NEXTのタイルを盤面に押し出す

        Returns
        -------
        tile_over_flow : bool
            タイルが列から溢れているか否か
        """
        tmp = None
        tile_over_flow = False
        for y in range(6):
            if tmp == 0:
               return tile_over_flow
            if y == 0:
                tmp = self.board[y][self.next_tile_colomn]
                self.board[y][self.next_tile_colomn] = self.next_tile
            else:
              try:
                tmp, self.board[y][self.next_tile_colomn] = self.board[y][self.next_tile_colomn], tmp
              except:
                tile_over_flow = True
                return tile_over_flow
    
    def _reward(self, done, moved, score):
        """
        報酬関数
        """
        if (not moved):
          return -1
        return score 
        
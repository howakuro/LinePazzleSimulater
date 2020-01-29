import pickle
import os
import numpy as np
import sys

args = sys.argv
path = None
if len(args) == 1:#
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	path = os.path.join(os.getcwd(), "game_record.dat")
elif len(args) == 2:
	path = args[1]
else: 
	print("Error:Invalid command line argument.")
	sys.exit(1)

if os.path.isfile(path): #ファイルが存在するときファイル読み込み
	with open(path, 'rb') as f:
		data = pickle.load(f)
	data = np.array(data)
	m_score, m_tile = np.max(data, axis=0)
	a_score, a_tile = np.average(data, axis=0)
	print("Max Score     :", m_score)
	print("Max Tile      :", m_tile)
	print("Average Score :", a_score)
	print("Average Tile  :", a_tile)
	print("Play num      :", data.size//2)
	for i in data:
		print(i)
else:
	print("Error:" + path + " is not found.")

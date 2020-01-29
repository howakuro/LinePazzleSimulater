# 実験関連の説明
配布されたゲーム環境で最低5回プレイしてください。<br>
5回以上プレイして頂いても構いません。<br>
プレイ結果は全てgame_record.datというファイルに記録されています。<br>
プレイ終了後にgame_record.datというファイルが存在しているかを確認してください。<br>
game_record.datの存在が確認できたらSlackで自分のアカウントにgame_record.datを送ってください。

# 必要パッケージ
必要パッケージです。
- numpy 
- gym  

# 使い方
1. 必要パッケージをインストールする
2. main.pyを実行する
```
python main.py
```

# 各種ファイル説明
- main.py<br>
    ゲームを遊ぶ際はこのファイルをPythonで実行してください。
- puzzle.py<br>
    ゲーム本体です。
- game_record.dat<br>
    ゲームのプレイ結果などが記録されているファイルです。初回のGAMEOVER時に生成されます。
- dat_preview.py<br>
   ゲームのプレイ結果を参照できます。参照するファイルは同じディレクトリの中にあるgame_record.datです。

## 注意事項
環境設定が変わってしまう恐れがあるので、各種プログラムには変更を加えないでください。

# 動作確認済み環境
このversion以外でも動作すると思われますが動作確認済みのバージョンを記載します。
- Python 
    - 3.7 
        - version 3.7.4.final.0
    - 3.6 
        - version 3.6.5.final.0
- numpy 
    - version 1.17.4
    - version 1.18.1
- gym
    - version 0.15.4

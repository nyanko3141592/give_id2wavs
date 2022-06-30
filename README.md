# wav_id_rename
 wavファイルを音声認識でその文章が該当するラベルをつける


## 利用にあたって
### env.pyの作成
このリポジトリの直下にenv.pyを以下を参考に作成
```
import os

# master dir　この中にすべて入る
master_name = 'test'
# master dir os.dir
master_dir = os.path.join('master', master_name)

# 入力path
input_dir_name = 'input'
# 出力path
out_dir_name = 'output'
# 文章json : absolute path
sentence_json_path = 'absolute path'

# rename failed file
rename_failed_file = 'failed.txt'

# 基準値 0~1.0
threshold = 0.5
```

## master/template_masterを複製し設定
複製したtemplate_masterのdirの名前を変更．
ラベルつけしたい音声ファイルをinput dirに配置．

## sentence_jsonの指定
env.pyで指定するsenetence_jsonは以下の形式のものとする
key(e.g id-1)をラベルづけする名称(id-1.wav)とし、textの内容に合う音声を自動でその名称に変更される
```
{
    "id-1": {
        "text": "ももくり１億年かき2000年",
    },
    "id-2": {
        "text": "石の上にもn年"
    }
}
```

## main.pyを実行
```
python main.py
```

# wav文字起こしで対応するIDに名前を変更する
import csv
import difflib
import json
import pprint
from typing import List, Dict
import re

import env

# wavのラベルのために読み込み
sentence_json : Dict[str, Dict[str, str]]
sentence_dict: Dict[str, str] = {}

# read json as dict
with open(env.sentence_json_path, 'r') as f:
    sentence_json = json.load(f)
for k, v in sentence_json.items():
    sentence_dict[k] = v['text']

def rm_txts(text: str, rm_list=None) -> str:
    if rm_list is None:
        rm_list = ["。", "、", " ", "　"]
    for rm in rm_list:
        text = text.replace(rm, "")
    return text


def search_id(gen_text, start: int = 1, end: int = -1, hurigana_re="（.*?）"):
    # start 行番号
    # end 行番号
    match_id = ''
    ratio = 0.0
    # 検索範囲を正規化
    if start <= 0:
        start = 1
    if end > len(sentence_dict):
        end = -1
    l = sorted(list(sentence_dict.keys())[start - 1:end])[::-1]
    for id in l:
        current_text = re.sub(hurigana_re, "", sentence_dict[id])
        r = difflib.SequenceMatcher(None, rm_txts(gen_text), rm_txts(current_text)).ratio()
        if ratio < r:
            ratio = r
            match_id = id
    if match_id == '':
        return match_id, '', '', ''
    index = list(sentence_dict.keys()).index(match_id) + 1
    return match_id, re.sub(hurigana_re, "", sentence_dict[match_id]), index, ratio


# 文章の一致率
def match_percent(a: str, b: str):
    return difflib.SequenceMatcher(None, a, b).ratio()


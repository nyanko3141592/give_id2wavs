"""This is the main file for the project."""
import glob
import os
import json
from typing import List, Dict

import env
import utils.check_sentence
from utils.check_files import check_lacked_files
from utils.voice2text import v2t

wav_sentence_json: str = "wav_sentence.json"

# get files in input dir
wav_files = glob.glob(os.path.join(env.master_dir, env.input_dir_name, '*.wav'))
print(f"wav_files: {len(wav_files)}")
# text file 作成
text_file = open(os.path.join(env.master_dir, env.rename_failed_file), 'w', encoding='utf-8')

# wav to speech recognition text
wav_sentence_dict: Dict[str, str] = {}
# read already exist wav_sentence_json
if os.path.exists(os.path.join(env.master_dir, wav_sentence_json)):
    with open(os.path.join(env.master_dir, wav_sentence_json), 'r', encoding='utf-8') as f:
        wav_sentence_dict = json.load(f)
l: List[str] =  sorted(list(set(wav_files) -  set(wav_sentence_dict.keys())))
for wav_file in l:
    wav_sentence_dict[wav_file] = v2t(wav_file)
    print(f"{wav_file}: {wav_sentence_dict[wav_file]}")
    # save dict as json
    with open(os.path.join(env.master_dir, wav_sentence_json), 'w', encoding='utf-8') as f:
        json.dump(wav_sentence_dict, f, ensure_ascii=False, indent=4)


# 音声ファイルのrename
l = sorted(wav_sentence_dict.keys())
for wav_file in l:
    voice_text = wav_sentence_dict[wav_file]
    sentence_id, text, index, ratio = utils.check_sentence.search_id(voice_text)
    print(f"id: {sentence_id}, voice: {voice_text}\n{' ' * (len(sentence_id) + 4)}current: {text}")
    # 閾値を超えた一致率のファイルをrename
    # ファイルが既にある場合
    if os.path.exists(os.path.join(env.master_dir, env.out_dir_name, sentence_id + '.wav')):
        # text 書き込み
        text_file.write(f"EXISTS {sentence_id} {wav_file} {text}\n")
        continue
    if ratio > env.threshold:
        # inputの音声ファイルをoutputにコピー・ファイル名を変更
        os.system(f"cp {wav_file} {os.path.join(env.master_dir, env.out_dir_name, sentence_id + '.wav')}")
    else:
        # text 書き込み
        text_file.write(f"NONE {sentence_id} {wav_file} {text}\n")
text_file.close()

# 抜けの確認
lacked_files: set[str] = check_lacked_files(env.sentence_json_path,
    os.path.join(env.master_dir,
    env.out_dir_name))
with open(os.path.join(env.master_dir, "lacked_sentence.txt"), 'w', encoding='utf-8') as f:
    lacked_files_sorted = sorted(list(lacked_files))
    for file in lacked_files_sorted:
        f.write(file + '\n')
print(f"lacked_files: {len(lacked_files)}")

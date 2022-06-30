import env
import glob
import os

import utils.check_sentence
from utils.check_files import check_lacked_files
from utils.voice2text import v2t

# get files in input dir
wav_files = glob.glob(os.path.join(env.master_dir, env.input_dir_name, '*.wav'))
print(f"wav_files: {len(wav_files)}")
# text file 作成
text_file = open(os.path.join(env.master_dir, env.rename_failed_file), 'w')

# 音声ファイルのrename
for wav_file in wav_files:
    voice_text = v2t(wav_file)
    id, text, index, ratio = utils.check_sentence.search_id(voice_text)
    print(f"id: {id}, voice: {voice_text}\n{' ' * (len(id) + 4)}current: {text}")
    # 閾値を超えた一致率のファイルをrename
    # ファイルが既にある場合
    if os.path.exists(os.path.join(env.master_dir, env.out_dir_name, id + '.wav')):
        # text 書き込み
        text_file.write(f"EXISTS {id} {wav_file} {text}\n")
        continue
    if ratio > env.threshold:
        # inputの音声ファイルをoutputにコピー・ファイル名を変更
        os.system(f"cp {wav_file} {os.path.join(env.master_dir, env.out_dir_name, id + '.wav')}")
    else:
        # text 書き込み
        text_file.write(f"NONE {id} {wav_file} {text}\n")
text_file.close()

# 抜けの確認
lacked_files: set[str] = check_lacked_files(env.sentence_json_path, os.path.join(env.master_dir, env.out_dir_name))
with open(os.path.join(env.master_dir, "lacked_sentence.txt"), 'w') as f:
    lacked_files_sorted = sorted(list(lacked_files))
    for file in lacked_files_sorted:
        f.write(file + '\n')
print(f"lacked_files: {len(lacked_files)}")
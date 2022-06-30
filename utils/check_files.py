from operator import le
import os
import json

from pip import main

def get_file_names(path):
    """
    Get all file names in a directory.
    """
    file_names = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_names.append(os.path.join(root, file))
    return file_names


# get file name from path
def get_file_name(path):
    """
    Get file name from path.
    """
    return os.path.basename(path)

def check_lacked_files(sentence_json_path: os.path, check_dir_path: os.path) -> set:
    file_names = get_file_names(check_dir_path)
    file_names = set(map(get_file_name, file_names))
    # read json as dict
    with open(sentence_json_path, 'r') as f:
        sentence_json = json.load(f)
    # get file name from sentence json
    sentence_file_names = set(map(lambda x: x + '.wav', sentence_json))
    # get lacking file names
    lacked_file_names = sentence_file_names - file_names
    return lacked_file_names

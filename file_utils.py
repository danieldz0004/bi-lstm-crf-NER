# encoding=utf8

import os


def load_text(path, filter_space=True):
    with open(path, "r", encoding="utf-8", errors='replace') as f:
        lines = f.read().splitlines()
    if not filter_space:
        return lines
    result = []
    for element in lines:
        str = element.replace(' ', '').replace('\u3000', '')
        result.append(str)
    return result


def save_list(list, path):
    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(path, "w", encoding="utf-8", errors='replace') as f:
       for line in list:
           if "\n" != line:
               f.write(line + "\n")
           else:
               f.write(line)
#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import sys
sys.path.append("../")
from file_utils import load_text, save_list

root_dir = '/data/nlu-dl-train/data/train/'
init_dir = root_dir + 'init/'
iob_dir = root_dir + 'iob/'
source_dir = root_dir + 'source/'
similar_path = init_dir + "similar/"
# known_path = os.path.join(init_dir, "known_result.txt")
unknown_path = os.path.join(init_dir, "unknown_result.txt")
dic_dir = os.path.join(init_dir, "dic")
known_success_path = os.path.join(init_dir, "out/success.txt")
known_fail_path = os.path.join(init_dir, "out/fail.txt")
known_out_path = os.path.join(init_dir, "out/out.txt")
known_train_path = os.path.join(iob_dir, "known.txt")
unknown_train_path = os.path.join(iob_dir, "unknown.txt")
dic_train_path = os.path.join(iob_dir, "dic.txt")


# 替换不符合规范的字符串
def pre_test():
    print('')
    # testPath = "/data/nlu-dl-train/true.txt"
    # initPath = "/data/nlu-dl-train/right_result.txt"
    # outPath = "/data/nlu-dl-train/out.txt"
    # lists = load_text(testPath)
    # initLists = load_text(initPath)
    # wordsLists = []
    # for e in initLists:
    #     wordsLists.append(e.split("\t")[0])
    # result = []
    # for e in lists:
    #     element = e.replace('""', '"').replace('"{', '{').replace('"}', '}')
    #     words = element.split("\t")[0]
    #     print(words)
    #     if words not in wordsLists:
    #         result.append(element)
    # save_list(result, outPath)


def load_similar_dict():
    names = ['app_name.json', 'app_operate.json', 'control_tv.json', 'live_name.json',
             'music_name.json', 'video_name.json', 'public_area.json', 'public_year.json',
             'video_category.json', 'video_type.json', 'music_tag.json',
             'user_defined.json']
    dic = {}
    for name in names:
        lines = load_text(similar_path + name)
        for element in lines:
            if '' == element.strip():
                continue
            json_str = json.loads(element)
            dic[json_str['original']] = json_str['similar']
    return dic


def trans(text, nlu_dict, similar_dict):
    label = ["O"]*len(text)
    ignore_keys = ["cl", "cl_words", "app_package", "control_extra", "video_part", "video_episode",
                   "domain"]
    words_keys = ["public_hot", "public_new", "public_hscore", "public_free"]
    for key in ignore_keys:
        del_dict(nlu_dict, key)
    if nlu_dict is None or 0 == len(nlu_dict):
        return label
    # if text == '请打开腾讯视频':
    #     print(text)
    for k in nlu_dict.keys():
        key = "operate" if ("operate" in k) else k
        words = nlu_dict.get(k)
        if key in words_keys:
            words = key
        index = text.find(words)
        if -1 == index:
            if key == "operate":
                continue
            else:
                # 查找相似词是否存在
                similar = similar_dict.get(words)
                if similar is None:
                    return None
                for s in similar:
                    index = text.find(s)
                    if -1 != index:
                        words = s
                        break
                if -1 == index:
                    return None
        for i in range(index, index+len(words)):
            if "O" != label[i]:
                return None
            sign = "I-" + key
            if i == index:
                sign = "B-" + key
            label[i] = sign
    return label


def del_dict(dict,key):
    if dict is None:
        return
    value = dict.get(key)
    if value is not None:
        dict.pop(key)


def trans_unknown_file():
    lines = load_text(unknown_path)
    success_list = []
    for one in lines:
        arr = one.split("\t")
        text = arr[0].upper()
        label = ["O"] * len(text)
        dic = {"text": text, "label": label}
        success_list.append(json.dumps(dic, ensure_ascii=False))
    save_list(success_list, unknown_train_path)
    print("unknown lines = ", len(success_list))

# def trans_known_file():
#     lines = load_text(known_path)
#     similar_dict = load_similar_dict()
#     success_list = []
#     out_list = []
#     fail_list = []
#     for one in lines:
#         arr = one.split("\t")
#         text = arr[0].upper()
#         nlu = json.loads(arr[1])
#         label = trans(text, nlu, similar_dict)
#         if label is None:
#             fail = arr[0] + "\t" + (arr[1])
#             fail_list.append(fail)
#         elif len(text) == len(label):
#             dic = {"text": text, "label": label}
#             success_list.append(json.dumps(dic, ensure_ascii=False))
#             for i in range(0, len(text)):
#                 line = text[i:i+1] + "\t" + label[i]
#                 out_list.append(line)
#             out_list.append("\n")
#     save_list(out_list, known_out_path)
#     save_list(fail_list, known_fail_path)
#     save_list(success_list, known_success_path)
#     save_list(success_list, known_train_path)
#     print("known:  all lines = ", len(lines),  " ; success lines = ", len(success_list),
#           " ; fail lines = ", len(fail_list))


def trans_dic_file():
    json_files = []
    iob_result = []
    for fpath, dirs, fs in os.walk(dic_dir):
        for f in fs:
            if f.endswith("json") and "cl.json" not in f and not f.startswith("."):
                json_path = os.path.join(fpath, f)
                json_files.append(json_path)
    for file in json_files:
        iob = dic_to_iob(file)
        iob_result = iob_result + iob
    print("dic iob = ", len(iob_result))
    save_list(iob_result, dic_train_path)


def dic_to_iob(path):
    iob = os.path.basename(path).replace(".json", "")
    if 'operate' in iob:
        iob = 'operate'
    lines = load_text(path)
    iob_list = []
    similar_list = []
    for element in lines:
        if '' == element.strip():
            continue
        json_str = json.loads(element)
        for s in json_str['similar']:
            similar_list.append(s)

    add_pre_list = []
    add_suffix_list = []
    if 'video_actor' in iob or 'video_director' in iob:
        add_suffix_list = ['的电影', '的电视剧']
    if 'music_singer' in iob:
        add_suffix_list = ['的歌', '的歌曲']
    if 'video_name' in iob:
        add_pre_list = ['我要看', '看', '播放', '搜索', '打开']
    elif 'music_name' in iob:
        add_pre_list = ['我要听', '播放', '听']
    elif 'live_name' in iob:
        add_pre_list = ['我要看', '看', '播放', '打开']
    elif 'app_name' in iob:
        add_pre_list = ['打开', '卸载', '关闭', '退出']
    for text in similar_list:
        label = ["I-"+iob] * len(text)
        label[0] = "B-" + iob
        dic = {"text": text, "label": label}
        iob_list.append(json.dumps(dic, ensure_ascii=False))

        for suffix in add_suffix_list:
            new_text = text + suffix
            suffix_label = ["O"] * len(suffix)
            new_label = label + suffix_label
            dic = {"text": new_text, "label": new_label}
            iob_list.append(json.dumps(dic, ensure_ascii=False))

        for pre in add_pre_list:
            new_text = pre + text
            pre_label = ["O"] * len(pre)
            new_label = pre_label + label
            dic = {"text": new_text, "label": new_label}
            iob_list.append(json.dumps(dic, ensure_ascii=False))
    #print('dic: ', iob, len(similar_list))
    return iob_list


def trans_file():
    trans_dic_file()
    trans_unknown_file()
    # trans_known_file()


def main():
     trans_file()


if __name__ == '__main__':
    main()

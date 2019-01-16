import json
import os
import random
import sys
sys.path.append("../")
from file_utils import load_text, save_list

root_dir = '/data/nlu-dl-train/data/train/'
init_dir = root_dir + 'init/'
iob_dir = root_dir + 'iob/'
source_dir = root_dir + 'source/'
train_dir = os.path.join(source_dir, "train.txt")
dev_dir = os.path.join(source_dir, "dev.txt")
test_dir = os.path.join(source_dir, "test.txt")
dic_only_train = True


def iob_to_train_data(iob_list):
    result = []
    for element in iob_list:
        if '' == element.strip():
            continue
        dic = json.loads(element)
        text = dic["text"]
        label = dic["label"]
        for i in range(0, len(text)):
            line = text[i:i + 1] + "\t" + label[i]
            result.append(line)
        result.append("\n")
    return result


def pre_deal_data():
    all_data_list = []
    dic_data_list = []
    for name in os.listdir(iob_dir):
        path = os.path.join(iob_dir, name)
        if os.path.isfile(path):
            lines = load_text(path)
            print(name, len(lines))
            if 'dic.txt' == name:
                dic_data_list = lines
            else:
                all_data_list = all_data_list + lines
    print("all data sum = ", len(all_data_list))
    if not dic_only_train:
        all_data_list = all_data_list + dic_data_list
        dic_data_list.clear()
    random.shuffle(all_data_list)
    train_len = int(len(all_data_list) * 0.7)
    test_len = int(len(all_data_list) * 0.2)
    dev_len = int(len(all_data_list) * 0.1)
    train_list = all_data_list[0: train_len]
    test_list = all_data_list[train_len: train_len + test_len]
    dev_list = all_data_list[train_len + test_len: train_len + test_len + dev_len]
    print('before train;test;dev:',len(train_list), len(test_list), len(dev_list))
    train_list = train_list + dic_data_list
    print('after train;test;dev:', len(train_list), len(test_list), len(dev_list))
    save_list(iob_to_train_data(train_list), train_dir)
    save_list(iob_to_train_data(test_list), test_dir)
    save_list(iob_to_train_data(dev_list), dev_dir)
    print("end pre deal data")

def main():
   pre_deal_data()

if __name__ == '__main__':
    main()

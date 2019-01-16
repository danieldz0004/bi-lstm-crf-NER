# -*- coding:utf-8 -*-
import pprint, pickle

def test():
    """
    Replace every digit in a string by a zero.
    """
    # text = '{"label": ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O"], "text": "རྙང་མ་འདོག"}'
    # output_file = '/data/tmp/ner_predict.utf8'
    # with open(output_file, "w", encoding='utf-8') as f:
    #     to_write = [text, '我要看电影']
    #     print(to_write)
    #     f.writelines(to_write)


    path = '/data/tmp/train/source/test.txt'
    # for line in lines:
    #     if '\u0a62' in line:
    #         print(line)

    results = ['我', 'ར', '1']
    output_file = '/data/tmp/train/source/123.txt'
    with open(output_file, "w", errors='replace') as f:
        to_write = []

        for line in results:
            to_write.append(line + "\n")
         #   f.writelines(line + "\n")
        f.writelines(to_write)


    #
    # with open(path, "r") as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         print(line)





def load_text(path, filter_space=True):
    with open(path, "r", encoding="utf-8", errors='ignore') as f:
        lines = f.read().splitlines()
    if not filter_space:
        return lines
    result = []
    for element in lines:
        str = element.replace(' ', '')
        result.append(str)
    return result


def main():
    test()


if __name__ == '__main__':
    main()
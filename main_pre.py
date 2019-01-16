#!/usr/bin/python
# -*- coding: utf-8 -*-

from pre_edit.trans_iob import trans_file
from pre_edit.train_data import pre_deal_data


def main():
    trans_file()
    pre_deal_data()


if __name__ == '__main__':
    main()

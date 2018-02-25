# -*- coding=utf-8 -*-


def selection_sort(lists):
    '''选择排序'''
    # count = lists.__len__()
    for i in range(0, lists.__len__()):
        _min = i
        for j in range(i+1, lists.__len__()):
            if lists[j] < lists[_min]:
                _min = j
        lists[i], lists[_min] = lists[_min], lists[i]
    return lists

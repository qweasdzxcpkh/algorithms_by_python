# -*- coding=utf-8 -*-


def shell_sort(lists):
    '''希尔排序'''
    increment = lists.__len__() / 2
    while increment > 0:
        for i in range(0, increment):
            j = i + increment
            while j < lists.__len__():
                tem = lists[j]
                k = j - increment
                while k >= 0:
                    if lists[k] > lists[k+increment]:
                        lists[k+increment] = lists[k]
                        lists[k] = tem
                    k -= increment
                j += increment
        increment /= 2
        print lists
    return lists

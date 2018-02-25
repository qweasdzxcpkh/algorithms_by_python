# -*- coding=utf-8 -*-


def bubble_sort(lists):
    '''冒泡排序'''
    for i in range(0, lists.__len__()):
        for j in range(0, lists.__len__()-i-1):
            if lists[j] > lists[j+1]:
                lists[j], lists[j+1] = lists[j+1], lists[j]
    return lists

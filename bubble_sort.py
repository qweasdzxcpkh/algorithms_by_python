# -*- coding=utf-8 -*-


def bubble_sort(lists):
    '''冒泡排序'''
    for i in range(0, lists.__len__()):
        for j in range(0, lists.__len__()-i-1):
            if lists[j] > lists[j+1]:
                lists[j], lists[j+1] = lists[j+1], lists[j]
    return lists


def bubble_sort_recursive(lists, left, right):
    '''冒泡排序递归实现'''
    if left == right:  # Base Case
        return lists

    for i in range(left, right):
        if lists[i] > lists[i+1]:
            lists[i], lists[i+1] = lists[i+1], lists[i]

    return bubble_sort_recursive(lists, left, right-1)

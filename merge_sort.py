# -*- coding=utf-8 -*-


def merge_sort(lists):
    '''归并排序'''
    size = lists.__len__()
    if size <= 1:
        return lists

    lists_left = merge_sort(lists[:size/2])
    lists_right = merge_sort(lists[size/2:])

    merge_lists = []
    i = j = 0
    while i < lists_left.__len__() and j < lists_right.__len__():
        if lists_left[i] < lists_right[j]:
            merge_lists.append(lists_left[i])
            i += 1
        else:
            merge_lists.append(lists_right[j])
            j += 1
    merge_lists += lists_left[i:]
    merge_lists += lists_right[j:]
    return merge_lists

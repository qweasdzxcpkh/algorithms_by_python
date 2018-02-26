# -*- coding=utf-8 -*-


def insert_sort_0(lists):
    '''插入排序'''
    for i in range(1, lists.__len__()):
        tem = lists[i]
        j = i - 1
        while True:
            if j >= 0 and lists[j] > tem:
                lists[j+1] = lists[j]
                j -= 1
            else:
                lists[j+1] = tem
                break
    return lists


def insert_sort_1(lists):
    '''插入排序(频繁对数组赋值)'''
    for i in range(1, lists.__len__()):
        tem = lists[i]
        j = i - 1
        while j >= 0:
            if lists[j] > tem:
                lists[j + 1] = lists[j]
                lists[j] = tem
            j -= 1
    return lists

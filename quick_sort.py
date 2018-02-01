# -*- coding=utf-8 -*-

'''细节实现可能略有不同'''


def quick_sort1(lists, left, right):
    '''快速排序'''
    if left >= right:
        return
    pivot = lists[left]
    low = left
    high = right
    while left < right:
        while left < right and lists[right] >= pivot:
            right -= 1
        lists[left] = lists[right]
        while left < right and lists[left] <= pivot:
            left += 1
        lists[right] = lists[left]
    lists[right] = pivot
    print lists  # 看排序过程
    quick_sort1(lists, low, left - 1)
    quick_sort1(lists, left + 1, high)
    return lists


def quick_sort2(lists, left, right):
    '''快速排序2'''
    if left >= right:
        return
    pivot = lists[right]
    storeIndex = left
    for i in range(left, right):
        if lists[i] <= pivot:
            lists[storeIndex], lists[i] = lists[i], lists[storeIndex]
            storeIndex += 1
    lists[storeIndex], lists[right] = lists[right], lists[storeIndex]
    print lists  # 看排序过程
    quick_sort2(lists, left, storeIndex-1)
    quick_sort2(lists, storeIndex+1, right)
    return lists

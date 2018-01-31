# -*- coding=utf-8 -*-

'''细节实现可能略有不同'''


def quick_sort1(lists, left, right):
    '''快速排序'''
    if left >= right:
        return lists
    key = lists[left]
    low = left
    high = right
    while left < right:
        while left < right and lists[right] >= key:
            right -= 1
        lists[left] = lists[right]
        while left < right and lists[left] <= key:
            left += 1
        lists[right] = lists[left]
    lists[right] = key
    quick_sort1(lists, low, left - 1)
    quick_sort1(lists, left + 1, high)
    return lists


def quick_sort2(lists, left, right):
    pass
'''function partition(a, left, right, pivotIndex)
     pivotValue := a[pivotIndex]
     swap(a[pivotIndex], a[right]) // 把 pivot 移到結尾
     storeIndex := left
     for i from left to right-1
         if a[i] < pivotValue
             swap(a[storeIndex], a[i])
             storeIndex := storeIndex + 1
     swap(a[right], a[storeIndex]) // 把 pivot 移到它最後的地方
     return storeIndex // 返回 pivot 的最终位置'''

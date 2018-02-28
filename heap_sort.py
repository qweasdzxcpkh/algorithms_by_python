# -*- coding=utf-8 -*-


def adjust_max_heap(lists, i, size):
    '''调整lists[0]到正确位置，需要lists本来就符合大顶堆结构'''
    lchild = 2 * i + 1
    rchild = 2 * i + 2

    _max = i

    # 找出i, lchild rchild下标中最大值的一个，与i交换
    if lchild < size and lists[lchild] > lists[_max]:
        _max = lchild
    if rchild < size and lists[rchild] > lists[_max]:
        _max = rchild
    if _max != i:
        lists[i], lists[_max] = lists[_max], lists[i]
        adjust_max_heap(lists, _max, size)


def adjust_min_heap(lists, i, size):
    '''调整lists[0]到正确位置，需要lists本来就符合小顶堆结构'''
    lchild = 2 * i + 1
    rchild = 2 * i + 2

    _min = i

    if lchild < size and lists[lchild] < lists[_min]:
        _min = lchild
    if rchild < size and lists[rchild] < lists[_min]:
        _min = rchild
    if _min != i:
        lists[i], lists[_min] = lists[_min], lists[i]
        adjust_min_heap(lists, _min, size)


def heap_sort(lists, is_asc=True):
    '''堆排序(升序)'''
    size = lists.__len__()
    if is_asc:
        func = adjust_max_heap
    else:
        func = adjust_min_heap

    # 倒序循环遍历第一个非叶子结点，构建堆结构
    for i in range(0, size/2)[::-1]:
        func(lists, i, size)
    # 排序
    for i in range(0, size)[::-1]:
        lists[0], lists[i] = lists[i], lists[0]
        func(lists, 0, i)
    return lists

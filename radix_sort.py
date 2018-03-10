# -*- coding=utf-8 -*-

import math


def radix_sort(lists, radix=10):
    '''基数排序'''
    # lists中最大值不能是0，不然math.log(0,10)报错
    loop = int(math.ceil(math.log(max(lists), radix)))
    for i in range(1, loop+1):
        bucket = [[] for _ in range(radix)]
        for val in lists:
            bucket[(val % radix**i)//(radix**(i-1))].append(val)
        del lists[:]
        for each in bucket:
            lists.extend(each)

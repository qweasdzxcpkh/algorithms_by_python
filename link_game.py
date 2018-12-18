# -*- coding=utf-8 -*-
'''
连连看的找可相连元素算法
demo使用A-Z表示图像, 如果游戏边缘无限制则需要增加一圈None表示空位
[x\y   y1   y2    y3    y4   y5
 x1  ['S', 'A',  None, 'C', None],
 x2  ['A', None, 'S',  'C', 'B'],
 x3  ['B', 'Q',  'Q',  'W', 'W'],
 x4  ...
 ..  ...
]

test case:
test = [
    ['S', 'A', None, 'C', None],
    ['A', None, 'A', 'B', 'Q'],
    ['Q', 'C', 'S', 'A', 'W'],
    ['E', 'W', 'B', None, 'Z'],
    ['E', 'Z', 'S', None, 'S']
]
LG = LinkGraph(test)
LG.find()
LG.clear(*LG.find())
'''

from itertools import combinations


class LinkGraph(object):

    def __init__(self, graph):
        self.origin_graph = self.work_graph = graph
        self.len = 0
        self.max_x, self.max_y = len(graph), len(graph[0])
        # 散列，记录每个点的坐标
        self.dict = dict()
        for i, row in enumerate(graph):
            for j, item in enumerate(row):
                if item is not None:
                    self.dict.setdefault(item, set())
                    self.dict[item].add((i, j))
                    self.len += 1

    def __len__(self):
        # reduce(lambda x: reduce(lambda y: 1 if y is not None else 0, x), (self.work_graph))
        return self.len

    # 判断一个点是否block
    def is_not_None(self, item):
        (x, y) = item
        return True if self.work_graph[x][y] is not None else False

    # 水平判断
    def horizon(self, item1, item2):
        (x1, y1), (x2, y2) = item1, item2
        if x1 != x2:
            return False
        for y in range(min(y1, y2)+1, max(y1, y2)):
            if self.is_not_None((x1, y)):
                return False
        return True

    # 垂直判断
    def vertical(self, item1, item2):
        (x1, y1), (x2, y2) = item1, item2
        if y1 != y2:
            return False
        for x in range(min(x1, x2)+1, max(x1, x2)):
            if self.is_not_None((x, y1)):
                return False
        return True

    # 单拐点判断
    def turn_once(self, item1, item2):
        (x1, y1), (x2, y2) = item1, item2
        t_point1, t_point2 = (x1, y2), (x2, y1)
        if (not self.is_not_None(t_point1)) and self.vertical(t_point1, item2) and self.horizon(t_point1, item1):
            return True
        if (not self.is_not_None(t_point2)) and self.vertical(t_point2, item1) and self.horizon(t_point2, item2):
            return True
        return False

    # 双拐点判断（兼容self. vertical/horizon/turn_once）
    def turn_twice(self, item1, item2):
        i1_left, i1_right, i1_up, i1_down = self.__get_block_from_point(item1)
        i2_left, i2_right, i2_up, i2_down = self.__get_block_from_point(item2)
        its_y = set(range(i1_left, i1_right+1)) & set(range(i2_left, i2_right+1))
        its_x = set(range(i1_up, i1_down+1)) & set(range(i2_up, i2_down+1))

        (x1, y1), (x2, y2) = item1, item2
        for y in its_y:
            if self.vertical((x1, y), (x2, y)):
                return True
        for x in its_x:
            if self.horizon((x, y1), (x, y2)):
                return True
        return False

    # 获取item的上下左右4个方向的最近block下标
    def __get_block_from_point(self, item):
        x, y = item
        left_y = right_y = y
        up_x = down_x = x
        for i in reversed(self.work_graph[x][0:y]):
            if i is not None:
                break
            left_y -= 1
        for i in self.work_graph[x][y+1:]:
            if i is not None:
                break
            right_y += 1
        while up_x-1 >= 0 and not self.is_not_None((up_x-1, y)):
            up_x -= 1
        while down_x+1 < len(self.work_graph) and not self.is_not_None((down_x, y)):
            down_x += 1
        return left_y, right_y, up_x, down_x

    # 执行判断item1、item2能否相连
    def judge(self, item1, item2):
        if item1 == item2:
            return False

        if self.horizon(item1, item2):
            return True
        if self.vertical(item1, item2):
            return True
        if self.turn_once(item1, item2):
            return True
        if self.turn_twice(item1, item2):
            return True
        return False

    def find(self):
        for k, v in self.dict.items():
            for item1, item2 in combinations(v, 2):
                if self.judge(item1, item2):
                    return k, item1, item2
        return None

    def clear(self, k, item1, item2):
        assert item1 in self.dict[k]
        assert item1 in self.dict[k]
        assert self.judge(item1, item2)
        (x1, y1), (x2, y2) = item1, item2
        self.work_graph[x1][y1] = None
        self.work_graph[x2][y2] = None
        self.dict[k].remove(item1)
        self.dict[k].remove(item2)

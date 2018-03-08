# -*- coding=utf-8 -*-


class Node(object):
    def __init__(self):
        self.Element = None
        self.Next = int()


class Memory(object):
    def __init__(self, size=0):
        '''初始化制定大小的链表'''
        if isinstance(size, int) and size > 0:
            self.__CursorSpace = [Node() * size]  # 10个位置的链表
            self.__EmptySpace()
        else:
            raise('arg: "size" must > 0')

    def __EmptySpace(self):
        '''初始化, 清空所有空间'''
        size = len(self.CursorSpace)
        for i in range(0, size-1):
            self.__CursorSpace[i].Next = i + 1
        self.__CursorSpace[-1].Next = 0

    def __CursorAlloc(self):
        '''注册空间'''
        P = self.__CursorSpace[0].Next
        self.__CursorSpace[0].Next = self.__CursorSpace[P].Next
        return P

    def __CursorFree(self, P):
        '''释放空间'''
        self.__CursorSpace[P].Next = self.__CursorSpace[0].Next
        self.__CursorSpace[0].Next = P

    def isLast(self, P):
        '''是否表尾'''
        return self.__CursorSpace[P].Next == 0

    def isEmpty(self, List):
        '''是否空表'''
        return self.__CursorSpace[List].Next == 0

    def FindPrevious(self, X, List):
        '''找前驱元'''
        P = List
        while self.__CursorSpace[P].Next != 0 and \
                self.__CursorSpace[self.__CursorSpace[P].Next].Element != X:
            P = P.Next
        return P

    def Find(self, X, List):
        '''查找 List 中 Element 为 X 的下标'''
        P = self.__CursorSpace[List].Next
        while P != 0 and self.__CursorSpace[P].Element != X:
            P = self.__CursorSpace[P].Next
        return P

    def Insert(self, X, List, P):
        '''在List中插入元素'''
        tmp = self.__CursorAlloc()
        if tmp == 0:
            raise('out of space!!!')
        self.__CursorSpace[tmp].Element = X
        self.__CursorSpace[tmp].Next = self.__CursorSpace[P].Next
        self.__CursorSpace[P] = tmp

    def Delete(self, X, List):
        '''在List中删除元素'''
        P = self.FindPrevious(X, List)
        if not self.isLast(P, List):
            tmp = self.__CursorSpace[P].Next
            self.__CursorSpace[P].Next = self.__CursorSpace[tmp].Next
            self.__CursorFree(tmp)

    def DeleteList(self, List):
        P = List
        while P != 0:
            tmp = self.__CursorSpace[P].Next
            self.__CursorFree(P)
            P = tmp

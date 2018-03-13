# -*- coding=utf-8 -*-


def permutations(li):
    if len(li) == 0:
        yield li
    else:
        for i in range(len(li)):
            li[0], li[i] = li[i], li[0]
            for item in permutations(li[1:]):
                yield li[0] + item


if __name__ == '__main__':
    t = permutations(range(4))
    for i in t:
        print i

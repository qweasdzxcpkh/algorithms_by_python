# -*- coding=utf-8 -*-
import arrow
from collections import deque
from itertools import groupby


# 加一秒
def a1s(t):
    return arrow.get(t).replace(seconds=+1)


# 减一秒
def s1s(t):
    return arrow.get(t).replace(seconds=-1)


class TimeRange(object):
    '''表示一个时间段的对象
    暂时只能以秒为单位表示时间段'''
    def __init__(self, start, end):
        self.start = arrow.get(start).floor('second')
        self.end = arrow.get(end).floor('second')

        if not self.start <= self.end:
            raise 'wrong argument: start must <= end'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'TimeRange object: {}~{}'.format(
            self.start.format('YYYY-MM-DD HH:mm:ssZZ'),
            self.end.format('YYYY-MM-DD HH:mm:ssZZ')
        )

    # 定义减法
    def __sub__(self, other):
        res = {
            'result': [],
            'other_shield': []
        }
        # 没有冲突的情况，直接返回self
        if self.end < other.start or other.end < self.start:
            # 没有冲突情况下，result为自身
            res['result'] = [self, ]
            return res

        # 有冲突的情况下，正式的减法: (  )代表self，{  }代表other
        # # (    {  )    }
        if self.start <= other.start <= self.end <= other.end:
            if self.start != other.start:
                res['result'].append(
                    TimeRange(
                        self.start,
                        s1s(other.start)
                    ),
                )
            if self.end != other.end:
                res['other_shield'].append(
                    TimeRange(
                        a1s(self.end),
                        other.end
                    ),
                )
        # # {   (  }   )
        elif other.start <= self.start <= other.end <= self.end:
            if other.start != self.start:
                res['other_shield'].append(
                    TimeRange(
                        other.start,
                        s1s(self.start)
                    )
                )
            if other.end != self.end:
                res['result'].append(
                    TimeRange(
                        a1s(other.end),
                        self.end
                    )
                )
        # # {   (  )   }
        elif other.start <= self.start <= self.end <= other.end:
            if other.start != self.start:
                res['other_shield'].append(
                    TimeRange(
                        other.start,
                        s1s(self.start)
                    )
                )
            if self.end != other.end:
                res['other_shield'].append(
                    TimeRange(
                        a1s(self.end),
                        other.end
                    )
                )
        # # (   {  }   )
        elif self.start <= other.start <= other.end <= self.end:
            if self.start != other.start:
                res['result'].append(
                    TimeRange(
                        self.start,
                        s1s(other.start)
                    )
                )
            if other.end != self.end:
                res['result'].append(
                    TimeRange(
                        a1s(other.end),
                        self.end
                    )
                )
        else:
            raise 'something error, it is a bug'
        return res


class TRdeque(deque):
    '''初始化一个时间段列表'''
    def __init__(self, time_list=None, *args, **kwargs):
        '''
        time_list应该是一个二维数组
        example: [
            ['2017-07-01 00:00:00+08:00', '2017-08-10 23:59:59+08:00'],
            ['2017-08-01 00:00:00+08:00', '2017-08-20 23:59:59+08:00']
        ]
        __init__会把时间段重复部分合并, 例如[['2017-07-01 00:00:00+08:00', '2017-08-20 23:59:59+08:00']]
        '''
        super(TRdeque, self).__init__(*args, **kwargs)

        # 根据最大的时间排序，合并重复的时间段并放进deque中
        if time_list is not None:
            time_list = sorted(
                [sorted(map(arrow.get, time_range)) for time_range in time_list if len(time_range) >= 1],
                key=lambda x: x[-1]
            )

            pre = time_list[0]
            for item in time_list[1:]:
                if pre[-1] >= item[0]:
                    pre = [min(item[0], pre[0]), max(item[-1], pre[-1])]
                else:
                    self.append(
                        TimeRange(pre[0], pre[-1])
                    )
                    pre = item
            self.append(
                TimeRange(pre[0], pre[-1])
            )

    def extendleft(self, obj):
        return super(TRdeque, self).extendleft(reversed(obj))

    def format_by_day(self):
        '''暂时只能以day为单位格式化
        example: [
            ['2017-01-01 04:30:00', '2017-01-01 08:00:00'],
            ['2017-01-01 11:30:00', '2017-01-01 13:00:00'],
            ['2017-01-01 23:00:00', '2017-01-02 13:00:00']
        ]

        return: {
            '2017-01-01': [{'s': '04:30', 'e': '08:00'},
                           {'s': '11:30', 'e': '13:00'},
                           {'s': '23:00', 'e': '23:59'}]
            '2017-01-02': [{'s': '00:00', 'e': '13:00'}]
        }
        '''
        # 预处理，把跨天的时间段分割
        tmp = []
        for TR in self:
            sr = arrow.Arrow.span_range('day', TR.start, TR.end)
            sr = map(lambda x: list(x), sr)
            sr[0][0], sr[-1][-1] = TR.start, TR.end
            # self已经排好序，直接extend后结果也是排好序
            tmp.extend(sr)

        itergroup = groupby(tmp, key=lambda x: x[0].format('YYYY-MM-DD'))
        return {k: map(lambda x: {'s': x[0].format('HH:mm'),
                                  'e': x[1].format('HH:mm')},
                       v) for k, v in itergroup}


def subtraction(open_list, shield_list):
    '''时间段减法'''
    # 预处理一下open_list
    open_que = TRdeque(open_list)
    shield_que = TRdeque(shield_list)
    result = TRdeque()
    while shield_que and open_que:
        open_TR = open_que.popleft()
        shield_TR = shield_que.popleft()

        # 没有时间冲突的两种情况
        if open_TR.end < shield_TR.start:
            result.append(open_TR)
            shield_que.appendleft(shield_TR)
            continue
        elif shield_TR.end < open_TR.start:
            open_que.appendleft(open_TR)
            continue

        res = open_TR - shield_TR
        open_que.extendleft(res['result'])
        shield_que.extendleft(res['other_shield'])

    for TR in open_que:
        result.append(TR)

    return result

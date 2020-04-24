# -*- coding: utf-8 -*-
# author: timor

from datetime import datetime, timedelta
import time


def create_time_pid():
    pid = datetime.now().strftime('%Y%m%d%H%M%S')
    return pid


def gen_pid():
    pid = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(time.time()).replace('.', '')[-5:]
    return pid


def diff_times_in_seconds(t1, t2):
    h1, m1, s1 = t1.hour, t1.minute, t1.second
    h2, m2, s2 = t2.hour, t2.minute, t2.second
    t1_secs = s1 + 60 * (m1 + 60 * h1)
    t2_secs = s2 + 60 * (m2 + 60 * h2)
    tc = str(timedelta(seconds=(t2_secs - t1_secs)))
    return tc


if __name__ == '__main__':
    print(gen_pid())

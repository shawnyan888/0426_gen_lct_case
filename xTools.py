#!/usr/bin/python  
# -*- coding: utf-8 -*-
import os

__author__ = 'Shawn Yan'
__date__ = '15:56 2018/4/23'


def say_it(msg, comments="", show=1, log_key="Y_O_S_E_L_O_G"):
    if not show:
        return
    #
    try:
        log = open(os.getenv(log_key), "a")
    except (TypeError, IOError):
        log = ""

    def _dump_it(notes):
        if log:
            print >> log, notes
        print str(notes)

    if comments:
        _dump_it(comments)
    if isinstance(msg, str):
        _dump_it(msg)
    elif isinstance(msg, list) or isinstance(msg, tuple):
        for item in msg:
            _dump_it("- %s" % item)
    elif isinstance(msg, dict):
        msg_keys = msg.keys()
        try:
            msg_keys.sort(key=str.lower)
        except (AttributeError, TypeError):
            msg_keys.sort()
        for key in msg_keys:
            value = msg.get(key)
            _dump_it(" - %-20s: %s" % (key, value))
    else:
        _dump_it(msg)
    if log:
        log.close()


def split_list(a_list, sub_lens=2):
    """
    Split a list
    :param a_list:
    :param sub_lens:
    :return:
    """
    div, mod = divmod(len(a_list), sub_lens)
    idx_list = list()
    end = 0
    for i in range(div):
        start = i * sub_lens
        end = (i+1) * sub_lens
        idx_list.append((start, end))
    if mod:
        idx_list.append((end, end+mod))
    return [a_list[foo[0]:foo[1]] for foo in idx_list]


if __name__ == "__main__":
    pass

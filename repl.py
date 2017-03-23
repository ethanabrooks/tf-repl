from __future__ import print_function

import os

import pygments
import tensorflow as tf
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.python import PythonLexer
from getch import getch
import cursor


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def highlight(arg):
    return pygments.highlight(str(arg), PythonLexer(ensurenl=False), TerminalFormatter())


def printf(arg):
    print(highlight(arg))


printf('import tensorflow as tf')

sess = tf.Session()
quit = False


def cursor_on(i, string):
    cursor_char = "\033[44;33m{}\033[m".format(string[i])
    return string[:i] + cursor_char + string[i + 1:]


def dec(index):
    return max(0, index - 1)


def inc(index, seq):
    return min(len(seq), index + 1)


blank_line = ' ' * 50
history = []


def read_input():
    I = len(history)
    string = ''
    history.append(string)
    i = 0
    while True:
        char = getch()
        key = ord(char)
        if key == 10:  # enter
            print('')
            break
        elif key == 127:  # delete
            i = dec(i)
            string = string[:i] + ' ' * (len(string) - i)
        elif key == 65:  # up
            I = dec(I)
            string = history[I]
        elif key == 66:  # down
            I = inc(I, history[:-1])
            string = history[I]
        elif key == 68:  # left
            i = dec(i)
        elif key == 67:  # right
            i = inc(i, string)
        elif key == 1:  # cmd + right
            i = 0
        elif key == 5:  # cmd + left
            i = len(string)
        elif key in [91, 27]:
            pass
        else:
            string = string[:i] + char + string[i:]
            if I == len(history) - 1:
                history[I] = string
            i += 1
        # i = min(len(string), i)
        formatted = highlight(string)
        # formatted = cursor_on(i, formatted)
        print('\r\033[6;{}H>>> {}'.format(i - 10, formatted + blank_line), end='')
        # print('\r(' + str(history) + str(I) + ')>>> ' + formatted, end='')
    return string


# with cursor.HiddenCursor():
while not quit:
    print('>>> ', end='')
    expr_string = read_input()
    history[-1] = expr_string

    # quit
    if expr_string in ['quit', 'q']:
        response = raw_input('Are you sure? [y|n] ')
        while response not in ['y', 'n']:
            response = raw_input('Please enter "y" or "n": ')
        if response == 'y':
            exit(0)
        else:
            continue

    try:
        if '=' in expr_string:
            exec expr_string
            expr_string = expr_string.split('=')[0]
        expr = eval(expr_string)
        try:
            printf(sess.run(expr))
        except (RuntimeError, TypeError):  # if not actually a tf expression
            printf(expr)
    except Exception as e:
        # print(type(e))
        print(e)

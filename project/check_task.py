# -*- coding: utf-8 -*-
import os
import subprocess
from .utils import get_task_file
# from utils import get_task_file
# import test
# import pywinauto
# import unittest
from threading import Thread
from time import sleep
from celery import shared_task


URL_TASK = 'http://127.0.0.1:5000/api/change_task'


def check_2():
    """
    Идея в том, что скопировать текст, встаивть его в функцию и потом провести тест
    вопрос... как ввести input
    """
    a = 'def test1():\n'
    with open('test.py') as f:
        for i in f.readlines():
            a += f'\t{i}'
        # a += f.read()

    with open('check_test.py', mode='w') as f:
        f.write(a)

    # test1()

    if 'Здравствуй, мир!' == test1():
        print('123')

    # a = subprocess.call(['python ./test.py'])
    # print(a)


def save_test(data):
    with open('check_test.py', mode='w', encoding='utf-8') as f:
        f.write(data)


# @shared_task(bind=True)
def start_check(user_data):

    # print(1, user_data)
    # sleep(1)
    # print(2, user_data['text'])
    # sleep(2)
    # print(3, user_data['lesson'])
    # sleep(3)
    # print(4, user_data['task'])
    # sleep(10)
    save_test(user_data['text'])

    task = get_task_file(user_data['lesson'])['tasks'][user_data['task']]
    print(task)
    for test in task['data']:
        print(test['num'])

        try:
            output = subprocess.check_output("python check_test.py", shell=True,
                                             input=test['data_in'].encode('WINDOWS-1251')).decode('WINDOWS-1251')
            # print(output.decode('WINDOWS-1251'), test)
            output = output.replace('\r', '')[:-1]

            print(repr(output), '_-_-_', repr(test['data_out']))
            if output == test['data_out']:
                print('Верно')
            else:
                print('Не верно')
                return False
        except SyntaxError as error:
            print('Синтаксическая ошибка')
            return False
        except Exception as e:
            print(type(e))
            print('Ошибка в коде')
            return False

    return True
    # ------------

    #
    # p = subprocess.Popen('python test.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    # p.stdin.write(b'123')
    # # p.stdin.write(b'123')
    # stdout, stderr = p.communicate(input=b'123\n123')
    # print(stdout.decode())


if __name__ == '__main__':
    a = {
        "lesson": 1,
        "task": 0
    }
    start_check({'text': '123', "lesson": '1', "task": '2'})

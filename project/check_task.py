# -*- coding: utf-8 -*-
import os
import subprocess

from project.models import Tasks
from .utils import get_task_file
from time import sleep
from . import db


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


def run():
    # run some code here
    print('Threaded task has been completed 1')
    sleep(10)
    print('Threaded task has been completed 2')
    sleep(1)
    print('Threaded task has been completed 3')


def save_test(data):
    with open('check_test.py', mode='w', encoding='utf-8') as f:
        f.write(data)


def start_check():
    print('Получены запрос')
    print('Получены запрос')
    tasks = Tasks.query.filter_by(is_check=True).all()
    print('Получены запрос')
    print(tasks)
    for task in tasks:
        print('Перебираем все задачи')
        res = check_task({'text': task.text, "lesson": task.lesson, "task": task.task})
        task.completed = res
        task.is_check = False
        db.session.commit()


def check_task(user_data):
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

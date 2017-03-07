# cobroadcast.py
#
# An example of broadcasting a data stream onto multiple coroutine targets.

# A data source.  This is not a coroutine, but it sends
# data into one (target)

import time


def coroutine(func):
    # декоратор coroutine
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr

    return start


def follow(thefile, target):
    thefile.seek(0, 2)  # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)  # Sleep briefly
            continue

        # если появилась новая строка пошлем ее объекту target
        # в данном случае это broadcast
        target.send(line)


# grep фильтрует по наличию патерна в строке
@coroutine
def grep(pattern, target):
    while True:
        line = (yield)  # Получаем строку с текстом

        if pattern in line:    # если подстрока есть в строке
            target.send(line)  # то шлем строку на printer


# A sink.  A coroutine that receives data
@coroutine
def printer():
    while True:
        line = (yield)
        print(line)


# Broadcast рассылает строку всем grep по списку
@coroutine
def broadcast(targets):
    while True:
        item = (yield)
        for target in targets:
            target.send(item)


# Example use
if __name__ == '__main__':
    f = open("access-log")

    # вызовем follow
    follow(f,
           broadcast([grep('python', printer()),
                      grep('ply', printer()),
                      grep('swig', printer())])
           )

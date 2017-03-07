import time


def follow(thefile):
    """
    Генератор, возвращает последнюю строку файла
    """
    thefile.seek(0, 2)  # Перемещаемся в конец файла

    # стартуем главный цикл генератора
    while True:
        # читаем строку
        line = thefile.readline()

        # если новой строки нет, продолжаем цикл
        if not line:
            time.sleep(0.1)  # Спим
            continue
        # если есть, вернем ее
        yield line


def grep(pattern, lines):
    """
    Генератор который ищет вхождение строки pattern в строках lines, или как в данном случае - в генераторе
    """
    for line in lines:
        if pattern in line:
            yield line


if __name__ == '__main__':
    with open("access-log") as logfile:
        loglines = follow(logfile)
        pylines = grep("python", loglines)

        # выводим результат
        for line in pylines:
            print(line)

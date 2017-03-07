def grep(pattern):
    print("Looking for %s" % pattern)
    while True:
        # получаем параметр через send()
        line = (yield)
        if pattern in line:
            print(line)


# Example use
if __name__ == '__main__':
    # создадим итератор с паттерном для поиска "python"
    g = grep("python")

    # запустим его
    next(g)
    # отправляем ему параметры
    g.send("Yeah, but no, but yeah, but no")
    g.send("A series of tubes")
    g.send("python generators rock!")

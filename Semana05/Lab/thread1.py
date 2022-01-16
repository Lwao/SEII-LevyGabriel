import time

def funcao(msg, num):
    for i in range(num):
        print(msg)
        time.sleep(.1)

funcao("primeira",10)
funcao("segunda",10)
funcao("terceira",10)
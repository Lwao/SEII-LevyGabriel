import time
import threading

count = 0

def funcao(i, total):
    global count
    for i in range(total):
        count += 1
        print(i, " - ", count)

for i in range(1000):
    funcao(i, 50)
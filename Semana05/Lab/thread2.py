import time
import threading

def funcao(msg, num):
    for i in range(num):
        print(msg)
        time.sleep(.5)

t1 = threading.Thread(target=funcao, args=("primeira",5))
t2 = threading.Thread(target=funcao, args=("segunda",5))
t3 = threading.Thread(target=funcao, args=("terceira",10))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
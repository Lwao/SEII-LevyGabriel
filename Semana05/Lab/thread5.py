import time
import threading

count = 0
th_lock = threading.Lock()

def funcao(i, total):
    print("Iniciando: ", threading.current_thread().ident)
    global count
    for i in range(total):
        th_lock.acquire()
        count += 1
        th_lock.release()
        time.sleep(.001)

threads = []
for i in range(200):
    t = threading.Thread(target=funcao, args=(i,5000))
    threads.append(t)
    t.start()

for t in threads:
    print("Finalizando: ", t.ident)
    t.join()

print("Total: ", count)
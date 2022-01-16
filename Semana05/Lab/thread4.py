import time
import threading

count = 0

def funcao(i, total):
    print("Iniciando: ", threading.current_thread().ident)
    global count
    for i in range(total):
        count += 1
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
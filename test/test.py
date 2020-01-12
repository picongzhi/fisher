import time
import threading


def worker():
    time.sleep(5)
    print('current thread name:', threading.current_thread().getName())


thread = threading.Thread(target=worker, name='sub_thread')
# thread.setDaemon(True)
thread.start()

print('current thread name:', threading.current_thread().getName())
# thread.join(2)

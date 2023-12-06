# EXAMPLE 1
import threading
import time


class myThread(threading.Thread):
    def __init__(self, threadId, name, count):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.count = count

    def run(self):
        print("Starting: " + self.name + "\n")
        threadLock.acquire()
        print_time(self.name, 1,self.count)
        threadLock.release()
        print("Exiting: " + self.name + "\n")

    def run_no_locks(self):
        print("Starting: " + self.name + "\n")
##        threadLock.acquire()
        print_time(self.name, 1,self.count)
        threadLock.release()
        print("Exiting: " + self.name + "\n")


def print_time(name, delay, count):
    while count:
        time.sleep(delay)
        print ("%s: %s %s" % (name, time.ctime(time.time()), count) + "\n")
        count -= 1


threadLock = threading.Lock()

thread1 = myThread(1, "Thread 1", 5)
thread2 = myThread(2, "Thread 2", 5)


thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("Done main thread")

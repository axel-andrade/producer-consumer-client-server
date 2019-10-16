import socket
from threading import Thread
import queue
import time

BUFFER_SIZE = 20
q = queue.Queue(2)


def action(number):
    return number * number


class Item(object):
    def __init__(self, data, conn):
        self.data = data
        self.conn = conn


class ConsumerThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        Thread.__init__(self)
        self.target = target
        self.name = name

    def run(self):
        while True:
            if not q.empty():
                item = q.get(block=False)
                print("Queueing data: ", item.data)
                time.sleep(3)
                print("Finshed queue: ", item.data)
                result = action(item.data)
                item.conn.send(str(result).encode('ascii'))


class ProducerThread(Thread):
    def __init__(self, conn, ip, port):
        Thread.__init__(self)
        self.conn = conn
        self.ip = ip
        self.port = port
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self):
        while True:
            data = self.conn.recv(2048)
            print("Server received data:", data)
            if not q.full():
                q.put(Item(int(data.decode('ascii')), self.conn))
                # conn.send("Done: " + data)  # echo


threads = []

c = ConsumerThread(name='numbers')
c.start()
threads.append(c)


def Main():
    host = '0.0.0.0'
    port = 2004
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        conn, addr = s.accept()
        print('Connected to :', addr[0], ':', addr[1])
        # Start a new thread and return its identifier
        newthread = ProducerThread(conn, addr[0], addr[1])
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()

    print('Sai da thread principal.')

    s.close()


if __name__ == '__main__':
    Main()

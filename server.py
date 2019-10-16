import socket
from threading import Thread, Condition
import time
import random

queue = []
MAX_NUM = 3
condition = Condition()


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
            condition.acquire()
            if not queue:
                print("Nada na fila, o consumidor está esperando")
                condition.wait()
                print("O produtor adicionou algo à fila e notificou o consumidor")
            item = queue.pop(0)
            print("Consumindo: ", item.data)
            result = action(item.data)
            item.conn.send(str(result).encode('ascii'))
            condition.notify()
            condition.release()
            time.sleep(random.random())


class ProducerThread(Thread):
    def __init__(self, conn, ip, port):
        Thread.__init__(self)
        self.conn = conn
        self.ip = ip
        self.port = port
        print("[+] Novo socket iniciado no servidor em " + ip + ":" + str(port))

    def run(self):

        while True:
            data = self.conn.recv(2048)
            print("Servidor recebeu:", data)
            condition.acquire()
            if len(queue) == MAX_NUM:
                print("Fila cheia, o produtor está aguardando")
                condition.wait()
                print("Espaço na fila, consumidor notificou o produtor")
            data = data.decode('ascii')
            if len(data) > 0:
                # adicionando na fila
                queue.append(Item(int(data), self.conn))
                print("Produzindo: ", data)
                condition.notify()
                condition.release()
                time.sleep(random.random())


def Main():
    threads = []
    c = ConsumerThread(name='numbers')
    c.start()
    threads.append(c)
    host = '0.0.0.0'
    port = 2004
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Socket ligado a porta: ", port)
    s.listen(5)
    print("Ouvindo ...")

    # loop infinito enquanto houver clientes
    while True:
        # estabelecendo conexão com o cliente
        conn, addr = s.accept()
        print('Connected to :', addr[0], ':', addr[1])
        # Iniciando uma nova thread e retornando seu identificador
        newthread = ProducerThread(conn, addr[0], addr[1])
        newthread.start()
        threads.append(newthread)

        for t in threads:
            t.join()

        print('Sai da thread principal.')

    s.close()


if __name__ == '__main__':
    Main()

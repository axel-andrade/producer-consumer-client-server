import socket
from threading import Thread, Condition
import time
import random

queue = []
condition = Condition()


def action(number):
    time.sleep(random.randint(0, 20))
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
            try:
                item = queue.pop(0)
                condition.notify()
                condition.release()
                print("Consumindo: ", item.data)
                result = action(item.data)
                item.conn.send((str(result)+" - Consumidor").encode('ascii'))
            except:
                condition.wait()


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
            data = data.decode('ascii')
            if len(data) > 0:
                print("Servidor recebeu:", data)
                # adicionando na fila
                queue.append(Item(int(data), self.conn))
                print("Produzindo: ", data)
                time.sleep(random.random())
            else:
                #     self.conn.close()
                break


TCP_IP = '0.0.0.0'
TCP_PORT = 2004


tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpServer.listen(5)
    print("Servidor aguardando conexão de clientes...")
    conn, addr = tcpServer.accept()
    print('Conectado em:', addr[0], ':', addr[1])
    if(random.randint(0, 1)):
        try:
            print("Rodando localmente ... ")
            data = conn.recv(2048)
            data = int(data.decode('ascii'))
            result = data * data
            conn.send((str(result)+" - Local").encode('ascii'))
        except Exception as e:
            pass
        finally:
            conn.close()

    else:
        c = ConsumerThread(name='numbers')
        c.start()
        threads.append(c)
        newthread = ProducerThread(conn, addr[0], addr[1])
        newthread.start()
        threads.append(newthread)

for t in threads:
    t.join()

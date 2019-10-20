from socket import *
from threading import Thread


class ClientThread(Thread):
    def __init__(self, c, server, port):
        self.c = c
        self.server = server
        self.port = port
        Thread.__init__(self)

    def run(self):
        # Criamos o socket e o conectamos ao servidor
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.server, self.port))
        # Enviando mensagem
        s.send(str(self.c).encode('ascii'))
        # Recuperando mensagem do servidor
        data = s.recv(2048)
        # Exibindo mensagem  recebida
        print('Enviado: ', self.c, 'Recebido: ', str(data.decode('ascii')))
        s.close()


host = '127.0.0.1'
port = 2004
threads = []
# Nós spawnamos os clientes
for c in range(20):
    t = ClientThread(c, host, port)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Geramos todos os clientes")

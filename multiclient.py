from socket import *
from threading import Thread


class ClientThread(Thread):
    """
    Classe que gera os clientes
    """

    def __init__(self, c, server, port):
        # Número de identificação do cliente
        self.c = c

        # Servidor a ser conectado
        self.server = server

        # Port para ser usada
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


# Configurações de conexão do servidor
# O nome do servidor pode ser o endereço de
# IP ou o domínio (ola.python.net)
host = '127.0.0.1'
port = 2004

# Nós spawnamos os clientes
for c in range(20):
    ClientThread(c, host, port).start()

print("Geramos todos os clientes")

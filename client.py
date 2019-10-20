import socket


def Main():
    host = '127.0.0.1'
    port = 2004
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    counter = 0
    while counter <= 50:
        # Enviando mensagem
        s.send(str(counter).encode('ascii'))
        # Recuperando mensagem do servidor
        data = s.recv(2048)
        # Exibindo mensagem  recebida
        print('Enviado: ', counter, 'Recebido: ', str(data.decode('ascii')))
        counter = counter + 1

    # Fechando conexao
    s.close()


if __name__ == '__main__':
    Main()

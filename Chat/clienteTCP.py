import socket
import threading



def recvMsg(tcp):
     while True:
        msg = tcp.recv(1024)
        if not msg: 
            break
        print ("\nServidor mandou:", tcp,msg.decode(),"\n")
        



HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta escutando
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
print ('Para sair digite fim\n')
threading.Thread(target=recvMsg, args=(tcp,)).start()
msg = input("Mensagem>> ")
while msg != 'fim':
    tcp.send (msg.encode('utf-8'))
    msg = input("\nMensagem>> ")
tcp.close()

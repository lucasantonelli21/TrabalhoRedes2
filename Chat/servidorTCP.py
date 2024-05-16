import socket
import threading


def connect(capacity):
    HOST = ''              # Endereco IP do Servidor
    PORT = 5000            # Porta que o Servidor esta escutando
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    clients= []
    while len(clients) < int(capacity):
        faltamConnec=int(capacity)-len(clients)
        print(f"Aguardando conexoes: {faltamConnec}")
        tcp.listen()
        connection = tcp.accept()
        clients.append(connection)
    for con in clients:
        threading.Thread(target=recvMsg, args=(con[0],con[1],clients,)).start()
    
        
    
    tcp.close()
    
def echoMsg(client,clients,msg):
    for con in clients:
        if(con[1]!=client):
            con[0].sendall(msg)
       
def recvMsg(connection,client,clients):
    print('Connected by ',client)
    while True:
        msg = connection.recv(1024)
        if not msg: 
            break
        print (client, msg.decode())
        echoMsg(client,clients,msg)
    print ('Finalizando conexao do cliente', client)
    
    connection.close()
    
       
        
        


if __name__ == "__main__":
    capacity=input("Digite a capacidade da sala:")
    connect(capacity)
    
    
    





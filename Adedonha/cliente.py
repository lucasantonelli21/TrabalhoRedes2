import socket
import threading
import time


    
    
    
    
def receive_messages(s,server_host,server_port):
    while True:
        data, _ = s.recvfrom(1024)  # Buffer size is 1024 bytes
        print(f"Mensagem Recebida: {data.decode()}")
        if data.decode() == "O jogo comecou.":
            answerQuestions(s,server_host,server_port)
        
def answerQuestions(s,server_host,server_port):
    nome = input("\nNome>> ") #"Nome:","Cidade:","Pais:","Animal:","Objeto:"
    cidade = input("Cidade>>")
    pais = input("País>>")
    animal = input("Animal>>")
    objeto = input("Objeto>>")
    message = f"{nome},{cidade},{pais},{animal},{objeto}"
    send_message(s, server_host, server_port,message)
    receive_messages(s,server_host,server_port)
    
def send_message(s, server_host, server_port,message):
        s.sendto(message.encode(), (server_host, server_port))

def udp_client(server_host='127.0.0.1', server_port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Envia uma mensagem inicial para registrar o cliente no servidor
        initial_message = "Cliente conectado!"
        s.sendto(initial_message.encode(), (server_host, server_port))
        receive_messages(s,server_host,server_port)
        

if __name__ == "__main__":
    udp_client()

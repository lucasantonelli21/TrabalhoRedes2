import socket
import threading

def receive_message(s):
    while True:
        data, _ = s.recvfrom(1024)  # Buffer size is 1024 bytes
        print(f"Received message: {data.decode()}")
        return data
    
def receive_messages(s):
    while True:
        data, _ = s.recvfrom(1024)  # Buffer size is 1024 bytes
        print(f"Received message: {data.decode()}")
        
def answerQuestions(s,server_host,server_port):
    i=0
    while(receive_message(s)!="END"):
        answer = input("\n>> ")
        answers=[]
        answers.append(answer)
        i+=1
    message=''.join(answers)
    send_message(s, server_host, server_port,message)
    
def send_message(s, server_host, server_port,message):
        s.sendto(message.encode(), (server_host, server_port))

def udp_client(server_host='127.0.0.1', server_port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Envia uma mensagem inicial para registrar o cliente no servidor
        initial_message = "Cliente conectado!"
        s.sendto(initial_message.encode(), (server_host, server_port))
        threading.Thread(target=receive_messages, args=(s,)).start()
        answerQuestions(s, server_host, server_port)

if __name__ == "__main__":
    udp_client()

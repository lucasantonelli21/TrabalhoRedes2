import socket
import threading
import random
import string
import time

class Player:
    def __init__(self,client_addrs) -> None:
        self.addres=client_addrs
        self.answer=[]
        
        
    def setAnswers(playersAnswers,answer):
        self.playersAnswers.append(answer)
class Room:
    def __init__(self, capacity,letter, players,clients_addr) -> None:
        self.capacity = capacity
        self.letter = letter
        self.players = players
        self.clients_addr=clients_addr
        self.playersQuestions =["Nome:","Cidade:","Pais:","Animal:","Objeto:"]
      

    
            
    
    
    
def startGame(s,room,start):
    gameStartedMessage="Game has been started\nQuestions:"
    send_messages(s,room.clients_addr,gameStartedMessage)
    for question in room.playersQuestions:
        send_messages(s,room.clients_addr,question)
    while(time.perf_counter()-start!=60):
        receive_messages(s,room)
    endOfGame="END"
    send_messages(s,room.clients_addr,endOfGame)
        
        
def receive_messages(s,room):
    answer, addr = s.recvfrom(1024)  # Buffer size is 1024 bytes
    for player in room.players:
        if addr == room.players.addres:
            room.players.setAnswers(answer)

def send_messages(s, clients_addr,message):
    for addr in clients_addr:
        s.sendto(message.encode(), addr)
        
def send_connection(s,client_addr):
    message="You're connected to the game.\n"
    s.sendto(message.encode(), client_addr)
    
    
def sortLetter(s, clients_addr):
    letters = string.ascii_uppercase
    letter = random.choice(letters)
    message = f'The sorted letter is {letter}\n'
    for addr in clients_addr:
        s.sendto(message.encode(), addr)
    return letter
    
def udp_serverInit(host='127.0.0.1', port=12345):
    capacity = 1
    players = []
    clients_addr =[]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        connected=0
        while(connected!=capacity):
            print(f"Waiting for Players:{capacity-connected}")
            data, addr = s.recvfrom(1024)  # Aguarda a primeira mensagem para obter o endereço do cliente
            send_connection(s,addr)
            player= Player(addr)
            players.append(player)
            clients_addr.append(addr)
            connected+=1
            print(f"Player has Connected\n")
        initialMessage = 'Sorting letter...\n'
        send_messages(s,clients_addr,initialMessage)
        time.sleep(3)
        letter = sortLetter(s,clients_addr)
        room = Room(capacity,players,letter,clients_addr)
        time.sleep(5)
        startGame(s,room,time.perf_counter())
        #threading.Thread(target=receive_messages, args=(s,)).start()
        
        


if __name__ == "__main__":
    udp_serverInit()

import socket
import threading
import random
import string
import time

class Player:
    def __init__(self,client_addrs) -> None:
        self.addres=client_addrs
        self.answer=[]
        self.points=0
        
        
    def setAnswers(self,answer):
        self.answer.append(answer)
class Room:
    def __init__(self, capacity,letter, players,clients_addr) -> None:
        self.capacity = capacity
        self.letter = letter
        self.players = players
        self.clients_addr=clients_addr
        self.playersQuestions =["Nome:","Cidade:","Pais:","Animal:","Objeto:"]
      

    
            
    
    
    
def startGame(s,room):
    gameStartedMessage="O jogo comecou."
    send_messages(s,room.clients_addr,gameStartedMessage)
    receive_answers(s,room)
    
        
        
def receive_answers(s,room):
    cont = 0
    while cont<room.capacity:
        data, addr = s.recvfrom(1024)  # Buffer size is 1024 bytes
        for player in room.players:
            if addr == player.addres:
                answers=[]
                answers = data.decode().split(',')
                for answer in answers:
                    player.setAnswers(answer)
                cont += 1
    validate_answers(s,room)

def validate_answers(s,room):
    for player in room.players:
        for answer in player.answer:
            if(answer==room.letter):
                player.points+=10
    send_answers(s,room)
    
           
def send_answers(s,room):
    for player in room.players:
        pontuacao = f"Sua pontuacao foi {player.points}."
        s.sendto(pontuacao.encode(),player.addres)
        

def send_messages(s, clients_addr,message):
    for addr in clients_addr:
        s.sendto(message.encode(), addr)
        
def send_connection(s,client_addr):
    message="Voce se conectou ao jogo.\n"
    s.sendto(message.encode(), client_addr)
    
    
def sortLetter(s, clients_addr):
    letters = string.ascii_uppercase
    letter = random.choice(letters)
    message = f'A letra sorteada e {letter}.\n'
    for addr in clients_addr:
        s.sendto(message.encode(), addr)
    return letter
    
def udp_serverInit(host='127.0.0.1', port=12345):
    capacity = 2
    players = []
    clients_addr =[]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        connected=0
        while(connected!=capacity):
            aguardandoPlayers= f'Esperando por jogadores:{capacity-connected}.'
            send_messages(s,clients_addr,aguardandoPlayers)
            print(aguardandoPlayers)
            data, addr = s.recvfrom(1024)  # Aguarda a primeira mensagem para obter o endereço do cliente
            send_connection(s,addr)
            player= Player(addr)
            players.append(player)
            clients_addr.append(addr)
            connected+=1
            print(f"{data.decode()}\n")
            
        initialMessage = 'Sorteando letra...\n'
        send_messages(s,clients_addr,initialMessage)
        time.sleep(3)
        letter = sortLetter(s,clients_addr)
        room = Room(capacity,letter,players,clients_addr)
        startGame(s,room)
        #threading.Thread(target=receive_messages, args=(s,)).start()
        
        


if __name__ == "__main__":
    udp_serverInit()

import pygame
from enum import Enum
import sys
# pylint: disable=no-member
import math
import pika
import uuid
import json
import time
from threading import Thread
from pygame import mixer

screen = pygame.display.set_mode((1250, 600))

backgroundImage = pygame.image.load("wall4.jpg")
image1 = pygame.image.load('UP4.png')
image2 = pygame.image.load('RIGHT4.png')
image3 = pygame.image.load('LEFT4.png')
image4 = pygame.image.load('DOWN4.png')
op1 = pygame.image.load('UP6.png')
op2 = pygame.image.load('DOWN6.png')
op3 = pygame.image.load('LEFT6.png')
op4 = pygame.image.load('RIGHT6.png')



IP = '34.254.177.17'
PORT = 5672
VIRTUAL_HOST = 'dar-tanks'
USERNAME = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'

pygame.init()


class TankRpcClient:
    def __init__(self):
        self.connection  = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,                                             
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()                      
        queue = self.channel.queue_declare(queue='',exclusive=True,auto_delete=True) 
        self.callback_queue = queue.method.queue 
        self.channel.queue_bind(exchange='X:routing.topic',queue=self.callback_queue)
        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response,
                                   auto_ack=True) 
    
        self.response= None    
        self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            print(self.response)

    def call(self, key, message={}):     
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message) 
        )
        while self.response is None:
            self.connection.process_data_events()

    def check_server_status(self): 
        self.call('tank.request.healthcheck')
        return self.response['status']== '200' 

    def obtain_token(self, room_id):
        message = {
            'roomId': room_id
        }
        self.call('tank.request.register', message)
        if 'token' in self.response:
            self.token = self.response['token']
            self.tank_id = self.response['tankId']
            self.room_id = self.response['roomId']
            return True
        return False

    def turn_tank(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)

    def fire_bullet(self, token):
        message = {
            'token': token,
        }
        self.call('tank.request.fire', message)

class TankConsumerClient(Thread):

    def __init__(self, room_id):
        super().__init__()
        self.connection  = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,                                                
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()                      
        queue = self.channel.queue_declare(queue='',exclusive=True,auto_delete=True)
        event_listener = queue.method.queue
        self.channel.queue_bind(exchange='X:routing.topic',queue=event_listener,routing_key='event.state.'+room_id)
        self.channel.basic_consume(
            queue=event_listener,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
       

    def run(self):
        self.channel.start_consuming()

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

MOVE_KEYS = {
    pygame.K_w: UP,
    pygame.K_a: LEFT,
    pygame.K_s: DOWN,
    pygame.K_d: RIGHT
}

def draw_bullet(x, y,  **kwargs):
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)
    pygame.display.update()
    



def draw_tank(x, y, id, direction,  **kwargs):
    if id == Bakyt_id:
        if direction == 'UP':
            screen.blit(image1, (x, y))
        if direction == 'LEFT':
            screen.blit(image3, (x, y))
        if direction == 'DOWN':
            screen.blit(image4, (x,y))
        if direction == 'RIGHT':
            screen.blit(image2, (x, y))
        pygame.display.update()
    else :
        if direction == 'UP':
            screen.blit(op1, (x, y))
        if direction == 'LEFT':
            screen.blit(op3, (x, y))
        if direction == 'DOWN':
            screen.blit(op2, (x,y))
        if direction == 'RIGHT':
            screen.blit(op4, (x, y))
        
        pygame.display.update()
     
    

def game_start():
    mainloop = True
    font = pygame.font.Font('freesansbold.ttf', 32)
    while mainloop:

        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                if event.key in MOVE_KEYS:
                    client.turn_tank(client.token, MOVE_KEYS[event.key])
                if event.key == pygame.K_SPACE:
                    client.fire_bullet(client.token)
    
            try:
                remaining_time = event_client.response['remainingTime']
                text = font.render('Remaining Time: {}'.format(remaining_time), True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = (500, 100)
                screen.blit(text, textRect)
                hits = event_client.response['hits']
                bullets = event_client.response['gameField']['bullets']
                winners = event_client.response['winners']
                tanks = event_client.response['gameField']['tanks']
                for tank in tanks:
                    draw_tank(**tank)


                for bullet in bullets:
 
                    draw_bullet(**bullet)
                for a in range (len(tanks)):
                    tank_x = tanks[a]['x']
                    tank_y = tanks[a]['y']
                    tank_height = tanks[a]['height']
                    tank_width = tanks[a]['width']
                    tank_id=tanks[a]['id']
                    tank_direction = tanks[a]['direction']
                    tank_score=tanks[a]['score']
                    tank_health=tanks[a]['health']
                    info_x=600
                    info_y=16*a+1
                    info = font.render('NAME : {}, SCORE: {} ,LIVES: {}'.format(tank_id,tank_score, tank_health), True, (255, 255, 255)) 
                    screen.blit(info, (info_x,info_y))

                    draw_tank(tank_x, tank_y, tank_width, tank_height, tank_direction)
                    
            except Exception as e:
               
                pass
            pygame.display.flip()
    
    client.connection.close()
    pygame.quit()


def Menu():
    pygame.draw.rect(screen, (0, 0, 255), (300, 140, 375, 150)) 
    pygame.draw.rect(screen, (255, 0, 0), (300, 270, 375, 150))
    pygame.draw.rect(screen, (0, 255, 0), (300, 400, 375, 150))
    
def addText():
    font = pygame.font.SysFont('Arial', 35)
    screen.blit(font.render('Single Player Mode', True, (255,255,255)), (320, 150))
    screen.blit(font.render('Multiplayer Mode', True, (255,255,255)), (320, 270))
    screen.blit(font.render('Multiplayer AI Mode', True, (255,255,255)), (320, 400))
    pygame.display.update()

run = True
while run:
    screen.fill((0, 0, 0))
    screen.blit(backgroundImage, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                Menu = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if pos_x > 300 and pos_x < 550 and pos_y > 140 and pos_y <220:
                    import Mytankimain.py
                if pos_x > 300 and pos_x < 550 and pos_y > 270 and pos_y <350:
                    client = TankRpcClient()
                    client.check_server_status()
                    client.obtain_token('room-10')
                    event_client = TankConsumerClient('room-10')
                    event_client.start()
                    Bakyt_id = client.tank_id
                    game_start()
                if pos_x > 300 and pos_x < 550 and pos_y > 400 and pos_y <490:
                    import third.py
    
    pos_x, pos_y = pygame.mouse.get_pos()
    Menu()
    addText()
    pygame.display.flip()


    
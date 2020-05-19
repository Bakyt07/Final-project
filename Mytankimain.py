import pygame
import random
import time
from enum import Enum
from pygame import mixer



pygame.init()

width=800
height=600
screen = pygame.display.set_mode((width, height))
backgroundImage = pygame.image.load("bg.jpg")
foodimage=pygame.image.load('lemon.png')
wallimage = pygame.image.load('wall.jpg')
wall1image = pygame.image.load('wall1.jpg')
wall2image = pygame.image.load('wall2.jpg')
wall3image = pygame.image.load('wall3.jpg')
font = pygame.font.SysFont('CALIBRI', 36) 
seconds=1/60

BulSound=pygame.mixer.Sound('bullet.wav')
CollSound=pygame.mixer.Sound('coll.wav')
Over=pygame.mixer.Sound('end.wav')




class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Tank:

    def __init__(self, x, y, speed, color, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN,d_shot=pygame.K_RETURN):
        self.x = x
        self.y = y
        self.score=3
        self.speed = speed+15
        self.color = color
        self.width = 40
        self.direction = Direction.RIGHT

        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                    d_up: Direction.UP, d_down: Direction.DOWN}

        self.KEYSHOT=d_shot


    def draw(self):
        tank_c = (int(self.x) + int(self.width / 2), int(self.y) + int(self.width / 2))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width), 2)
        pygame.draw.circle(screen, self.color, tank_c, int(self.width / 2))

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c, (int(self.x) + self.width + int(self.width/2), int(self.y)  + int(self.width/2)), 4)

        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (int(self.x) - int(self.width/2), int(self.y)  + int(self.width/2)), 4)

        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (int(self.x) + int(self.width/2), int(self.y)  - int(self.width/2)), 4)
        
        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c, (int(self.x) + int(self.width/2), int(self.y)  + self.width + int(self.width/2)), 4)


    def change_direction(self,direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed*seconds
            if self.x <=0:
                self.x = 800
        if self.direction == Direction.RIGHT:
            self.x += self.speed*seconds
            if self.x >= 800:
                self.x = 0
        if self.direction == Direction.UP:
            self.y -= self.speed*seconds
            if self.y <= 0:
                self.y = 600
        if self.direction == Direction.DOWN:
            self.y += self.speed*seconds
            if self.y >=600:
                self.y = 0
        self.draw()

class Lemon:
    def __init__(self):
        self.x=random.randint(20,765)
        self.y=random.randint(320,555)
    def draw(self):
        screen.blit(foodimage, (self.x, self.y))     

class Wall:
    def __init__(self):
       self.x=random.randint(30,760)
       self.y=random.randint(250, 475)
    def draw(self):
        screen.blit(wallimage, (self.x, self.y))
    



class Bullet:
    def __init__(self,bullet_x=0,bullet_y=0,bullet_color=(0,0,0),direction=Direction.LEFT,bullet_speed=15):
        self.bullet_x = bullet_x
        self.bullet_y = bullet_y
        self.bullet_color = bullet_color
        self.bullet_speed = bullet_speed
        self.direction=direction
        self.bullet_radius = 10
        self.bullet_status = True


    def move(self):
        if self.direction == Direction.LEFT:
            self.bullet_x -= self.bullet_speed
        if self.direction == Direction.RIGHT:
            self.bullet_x += self.bullet_speed
        if self.direction == Direction.UP:
            self.bullet_y -= self.bullet_speed
        if self.direction == Direction.DOWN:
            self.bullet_y += self.bullet_speed
        self.draw()

    def draw(self):
        if self. bullet_status:
            pygame.draw.circle(screen,self.bullet_color,(int(self.bullet_x),int(self.bullet_y)),self.bullet_radius)

def location(tank):
    if tank.direction == Direction.RIGHT:
        bullet_x=tank.x + tank.width + int(tank.width / 2)
        bullet_y=tank.y + int(tank.width / 2)

    if tank.direction == Direction.LEFT:
        bullet_x=tank.x - int(tank.width / 2)
        bullet_y=tank.y + int(tank.width / 2)

    if tank.direction == Direction.UP:
        bullet_x=tank.x + int(tank.width / 2)
        bullet_y=tank.y - int(tank.width / 2)

    if tank.direction == Direction.DOWN:
        bullet_x=tank.x + int(tank.width / 2)
        bullet_y=tank.y + tank.width + int(tank.width / 2)

    bull=Bullet(bullet_x,bullet_y,tank.color,tank.direction)
    bullet.append(bull)

def Impact():
    if (food.y< tank1.y +20 and food.y >= tank1.y -20) and (food.x>= tank1.x and food.x<tank1.x+18) :
        tank1.is_add = True  
        
        if tank1.is_add == True:
            tank1.speed*=2 
            food.x = random.randint(12, 760)
            food.y = random.randint(12, 560)
            
def Impact2():
    if (food.y<tank2.y + 20 and food.y >= tank2.y - 20) and (food.x>= tank2.x and food.x<tank2.x + 20):
        tank2.is_add = True
        if tank2.is_add == True:
            tank2.speed*=2
            food.x = random.randint(12, 760)
            food.y = random.randint(12, 560) 


def WImpact():
  if (brick.y<tank1.y + 20 and brick.y >= tank1.y - 20  ) and (brick.x>= tank1.x + 20 and brick.x<tank1.x - 20) :
        tank1.score-=1
        wall1image = random.randint(20, 730)
        wall1image = random.randint(20, 530) 


def WImpact2():
    if (brick.y<tank2.y +20 and brick.y >= tank2.y -20) and (brick.x>= tank2.x and brick.x<tank2.x+18) :
       tank2.score-=1
       brick.x = random.randint(20, 730)
       brick.y = random.randint(20, 530) 


def collision():

    for bull in bullet:
        
        for tank in tanks:
            
            if (tank.x+tank.width+bull. bullet_radius > bull. bullet_x > tank.x - bull. bullet_radius ) and ((tank.y+tank.width + bull. bullet_radius > bull. bullet_y > tank.y - bull. bullet_radius)) and bull. bullet_status==True:
                CollSound.play()
                bull.bullet_color=(0,0,0)
                tank.score -= 1
                
                bull.bullet_status=False
                
                tank.x=random.randint(50,width-70)
                tank.y=random.randint(50,height-70)
            if tanks[1].score == 0:
                font1 = pygame.font.SysFont('Arial', 50)
                text = font1.render("GAME OVER! Purple tank is winner", 1, (128,0,128))
                coordinates = text.get_rect(center = (400, 300))
                screen.blit(text, coordinates)
                Over.play()
            elif tanks[0].score == 0:
                font2 = pygame.font.SysFont('Arial', 50)
                text = font2.render("GAME OVER! Yellow tank is winner!", 1, (204, 196, 0))
                coordinates = text.get_rect(center = (400, 300))
                screen.blit(text, coordinates)
                Over.play()


def score():
    score1= tanks[1].score
    score2= tanks[0].score
    res = font.render(str(score1), True, (204, 196, 0))
    res1 = font.render(str(score2), True, (128,0,128))
    screen.blit(res, (30,30))
    screen.blit(res1, (750,30))




mainloop = True
tank1 = Tank(350,350,20,(128,0,128))
tank2 = Tank(100,100,20,(204, 196, 0),pygame.K_d,pygame.K_a,pygame.K_w,pygame.K_s,pygame.K_SPACE)

bullet1=Bullet()
bullet2=Bullet()
food= Lemon()
brick = Wall()
tanks = [tank1, tank2]
bullet= [bullet1,bullet2]

while mainloop:
    
    screen.blit(backgroundImage, (0, 0))
    
    score()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                quit()
            pressed = pygame.key.get_pressed()
            for tank in tanks:
                if event.key in tank.KEY.keys():
                    tank.change_direction(tank.KEY[event.key])

                if event.key in tank.KEY.keys():
                    tank.move()
                
                if pressed[tank.KEYSHOT]:
                    BulSound.play()
                    location(tank)
        
                    
    Impact()
    Impact2()
    WImpact()
    WImpact2()
    collision()
    food.draw()
    brick.draw()
    for bull in bullet:
        bull.move()
    
    for tank in tanks:
        tank.draw() 
    tank1.move()
    tank2.move()
    

    
    pygame.display.flip()
    

pygame.quit()   
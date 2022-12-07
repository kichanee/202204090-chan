import pygame
from pygame.rect import *
import random

def restart():
    global isGameOver, score
    isGameOver = False
    score = 0
    for i in range(len(asteroid)):
        asteroid_rect[i].y = -1

    for i in range(len(alien)):
        alien_rect[i].y = -1

    for i in range(len(missile)):
        missile_rect[i].y = -1

asteroid_speed=10000
alien_speed=10000


def eventProcess():
    global running

    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            running = False  

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:  
                move.x = -1
            if event.key == pygame.K_RIGHT:  
                move.x = 1
            if event.key == pygame.K_UP:  
                move.y = -1
            if event.key == pygame.K_DOWN: 
                move.y = 1
            if event.key == pygame.K_BACKSPACE:
                restart()
            
            if event.key == pygame.K_a:
                move.x = -1
            if event.key == pygame.K_d:  
                move.x = 1
            if event.key == pygame.K_w:
                move.y = -1
            if event.key == pygame.K_s:  
                move.y = 1
                
        
            if event.key == pygame.K_LSHIFT:
                restart()
            if event.key == pygame.K_RSHIFT:
                restart()
            if event.key == pygame.K_SPACE:
                makeMissile()
            if event.key == pygame.K_j:
                makeMissile()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                move.x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                move.y = 0


def movePlayer():
    if not isGameOver:
        player_rect.x += move.x
        player_rect.y += move.y

    if player_rect.x < 0:
        player_rect.x = 0
    if player_rect.x > screen_width - player_rect.width:
        player_rect.x = screen_width - player_rect.width

    if player_rect.y < 0:
        player_rect.y = 0
    if player_rect.y > screen_height - player_rect.height:
        player_rect.y = screen_height - player_rect.height

    screen.blit(player, player_rect)

def timeDelay500ms():
    global time_delay_500ms
    if time_delay_500ms > 5:
        time_delay_500ms = 0
        return True

    time_delay_500ms += 1
    return False

def makeAsteroid():
    if isGameOver:
        return
    if timeDelay500ms():
        idex = random.randint(0, len(asteroid)-1)
        if asteroid_rect[idex].y == -1:
            asteroid_rect[idex].x = random.randint(0, screen_width)
            asteroid_rect[idex].y = 0

def makeAlien():
    if isGameOver:
        return
    if timeDelay500ms():
        idex = random.randint(0, len(alien)-1)
        if alien_rect[idex].y == -1:
            alien_rect[idex].x = random.randint(0, screen_width)
            alien_rect[idex].y = 0

def moveAsteroid():
    makeAsteroid()

    for i in range(len(asteroid)):
        if asteroid_rect[i].y == -1:
            continue

        if not isGameOver:
            asteroid_rect[i].y += 1
        if asteroid_rect[i].y > screen_height:
            asteroid_rect[i].y = 0

        screen.blit(asteroid[i], asteroid_rect[i])

def moveAlien():
    makeAlien()

    for i in range(len(alien)):
        if alien_rect[i].y == -1:
            continue

        if not isGameOver:
            alien_rect[i].y += 1
        if alien_rect[i].y > screen_height:
            alien_rect[i].y = 0

        screen.blit(alien[i], alien_rect[i])

def CheckCollisionMissile():
    global score, isGameOver

    if isGameOver:
        return

    for rec in asteroid_rect:
        if rec.y == -1:
            continue
        for recM in missile_rect:
            if rec.top < recM.bottom \
                and recM.top < rec.bottom \
                and rec.left < recM.right \
                and recM.left < rec.right:
                rec.y = -1
                recM.y = -1
                score += 10
                break

    for rec in alien_rect:
        if rec.y == -1:
            continue
        for recM in missile_rect:
            if rec.top < recM.bottom \
                and recM.top < rec.bottom \
                and rec.left < recM.right \
                and recM.left < rec.right:
                rec.y = -1
                recM.y = -1
                score += 10
                break

def makeMissile():
    if isGameOver:
        return
    for i in range(len(missile)):
        if missile_rect[i].y == -1:
            missile_rect[i].x = player_rect.x
            missile_rect[i].y = player_rect.y
            break

def moveMissile():
    for i in range(len(missile)):
        if missile_rect[i].y == -1:
            continue

        if not isGameOver:
            missile_rect[i].y -= 1
        if missile_rect[i].y < 0:
            missile_rect[i].y = -1

        screen.blit(missile[i], missile_rect[i])

def CheckCollision():
    global score, isGameOver

    if isGameOver:
        return

    for rec in asteroid_rect:
        if rec.y == -1:
            continue
        if rec.top < player_rect.bottom \
            and player_rect.top < rec.bottom \
            and rec.left < player_rect.right \
            and player_rect.left < rec.right:
            print('충돌')
            isGameOver = True
            break
    
    for rec in alien_rect:
        if rec.y == -1:
            continue
        if rec.top < player_rect.bottom \
            and player_rect.top < rec.bottom \
            and rec.left < player_rect.right \
            and player_rect.left < rec.right:
            print('충돌')
            isGameOver = True
            break

def blinking():
    global time_dealy_4sec, toggle
    time_dealy_4sec += 1
    if time_dealy_4sec > 40:
        time_dealy_4sec = 0
        toggle = ~toggle

    return toggle


def setText():
    mFont = pygame.font.SysFont("arial", 20, True, False)
    screen.blit(mFont.render(
        f'SCORE {score}', True, 'yellow'), (10, 10, 0, 0))

    if isGameOver and blinking():
        mFont = pygame.font.SysFont("arial", 100, True, False)
        screen.blit(mFont.render(
            'GAME', True, 'white'), (85, 200, 0, 0))
        mFont = pygame.font.SysFont("arial", 100, True, False)
        screen.blit(mFont.render(
            'OVER', True, 'white'), (95, 300, 0, 0))
        mFont = pygame.font.SysFont("arial", 20, True, False)
        screen.blit(mFont.render(
            'Press backspace Key Restart', True, 'white'), (145, 450, 0, 0))

running = True  
screen_width = 480
screen_height = 640
move = Rect(0, 0, 0, 0) # x, y, 가로, 세로
time_delay_500ms = 0
time_dealy_4sec = 0
toggle = False
score = 0
isGameOver = False

pygame.init()
pygame.mixer.init()



# 화면 크기 설정
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("background3.png")
background = pygame.transform.scale(background,(980,980))
pygame.display.set_caption('Annoying Ghost')

# 플레이어
player = pygame.image.load("우주선.png")
player = pygame.transform.scale(player, (80, 80))
player_rect = player.get_rect()
player_size = player.get_rect().size 
player_rect.centerx = (screen_width / 2) 
player_rect.centery = (screen_height / 2) 

# 소행성 에일리언

asteroid = [pygame.image.load("소행성.png") for i in range(20)]
asteroid_rect = [None for i in range(len(asteroid))]
for i in range(len(asteroid)):
    asteroid[i] = pygame.transform.scale(asteroid[i], (50, 50))
    asteroid_rect[i] = asteroid[i].get_rect()
    asteroid_rect[i].y = -1


alien = [pygame.image.load("외계인.png") for i in range(20)]
alien_rect = [None for i in range(len(alien))]
for i in range(len(alien)):
    alien[i] = pygame.transform.scale(alien[i], (50, 50))
    alien_rect[i] = alien[i].get_rect()
    alien_rect[i].y = -1


# 미사일
missile = [pygame.image.load("missile.png") for i in range(30)]
missile_rect = [None for i in range(len(missile))]
for i in range(len(missile)):
    missile[i] = pygame.transform.scale(missile[i], (40, 40))
    missile_rect[i] = missile[i].get_rect()
    missile_rect[i].y = -1


clock = pygame.time.Clock()

#반복 이벤트
while running:
    screen.blit(background, (0, 0)) 

    eventProcess() 
    movePlayer() 
    moveAsteroid() 
    moveAlien() 
    moveMissile() 
    CheckCollisionMissile()
    CheckCollision() 
    setText() 
    pygame.display.flip()  
    clock.tick(100) 
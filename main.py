import pygame
import random

pygame.init()


# SCREEN SETTINGS 
x = 1280
y = 720

screen = pygame.display.set_mode((x,y))
pygame.display.set_caption('Pygame Project')


# BACKGROUND CONFIG 
background = pygame.image.load('imgs/bg_0.jpg').convert_alpha()
background = pygame.transform.scale(background, (x,y))


# PLAYER // ENEMY // MISSILE CONFIG
alien1 = pygame.image.load('imgs/enemy1.png').convert_alpha()
alien1 = pygame.transform.scale(alien1, (70,70))

alien0 = pygame.image.load('imgs/enemy0.png').convert_alpha()
alien0 = pygame.transform.scale(alien0, (70,70))

player = pygame.image.load('imgs/player0.png').convert_alpha()
player = pygame.transform.scale(player, (60,60))
player = pygame.transform.rotate(player, -90)

missile = pygame.image.load('imgs/missile.png').convert_alpha()
missile = pygame.transform.scale(missile, (30,30))
missile = pygame.transform.rotate(missile, -45)


pos_alien0_x = 500
pos_alien0_y = 360

pos_alien1_x = 450
pos_alien1_y = 600

pos_player_x = 200
pos_player_y = 300

vel_missile_x = 0
pos_missile_x = 200
pos_missile_y = 300


triggered = False
working = True
points = 5


# FONT
font = pygame.font.SysFont('fonts/PixelGameFont.tft', 50)



player_rect = player.get_rect()
alien0_rect = alien0.get_rect()
alien1_rect = alien1.get_rect()
missile_rect = missile.get_rect()


# FUNCTIONS
def respawn():
    x = 1350
    y = random.randint(1,640)
    return[x,y]

def respawn_missile():
    triggered = False
    respawn_missile_x = pos_player_x
    respawn_missile_y = pos_player_y
    vel_x_missile = 0
    return [respawn_missile_x, respawn_missile_y, triggered, vel_x_missile]

def colisions():
    global points
    if player_rect.colliderect(alien0_rect) or alien0_rect.x == 60:
        points -= 1
        return True
    elif player_rect.colliderect(alien1_rect) or alien1_rect.x == 60:
        points -= 1
        return True
    elif missile_rect.colliderect(alien0_rect):
        points += 1
        return True
    elif missile_rect.colliderect(alien1_rect):
        points += 1
        return True
    else:
        return False


while working:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            working = False 
    
    screen.blit(background, (0,0))


# CHANGE BACKGROUND 
    rel_x = x % background.get_rect().width
    screen.blit(background, (rel_x - background.get_rect().width,0))
    if rel_x < 1280:
        screen.blit(background, (rel_x, 0))


# CONTROLS
    control = pygame.key.get_pressed()
    if control[pygame.K_UP] and pos_player_y > 1:
        pos_player_y -= 1
        if not triggered:
            pos_missile_y -= 1
    if control[pygame.K_DOWN] and pos_player_y < 665:
        pos_player_y += 1
        if not triggered:
            pos_missile_y += 1
    if control[pygame.K_SPACE]:
        triggered = True
        vel_missile_x =  1.6 

    if points == -1:
        working = False


# RESPAWN
    if pos_alien0_x == 50:
        pos_alien0_x = respawn()[0]
        pos_alien0_y = respawn()[1]
    if pos_alien1_x == 50 or colisions():
        pos_alien1_x = respawn()[0]
        pos_alien1_y = respawn()[1]

    if pos_missile_x == 1300:
            pos_missile_x, pos_missile_y, triggered, vel_missile_x = respawn_missile()


# RECT CONFIGS
    player_rect.y = pos_player_y
    player_rect.x = pos_player_x

    missile_rect.x = pos_missile_x
    missile_rect.y = pos_missile_y

    alien0_rect.x = pos_alien0_x
    alien0_rect.y = pos_alien0_y

    alien1_rect.x = pos_alien1_x
    alien1_rect.y = pos_alien1_y


# SPEEDS
    x -= 0.5
    pos_alien0_x -= 1
    pos_alien1_x -= 1.6
    pos_missile_x += vel_missile_x


    pygame.draw.rect(screen, (255, 0, 0), missile_rect, 4)
    pygame.draw.rect(screen, (255, 0, 0), alien0_rect, 4)
    pygame.draw.rect(screen, (255, 0, 0), alien1_rect, 4)


    score = font.render(f' Points: {int(points)}', True, (0, 0 , 0))
    score.blit(score, (50,50))


    screen.blit(alien0, (pos_alien0_x, pos_alien0_y))
    screen.blit(alien1, (pos_alien1_x, pos_alien1_y))
    screen.blit(player, (pos_player_x, pos_player_y))

    print(points)

    pygame.display.update()

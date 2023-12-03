import pygame
import random
import math
pygame.init()
fps = 60
timer = pygame.time.Clock()
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_color = (0,0,0)
apple_size = 10
carrot_size = 10
delay = 100
player_x = 0
side_to_side = 0
jumping = False
grounded = True
movement_speed = 3
jump_speed = 0
acc = 0
apple_id = 0
carrot_id = 0
time = 0
carrot_time = 0
apple_time = 0
lose_screen = False
win_screen = False
apple_count = 0
carrot_count = 0

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}
duck = []
carrots = []
apples = []
win = []
lose = []
bgs = "assets/bg.png"
player_duck = pygame.image.load("assets/duck_cropped.png")
player_duck = pygame.transform.scale (player_duck,(200,200))
apple_item = pygame.image.load("assets/apple_cropped.png")
apple_item = pygame.transform.scale (apple_item, (50,50))
carrot_item = pygame.image.load("assets/carrot_cropped.png")
carrot_item = pygame.transform.scale (carrot_item, (50,50))
win_game = pygame.image.load("assets/win_screen.png")
win_game = pygame.transform.scale(win_game, (WIDTH, HEIGHT))
lose_game = pygame.image.load("assets/lose_screen.png")
lose_game = pygame.transform.scale (lose_game, (WIDTH,HEIGHT))
player_y = HEIGHT - player_duck.get_height()
for i in range (1,1):
    bgs.append(pygame.image.load(f'assets/bgs/{i}.png'))
def spawn_apple():
    global apple_id
    w = apple_item.get_width()
    x = random.randint(0,WIDTH - w)
    y = HEIGHT - player_duck.get_height() - 90
    apples.append((time,x,y))
def spawn_carrot():
    global carrot_id
    w = carrot_item.get_width()
    x = random.randint(0,WIDTH - w)
    y = HEIGHT - player_duck.get_height() - 80
   
    carrots.append((time,x,y))
spawn_carrot()
spawn_apple()
def apple_collision():
    global carrot_count, apple_count
    player_rect = pygame.Rect(player_x, player_y, player_duck.get_width(), player_duck.get_height())
    for i in reversed (range(len(apples))):
        apple = apples [i]
        apple_rect = pygame.Rect(apple[1], apple[2], apple_item.get_width(), apple_item.get_height())
        if player_rect.colliderect(apple_rect):
            del apples [i]
            apple_count += 1
        if time> apple[0]+3000 :
            del apples [i]
    for i in reversed (range (len(carrots))):
        carrot = carrots [i]
        carrot_rect = pygame.Rect(carrot[1],carrot[2], carrot_item.get_width(), carrot_item.get_height())
        if player_rect.colliderect(carrot_rect):
            del carrots [i]
            carrot_count += 1
        if time> carrot[0]+3000:
            del carrots [i]
def draw_image(img, x, y ):
    rect = img.get_rect()
    rect.move((x, y))
    screen.blit(img,(x,y))
def draw():
    screen.fill(background_color)
    draw_image (player_duck, player_x, player_y )
    for apple in apples:
        draw_image(apple_item, apple[1],apple[2])
    for carrot in carrots:
        draw_image(carrot_item,carrot[1],carrot[2])
    if apple_count == 5:
        draw_image(win_game, 0,0)
    if carrot_count == 1:
        draw_image(lose_game, 0,0)
    player_rect = pygame.Rect(player_x, player_y, player_duck.get_width(), player_duck.get_height())
    pygame.display.flip()
def update():
    global player_x , movement_speed, grounded, player_y, acc, jumping, jump_speed, time, win_screen, lose_screen
    if apple_count == 5:
        win_screen = True
    if carrot_count == 1:
        lose_screen = True
    if win_screen or lose_screen:
        return
    player_x += side_to_side * movement_speed
    floor = HEIGHT-player_duck.get_height()
    grounded = abs(floor-player_y)<5
    player_y -= jump_speed
    jump_speed += acc
    if jumping:
        jump_speed = 10
        acc = 5
        jumping = False
    elif grounded:
        acc = 0
    acc -= .1
    if player_y > floor:
        player_y = floor
    global apple_time, carrot_time
    apple_collision()
    dt = timer.get_time()
    apple_time += dt
    time += dt
    carrot_time += dt
    if apple_time > 5000:
        apple_time = 0
        spawn_apple()
    if carrot_time > 3000:
        carrot_time = 0
        spawn_carrot()
    timer.tick(fps)

running= True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                side_to_side = -1
            if event.key == pygame.K_RIGHT:
                side_to_side = 1
            if event.key == pygame.K_UP and grounded:
                jumping = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                side_to_side = 0
            if event.key == pygame.K_RIGHT:
                side_to_side = 0
            if event.key == pygame.K_UP:
                jumping = False
                
    update()
    draw()
import pygame
from sys import exit
import random
#game variables
game_width = 360
game_height = 640

#bird class
bird_x = game_width/8
bird_y = game_height/2
bird_width = 34
bird_height = 24

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img

#pipe class
pipe_x = game_width
pipe_y = 0
pipe_width = 64
pipe_height = 512

class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False
#game images
bg_image = pygame.image.load("FLAPPY BIRD/flappybirdbg.png")
bird_img = pygame.image.load("FLAPPY BIRD/flappybird.png")
bird_img = pygame.transform.scale(bird_img,(bird_width, bird_height))
top_pipe_img = pygame.image.load("FLAPPY BIRD/toppipe.png")
top_pipe_img = pygame.transform.scale(top_pipe_img,(pipe_width,pipe_height))
bottom_pipe_img = pygame.image.load("FLAPPY BIRD/bottompipe.png")
bottom_pipe_img = pygame.transform.scale(bottom_pipe_img,(pipe_width,pipe_height))

#game logic
bird = Bird(bird_img)
pipes = []
vel_x = -2 #moves pipes to the left
vel_y = 0 #move bird up/down
gravity = 0.4
score = 0
game_over = False

def draw():
    window.blit(bg_image,(0,0))
    window.blit(bird.img, bird)

    for pipe in pipes:
        window.blit(pipe.img, pipe)

    text_str = str(int(score))
    if game_over:
        text_str = "Game Over: "+text_str

    text_font = pygame.font.SysFont("Comic Sans MS", 45)
    text_render = text_font.render(text_str, True, "white")
    window.blit(text_render,(5,0))

def move():
    global vel_y, score, game_over
    vel_y += gravity
    bird.y += vel_y
    bird.y = max(bird.y, 0)

    if bird.y>game_height:
        game_over = True
        return

    for pipe in pipes:
        pipe.x += vel_x

        if not pipe.passed and bird.x>pipe.x+pipe.width:
            score += 0.5
            pipe.passed = True

        if bird.colliderect(pipe):
            game_over = True
            return

    while len(pipes)>0 and pipes[0].x<-pipe_width:
        pipes.pop(0) #removes first element from the list

def create_pipes():
    random_pipe_y = pipe_y - pipe_height/4 - random.random()*(pipe_height/2)
    opening_space = game_height/4
    top_pipe = Pipe(top_pipe_img)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)
    bottom_pipe = Pipe(bottom_pipe_img)
    bottom_pipe.y = top_pipe.y+top_pipe.height+opening_space
    pipes.append(bottom_pipe)

    print(len(pipes))

pygame.init()
window = pygame.display.set_mode((game_width,game_height))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

create_pipes_timer = pygame.USEREVENT+0
pygame.time.set_timer(create_pipes_timer, 1500) #marks every 1.5 seconds

while True: #game loop
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

        if event.type==create_pipes_timer and not game_over:
            create_pipes()

        if event.type==pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                vel_y = -6

                #reset game
                if game_over:
                    bird.y = bird_y
                    pipes.clear()
                    score = 0
                    game_over = False
    if not game_over:
        move()
        draw()
        pygame.display.update()
        clock.tick(60) #60 fps
import pygame  #pip install pygame
import random
import os
from time import sleep

#=============================initializing game window=============================#
pygame.init()
screen_width = 600
screen_height = 500
gamewindow = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("SNAKE GAME")

pygame.mixer.init()

clock = pygame.time.Clock()
lives = 3

if(not os.path.exists("highscore.txt")):
    with open("highscore.txt", "w") as f:
        f.write("0")

def text_screen(text, color, style, size, x, y):
    font = pygame.font.SysFont(style, size)
    screen_text = font.render(text, True, color)
    gamewindow.blit(screen_text, [x,y])

def plot_snake(gamewindow, colour, snake_lst, snake_size):
    for x, y in snake_lst:
        pygame.draw.rect(gamewindow, colour, [x, y, snake_size, snake_size])

#=============================creating welcome page=============================#
def welcome():
    exit_game = False
    while not exit_game:
        gamewindow.fill((195, 108, 224))
        text_screen("Welcome to Snakes", "black", "algerian", 50, 50, 100)
        text_screen("Press Space Bar To Play", "black", "algerian", 30, 100, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("game-start.mp3")
                    pygame.mixer.music.play()
                    sleep(0.5)
                    gameloop(lives, 0, 0, 0)

        pygame.display.update()
        clock.tick(60)

def gameloop(lives, scores, f1, f2):
    #=============================initializing game variables=============================#
    exit_game = False
    over_game = False

    snake_x = 45
    snake_y = 45
    snake_size = 20
    snake_increment = 0
    snake_lst = []
    snake_length = 1

    vel_x = 0
    vel_y = 0
    vel_fact = 2

    food_x = random.randint(50, screen_width-50)
    food_y = random.randint(50, screen_height-50)

    score = scores
    f1 = f1
    f2 = f2
    fps = 60

    with open("highscore.txt", "r") as f:
        highscore = f.read()
    

    #=============================creating loop=============================#
    while not exit_game:
        if over_game == True and lives == 1:
            if f2 == 0:
                f2 = 1
                pygame.mixer.music.load("mixkit-arcade-retro-game-over.wav")
                pygame.mixer.music.play()
                sleep(0.5)
            gamewindow.fill((255,255,255))
            with open("highscore.txt", "w") as f:
                hs = f.write(highscore)
            text_screen("GAME OVER", "red", "algerian", 50, 150, 100)
            text_screen("YOUR SCORE = "+str(score), "BLUE", "algerian", 40, 130, 150)
            text_screen("HIGHEST SCORE = "+str(highscore), "BLUE", "algerian", 40, 100, 230)
            text_screen("PRESS ENTER TO CONTINUE", "red", "algerian", 35, 70, 300)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        lives = 3
                        welcome()
        
        elif over_game == True and lives > 0:
            lives = lives-1
            gameloop(lives, score, f1, f2)

        else:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    exit_game = True

                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_RIGHT:
                        vel_x = vel_fact
                        vel_y = 0

                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_LEFT:
                        vel_x = -vel_fact
                        vel_y = 0

                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_UP:
                        vel_x = 0
                        vel_y = -vel_fact

                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_DOWN:
                        vel_x = 0
                        vel_y = vel_fact

            snake_x+=vel_x
            snake_y+=vel_y

            if abs(snake_x-food_x)<15 and abs(snake_y-food_y)<15:
                score+=10
                snake_length+=20
                vel_fact+=0.25
                food_x = random.randint(50, screen_width-50)
                food_y = random.randint(50, screen_height-50)
                pygame.mixer.music.load("success-1.mp3")
                pygame.mixer.music.play()

            

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_lst.append(head)

            if len(snake_lst) > snake_length:
                del snake_lst[0]

            if head in snake_lst[0:-1]:
                over_game = True

            if score > int(highscore):
                if f1 == 0:
                    f1 = 1
                    pygame.mixer.music.load("success-fanfare-trumpets.mp3")
                    pygame.mixer.music.play()
                    sleep(0.5)
                highscore = str(score)
            
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_lst.append(head)

            if len(snake_lst) > snake_length:
                del snake_lst[0]

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                over_game = True
                pygame.mixer.music.load("negative_beeps-6008.mp3")
                pygame.mixer.music.play()

            gamewindow.fill((0,0,0))
            text_screen(f"SCORE = {score}", "green", "algerian", 20, 5, 5)
            text_screen(f"LIVES = {lives}", "green", "algerian", 20, 200, 5)
            text_screen(f"HIGH SCORE = {int(highscore)}", "green", "algerian", 20, 380, 5)
            plot_snake(gamewindow, "#808080", snake_lst, snake_size)
            pygame.draw.rect(gamewindow, "red", [food_x, food_y, snake_size, snake_size])

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()





welcome()
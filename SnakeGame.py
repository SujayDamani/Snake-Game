import pygame
from random import randint
import os

pygame.init()

#different colors 
white = (255,255, 255)
blue = (0, 0, 200)
brown = (165, 42, 42)
black=(0,0,0)


snake_size=10

#screen size
screen_width=800
screen_height=600

#board size
board_width = 700
board_height = 550


dis = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

finished = False

x1 = 300
y1 = 300

x1_change = 0
y1_change = 0

best_score=0

current_direcion=0
#if file does not exist , create one
if os.path.isfile("Best Score.txt") is False:
    f = open("Best Score.txt", "w+")
    f.close()
best_score_file = open(r"Best Score.txt", "r")
temp_best_score = best_score_file.read()


if len(temp_best_score)>0:
    best_score = int(temp_best_score)
print(temp_best_score)
best_score_file.close()


#rounding after dividing by 10 and then multiplying by 10 is done 
#beacuse we need a multiple of 10 due snakes head by size 10 and it would only move at multiple of 10
#starting from 10 for width as the boundary size is 10

#initial coordinates for first food item
cur_food_x = round(randint(10, screen_width)/10) * 10
cur_food_y = round(randint(screen_height-board_height+10, screen_height)/10) * 10

#font style to display messages
font_style = pygame.font.SysFont(None, 50)

clock = pygame.time.Clock()

#coordinates for snakes body
snake_List = []

#length of snake
Length_of_snake = 1


#drawing boundary
def draw_board(b_width,b_height, s_width, s_height):
    for w1 in range(0,s_width,10):
        pygame.draw.rect(dis, brown, [w1, s_height-b_height, snake_size, snake_size],0)
        pygame.draw.rect(dis, black, [w1, s_height-b_height, snake_size, snake_size],1)
    for h1 in range(s_height-b_height, s_height, 10):
        pygame.draw.rect(dis, brown, [0, h1, 10, 10],0)
        pygame.draw.rect(dis, black, [0, h1, 10, 10],1)
    for w2 in range(0, s_width, 10):
        pygame.draw.rect(dis, brown, [w2, s_height-10, 10, 10],0)
        pygame.draw.rect(dis, black, [w2, s_height-10, 10, 10],1)
    for h2 in range(s_height-b_height, s_height, 10):
        pygame.draw.rect(dis, brown, [screen_width-10, h2, 10, 10],0)
        pygame.draw.rect(dis, black, [screen_width-10, h2, 10, 10],1)
    
#check if food is eaten, and then just draw another food item
def is_eaten(x, y, food_x, food_y,size):
    if x==food_x and food_y==y:
        food_x = round(randint(10, screen_width-20)/10) * 10
        food_y = round(randint(screen_height-board_height+10, screen_height-20)/10) * 10
        size=size+1
        return food_x,food_y,size
    else:
        return food_x,food_y,size


#checking if player dies
def game_over(x,y,snake_body_pos):
    if y < (screen_height-board_height+10) or y>screen_height-20 or x<10 or x>screen_width-20:
        return True
    head_pos=snake_body_pos[0]
    for pos in range(1,len(snake_body_pos)):
        position=snake_body_pos[pos]
        if position[0]==head_pos[0] and position[1]==head_pos[1]:
            print(snake_body_pos)
            print(position,x,y)
            return True

    return False

#writing message after game is lost
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [screen_width/4, screen_height/3])

#display current score
def curr_score(msg,color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg,(0, 0))

#display best score 
def best_score_display(msg, color,b_score,c_score):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, (500, 0))
    if c_score>b_score:
        return c_score
    else:
        return b_score

#draw snake for each coordinates
def our_snake(snake_block, snake_body_pos):
    with_eyes=snake_body_pos[len(snake_body_pos)-1]
    for x in snake_body_pos:
        #drawing eyes
        if with_eyes==x:
            pygame.draw.rect(dis, blue, [x[0], x[1], snake_block, snake_block])
            centre = 1
            radius = 1
            circleMiddle = (x[0]+int(10/5), x[1]+5)
            circleMiddle2 = (x[0]+7, x[1]+5)
            pygame.draw.circle(dis, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(dis, (0, 0, 0), circleMiddle2, radius)
        else:    
            pygame.draw.rect(dis, blue, [x[0], x[1], snake_block, snake_block])


while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        
        if event.type == pygame.KEYDOWN:
            #the later condition in each if statements is checking if the key pressed is in reverse direction
            if event.key == pygame.K_LEFT and current_direcion!=2:
                current_direcion=4
                x1_change = -10
                y1_change = 0
            elif event.key == pygame.K_RIGHT and current_direcion!=4:
                current_direcion = 2
                x1_change = 10
                y1_change = 0
            elif event.key == pygame.K_UP and current_direcion!=3:
                current_direcion=1
                y1_change = -10
                x1_change = 0
            elif event.key == pygame.K_DOWN and current_direcion!=1:
                current_direcion = 3
                y1_change = 10
                x1_change = 0
            
            break

    x1 += x1_change
    y1 += y1_change
    dis.fill(white)
    draw_board(board_width,board_height,screen_width,screen_height)
    snake_Head = []
    snake_Head.append(x1)
    snake_Head.append(y1)
    snake_List.append(snake_Head)
    if len(snake_List) > Length_of_snake:
            del snake_List[0]
    our_snake(snake_size, snake_List)
    cur_food_x,cur_food_y,Length_of_snake=is_eaten(x1,y1,cur_food_x,cur_food_y,Length_of_snake)
    pygame.draw.rect(dis, (0, 0, 0), [cur_food_x, cur_food_y, snake_size, snake_size])
    curr_score("Current Score :{}".format(Length_of_snake), blue)
    best_score=best_score_display("Best Score :{}".format(best_score), blue, best_score, Length_of_snake)
    if game_over(x1,y1,snake_List):
        finished=True
        clock.tick(30)
    pygame.display.update()
    clock.tick(10)

#writing best score in file
best_score_file = open(r"Best Score.txt", "w")
best_score_file.write(str(best_score))
best_score_file.close()
dis.fill(white)
message("You lost", blue)
pygame.display.update()
clock.tick(2)
pygame.quit()
quit()

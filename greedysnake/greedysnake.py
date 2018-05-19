#!/usr/bin/env python
import pygame 
from pygame.locals import *
from sys import exit
import time
import random
from settings import *

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
pygame.display.set_caption(SCREEN_CAPTION)
font = pygame.font.SysFont("arial", 40)



class SNAKE(object):
    def __init__(self):
	self.name = 'greedysnake'
	self.bodys = [[BIRTH_POS-3,BIRTH_POS],
		     [BIRTH_POS-2,BIRTH_POS],
		     [BIRTH_POS-1,BIRTH_POS],
		     [BIRTH_POS,BIRTH_POS]
		    ]
	self.bulk = len(self.bodys)
	self.velocity = int(4)                 #chang 10 to adjust velocity
	self.direction = DIRECTIONS['right'] 
	self.body_font = font.render('o',True,SNAKE_COLOR)
	self.barrier_font = font.render('o',True,BARRIER_COLOR)
	self.barrierPos = None
	self.score = 0


    def moveAndEat(self):
	if self.direction == DIRECTIONS['left']:
	    head_pos = [self.bodys[-1][0]-1,self.bodys[-1][1]]
	if self.direction == DIRECTIONS['right']:
	    head_pos = [self.bodys[-1][0]+1,self.bodys[-1][1]]
	if self.direction == DIRECTIONS['up']:
	    head_pos = [self.bodys[-1][0],self.bodys[-1][1]-1]
	if self.direction == DIRECTIONS['down']:
	    head_pos = [self.bodys[-1][0],self.bodys[-1][1]+1]
	self.bodys.append(head_pos)
	if self.barrierPos == head_pos: 
	    self.score += 1
	    self.createBarrier()
	else:
	    del self.bodys[0]	
	self.is_over()
	screen.blit(self.barrier_font,virt2real(self.barrierPos))
	for body in self.bodys:
	    temp_pos = virt2real(body)
	    screen.blit(self.body_font,temp_pos)
	self.drawScoreBoard()	

    def drawScoreBoard(self):
	headPos_font = font.render(str(self.bodys[-1]),True,(0,255,0))
	score_font = font.render('score:'+str(self.score),True,(0,255,0))
	screen.blit(headPos_font,SNAKEPOS_COORDINATE)
	screen.blit(score_font,SCORE_COORDINATE)
	

    def is_over(self):
	x,y = self.bodys[-1]
	if x<0 or x>SPOTGRIDNUM or y<0 or y>SPOTGRIDNUM:
	    exit() 
	if self.bodys[-1] in self.bodys[:-1]:
	    exit()
    
    def createBarrier(self):	
	while True:
	    x , y = random.randint(0,SPOTGRIDNUM),random.randint(0,SPOTGRIDNUM)
	    if [x,y] in self.bodys:
		continue	
	    else:
		self.barrierPos = [x,y]
		break
def virt2real(coordinate):
    return (coordinate[0]*SNAKEWIDTH+30,coordinate[1]*SNAKEHEIGHT+30)

def drawSpot():
    pygame.draw.rect(screen,SPOTLINE_COLOR,Rect(SPOTSTART_POS,SPOTEND_POS),SPOTNOTFILL)

def main():
    snake = SNAKE()
    count = 0
    snake.createBarrier()
    while True:
	for event in pygame.event.get():
	    if event.type == QUIT:
		exit()

	pressed_keys = pygame.key.get_pressed()
	if pressed_keys[K_w]:
	    if snake.direction != DIRECTIONS['down']:
		snake.direction = DIRECTIONS['up']
	if pressed_keys[K_s]:
	    if snake.direction != DIRECTIONS['up']:
		snake.direction = DIRECTIONS['down']
	if pressed_keys[K_a]:
	    if snake.direction != DIRECTIONS['right']:
		snake.direction = DIRECTIONS['left']
	if pressed_keys[K_d]:
	    if snake.direction != DIRECTIONS['left']:
		snake.direction = DIRECTIONS['right']
	if pressed_keys[K_q]:
	    exit()

	if count%snake.velocity == 0:
	    screen.fill(BACKGROUND_COLOR)
	    drawSpot()
	    snake.moveAndEat()
	    pygame.display.update()
	    count = 0
	time.sleep(0.01)
	count += 1
    print snake.score
	
    
if __name__=="__main__":
    main()

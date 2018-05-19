#!/usr/bin/env python
import pygame
from pygame.locals import *
from sys import exit
import random

SCREEN_SIZE = (640,480)
stringList = []

class character(object):
    def __init__(self):
	self.name = chr(random.randint(65,122))
	self.ch_size = 20
	self.pos_column = random.randrange(0,640,self.ch_size)
	self.pos_row = -20
	self.velocity = 2
	self.font = pygame.font.SysFont("arial", self.ch_size)
	self.specialColor = random.randint(0,10)
	if random.randint(0,20)==1:
	    self.text = self.font.render(self.name,True,(255,255,125))
	else:
	    self.text = self.font.render(self.name,True,(0,255,0))

    def move(self):
	self.pos_row += self.velocity

def make_string():
    for ch in stringList:
	ch.move()
	if ch.pos_row > 480:
	    stringList.remove(ch)
    temp_character = character()
    for ch in stringList:
	if ch.pos_column==temp_character.pos_column and ch.pos_row<ch.ch_size:
	    break
    else:
	stringList.append(temp_character) 
    
def coderain():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
    pygame.display.set_caption('coderain')
    make_string()
    
    while True:
	for event in pygame.event.get():
	    if event.type == QUIT:
		exit()
	make_string()
	screen.fill((0,0,0))
	for ch in stringList:
	    screen.blit(ch.text,(ch.pos_column,ch.pos_row))
	pygame.display.update()
    
    

if __name__=="__main__":
    coderain()

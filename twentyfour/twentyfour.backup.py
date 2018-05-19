#!/usr/bin/env python
import pygame
from pygame.locals import *
from sys import exit
import random
import time
from settings import *

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
pygame.display.set_caption(SCREEN_CAPTION)
font = pygame.font.SysFont(NUMBER_FONT, NUMBER_SIZE)
flag = 0


class QUESTION(object):
    def __init__(self):
	self.seriesNum = [random.choice(NUMBER_DICTIONARY.keys()) for i in range(4)]
	self.symbols = [None for i in range(3)]
	self.selectedItems = [None for i in range (2)]
	self.arithmetic = None
	self.__makeArithmetic()
	self.HEAD = 0
	self.answer = 24
	self.isWin = 0
	self.groupOne = []
	self.groupTwo = []

    def __makeArithmetic(self):
	self.arithmetic = self.seriesNum
	for i,symbol in enumerate(self.symbols):
	    self.arithmetic.insert(i*2+1,symbol)

    def drawAllElements(self):
	self.__drawPlaceHolder()
	self.__drawNumbersAndSymbols()
	self.__drawSelectedBox()
	self.__drawWinSignal()
    def __drawWinSignal(self):
	if self.isWin == 1:
	    winFont = font.render(WIN_TEXT,True,NUMBER_COLOR)
	    screen.blit(winFont,WINPOS)
	else:
	    pass

    def __drawNumbersAndSymbols(self):
	for i,item in enumerate(self.arithmetic):
	    if i%2==0:
		numFont = font.render(item,True,NUMBER_COLOR)
		screen.blit(numFont,ARITHMETIC_POS[i])
	    else:
		if item is not None:
		    symbolFont = font.render(item,True,SYMBOL_COLOR)
		    screen.blit(symbolFont,ARITHMETIC_POS[i])
    def addSymbol(self,symbol):
	if self.HEAD%2 == 1:
	    self.arithmetic[self.HEAD] = symbol
	    
	    	
    def groupPlaceholder(num):
	if num == GROUPONE:
	    placeHolder = self.arithmetic[self.HEAD]
	    if placeHolder is not None:
		self.groupOne.append(self.HEAD)
	if num == GROUPTWO:
	    placeHolder = self.arithmetic[self.HEAD]
	    if placeHolder is not None:
		self.groupTwo.append(self.HEAD)
		
    def selectPlaceholder(self):
	if self.HEAD%2 == 0:
	    placeHolder = self.arithmetic[self.HEAD]
	    if placeHolder is not None:
		if self.selectedItems.count(None) >=2:
		    self.selectedItems[0] = self.HEAD
		else:
		    self.selectedItems[1] = self.HEAD
		    self.changeSelectItems()
		    self.selectedItems = [None for i in range (2)]

    def __drawPlaceHolder(self):
	startPos = ARITHMETIC_POS[self.HEAD]
	pygame.draw.rect(screen,SELECTBOX_COLOR,Rect(startPos,SELECTBOX_SIZE),BOXNOTFILL)
	

    def __drawSelectedBox(self):
	for item in self.selectedItems:
	    if item is not None:
		startPos = ARITHMETIC_POS[item]
		pygame.draw.rect(screen,SELECTEDBOX_COLOR,Rect(startPos,SELECTBOX_SIZE),BOXNOTFILL)
	
    def __getEndPos(self,startPos):               #no use
	return (startPos[0]+SELECTBOX_WIDTH,startPos[1]+SELECTBOX_HEIGHT)


    def movePlaceHolder(self):
	if self.HEAD >= len(self.arithmetic)-1:
	    self.HEAD = 0
	else:
	    self.HEAD += 1

    def changeSelectItems(self):
	self.arithmetic[self.selectedItems[0]],self.arithmetic[self.selectedItems[1]] = self.arithmetic[self.selectedItems[1]],self.arithmetic[self.selectedItems[0]] 
	    
	
    def solute(self):
	global flag
	if self.arithmetic.count(None) == 0:
	    
	    self.arithmetic.insert(0,'+')
	    x = 0
	    for i in range(4):
		x = eval('x' + self.arithmetic[i*2] + str(NUMBER_DICTIONARY[self.arithmetic[i*2+1]]))
	    del self.arithmetic[0]
	    if x == self.answer:
		self.isWin = 1
		flag = 1
	    
	

def keyDetect(question):
    global flag
    for event in pygame.event.get():
	if event.type == QUIT:
	    exit()
	if event.type == KEYDOWN:
	    if event.key == K_q:
		exit()
	    if event.key == K_r:
		flag = 2
	    if event.key == K_a:
		question.solute()
	    if event.key == K_SPACE:
		question.movePlaceHolder()
	    if event.key == K_RETURN:
		question.selectPlaceholder()
	    if event.key == K_1:
		question.groupPlaceholder(GROUPONE)
	    if event.key == K_2:
		question.groupPlaceholder(GROUPTWO)
	    if event.key in SYMBOL_DICTIONARY.keys():
		question.addSymbol(SYMBOL_DICTIONARY[event.key])
    
    


def twentyFour(question):
    global flag
    while True:
	if flag == 0:
	    keyDetect(question)
	    screen.fill(BACKGROUND_COLOR)

	    question.drawAllElements()

	    pygame.display.update()
	    time.sleep(DELAY_TIME)
	else:
	    return 0 

if __name__=="__main__":
    while True:
	for event in pygame.event.get():
	    if event.type == KEYDOWN:
		if event.key == K_RETURN:
		    flag = 0
	if flag == 2:
	    flag = 0
	if flag == 0:
	    twentyFour(QUESTION())
	time.sleep(0.1)

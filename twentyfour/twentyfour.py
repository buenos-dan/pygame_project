#!/usr/bin/env python
import pygame
from pygame.locals import *
from sys import exit
import itertools
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
	self.arithmetic = []
	self.__makeArithmetic()
	self.HEAD = 0
	self.answer = 24.0
	self.isWin = 0
	self.groupOne = []
	self.groupTwo = []
	self.solution = []
	self.answer = []
	self.__AI()

    def __AI(self):
	seq = ['' for i in range(15)]
	num = [1,5,9,13]
	sym = [3,7,11]
	symbol = ['+','-','*','/']
	symbols = []
	leftbracket = [0,4,8,12]
	rightbracket = [2,6,10,14]
        series = list(itertools.permutations(self.seriesNum,len(self.seriesNum)))
	for i in symbol:
	    for j in symbol:
		for k in symbol:
		    symbols.append([i,j,k])
	for ser in series:
	    for i,p in enumerate(num):
		seq[p] = ser[i]	
	    for sy in symbols:
		for i,p in enumerate(sym):
		    seq[p] = sy[i]
		for q in leftbracket:
		    seq[q] = '(' 
		    for p in rightbracket:
			seq[p] = ')'
			yes = ''
			for i in seq:
			    if i in NUMBER_DICTIONARY.keys():
				i = str(NUMBER_DICTIONARY[i])
			    yes += i
			try:
			    x = eval(yes)
			    if x == 24.0:
				self.answer.append(yes)
			except:	
			    pass
			seq[p] = ''
		    seq[q] = ''
	for ser in series:
	    for i,p in enumerate(num):
		seq[p] = ser[i]	
	    for sy in symbols:
		for i,p in enumerate(sym):
		    seq[p] = sy[i]
		seq[0] = '(' 
		seq[8] = '(' 
		seq[6] = ')'
		seq[14] = ')'
		yes = ''
		for i in seq:
		    if i in NUMBER_DICTIONARY.keys():
			i = str(NUMBER_DICTIONARY[i])
		    yes += i
		try:
		    x = eval(yes)
		    if x == 24.0:
			self.answer.append(yes)
		except:	
		    pass
		seq[0] = '' 
		seq[8] = '' 
		seq[6] = ''
		seq[14] = ''
    
	
			
	

    def __makeArithmetic(self):
	self.arithmetic = self.seriesNum[:]
	for i,symbol in enumerate(self.symbols):
	    self.arithmetic.insert(i*2+1,symbol)

    def drawAllElements(self):
	self.__drawGroupBox()
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
	    
	    	
    def groupPlaceholder(self,num):
	if num == GROUPONE:
	    if self.HEAD in self.groupOne:
		self.groupOne.remove(self.HEAD)
	    else:
		placeHolder = self.arithmetic[self.HEAD]
		if placeHolder is not None:
		    self.groupOne.append(self.HEAD)
	if num == GROUPTWO:
	    if self.HEAD in self.groupTwo:
		self.groupTwo.remove(self.HEAD)
	    else:
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
	

    def __drawGroupBox(self):
	for item in self.groupOne:
	    startPos = ARITHMETIC_POS[item]
	    pygame.draw.rect(screen,GROUPONEBOX_COLOR,Rect(startPos,SELECTBOX_SIZE),BOXISFILL)
	for item in self.groupTwo:
	    startPos = ARITHMETIC_POS[item]
	    pygame.draw.rect(screen,GROUPTWOBOX_COLOR,Rect(startPos,SELECTBOX_SIZE),BOXISFILL)

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
	    for i in self.arithmetic:
		self.solution.append(i) 
	    if len(self.groupOne) != 0:
		self.groupOne.sort()
		self.solution.insert(self.groupOne[0],'(')
		self.solution.insert(self.groupOne[-1]+2,')')
		if len(self.groupTwo) != 0:
		    self.groupTwo.sort()
		    self.solution.insert(self.groupTwo[0]+2,'(')
		    self.solution.insert(self.groupTwo[-1]+4,')')
	    else:
		if len(self.groupTwo) != 0:
		    self.groupTwo.sort()
		    self.solution.insert(self.groupTwo[0],'(')
		    self.solution.insert(self.groupTwo[-1]+2,')')
	    x = ''
	    for i in self.solution:
		if i in NUMBER_DICTIONARY.keys():
		    i = str(NUMBER_DICTIONARY[i])
		x += i
	    ii = eval(x)
	    if ii == 24.0:
		self.isWin = 1
		flag = 1
	self.solution = []
	    
	

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
	    if event.key == K_u:
		print "\n"*4
		print question.answer
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

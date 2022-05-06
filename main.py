'''
Programmed by Alexander Kung
'''

import sys
import pygame
import random
import copy
import math
from piece import piece
pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 800,800
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('AI Chess')

WHITE = (255,255,255)
DARKGREEN = (119, 149, 86)
LIGHTGREEN = (235, 236, 208)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
SILVER = (192,192,192)
DARKGREY = 	(100,100,100)
BEIGE = (217,179,130)
DARKERGREEN = (1,49,31)

DARKSQUARE = DARKGREEN
LIGHTSQUARE = LIGHTGREEN

# AIMovesChecked = 0

whitePawn = pygame.image.load('white-pawn.png')
whiteRook = pygame.image.load('white-rook.png')
whiteKnight = pygame.image.load('white-knight.png')
whiteBishop = pygame.image.load('white-bishop.png')
whiteQueen = pygame.image.load('white-queen.png')
whiteKing = pygame.image.load('white-king.png')

blackBishop = pygame.image.load('black-bishop.png')
blackKing = pygame.image.load('black-king.png')
blackKnight = pygame.image.load('black-knight.png')
blackPawn = pygame.image.load('black-pawn.png')
blackQueen = pygame.image.load('black-queen.png')
blackRook = pygame.image.load('black-rook.png')

whitePawn = pygame.transform.scale(whitePawn, (100, 100))
whiteRook = pygame.transform.scale(whiteRook, (100, 100))
whiteKnight = pygame.transform.scale(whiteKnight, (100, 100))
whiteBishop = pygame.transform.scale(whiteBishop, (100, 100))
whiteQueen = pygame.transform.scale(whiteQueen, (100, 100))
whiteKing = pygame.transform.scale(whiteKing, (100, 100))

blackPawn = pygame.transform.scale(blackPawn, (100, 100))
blackRook = pygame.transform.scale(blackRook, (100, 100))
blackKnight = pygame.transform.scale(blackKnight, (100, 100))
blackBishop = pygame.transform.scale(blackBishop, (100, 100))
blackQueen = pygame.transform.scale(blackQueen, (100, 100))
blackKing = pygame.transform.scale(blackKing, (100, 100))

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None,passedValue=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(int(x),int(y),int(w),int(h)))

        if click[0] == 1 and action != None:
            if passedValue == None:
                action()
            else:
                action(passedValue) 
    else:
        pygame.draw.rect(screen, ic,(int(x),int(y),int(w),int(h)))

    smallText = pygame.font.SysFont("arial",30)
    textSurf, textRect = text_objects(msg, smallText, WHITE)
    textRect.center = ( (int(x+(w/2))), int((y+(h/2))) )
    screen.blit(textSurf, textRect)


def pieceDraw(name, x, y):
    if name == -1:
        screen.blit(blackPawn, (x*100,y*100))
    elif name == -6:
        screen.blit(blackKing, (x*100,y*100))
    elif name == -5:
        screen.blit(blackQueen, (x*100,y*100))
    elif name == -4:
        screen.blit(blackRook, (x*100,y*100))
    elif name == -2:
        screen.blit(blackKnight, (x*100,y*100))
    elif name == -3:
        screen.blit(blackBishop, (x*100,y*100))
    
    elif name == 1:
        screen.blit(whitePawn, (x*100,y*100))
    elif name == 6:
        screen.blit(whiteKing, (x*100,y*100))
    elif name == 5:
        screen.blit(whiteQueen, (x*100,y*100))
    elif name == 4:
        screen.blit(whiteRook, (x*100,y*100))
    elif name == 2:
        screen.blit(whiteKnight, (x*100,y*100))
    elif name == 3:
        screen.blit(whiteBishop, (x*100,y*100))


def scoreCalcBasic(board):
    currentScore = 0

    for i in board:
        for j in i:
            if j and j.name > 0:
                if abs(j.name) == 1:
                    currentScore += 1
                if abs(j.name) == 2:
                    currentScore += 3
                if abs(j.name) == 3:
                    currentScore += 3
                if abs(j.name) == 4:
                    currentScore += 5
                if abs(j.name) == 5:
                    currentScore += 9
            if j and j.name < 0:
                if abs(j.name) == 1:
                    currentScore -= 1
                if abs(j.name) == 2:
                    currentScore -= 3
                if abs(j.name) == 3:
                    currentScore -= 3
                if abs(j.name) == 4:
                    currentScore -= 5
                if abs(j.name) == 5:
                    currentScore -= 9
    return currentScore

def scoreCalcMiddleRush(board):
    currentScore = 0

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] and board[i][j].name > 0:
                distanceFromCenter = math.sqrt(((i-4.5)**2) + ((j-4.5)**2))
                if abs(board[i][j].name) == 1:
                    currentScore += 4
                    currentScore += ((6-round(distanceFromCenter))/30)
                if abs(board[i][j].name) == 2:
                    currentScore += 12
                    currentScore += ((6-round(distanceFromCenter))/30)
                if abs(board[i][j].name) == 3:
                    currentScore += 12
                    currentScore += ((6-round(distanceFromCenter))/30)
                if abs(board[i][j].name) == 4:
                    currentScore += 20
                    currentScore += ((6-round(distanceFromCenter))/30)
                if abs(board[i][j].name) == 5:
                    currentScore += 32
                    currentScore += ((6-round(distanceFromCenter))/30)
            if board[i][j] and board[i][j].name < 0:
                distanceFromCenter = math.sqrt(((i-4.5)**2) + ((j-4.5)**2))
                if abs(board[i][j].name) == 1:
                    currentScore -= 4
                    currentScore -= ((6-round(distanceFromCenter))/30)
                if abs(board[i][j].name) == 2:
                    currentScore -= 12
                    currentScore -= ((6-round(distanceFromCenter))/30)
                if abs(board[i][j].name) == 3:
                    currentScore -= 12
                    currentScore -= ((6-round(distanceFromCenter))/30)
                if abs(board[i][j].name) == 4:
                    currentScore -= 20
                    currentScore -= ((6-round(distanceFromCenter))/30)
                if abs(board[i][j].name) == 5:
                    currentScore -= 32
                    currentScore -= ((6-round(distanceFromCenter))/30)
    return currentScore


def scoreCalc(board):
    return scoreCalcMiddleRush(board)


def AI(board, turn, movesMade, depth, alpha, beta):
    #Minimax AI that beats you
    #White maximizing, Black minimizing
    # global AIMovesChecked

    checkmateCheckData1 = checkmateCheck(board, 1, movesMade)
    checkmateCheckData2 = checkmateCheck(board, -1, movesMade)

    if checkmateCheckData1 == 1:
        #Black Wins
        return [float('-inf'), board]
    if checkmateCheckData2 == -1:
        #White Wins
        return [float('inf'), board]

    if depth == 0:
        return [scoreCalc(board), board]

    if turn == 1:
        #Maximizing White
        maxScore = float('-inf')
        maxBoard = copy.deepcopy(board)

        breakAll = False
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] and board[i][j].name > 0:
                    #Is White Piece
                    possibleMoves = findMoves(board, board[i][j].name, i, j, movesMade)
                    if board[i][j].name == 6:
                        possibleMoves[:] = killRestrict(board, board[i][j].name, i, j, possibleMoves, movesMade)
                    possibleMoves[:] = checkRestrict(board, board[i][j].name, [i,j],possibleMoves, movesMade)

                    for move in possibleMoves:
                        #Duplicate board and do possible move 'a'
                        tempBoard = copy.deepcopy(board)

                        makeMove(tempBoard,[i,j], move, movesMade)

                        score = AI(tempBoard, turn*-1, movesMade+1, depth-1, alpha, beta)[0]

                        previousMaxScore = maxScore
                        maxScore = max(score, maxScore)
                        # AIMovesChecked += 1

                        if maxScore != previousMaxScore:
                            maxBoard = copy.deepcopy(tempBoard)
                        
                        alpha = max(alpha, score)

                        if beta <= alpha:
                            breakAll = True
                            break
                if breakAll:
                    break
            if breakAll:
                break
        return [maxScore, maxBoard]   

    if turn == -1:
        #Minimizing Black
        minScore = float('inf')
        minBoard = copy.deepcopy(board)

        breakAll = False
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] and board[i][j].name < 0:
                    #Is White Piece
                    possibleMoves = findMoves(board, board[i][j].name, i, j, movesMade)
                    if board[i][j].name == 6:
                        possibleMoves[:] = killRestrict(board, board[i][j].name, i, j, possibleMoves, movesMade)
                    possibleMoves[:] = checkRestrict(board, board[i][j].name, [i,j],possibleMoves, movesMade)

                    for move in possibleMoves:
                        #Duplicate board and do possible move 'a'
                        tempBoard = copy.deepcopy(board)

                        makeMove(tempBoard,[i,j], move, movesMade)


                        score = AI(tempBoard, turn*-1, movesMade+1, depth-1, alpha, beta)[0]

                        previousMinScore = minScore
                        minScore = min(score, minScore)
                        # AIMovesChecked += 1

                        if minScore != previousMinScore:
                            minBoard = copy.deepcopy(tempBoard)
                        
                        beta = min(beta, score)

                        if beta <= alpha:
                            breakAll = True
                            break
                if breakAll:
                    break
            if breakAll:
                break
        return [minScore, minBoard]    







def findMoves(board, name, x, y, movesMade):
    possibleMoves = [] #x, y, Kill
    color = 0
    if name > 0:
        color = 1
    if name < 0:
        color = -1

    if name == 1:
        #White Pawn
        if y == 6:
            if x in range(0,8) and y-2 in range(0,8):
                if not board[x][y-2] and not board[x][y-1]:
                    possibleMoves.append([x,y-2,False])
            if x in range(0,8) and y-1 in range(0,8):
                if not board[x][y-1]:
                    possibleMoves.append([x,y-1,False])
            if x-1 in range(0,8) and y-1 in range(0,8):
                if board[x-1][y-1] and board[x-1][y-1].name < 0:
                    possibleMoves.append([x-1,y-1,True])
            if x+1 in range(0,8) and y-1 in range(0,8):
                if board[x+1][y-1] and board[x+1][y-1].name < 0:
                    possibleMoves.append([x+1,y-1,True])
        else:
            if x in range(0,8) and y-1 in range(0,8):
                if not board[x][y-1]:
                    possibleMoves.append([x,y-1,False])
            if x-1 in range(0,8) and y-1 in range(0,8):
                if board[x-1][y-1] and board[x-1][y-1].name < 0:
                    possibleMoves.append([x-1,y-1,True])
            if x+1 in range(0,8) and y-1 in range(0,8):
                if board[x+1][y-1] and board[x+1][y-1].name < 0:
                    possibleMoves.append([x+1,y-1,True])
        if y == 3:
            #En Passant
            #print(movesMade)
            if x-1 in range(0,8):
                if board[x-1][y] and board[x-1][y].lastMoved == movesMade-1 and abs(board[x-1][y].name) == 1:
                    possibleMoves.append([x-1,y-1,True,'p'])
            if x+1 in range(0,8):
                if board[x+1][y] and board[x+1][y].lastMoved == movesMade-1 and abs(board[x+1][y].name) == 1:
                    possibleMoves.append([x+1,y-1,True,'p'])
        

    elif name == -1:
        if y == 1:
            if x in range(0,8) and y+2 in range(0,8):
                if not board[x][y+2] and not board[x][y+1]:
                    possibleMoves.append([x,y+2,False])
            if x in range(0,8) and y+1 in range(0,8):
                if not board[x][y+1]:
                    possibleMoves.append([x,y+1,False])
            if x-1 in range(0,8) and y+1 in range(0,8):
                if board[x-1][y+1] and board[x-1][y+1].name > 0:
                    possibleMoves.append([x-1,y+1,True])
            if x+1 in range(0,8) and y+1 in range(0,8):
                if board[x+1][y+1] and board[x+1][y+1].name > 0:
                    possibleMoves.append([x+1,y+1,True])
        else:
            if x in range(0,8) and y+1 in range(0,8):
                if not board[x][y+1]:
                    possibleMoves.append([x,y+1,False])
            if x-1 in range(0,8) and y+1 in range(0,8):
                if board[x-1][y+1] and board[x-1][y+1].name > 0:
                    possibleMoves.append([x-1,y+1,True])
            if x+1 in range(0,8) and y+1 in range(0,8):
                if board[x+1][y+1] and board[x+1][y+1].name > 0:
                    possibleMoves.append([x+1,y+1,True])
        
        if y == 4:
            #En Passant
            if x-1 in range(0,8):
                if board[x-1][y] and board[x-1][y].lastMoved == movesMade-1 and abs(board[x-1][y].name) == 1:
                    possibleMoves.append([x-1,y+1,True,'p'])
            if x+1 in range(0,8):
                if board[x+1][y] and board[x+1][y].lastMoved == movesMade-1 and abs(board[x+1][y].name) == 1:
                    possibleMoves.append([x+1,y+1,True,'p'])

    elif abs(name) == 2:
        #Knight
        if x+2 in range(0,8) and y+1 in range(0,8):
            if not board[x+2][y+1]:
                possibleMoves.append([x+2,y+1,False])
            elif board[x+2][y+1] and ((board[x+2][y+1].name > 0 and color < 0) or (board[x+2][y+1].name < 0 and color > 0)):
                possibleMoves.append([x+2,y+1,True])
        if x+2 in range(0,8) and y-1 in range(0,8):
            if not board[x+2][y-1]:
                possibleMoves.append([x+2,y-1,False])
            elif board[x+2][y-1] and ((board[x+2][y-1].name > 0 and color < 0) or (board[x+2][y-1].name < 0 and color > 0)):
                possibleMoves.append([x+2,y-1,True])
        if x-2 in range(0,8) and y+1 in range(0,8):
            if not board[x-2][y+1]:
                possibleMoves.append([x-2,y+1,False])
            elif board[x-2][y+1] and ((board[x-2][y+1].name > 0 and color < 0) or (board[x-2][y+1].name < 0 and color > 0)):
                possibleMoves.append([x-2,y+1,True])
        if x-2 in range(0,8) and y-1 in range(0,8):
            if not board[x-2][y-1]:
                possibleMoves.append([x-2,y-1,False])
            elif board[x-2][y-1] and ((board[x-2][y-1].name > 0 and color < 0) or (board[x-2][y-1].name < 0 and color > 0)):
                possibleMoves.append([x-2,y-1,True])
        if x+1 in range(0,8) and y-2 in range(0,8):
            if not board[x+1][y-2]:
                possibleMoves.append([x+1,y-2,False])
            elif board[x+1][y-2] and ((board[x+1][y-2].name > 0 and color < 0) or (board[x+1][y-2].name < 0 and color > 0)):
                possibleMoves.append([x+1,y-2,True])
        if x+1 in range(0,8) and y+2 in range(0,8):
            if not board[x+1][y+2]:
                possibleMoves.append([x+1,y+2,False])
            elif board[x+1][y+2] and((board[x+1][y+2].name > 0 and color < 0) or (board[x+1][y+2].name < 0 and color > 0)):
                possibleMoves.append([x+1,y+2,True])
        if x-1 in range(0,8) and y+2 in range(0,8):
            if not board[x-1][y+2]:
                possibleMoves.append([x-1,y+2,False])
            elif board[x-1][y+2] and ((board[x-1][y+2].name > 0 and color < 0) or (board[x-1][y+2].name < 0 and color > 0)):
                possibleMoves.append([x-1,y+2,True])
        if x-1 in range(0,8) and y-2 in range(0,8):
            if not board[x-1][y-2]:
                possibleMoves.append([x-1,y-2,False])
            elif board[x-1][y-2] and ((board[x-1][y-2].name > 0 and color < 0) or (board[x-1][y-2].name < 0 and color > 0)):
                possibleMoves.append([x-1,y-2,True])
    
    elif abs(name) == 5:
        #Queen
        blocked = [False,False,False,False,False,False,False,False]
        for i in range(1,8):
            if x+i in range(0,8) and blocked[0] == False:
                if not board[x+i][y]:
                    possibleMoves.append([x+i,y,False])
                elif board[x+i][y] and ((board[x+i][y].name > 0 and color < 0) or (board[x+i][y].name < 0 and color > 0)):
                    possibleMoves.append([x+i,y,True])
                    blocked[0] = True
                else:
                    blocked[0] = True
            if x-i in range(0,8) and blocked[1] == False:
                if not board[x-i][y]:
                    possibleMoves.append([x-i,y,False])
                elif board[x-i][y] and ((board[x-i][y].name > 0 and color < 0) or (board[x-i][y].name < 0 and color > 0)):
                    possibleMoves.append([x-i,y,True])
                    blocked[1] = True
                else:
                    blocked[1] = True
            if y+i in range(0,8) and blocked[2] == False:
                if not board[x][y+i]:
                    possibleMoves.append([x,y+i,False])
                elif board[x][y+i] and ((board[x][y+i].name > 0 and color < 0) or (board[x][y+i].name < 0 and color > 0)):
                    possibleMoves.append([x,y+i,True])
                    blocked[2] = True
                else:
                    blocked[2] = True
            if y-i in range(0,8) and blocked[3] == False:
                if not board[x][y-i]:
                    possibleMoves.append([x,y-i,False])
                elif board[x][y-i] and ((board[x][y-i].name > 0 and color < 0) or (board[x][y-i].name < 0 and color > 0)):
                    possibleMoves.append([x,y-i,True])
                    blocked[3] = True
                else:
                    blocked[3] = True
            if x-i in range(0,8) and y-i in range(0,8) and blocked[4] == False:
                if not board[x-i][y-i]:
                    possibleMoves.append([x-i,y-i,False])
                elif board[x-i][y-i] and ((board[x-i][y-i].name > 0 and color < 0) or (board[x-i][y-i].name < 0 and color > 0)):
                    possibleMoves.append([x-i,y-i,True])
                    blocked[4] = True
                else:
                    blocked[4] = True
            if x+i in range(0,8) and y+i in range(0,8) and blocked[5] == False:
                if not board[x+i][y+i]:
                    possibleMoves.append([x+i,y+i,False])
                elif board[x+i][y+i] and ((board[x+i][y+i].name > 0 and color < 0) or (board[x+i][y+i].name < 0 and color > 0)):
                    possibleMoves.append([x+i,y+i,True])
                    blocked[5] = True
                else:
                    blocked[5] = True
            if x-i in range(0,8) and y+i in range(0,8) and blocked[6] == False:
                if not board[x-i][y+i]:
                    possibleMoves.append([x-i,y+i,False])
                elif board[x-i][y+i] and ((board[x-i][y+i].name > 0 and color < 0) or (board[x-i][y+i].name < 0 and color > 0)):
                    possibleMoves.append([x-i,y+i,True])
                    blocked[6] = True
                else:
                    blocked[6] = True
            if x+i in range(0,8) and y-i in range(0,8) and blocked[7] == False:
                if not board[x+i][y-i]:
                    possibleMoves.append([x+i,y-i,False])
                elif board[x+i][y-i] and ((board[x+i][y-i].name > 0 and color < 0) or (board[x+i][y-i].name < 0 and color > 0)):
                    possibleMoves.append([x+i,y-i,True])
                    blocked[7] = True
                else:
                    blocked[7] = True


    elif abs(name) == 4:
        #Rook
        blocked = [False,False,False,False]
        for i in range(1,8):
            if x+i in range(0,8) and blocked[0] == False:
                if not board[x+i][y]:
                    possibleMoves.append([x+i,y,False])
                elif board[x+i][y] and ((board[x+i][y].name > 0 and color < 0) or (board[x+i][y].name < 0 and color > 0)):
                    possibleMoves.append([x+i,y,True])
                    blocked[0] = True
                else:
                    blocked[0] = True
            if x-i in range(0,8) and blocked[1] == False:
                if not board[x-i][y]:
                    possibleMoves.append([x-i,y,False])
                elif board[x-i][y] and ((board[x-i][y].name > 0 and color < 0) or (board[x-i][y].name < 0 and color > 0)):
                    possibleMoves.append([x-i,y,True])
                    blocked[1] = True
                else:
                    blocked[1] = True
            if y+i in range(0,8) and blocked[2] == False:
                if not board[x][y+i]:
                    possibleMoves.append([x,y+i,False])
                elif board[x][y+i] and ((board[x][y+i].name > 0 and color < 0) or (board[x][y+i].name < 0 and color > 0)):
                    possibleMoves.append([x,y+i,True])
                    blocked[2] = True
                else:
                    blocked[2] = True
            if y-i in range(0,8) and blocked[3] == False:
                if not board[x][y-i]:
                    possibleMoves.append([x,y-i,False])
                elif board[x][y-i] and ((board[x][y-i].name > 0 and color < 0) or (board[x][y-i].name < 0 and color > 0)):
                    possibleMoves.append([x,y-i,True])
                    blocked[3] = True
                else:
                    blocked[3] = True

    elif abs(name) == 3:
        #Bishop
        blocked = [False,False,False,False]
        for i in range(1,8):
            if x-i in range(0,8) and y-i in range(0,8) and blocked[0] == False:
                if not board[x-i][y-i]:
                    possibleMoves.append([x-i,y-i,False])
                elif board[x-i][y-i] and ((board[x-i][y-i].name > 0 and color < 0) or (board[x-i][y-i].name < 0 and color > 0)):
                    possibleMoves.append([x-i,y-i,True])
                    blocked[0] = True
                else:
                    blocked[0] = True
            if x+i in range(0,8) and y+i in range(0,8) and blocked[1] == False:
                if not board[x+i][y+i]:
                    possibleMoves.append([x+i,y+i,False])
                elif board[x+i][y+i] and ((board[x+i][y+i].name > 0 and color < 0) or (board[x+i][y+i].name < 0 and color > 0)):
                    possibleMoves.append([x+i,y+i,True])
                    blocked[1] = True
                else:
                    blocked[1] = True
            if x-i in range(0,8) and y+i in range(0,8) and blocked[2] == False:
                if not board[x-i][y+i]:
                    possibleMoves.append([x-i,y+i,False])
                elif board[x-i][y+i] and ((board[x-i][y+i].name > 0 and color < 0) or (board[x-i][y+i].name < 0 and color > 0)):
                    possibleMoves.append([x-i,y+i,True])
                    blocked[2] = True
                else:
                    blocked[2] = True
            if x+i in range(0,8) and y-i in range(0,8) and blocked[3] == False:
                if not board[x+i][y-i]:
                    possibleMoves.append([x+i,y-i,False])
                elif board[x+i][y-i] and ((board[x+i][y-i].name > 0 and color < 0) or (board[x+i][y-i].name < 0 and color > 0)):
                    possibleMoves.append([x+i,y-i,True])
                    blocked[3] = True
                else:
                    blocked[3] = True


    elif abs(name) == 6:
        #King
        if x+1 in range(0,8) and y+1 in range(0,8):
            if not board[x+1][y+1]:
                possibleMoves.append([x+1,y+1,False])
            elif board[x+1][y+1] and ((board[x+1][y+1].name > 0 and color < 0) or (board[x+1][y+1].name < 0 and color > 0)):
                possibleMoves.append([x+1,y+1,True])
        if x+1 in range(0,8) and y-1 in range(0,8):
            if not board[x+1][y-1]:
                possibleMoves.append([x+1,y-1,False])
            elif board[x+1][y-1] and ((board[x+1][y-1].name > 0 and color < 0) or (board[x+1][y-1].name < 0 and color > 0)):
                possibleMoves.append([x+1,y-1,True])
        if x-1 in range(0,8) and y+1 in range(0,8):
            if not board[x-1][y+1]:
                possibleMoves.append([x-1,y+1,False])
            elif board[x-1][y+1] and ((board[x-1][y+1].name > 0 and color < 0) or (board[x-1][y+1].name < 0 and color > 0)):
                possibleMoves.append([x-1,y+1,True])
        if x-1 in range(0,8) and y-1 in range(0,8):
            if not board[x-1][y-1]:
                possibleMoves.append([x-1,y-1,False])
            elif board[x-1][y-1] and ((board[x-1][y-1].name > 0 and color < 0) or (board[x-1][y-1].name < 0 and color > 0)):
                possibleMoves.append([x-1,y-1,True])

        if x+1 in range(0,8):
            if not board[x+1][y]:
                possibleMoves.append([x+1,y,False])
            elif board[x+1][y] and ((board[x+1][y].name > 0 and color < 0) or (board[x+1][y].name < 0 and color > 0)):
                possibleMoves.append([x+1,y,True])
        if x-1 in range(0,8):
            if not board[x-1][y]:
                possibleMoves.append([x-1,y,False])
            elif board[x-1][y] and ((board[x-1][y].name > 0 and color < 0) or (board[x-1][y].name < 0 and color > 0)):
                possibleMoves.append([x-1,y,True])
        if y+1 in range(0,8):
            if not board[x][y+1]:
                possibleMoves.append([x,y+1,False])
            elif board[x][y+1] and ((board[x][y+1].name > 0 and color < 0) or (board[x][y+1].name < 0 and color > 0)):
                possibleMoves.append([x,y+1,True])
        if y-1 in range(0,8):
            if not board[x][y-1]:
                possibleMoves.append([x,y-1,False])
            elif board[x][y-1] and ((board[x][y-1].name > 0 and color < 0) or (board[x][y-1].name < 0 and color > 0)):
                possibleMoves.append([x,y-1,True])

        if name > 0:
            #White King
            #Add Castle
            if not board[x][y].moved:
                #King Hasn't Moved
                if not board[1][7] and not board[2][7] and not board[3][7] and board[0][7] and not board[0][7].moved:
                    #No in between pieces and rook left rook hasn't moved
                    possibleMoves.append([2,7,False,'c'])
                if not board[5][7] and not board[6][7] and board[7][7] and not board[7][7].moved:
                    #No in between pieces and rook left rook hasn't moved
                    possibleMoves.append([6,7,False,'c'])

        if name < 0:
            #Black King
            #Add Castle
            if not board[x][y].moved:
                #King Hasn't Moved
                if not board[1][0] and not board[2][0] and not board[3][0] and board[0][0] and not board[0][0].moved:
                    #No in between pieces and rook left rook hasn't moved
                    possibleMoves.append([2,0,False,'c'])
                if not board[5][0] and not board[6][0] and board[7][0] and not board[7][0].moved:
                    #No in between pieces and rook left rook hasn't moved
                    possibleMoves.append([6,0,False,'c'])

    return possibleMoves

def makeMove(board, selectedPiece, move, movesMade):
    newPiece = board[selectedPiece[0]][selectedPiece[1]]
    newPiece.moved = True
    newPiece.lastMoved = movesMade

    board[move[0]][move[1]] = newPiece
    board[selectedPiece[0]][selectedPiece[1]] = None

    if len(move) == 4:
        #Castle
        if(move[3] == 'c'):
            if(move[:2] == [2,7]):
                rookPiece = board[0][7]
                rookPiece.moved = True
                board[3][7] = rookPiece
                board[0][7] = None
            if(move[:2] == [6,7]):
                rookPiece = board[7][7]
                rookPiece.moved = True
                board[5][7] = rookPiece
                board[7][7] = None
            if(move[:2] == [2,0]):
                rookPiece = board[0][0]
                rookPiece.moved = True
                board[3][0] = rookPiece
                board[0][0] = None
            if(move[:2] == [6,0]):
                rookPiece = board[7][0]
                rookPiece.moved = True
                board[5][0] = rookPiece
                board[7][0] = None

        #En Passant
        if(move[3] == 'p'):
            if move[0] == selectedPiece[0]-1 and selectedPiece[1] == 3:
                board[move[0]][move[1]+1] = None
            if move[0] == selectedPiece[0]+1 and selectedPiece[1] == 3:
                board[move[0]][move[1]+1] = None
            if move[0] == selectedPiece[0]-1 and selectedPiece[1] == 4:
                board[move[0]][move[1]-1] = None
            if move[0] == selectedPiece[0]+1 and selectedPiece[1] == 4:
                board[move[0]][move[1]-1] = None

def killRestrict(board, name, x, y, possibleMoves, movesMade):
    
    deathSpots = []
    if name > 0:
        for move in possibleMoves:
            tempBoard = copy.deepcopy(board)
            makeMove(tempBoard, [x,y], move, movesMade)

            for a in range(8):
                for b in range(8):
                    if tempBoard[a][b] and tempBoard[a][b].name < 0:
                        tempMoves = findMoves(tempBoard, tempBoard[a][b].name, a, b, movesMade+1)

                        for k in tempMoves:
                            if k[0] == move[0] and k[1] == move[1] and k[2] == True:
                                deathSpots.append(k[:2])
    if name < 0:
        for move in possibleMoves:
            tempBoard = copy.deepcopy(board)
            makeMove(tempBoard, [x,y], move, movesMade)

            for a in range(8):
                for b in range(8):
                    if tempBoard[a][b] and tempBoard[a][b].name > 0:
                        tempMoves = findMoves(tempBoard, tempBoard[a][b].name, a, b, movesMade+1)

                        for k in tempMoves:
                            if k[0] == move[0] and k[1] == move[1] and k[2] == True:
                                deathSpots.append(k[:2])

    updatedPossibleMoves = []
    for i in possibleMoves:
        if [i[0],i[1]] not in deathSpots:
            updatedPossibleMoves.append(i)
    return updatedPossibleMoves


def checkCheck(board, turn, movesMade):
    #Function checks if the player with the passed turn is in check

    if turn == 1:
        #Check if white king in check
        whiteKingPos = []
        for i in range(len(board)):
            breakAll = False
            for j in range(len(board[i])):
                if board[i][j] == 6:
                    whiteKingPos = [i,j]
                if whiteKingPos != []:
                    breakAll = True
                    break
            if breakAll:
                break

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] and board[i][j].name < 0:
                    #Finds black moves
                    currentMoves = findMoves(board, board[i][j].name, i, j, movesMade)
                    if board[i][j] == -6:
                        currentMoves = killRestrict(board, board[i][j].name, i, j, currentMoves, movesMade)
                    for k in currentMoves:
                        if k[0] == whiteKingPos[0] and k[1] == whiteKingPos[1]:
                            return True

    if turn == -1:

        blackKingPos = []
        for i in range(len(board)):
            breakAll = False
            for j in range(len(board[i])):
                if board[i][j] == -6:
                    blackKingPos = [i,j]
                if blackKingPos != []:
                    breakAll = True
                    break
            if breakAll:
                break

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] and board[i][j].name > 0:
                    #Finds white moves
                    currentMoves = findMoves(board, board[i][j].name, i, j, movesMade)
                    if board[i][j] == 6:
                        currentMoves = killRestrict(board, board[i][j].name, i, j, currentMoves, movesMade)
                    for k in currentMoves:
                        if k[0] == blackKingPos[0] and k[1] == blackKingPos[1]:
                            return True

    return False

def checkmateCheck(board, turn, movesMade):
    #Function checks if the player with the passed turn is in checkmate

    if turn == 1:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] and board[i][j].name > 0:
                    currentMoves = findMoves(board, board[i][j].name, i, j, movesMade)
                    currentMoves[:] = checkRestrict(board, board[i][j].name, [i,j], currentMoves, movesMade)
                    if len(currentMoves) > 0:
                        return False
    if turn == -1:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] and board[i][j].name < 0:
                    currentMoves = findMoves(board, board[i][j].name, i, j, movesMade)
                    currentMoves[:] = checkRestrict(board, board[i][j].name, [i,j], currentMoves, movesMade)
                    if len(currentMoves) > 0:
                        return False
    return True


def checkRestrict(board, name, selectedPiece, possibleMoves, movesMade):


    restrictedSpots = []

    if name > 0:
        for move in possibleMoves:
            tempBoard = copy.deepcopy(board)
            makeMove(tempBoard, selectedPiece, move, movesMade)

            if checkCheck(tempBoard, 1, movesMade+1):
                restrictedSpots.append([move[0],move[1]])
    if name < 0:
        for move in possibleMoves:
            tempBoard = copy.deepcopy(board)
            makeMove(tempBoard, selectedPiece, move, movesMade)

            if checkCheck(tempBoard, -1, movesMade+1):
                restrictedSpots.append([move[0],move[1]])
    
    updatedPossibleMoves = []
    for i in possibleMoves:
        if [i[0],i[1]] not in restrictedSpots:
            updatedPossibleMoves.append(i)


    return updatedPossibleMoves


def choosePosition(pos, turn, board, selectedPiece, possibleMoves, movesMade):
    x = -1
    y = -1
    for i in range(0,8):
        if pos[0] in range(i*100, i*100 + 100):
            x = i
        if pos[1] in range(i*100, i*100 + 100):
            y = i

    if turn == 1:
        if selectedPiece == []:
            if board[x][y] and board[x][y].name > 0:
                selectedPiece[:] = [x,y]
                possibleMoves[:] = findMoves(board, board[x][y].name, x, y, movesMade)
                if board[x][y].name == 6:
                    possibleMoves[:] = killRestrict(board, board[x][y].name, x, y, possibleMoves, movesMade)
                possibleMoves[:] = checkRestrict(board, board[x][y].name, [x,y],possibleMoves, movesMade)
            
                
        else:
            if [x,y] == selectedPiece or ([x,y,False] not in possibleMoves and [x,y,True] not in possibleMoves and [x,y,False,'c'] not in possibleMoves and [x,y,True,'p'] not in possibleMoves):
                #Unselect Piece
                selectedPiece[:] = []
                possibleMoves[:] = []
            elif [x,y,False] in possibleMoves or [x,y,True] in possibleMoves:
                makeMove(board, selectedPiece, [x,y], movesMade)
                selectedPiece[:] = []
                possibleMoves[:] = []
                turn *= -1
                movesMade += 1
                #print(checkCheck(board, turn, movesMade))
            elif [x,y,False,'c'] in possibleMoves:
                makeMove(board, selectedPiece, [x,y,False,'c'], movesMade)
                selectedPiece[:] = []
                possibleMoves[:] = []
                turn *= -1
                movesMade += 1
                #print(checkCheck(board, turn, movesMade))
            elif [x,y,True,'p'] in possibleMoves:
                makeMove(board, selectedPiece, [x,y,True,'p'], movesMade)
                selectedPiece[:] = []
                possibleMoves[:] = []
                turn *= -1
                movesMade += 1
                #print(checkCheck(board, turn, movesMade))

    if turn == -1:
        if selectedPiece == []:
            if board[x][y] and board[x][y].name < 0:
                selectedPiece[:] = [x,y]
                possibleMoves[:] = findMoves(board, board[x][y].name, x, y, movesMade)
                if board[x][y].name == -6:
                    possibleMoves[:] = killRestrict(board, board[x][y].name, x, y, possibleMoves, movesMade)
                possibleMoves[:] = checkRestrict(board, board[x][y].name, [x,y],possibleMoves, movesMade)
        else:
            if [x,y] == selectedPiece or ([x,y,False] not in possibleMoves and [x,y,True] not in possibleMoves and [x,y,False,'c'] not in possibleMoves and [x,y,True,'p'] not in possibleMoves):
                #Unselect Piece
                selectedPiece[:] = []
                possibleMoves[:] = []
            elif [x,y,False] in possibleMoves or [x,y,True] in possibleMoves:
                makeMove(board, selectedPiece, [x,y], movesMade)
                selectedPiece[:] = []
                possibleMoves[:] = []
                turn *= -1
                movesMade += 1
                #print(checkCheck(board, turn, movesMade))
            elif [x,y,False,'c'] in possibleMoves:
                makeMove(board, selectedPiece, [x,y,False,'c'], movesMade)
                selectedPiece[:] = []
                possibleMoves[:] = []
                turn *= -1
                movesMade += 1
                #print(checkCheck(board, turn, movesMade))
            elif [x,y,True,'p'] in possibleMoves:
                makeMove(board, selectedPiece, [x,y,True,'p'], movesMade)
                selectedPiece[:] = []
                possibleMoves[:] = []
                turn *= -1
                movesMade += 1
                #print(checkCheck(board, turn, movesMade))
    
    return turn, movesMade


def inGame():
    '''
    1 = pawn
    2 = knight
    3 = bishop
    4 = rook
    5 = queen
    6 = king
    - = black
    + = white
    '''

    board = [
        [piece(-4),piece(-1),None,None,None,None,piece(1),piece(4)],
        [piece(-2),piece(-1),None,None,None,None,piece(1),piece(2)],
        [piece(-3),piece(-1),None,None,None,None,piece(1),piece(3)],
        [piece(-5),piece(-1),None,None,None,None,piece(1),piece(5)],
        [piece(-6),piece(-1),None,None,None,None,piece(1),piece(6)],
        [piece(-3),piece(-1),None,None,None,None,piece(1),piece(3)], 
        [piece(-2),piece(-1),None,None,None,None,piece(1),piece(2)],
        [piece(-4),piece(-1),None,None,None,None,piece(1),piece(4)]
    ]

    selectedPiece = []
    turn = 1 #White starts
    movesMade = 0
    possibleMoves = []
    inCheck = 0 #-1 means black in Check, 1 means white in Check

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                # if turn == 1:
                turn, movesMade = choosePosition(pygame.mouse.get_pos(), turn, board, selectedPiece, possibleMoves, movesMade)
                checkmateVal = checkmateCheck(board, turn, movesMade) 
                if checkmateVal:
                    if turn == 1:
                        # print("CHECKMATE \nBLACK WINS")
                        endScreen(board, turn)
                        return 
                    if turn == -1:
                        # print("CHECKMATE \nWHITE WINS")
                        endScreen(board, turn)
                        return


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        screen.fill((0, 0, 0))

        for i in range(0,8,2):
            for j in range(0,8,2):
                pygame.draw.rect(screen, LIGHTSQUARE, (i*100,j*100,100,100))
        for i in range(1,9,2):
            for j in range(1,9,2):
                pygame.draw.rect(screen, LIGHTSQUARE, (i*100,j*100,100,100))

        for i in range(0,8,2):
            for j in range(0,8,2):
                pygame.draw.rect(screen, DARKSQUARE, (i*100+100,j*100,100,100))
        for i in range(1,9,2):
            for j in range(1,9,2):
                pygame.draw.rect(screen, DARKSQUARE, (i*100-100,j*100,100,100))

        for i in range(8):
            for j in range(8):
                if (board[i][j]):
                    pieceDraw(board[i][j].name, i, j)

        for i in range(8):
            largeText = pygame.font.SysFont("arial",15)
            TextSurf, TextRect = text_objects(str(8-i), largeText, BLACK)
            TextRect.center = (10,50 + i*100)
            screen.blit(TextSurf, TextRect)

            # largeText = pygame.font.SysFont("arial",15)
            # TextSurf, TextRect = text_objects(str(i), largeText, BLACK)
            # TextRect.center = (50 + i*100, 10)
            # screen.blit(TextSurf, TextRect)

        alph = "ABCDEFGH"
        for i in range(len(alph)):
            largeText = pygame.font.SysFont("arial",15)
            TextSurf, TextRect = text_objects(alph[i], largeText, BLACK)
            TextRect.center = (50 + i*100,10)
            screen.blit(TextSurf, TextRect)

        if selectedPiece != []:
            for i in possibleMoves:
                if i[2] == False:
                    pygame.draw.rect(screen, BLUE, (i[0]*100, i[1]*100, 100, 100), 3)
                else:
                    pygame.draw.rect(screen, RED, (i[0]*100, i[1]*100, 100, 100), 3)

            pygame.draw.rect(screen, BLACK, (selectedPiece[0]*100, selectedPiece[1]*100, 100, 100), 3)

        pygame.display.flip()
        fpsClock.tick(fps)

        if turn == -1:
            board = copy.deepcopy(AI(board, turn, movesMade, 3, float('-inf'), float('inf'))[1])
            movesMade += 1
            turn *= -1
            # global AIMovesChecked
            # print(AIMovesChecked)
            # AIMovesChecked = 0
            

            # print("hi")

            if checkmateCheck(board, turn, movesMade):
                endScreen(board, turn) 
                return
        
        # if turn == 1:
        #     board = copy.deepcopy(AI(board, turn, movesMade, 2, float('-inf'), float('inf'))[1])
        #     movesMade += 1
        #     turn *= -1

        #     # print("hi")

        #     if checkmateCheck(board, turn, movesMade):
        #         endScreen(board, turn)
        #         return
            


def endScreen(board, loser):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        screen.fill((0, 0, 0))
        

        for i in range(0,8,2):
            for j in range(0,8,2):
                pygame.draw.rect(screen, LIGHTSQUARE, (i*100,j*100,100,100))
        for i in range(1,9,2):
            for j in range(1,9,2):
                pygame.draw.rect(screen, LIGHTSQUARE, (i*100,j*100,100,100))

        for i in range(0,8,2):
            for j in range(0,8,2):
                pygame.draw.rect(screen, DARKSQUARE, (i*100+100,j*100,100,100))
        for i in range(1,9,2):
            for j in range(1,9,2):
                pygame.draw.rect(screen, DARKSQUARE, (i*100-100,j*100,100,100))

        for i in range(8):
            for j in range(8):
                if (board[i][j]):
                    pieceDraw(board[i][j].name, i, j)

        text = pygame.font.SysFont("arial",50,bold=True)
        if loser == 1:
            TextSurf, TextRect = text_objects("CHECKMATE BLACK WINS", text, DARKGREY)
            TextRect.center = (400,350)
            screen.blit(TextSurf, TextRect)
        if loser == -1:
            TextSurf, TextRect = text_objects("CHECKMATE WHITE WINS", text, DARKGREY)
            TextRect.center = (400,350)
            screen.blit(TextSurf, TextRect)

        text = pygame.font.SysFont("arial",30)
        TextSurf, TextRect = text_objects("Press Escape to Restart", text, DARKGREY)
        TextRect.center = (400,550)
        screen.blit(TextSurf, TextRect)
        w = 200
        h = 80

        pygame.display.flip()
        fpsClock.tick(fps)





def intro():
    '''
    1 = pawn
    2 = knight
    3 = bishop
    4 = rook
    5 = queen
    6 = king
    - = black
    + = white
    '''

    # board = [
    #     [-4,-1,0,0,0,0,1,4],
    #     [-2,-1,0,0,0,0,1,2],
    #     [-3,-1,0,0,0,0,1,3],
    #     [-5,-1,0,0,0,0,1,5],
    #     [-6,-1,0,0,0,0,1,6],
    #     [-3,-1,0,0,0,0,1,3], 
    #     [-2,-1,0,0,0,0,1,2],
    #     [-4,-1,0,0,0,0,1,4]
    # ]

    board = [
        [piece(-4),piece(-1),None,None,None,None,piece(1),piece(4)],
        [piece(-2),piece(-1),None,None,None,None,piece(1),piece(2)],
        [piece(-3),piece(-1),None,None,None,None,piece(1),piece(3)],
        [piece(-5),piece(-1),None,None,None,None,piece(1),piece(5)],
        [piece(-6),piece(-1),None,None,None,None,piece(1),piece(6)],
        [piece(-3),piece(-1),None,None,None,None,piece(1),piece(3)], 
        [piece(-2),piece(-1),None,None,None,None,piece(1),piece(2)],
        [piece(-4),piece(-1),None,None,None,None,piece(1),piece(4)]
    ]

    while True:
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pass

        screen.fill((0, 0, 0))
        

        for i in range(0,8,2):
            for j in range(0,8,2):
                pygame.draw.rect(screen, LIGHTSQUARE, (i*100,j*100,100,100))
        for i in range(1,9,2):
            for j in range(1,9,2):
                pygame.draw.rect(screen, LIGHTSQUARE, (i*100,j*100,100,100))

        for i in range(0,8,2):
            for j in range(0,8,2):
                pygame.draw.rect(screen, DARKSQUARE, (i*100+100,j*100,100,100))
        for i in range(1,9,2):
            for j in range(1,9,2):
                pygame.draw.rect(screen, DARKSQUARE, (i*100-100,j*100,100,100))

        for i in range(8):
            for j in range(8):
                if (board[i][j]):
                    pieceDraw(board[i][j].name, i, j)


        w = 200
        h = 80
        button("START",400 - w/2,400 - h/2,w,h,DARKERGREEN,SILVER,inGame)

        pygame.display.flip()
        fpsClock.tick(fps)



intro()
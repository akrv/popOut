# -*- coding: iso-8859-15 -*-
'''
Created on 02.06.2014

@author: Aswin
'''

import numpy as np
#import random

def enum(**enums):
    return type('Enum', (), enums)

class Config: #initial configuration that can be modified using the interface
    fixationDuration = 1
    #questionDuration = 2
    counter = 0
    
    
    noOfBlocks = [1,2,3,4,5,6]
    subject = None
    outputFolder = "."
    
    
    '''creating the points on the screen'''
    positionX = np.linspace(-23.5, 23.5, num=10, endpoint=True, retstep=False)
    positionY = np.linspace(-14.1, 14.1, num=6, endpoint=True, retstep=False)
    xys = np.transpose([np.tile(positionX, len(positionY)), np.repeat(positionY, len(positionX))])
    
    '''creating the constellation using the code for six time: constellation = random.sample(xrange(1, 61), 60)'''
    constellation1 = [7, 43, 46, 16, 27, 5, 31, 36, 44, 52, 22, 25, 59, 24, 17, 48, 8, 32, 40, 20, 29, 21, 57, 15, 26, 13, 10, 35, 53, 2, 51, 30, 33, 38, 47, 34, 3, 55, 4, 6, 50, 23, 28, 12, 54, 1, 9, 60, 18, 37, 42, 39, 11, 19, 14, 41, 45, 58, 56, 49]
    constellation2 = [29, 9, 1, 4, 45, 3, 35, 16, 13, 22, 57, 25, 24, 37, 19, 26, 60, 32, 59, 36, 2, 18, 46, 58, 14, 48, 49, 44, 12, 39, 38, 40, 56, 8, 51, 28, 47, 43, 50, 34, 41, 21, 55, 31, 33, 17, 53, 42, 30, 15, 23, 11, 7, 52, 20, 54, 10, 6, 27, 5]
    constellation3 = [57, 19, 53, 47, 13, 55, 14, 52, 29, 39, 9, 1, 25, 38, 18, 56, 49, 31, 28, 15, 3, 5, 4, 54, 58, 41, 27, 2, 44, 59, 35, 60, 24, 16, 40, 23, 43, 34, 32, 20, 17, 37, 6, 26, 33, 45, 51, 11, 50, 46, 30, 8, 36, 22, 48, 12, 21, 7, 42, 10]
    constellation4 = [13, 27, 32, 49, 2, 57, 35, 60, 11, 25, 19, 5, 59, 24, 34, 6, 54, 21, 3, 51, 52, 23, 18, 31, 42, 45, 9, 10, 15, 38, 16, 53, 47, 8, 22, 37, 4, 40, 44, 17, 58, 7, 29, 46, 12, 20, 39, 26, 50, 56, 14, 1, 43, 33, 36, 30, 41, 55, 48, 28]
    constellation5 = [51, 27, 15, 48, 59, 20, 9, 19, 53, 13, 43, 39, 37, 58, 38, 45, 47, 40, 31, 17, 18, 26, 30, 8, 32, 4, 55, 54, 56, 25, 14, 50, 1, 12, 28, 16, 10, 44, 52, 24, 3, 34, 6, 5, 42, 35, 46, 36, 57, 7, 23, 11, 21, 22, 60, 2, 41, 49, 29, 33]
    constellation6 = [20, 60, 35, 54, 26, 7, 4, 29, 30, 59, 34, 37, 42, 1, 46, 48, 9, 31, 21, 36, 32, 45, 5, 33, 53, 14, 22, 11, 55, 23, 18, 28, 52, 2, 25, 41, 51, 47, 43, 27, 10, 57, 6, 40, 50, 49, 19, 39, 56, 13, 8, 12, 16, 3, 17, 38, 15, 24, 44, 58]
    constellationPrac = [19, 43, 39, 13, 12, 46, 25, 41, 16, 60, 20, 49, 8, 33, 36, 35, 9, 37, 21, 42, 31, 55, 23, 24, 34, 57, 53, 5, 18, 14, 32, 1, 26, 11, 3, 50, 15, 4, 30, 58, 22, 54, 56, 45, 28, 47, 38, 40, 29, 44, 10, 59, 7, 6, 52, 27, 51, 17, 48, 2]
    
    '''a dict to access the constellation block wise'''
    constellation = {
                     1 : constellation1,
                     2 : constellation2,
                     3 : constellation3,
                     4 : constellation4,
                     5 : constellation5,
                     6 : constellation6,
                     7 : constellationPrac
                     }
    
 
    
    
    '''a array for all the questions'''   
    questions = ['der grüne Kreis',
                 'das unvollständige Quadrat',
                 'die Raute',
                 'das rote Dreieck',
                 'der Stern'
                 ]
    
    '''We have 5 target objects and every object is shown six times with and six times without the appearance of this object'''
    a = np.array([0,1,2,3,4]) #will be used to index the questions in the list questions
    y = np.tile(a,12)
    ze = np.zeros((30,), dtype= np.int)
    on = np.ones((30,), dtype= np.int)
    zeon = np.append(ze, on) #will be used to check the boolean if the object is present or not
    questionIdx = np.transpose([y,zeon])
    
    '''for practice'''
    y1 = np.tile(a,2)
    ze1 = np.zeros((5,), dtype= np.int)
    on1 = np.ones((5,), dtype= np.int)
    zeon1 = np.append(on1, ze1)
    questionIdxPrac = np.transpose([y1,zeon1])
    '''50 numbers in random to call the questions [questionIdx,trueFalse] for 6 blocks'''
    
    order1 = [28, 43, 34, 31, 55, 25, 30, 32, 52, 6, 29, 37, 36, 38, 9, 54, 21, 27, 47, 49, 23, 45, 15, 46, 56, 59, 44, 40, 50, 22, 17, 42, 18, 4, 41, 1, 57, 3, 12, 7, 14, 53, 11, 33, 35, 26, 24, 51, 39, 2, 13, 19, 58, 48, 16, 5, 10, 20, 8, 0]
    order2 = [3, 12, 43, 10, 14, 21, 56, 22, 17, 15, 8, 53, 58, 4, 33, 36, 27, 20, 51, 26, 37, 1, 29, 55, 38, 6, 35, 46, 24, 44, 2, 57, 5, 11, 23, 34, 16, 28, 59, 13, 54, 41, 18, 42, 48, 39, 31, 19, 32, 47, 52, 7, 50, 30, 40, 49, 25, 0, 45, 9]
    order3 = [32, 37, 54, 43, 26, 27, 28, 58, 13, 19, 36, 35, 52, 41, 24, 30, 42, 7, 40, 56, 53, 17, 1, 39, 5, 0, 21, 6, 57, 20, 10, 34, 23, 59, 33, 14, 44, 50, 25, 55, 2, 8, 51, 12, 48, 45, 3, 15, 47, 22, 31, 18, 38, 9, 16, 11, 4, 49, 29, 46]
    order4 = [25, 29, 43, 36, 42, 31, 39, 22, 55, 41, 37, 16, 3, 10, 8, 21, 44, 15, 9, 49, 50, 5, 19, 45, 6, 0, 1, 53, 34, 26, 12, 17, 33, 2, 40, 58, 51, 28, 57, 11, 18, 52, 30, 35, 20, 24, 56, 27, 4, 23, 32, 7, 13, 47, 54, 48, 46, 14, 38, 59]
    order5 = [50, 34, 42, 11, 48, 16, 54, 12, 5, 8, 43, 59, 29, 1, 47, 51, 36, 18, 39, 9, 7, 4, 53, 20, 35, 58, 17, 49, 21, 41, 46, 23, 33, 24, 57, 55, 22, 32, 40, 0, 56, 15, 14, 30, 10, 28, 13, 44, 6, 19, 27, 38, 31, 2, 26, 52, 45, 37, 25, 3]
    order6 = [11, 58, 23, 1, 50, 19, 24, 41, 53, 45, 20, 18, 0, 16, 2, 48, 10, 7, 6, 35, 49, 59, 29, 42, 26, 15, 30, 25, 21, 33, 14, 37, 39, 44, 57, 9, 54, 38, 13, 55, 36, 43, 56, 5, 3, 32, 22, 47, 31, 46, 40, 17, 27, 52, 8, 34, 28, 51, 12, 4]
    
    orderBlock = {1 : order1,
                  2 : order2,
                  3 : order3,
                  4 : order4,
                  5 : order5,
                  6 : order6
                  }
    
    
    def __init__(self):
        pass
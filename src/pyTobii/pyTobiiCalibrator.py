# -*- coding: iso-8859-15 -*-
'''
Created on 08.11.2010

@author: Oskar
'''

from pyTobiiCalibShapes import Cross, Quad
import pyTetClient
import pyTobiiConfiguration
import random

from psychopy import core, event

class pyTobiiCalibrator:
    def __init__(self, window, tetClient):
        self.__window = window
        self.__tc = tetClient
        
        self.__cross = Cross(self.__window, pyTobiiConfiguration.calibrationCrossSize, pyTobiiConfiguration.fixationColor)
        self.__quad = Quad(self.__window, pyTobiiConfiguration.calibrationQuadSize, pyTobiiConfiguration.fixationColor)
        
        self.__isCalibrating = False

        
    def isCalibrating(self):
        '''Gibt zurück, ob das Modul gerade kalibriert.'''
        return self.__isCalibrating
    
    
    def clearCalibration(self):
        '''
        Entferne alte Kalibrierung.
        (Sollte vor jeder neuen ausgeführt werden.)
        '''
        self.__tc.ClearCalibration()
        
        
    def calibrate(self, points, filename, fake = False):
        '''
        Startet die Kalibrierung an den übergebenen Punkten.
        Speichert das Ergebnis in der entsprechenden Datei.
        '''
        self.__isCalibrating = True
        
        #randomisiere reihenfolge
        points = list(points)
        random.shuffle(points)
        
        #sammle daten für jeden punkt
        for i, posi in enumerate(points):
            self.__calibPoint(posi[0], posi[1], fake)
            
        if not fake:
            #speichere neue calibration
            self.__tc.CalculateAndSetCalibration()
            self.__tc.SaveCalibrationToFile(filename)
        self.__isCalibrating = False
        
    
    def getMissingPoints(self, points, filename):
        '''Prüft die Kalibrierung und gibt nicht kalibrierte Positionen zurück.'''
        try:
            result = self.__tc.GetCalibrationResult(filename)
        except:
            print "Error in getMissingPoints(): Could not read calibration"
            return []
        
        successfullPoints = []
        for i in range(result.size):
            current = result.GetAt(i)
            if current.leftValidity == current.rightValidity == 1:
                posi = current.truePointX, current.truePointY
                posi = pyTetClient.tobiiToPsyCoord(*posi)
                posi = round(posi[0], 1), round(posi[1], 1)
                if posi not in successfullPoints:
                    successfullPoints.append(posi)
        
        
        missingPoints = []
        for posi in points:
            roundPos = round(posi[0], 1), round(posi[1], 1)
            if roundPos not in successfullPoints:
                missingPoints.append(posi)
        
        print "points"
        print points
        print "successful"
        print successfullPoints
        print "missing"
        print missingPoints
        
        return missingPoints


    def __calibPoint(self, x, y, fake = False):
        '''Nimmt Daten zu einem Punkt auf.'''
        self.__quad.setPosition(x,y)
        self.__cross.setPosition(x,y)

        self.__quad.setAutoDraw(True)
        self.__window.flip()
        
        self.__shrinkQuad(pyTobiiConfiguration.calibrationShrinkSpeed)

        self.__quad.setAutoDraw(False)
        self.__cross.setAutoDraw(True)
        self.__window.flip()
        
        event.waitKeys(keyList=['space'])

        if not fake:
            tobiiX, tobiiY = pyTetClient.psyToTobiiCoord(x, y)
            self.__tc.AddCalibrationPoint(tobiiX, tobiiY, numGoodSamples = pyTobiiConfiguration.calibrationNumGoodSamples, block = True)
        
        core.wait(0.1)
        self.__cross.setAutoDraw(False)
        self.__window.flip()

        
    def __shrinkQuad(self, duration = 0.5):
        '''
        Animiert das kleinerwerden des Quadrats über die angegebene Zeitspanne.
        (Blockierend)
        '''
        self.__quad.scale(1)
        minScale = 0.1
        startTime = core.getTime()
        currentTime = startTime
        while currentTime - startTime < duration:
            curScale = minScale + (1-(currentTime-startTime)/duration) * (1-minScale)
            self.__quad.scale(curScale)
            self.__window.flip()
            currentTime = core.getTime()

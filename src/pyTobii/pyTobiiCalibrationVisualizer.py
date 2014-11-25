# -*- coding: iso-8859-15 -*-
'''
Created on 04.02.2010

@author: Oskar
'''

from pyTobiiCalibShapes import Disc
from pyTetClient import tobiiToPsyCoord
import pyTobiiConfiguration
from psychopy import visual

class pyTobiiCalibrationVisualizer:
    '''Klasse zur Visualisierung des Kalibrationsergebnisses.'''
    def __init__(self, window, tc):
        self.__window = window
        self.__tc = tc
        
        self.__baseDisc         = Disc(self.__window)

        self.calibData        = {}
        self.__cachedAverages   = {}
        self.__truePointDiscs   = []    #die zu kalibrierende koordinate
        self.__leftPointDiscs   = []    #die dazu aufgenommenen daten des linken auges
        self.__rightPointDiscs  = []    #die dazu aufgenommenen daten des rechten auges
        self.__netTruePoints    = []    #die zu kalibrierende koordinate für das netz
        self.__netLeftPoints    = []    #die dazu aufgenommenen daten des linken auges
        self.__netRightPoints   = []    #die dazu aufgenommenen daten des rechten auges
        self.__netLeftLines     = []    #linien des netzes für das linke auge
        self.__netRightLines    = []    #linien des netzes für das rechte auge
        

    def processCalib(self, filename):
        '''Speichert die Kalibrierung intern neu.'''
        self.calibData = {}
        try:
            calib = self.__tc.GetCalibrationResult(filename)
        except:
            raise Exception("Error in processCalib(): A calibration must be set.")
        
        for i in range(calib.size):
            curData = calib.GetAt(i)
            #validity: -1 = nicht erkannt, 0 = erkannt aber nicht genommen, 1 = erkannt und genommen
            if not (curData.leftValidity == 1 == curData.rightValidity): continue
            
            key = round(curData.truePointX, 2), round(curData.truePointY, 2)
            if not key in self.calibData:
                self.calibData[key] = []
            
            value = curData.leftMapX, curData.leftMapY, curData.rightMapX, curData.rightMapY
            self.calibData[key].append(value)
            print key
            print value
            

    def __addDisc(self, tobiiX, tobiiY, pointArray, color = None, scale = 1.0):
        '''Speichere zu jedem kalibrierten Punkt alle mapped Punkte.'''
        x, y = tobiiToPsyCoord(tobiiX, tobiiY)
        disc = self.__baseDisc.copy()
        disc.setPosition(x,y)
        if color: 
            disc.color(color)
        disc.scale(scale)
        pointArray.append(disc)
        
        disc.draw()
    
    def showResultPoints(self, filename):
        '''
        Zeigt das Ergbnis der in "filename" gespeicherten Kalibrierung an.
        Es werden Punkte für die Augenpositionen angezeigt.
        '''
        if self.__truePointDiscs: 
            self.hideResultPoints()
        self.processCalib(filename)
        
        for truePoint, calibData in self.calibData.iteritems():    #gehe alle punkte und deren daten durch
            truePointX, truePointY = truePoint
            self.__addDisc(truePointX, truePointY, self.__truePointDiscs, scale = 0.6)  #zeige kalibrierungspunkte an
            for leftMapX, leftMapY, rightMapX, rightMapY in calibData:  #zeige dazu aufgenommene, gemappte punkte an
                #left disc
                self.__addDisc(leftMapX, leftMapY, self.__leftPointDiscs, pyTobiiConfiguration.leftColor, scale = 0.3)
                #right disc
                self.__addDisc(rightMapX, rightMapY, self.__rightPointDiscs, pyTobiiConfiguration.rightColor, scale = 0.3)

        self.__window.flip()

    def hideResultPoints(self):
        '''Entfernt die Netze.'''
        toRemove = (self.__truePointDiscs, 
                    self.__leftPointDiscs,
                    self.__rightPointDiscs)
        
        for lst in toRemove:
            for entry in lst:
                del entry
                
        self.__truePointDiscs   = []
        self.__leftPointDiscs   = []
        self.__rightPointDiscs  = []
        
        self.__window.flip()


    def __getAvgForMappedPosi(self, truePosiKey):
        '''Errechnet den durchschnittswert aller aufgenommenen Punkte zu dem übergebenen zu kalibrierenden Punkt.''' 
        if truePosiKey in self.__cachedAverages:
            return self.__cachedAverages[truePosiKey]
        
        if truePosiKey not in self.calibData:
            print "key missing", truePosiKey
            print self.calibData
            return -1, -1, -1, -1
        
        calibData = self.calibData[truePosiKey]
        
        sampleCount = len(calibData)
        avgLeftX = avgLeftY = avgRightX = avgRightY = 0
        
        for leftMapX, leftMapY, rightMapX, rightMapY in calibData:
            avgLeftX += leftMapX 
            avgLeftY += leftMapY
            avgRightX += rightMapX
            avgRightY += rightMapY
            
        avgLeftX /= sampleCount 
        avgLeftY /= sampleCount
        avgRightX /= sampleCount
        avgRightY /= sampleCount
        self.__cachedAverages[truePosiKey] = avgLeftX, avgLeftY, avgRightX, avgRightY
        
        return avgLeftX, avgLeftY, avgRightX, avgRightY
        
    
    def __drawLine(self, tobiiStartCoords, tobiiEndCoords, color):
        '''Zeichnet eine Linie von der Start- bis zur Endposition.'''
        line = visual.Line(win=self.__window, lineColor=color, lineColorSpace="rgb", start=tobiiToPsyCoord(*tobiiStartCoords), end=tobiiToPsyCoord(*tobiiEndCoords), interpolate=False)
        line.draw()
        
        return line
        

    def showResultNet(self, filename):
        '''
        Zeigt das Ergbnis der in "filename" gespeicherten Kalibrierung an.
        Es wird ein Netz für die durchschnittliche Augenposition angezeigt.
        '''
        if self.__netTruePoints: 
            self.hideResultNet()
        self.processCalib(filename)
        
        #zeichne zu kalibrierende punkte ein
        for truePointX, truePointY in self.calibData.iterkeys():
            self.__addDisc(truePointX, truePointY, self.__netTruePoints, scale = 0.6)

            #zeichne discs zu den durchschnittswerten
            leftX, leftY, rightX, rightY = self.__getAvgForMappedPosi((truePointX, truePointY))
            self.__addDisc(leftX, leftY, self.__netLeftPoints, scale = 0.3, color = pyTobiiConfiguration.leftColor)
            self.__addDisc(rightX, rightY, self.__netRightPoints, scale = 0.3, color = pyTobiiConfiguration.rightColor)
            
        #alle verbindungen des netzes
        netLines = (((0.0, 0.0), (0.5, 0.0)),
                    ((0.0, 0.0), (0.0, 0.5)),
                    ((0.5, 0.0), (1.0, 0.0)),
                    ((0.5, 0.0), (0.5, 0.5)),
                    ((1.0, 0.0), (1.0, 0.5)),
                    ((0.0, 0.5), (0.5, 0.5)),
                    ((0.0, 0.5), (0.0, 1.0)),
                    ((0.5, 0.5), (1.0, 0.5)),
                    ((0.5, 0.5), (0.5, 1.0)),
                    ((1.0, 0.5), (1.0, 1.0)),
                    ((0.0, 1.0), (0.5, 1.0)),
                    ((1.0, 1.0), (0.5, 1.0)))
        
        for line in netLines:
            #bastel key für das calib dictionary
            startKey = round(line[0][0], 2), round(line[0][1], 2)
            endKey = round(line[1][0], 2), round(line[1][1], 2)
            
            #ermittel durchschnittswerte
            startLeftX, startLeftY, startRightX, startRightY = self.__getAvgForMappedPosi(startKey)
            endLeftX, endLeftY, endRightX, endRightY = self.__getAvgForMappedPosi(endKey)
            
            #zeichne linien zu den durchschnittswerten
            leftLine = self.__drawLine((startLeftX, startLeftY), (endLeftX, endLeftY), color = (0, 1, 0))
            rightLine = self.__drawLine((startRightX, startRightY), (endRightX, endRightY), color = (1, 0, 0))
            self.__netLeftLines.append(leftLine)
            self.__netRightLines.append(rightLine)
            
        self.__window.flip()

    
    def hideResultNet(self):
        '''Entfernt die Netze.'''
        toRemove = (self.__netTruePoints,
                    self.__netLeftPoints, 
                    self.__netRightPoints,
                    self.__netLeftLines,  
                    self.__netRightLines)
        
        for lst in toRemove:
            for entry in lst:
                del entry
                
        self.__cachedAverages   = {}
        self.__netTruePoints    = []
        self.__netLeftPoints    = []
        self.__netRightPoints   = []
        self.__netLeftLines     = []
        self.__netRightLines    = []
        
        self.__window.flip()
        
# -*- coding: iso-8859-15 -*-
'''
Created on 11.11.2010

@author: oskar
'''

from pyTobiiCalibShapes import Disc
#import math
import pickle
import pyTetClient
import pyTobii
import pyTobiiConfiguration
from psychopy import core

class GazeProcessor():
    def __init__(self, window):
        self.__window           = window
        self.__openDataName     = ""
        self.__outPickle        = None      #datei für die pickle ausgabe
        self.__outPlain         = None      #datei für plaintext ausgabe
        self.__lastTrigger      = -1        #damit nur änderungen der trigger geschrieben werden
        self.__dataCount        = 0         #zähler
        self.__lastStoreTime    = 0         #viz.tick() der letzten speicherung des buffers
        self.__dataSaveIntervall= pyTobiiConfiguration.dataSaveIntervall  #intervall in dem der buffer gespeichert werden soll
        self.__buffer           = []        #buffer aller daten
        self.__buffersize       = pyTobiiConfiguration.gazeProcessorBuffersize
        self.__showGazePoint    = False
        self.__dataIndex        = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]] #zählt auf wie oft jeder fehlercode für die datenerfassung vorkam (links, rechts)
        
        #erstelle die 3 discs zur anzeige des punktes
        self.__discAvg = Disc(self.__window)
        self.__discAvg.setPosition(0, 0)
        self.__discLeft = self.__discAvg.copy()
        self.__discLeft.color([0,1,0])
        self.__discRight = self.__discAvg.copy()
        self.__discRight.color([1,0,0])
        
        #self.callback(pyTetClient.VizEventSink.OnGazeData, self.__onGazeData)
        #self.callback(viz.EXIT_EVENT, self.__closeFiles())
        self.__storing = False
        
    
    def __openFiles(self):
        '''Öffnet die Ausgabedateien.'''
        self.__openDataName = str(pyTobii.getDataName())
        if not self.__openDataName: 
            return
        self.__outPickle = open(self.__openDataName + ".pic", "wb") 
        self.__outPlain = open(self.__openDataName + ".tob", "w") 
        self.__outPlain.write("time, trigger, leftValidity, rightValidity, leftX, leftY, rightX, rightY\n")
        self.__outPlain.flush()
        self.__dataIndex        = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        
    
    def closeFiles(self):
        '''Schließt die Ausgabedateien.'''
        try:
            self.__outPickle.dump() 
            self.__outPickle.close() 
        except: 
            pass
        try:
            self.__outPlain.dump()
            self.__outPlain.close()
        except: 
            pass
        self.__outPickle = None 
        self.__outPlain = None
    
    
    def checkErrors(self):
        '''Prüft ob die anzahl nicht erkannter rechter oder linker augen über einem Schwellwert liegt und sendet einen Fehler.'''
        dataSum = sum(self.__dataIndex[0]) + sum(self.__dataIndex[1])
        errorSum = self.__dataIndex[0][4] + self.__dataIndex[1][4]
        print "errordata: %s, dataSum: %i, errorSum: %i" % (str(self.__dataIndex), dataSum, errorSum)
        if dataSum > 0 and float(errorSum) / float(dataSum) > 0.5:
            #viz.message("ACHTUNG: Tobii liefert eventuell falsche Daten!")
            print "ACHTUNG: Tobii liefert eventuell falsche Daten!"
        
    
    def updateFilename(self):
        '''Falls sich der Ausgabename geändert hat, werden die Dateien entsprechend verändert.'''
        newName = str(pyTobii.getDataName())
        if newName == self.__openDataName or not self.__outPickle: 
            return   #wenn noch nix geöffnet wurde, nix machen
        
        self.__storeData()
        self.__closeFiles()
        #open wird beim nächsten speicheraufruf ausgeführt
        
        
    def showGazePoint(self):
        '''Zeigt den betrachteten Punkt auf dem Bildschirm.'''
        self.__showGazePoint = True
        self.__discAvg.setAutoDraw(True)
        self.__discLeft.setAutoDraw(True)
        self.__discRight.setAutoDraw(True)

    
    def hideGazePoint(self):
        '''Versteckt den betrachteten Punkt auf dem Bildschirm.'''
        self.__showGazePoint = False
        self.__discAvg.setAutoDraw(False)
        self.__discLeft.setAutoDraw(False)
        self.__discRight.setAutoDraw(False)

    
    def setTrigger(self, triggerNum):
        '''Setzt einen Trigger für die Ausgabedateien.'''
        if triggerNum == self.__lastTrigger: 
            return
        self.__lastTrigger = triggerNum
        trigger = core.getTime(), triggerNum
        self.__buffer.append(trigger)

        
    def setBuffersize(self, buffsize):
        '''Setzt die Puffergröße neu.'''
        self.__buffersize = buffsize
        firstPos = len(self.__buffer) - self.__buffersize
        if firstPos > 0:
            self.__buffer = self.__buffer[firstPos:]
    
    
    def getCurrentPoint(self):
        '''Gibt die aktuellste Gazedata zurück.'''
        return self.__buffer[-1]
    

    def __storeData(self):
        '''Schreibt die im Puffer seit der letzten speicherung angesammelten Daten in die Ausgabedateien.'''
        startItem = -1
        for i, entry in enumerate(self.__buffer):
            if entry[0] > self.__lastStoreTime:
                startItem = i
                break
        
        if startItem == -1:
            print "no gazedata to store!"
            return
        
        if not self.__outPickle:
            self.__openFiles()  #öffne jetzt erst die ausgabedateien, um nicht schon bei programmstart alles zu überschreiben
        if not self.__outPickle:
            return
        
        #nimm nur die neuen, noch nicht gespeicherten daten
        toStore = self.__buffer[startItem:]
        pickle.dump(toStore, self.__outPickle, -1)
        self.__outPickle.flush()

        #formatierung für plaintext ausgabe
        for entry in toStore:
            tick, data = entry
            if isinstance(data, int):#trigger
                plainTextData = "%f, %i\n" % (tick, data)
            else:#alles andere
                vl = data.validity_lefteye
                vr = data.validity_righteye
                lx = data.x_gazepos_lefteye 
                ly = data.y_gazepos_lefteye 
                rx = data.x_gazepos_righteye 
                ry = data.y_gazepos_righteye
                
                lx, ly = pyTetClient.tobiiToPsyCoord(lx, ly)
                rx, ry = pyTetClient.tobiiToPsyCoord(rx, ry)
                
                plainTextData = "%f %i %i %i %f %f %f %f\n" % (round(tick, 3), self.__lastTrigger, vl, vr, lx, ly, rx, ry) 
                self.__dataIndex[0][vl] += 1
                self.__dataIndex[1][vr] += 1
            self.__outPlain.write(plainTextData)
        
        self.__outPlain.flush()
        self.__lastStoreTime = self.__buffer[-1][0] #speichere die zeit
        
        
    def onGazeData(self, data):
        '''
        Wird aufgerufen, wenn der Tobii neue Daten errechnet und rausgeschickt hat.
        Diese Daten werden im Buffer gespeichert.
        '''
        self.__dataCount += 1
  
        if len(self.__buffer) >= self.__buffersize:
            self.__buffer.pop(0)
        self.__buffer.append((core.getTime(), data))

        if self.__storing:
            print "\n\nomg storing\n\n", core.getTime()
        if core.getTime() - self.__lastStoreTime > self.__dataSaveIntervall:
            self.__storing = True
            self.__storeData()
            self.__storing = False
        
        lx = data.x_gazepos_lefteye 
        ly = data.y_gazepos_lefteye 
        rx = data.x_gazepos_righteye 
        ry = data.y_gazepos_righteye
        
        lx, ly = pyTetClient.tobiiToPsyCoord(lx, ly)
        rx, ry = pyTetClient.tobiiToPsyCoord(rx, ry)
        
        avgX = (lx + rx) / 2
        avgY = (ly + ry) / 2
        
        if self.__showGazePoint:
            #passe posi der discs an
            #print "lx:%f\tly:%f\trx:%f\try:%f" % (lx, ly, rx, ry)
            self.__discAvg.setPosition(avgX, avgY)
            self.__discLeft.setPosition(lx, ly)
            self.__discRight.setPosition(rx, ry)
        
                
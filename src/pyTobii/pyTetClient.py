# -*- coding: iso-8859-15 -*-
'''
Created on 08.11.2010

@author: Oskar
'''

from comtypes.client import CreateObject, ShowEvents, GetEvents, PumpEvents
from threading import Thread, Event
import pyTobiiConfiguration
import pythoncom
import time
import GazeProcessor

class pyTetClient(Thread):
    '''
    Wrapperklasse für den TetClient.
    '''
    def __init__(self, eventSink = None):
        '''
        eventSink: "verbose" für detailierte Ausgaben, ansonsten eine Klasse wie VizEventSink (siehe unten)
        '''
        Thread.__init__(self)
        self.__run  = True
        self.__sink = eventSink
        self.daemon = True
        
        self.__initialized = Event()
        self.start()
        self.__initialized.wait()
        

    def run(self):
        pythoncom.CoInitialize()
        
        self.__tc = CreateObject("TobiiStudio.TetClient.2")
        if self.__sink == "verbose":
            eventProcessor = ShowEvents(self.__tc)
        else:
            eventProcessor = GetEvents(self.__tc, self.__sink)
        self.__initialized.set()
        while self.__run:   #pumpevents ist blockierend, aber wir möchten ja irgendwann das programm beenden können
            PumpEvents(0.5)
        del eventProcessor
        time.sleep(0.1)
        pythoncom.CoUninitialize()


    def stopEventProcessing(self):
        '''
        Beendet den TetClient.
        '''
        self.__run = False
        self.join(2)                #warte bis alles deaktiviert ist
        
    
    def AddCalibrationPoint(self, x, y, numGoodSamples, block):
        '''
        Fügt einen neuen Kalibrationspunkt hinzu, siehe TobiiSDK.
        '''
        result = False
        try:
            result = self.__tc.AddCalibrationPoint(x, y, numGoodSamples, block)
        except:
            pass
        return result


    def CalculateAndSetCalibration(self, *args):
        '''
        Berechnet eine neue Kalibration, siehe TobiiSDK.
        '''
        result = False
        try:
            result = self.__tc.CalculateAndSetCalibration(*args)
        except:
            pass
        return result


    def ClearCalibration(self, *args):
        '''
        Löscht die Kalibrierung, siehe TobiiSDK.
        '''
        result = False
        try:
            self.__tc.ClearCalibration(*args)
        except: pass
        return result


    def Connect(self, *args):
        '''
        Verbindet den TetClient mit dem TetServer, siehe TobiiSDK.
        '''
        result = False
        try:
            result = self.__tc.Connect(*args)
        except:
            pass
        return result


    def Disconnect(self, *args):
        '''
        Trennt den TetClient vom TetServer, siehe TobiiSDK.
        '''
        return self.__tc.Disconnect(*args)


    def GetCalibrationResult(self, *args):
        '''
        Gibt das Resultat der Kalibrierung wieder, siehe TobiiSDK.
        '''
        return self.__tc.GetCalibrationResult(*args)


    def GetNumPendingPostGazeData(self, *args):
        '''
        Siehe TobiiSDK.
        '''
        return self.__tc.GetNumPendingPostGazeData(*args)


    def GetSerialNumber(self, *args):
        '''
        Siehe TobiiSDK.
        '''
        return self.__tc.GetSerialNumber(*args)


    def GetTimeStamp(self, *args):
        '''
        Gibt den aktuellen TimeStamp des Tobii wieder. (data.sec, data.microsec) 
        '''
        return self.__tc.GetTimeStamp(*args)


    def InterruptAddCalibrationPoint(self, *args):
        '''
        Unterbricht das Hinzufügen eines Kalibrierungspunktes, siehe TobiiSDK.
        '''
        return self.__tc.InterruptAddCalibrationPoint(*args)


    def LoadCalibrationFromFile(self, *args):
        '''
        Lädt eine gespeicherte kalibrierung, siehe TobiiSDK.
        '''
        return self.__tc.LoadCalibrationFromFile(*args)


    def PerformSystemCheck(self, *args):
        '''
        Siehe TobiiSDK.
        '''
        return self.__tc.PerformSystemCheck(*args)


    def RemoveCalibrationPoints(self, *args):
        '''
        Siehe TobiiSDK.
        '''
        return self.__tc.RemoveCalibrationPoints(*args)


    def SaveCalibrationToFile(self, *args):
        '''
        Speichert die aktuelle Kalibrierung in eine Datei, siehe TobiiSDK.
        '''
        result = False
        try:
            result = self.__tc.SaveCalibrationToFile(*args)
        except:
            pass
        return result


    def StartTracking(self, *args):
        '''
        Beginnt das Tracking und somit das versenden der damit zusammenhängenden Events.
        '''
        result = False
        try:
            result = self.__tc.StartTracking(*args)
        except:
            pass
        return result


    def StopTracking(self, *args):
        '''
        Stoppt das Tracking.
        '''
        result = False
        try:
            result = self.__tc.StopTracking(*args)
        except:
            pass
        return result

    
    @property
    def GazeDataDelivery(self):
        return self.__tc.GazeDataDelivery
    
    @property
    def IsAddingCalibrationPoint(self):
        return self.__tc.IsAddingCalibrationPoint

    @property
    def IsConnected(self):
        return self.__tc.IsConnected

    @property
    def IsTracking(self):      
        return self.__tc.IsTracking

    @property
    def ServerAddress(self):       
        return self.__tc.ServerAddress

    @property
    def SynchronizationMode(self):    
        return self.__tc.SynchronizationMode

    @property
    def portNumber(self):
        return self.__tc.portNumber


def tobiiToPsyCoord(x, y):
    '''
    Rechnet die x, y-Koordinaten in die entsprechenden Vizard Koordinaten um.
    '''
    horizontal = pyTobiiConfiguration.calibPosis[8][0] - pyTobiiConfiguration.calibPosis[0][0]
    vertical = pyTobiiConfiguration.calibPosis[8][1] - pyTobiiConfiguration.calibPosis[0][1]
    x = horizontal * x + pyTobiiConfiguration.calibPosis[0][0]
    y = vertical * y + pyTobiiConfiguration.calibPosis[0][1]
    return x, y


def psyToTobiiCoord(x, y):
    '''
    Rechnet die x, y-Koordinaten in die entsprechenden Tobii Koordinaten um.
    '''
    horizontal = pyTobiiConfiguration.calibPosis[8][0] - pyTobiiConfiguration.calibPosis[0][0]
    vertical = pyTobiiConfiguration.calibPosis[8][1] - pyTobiiConfiguration.calibPosis[0][1]
    x = abs((x - pyTobiiConfiguration.calibPosis[0][0]) / horizontal)
    y = abs((y - pyTobiiConfiguration.calibPosis[0][1]) / vertical)
    return x, y


class MyEventSink:
    '''
    Diese Klasse dient comtypes.client.pumpevents als Eingabe. Sie empfängt die Nachrichten vom TetClient und sendet sie als viz-events weiter.
    '''
    gazeProcessor = None
    
    def __init__(self, gp):
        self.gazeProcessor = gp
        
        
    def DTetClientEvents_OnGazeData(self, this, gazeDataHolder, param):
        #print "Event: OnGazeData"
        data = gazeDataHolder.GetGazeData()
        self.gazeProcessor.onGazeData(data)
        #print str(data.timestamp_microsec)+" "+str(data.distance_lefteye)+" "+str(data.distance_righteye)
    
    
    def DTetClientEvents_OnPostGazeData(self, this, gazeDataHolder, param):
        print "Event: OnPostGazeData"
    
    
    def DTetClientEvents_OnCalibrationGazeData(self, this, gazeDataHolder, param):
        print "Event: OnCalibrationGazeData"
    
    
    def DTetClientEvents_OnPostCalibrationGazeData(self, this, gazeDataHolder, param):
        print "Event: OnPostCalibrationGazeData"
    
    
    def DTetClientEvents_OnTrackingStarted(self, this, param):
        print "Event: OnTrackingStarted"
    
    
    def DTetClientEvents_OnTrackingStopped(self, this, param):
        print "Event: OnTrackingStopped"
    
    
    def DTetClientEvents_OnAddCalibrationPointStarted(self, this, param):
        print "Event: OnAddCalibrationPointStarted"
    
    
    def DTetClientEvents_OnAddCalibrationPointEnded(self, this, param):
        print "Event: OnAddCalibrationPointEnded"

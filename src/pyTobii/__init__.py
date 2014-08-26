# -*- coding: iso-8859-15 -*-
'''
Created on 09.11.2010

@author: Oskar
'''

from GazeProcessor import GazeProcessor
from pyTobiiCalibrationVisualizer import pyTobiiCalibrationVisualizer
from pyTobiiCalibrator import pyTobiiCalibrator
import os
import pickle
import pyTetClient
import time
import pyTobiiConfiguration
from psychopy import core

_window         = None
_dataName       = ""
_filepath       = ""
_tc             = None
_eventSink      = None
_calibrator     = None
_calibVisualizer= None
_gazeProcessor  = None
_isTracking     = False
_isShowingGaze  = False
_isShowingCalibrationResultPoints = False
_isShowingCalibrationResultNet = False


def init(window, path, filename = ""):
    '''Initialisiert die nötigen Klassen.'''
    global _tc, _eventSink, _calibrator, _calibVisualizer, _gazeProcessor, _dataName, _window, _filepath
    
    _dataName = path + filename
    _filepath = path
    _window = window
    
    #blickdaten verarbeitung
    _gazeProcessor = GazeProcessor(_window)

    #event verarbeitung
    _eventSink = pyTetClient.MyEventSink(_gazeProcessor)
    
    #tetclient
    _tc = pyTetClient.pyTetClient(_eventSink)
    _tc.Connect(*pyTobiiConfiguration.connection)
    
    #kalibrierung
    _calibrator = pyTobiiCalibrator(_window, _tc)
    #kalibrierungsauswertung
    _calibVisualizer = pyTobiiCalibrationVisualizer(_window, _tc)
    

def setDataName(name):
    '''Setzt den Namen für alle Ausgaben (ohne Erweiterung).'''
    global _dataName
    #path = './Data/'       #dateipfad herausfinden
    path = _filepath
    if not os.path.isdir(path):
        os.mkdir(path)
    
    _dataName = path + name
    _gazeProcessor.updateFilename()


def checkForErrors():
    _gazeProcessor.checkErrors()
    

def getDataName():
    '''Gibt den Namen für alle Ausgaben zurück (ohne Erweiterung).'''
    return _dataName


def isTracking():
    '''Gibt zurück, ob Tobii gerade die Augen trackt.'''
    return _isTracking


def isShowingGaze():
    '''Gibt zurück, ob der Gazepoint gerade angezeigt wird.'''
    return _isShowingGaze


def isShowingCalibrationResultPoints():
    '''Gibt zurück, ob die Ergebnisse der Kalibrierung gerade als Punkte angezeigt werden.'''
    return _isShowingCalibrationResultPoints


def isShowingCalibrationResultNet():
    '''Gibt zurück, ob die Ergebnisse der Kalibrierung gerade als Netz angezeigt werden.'''
    return _isShowingCalibrationResultNet


def startTracking():
    '''Beginnt mit dem Tracking.'''
    global _isTracking
    _isTracking = True
    _tc.StartTracking()
    _gazeProcessor.updateFilename()


def stopTracking():
    '''Stoppt das Tracking.'''
    global _isTracking
    _isTracking = False
    _tc.StopTracking()
    _gazeProcessor.updateFilename()


def kill():
    '''Beendet alle Tobii-Prozesse.'''
    _tc.stopEventProcessing()
    
        
def calibrate(points = None, perfect = False, filename = ""):
    '''
    Startet den Kalibrierungsvorgang.
    Als Parameter müssen alle gewünschten Punkte in einer Liste übergeben werden, sonst wird die Config genutzt. ((x1,y1), (x2,y2))
    Falls 'perfect = True' übergeben wird, wird der Kalibrierungsvorgang solange bei fehlerhaften Punkten wiederholt, bis diese erfasst wurden.
    '''
    #zum kalibrieren das tracking stoppen
    wasTracking = isTracking()
    wasShowingDiscs = isShowingCalibrationResultPoints()
    wasShowingNet = isShowingCalibrationResultNet()
    if wasTracking:
        stopTracking()
    
    if not points: 
        points = pyTobiiConfiguration.calibPosis

    #alte kalibrierung entfernen
    path = _filepath
    if not os.path.isdir(path):
        os.mkdir(path)
        
    _calibrator.clearCalibration()
    if not filename:
        filename = str(_dataName) + ".cal"
    else:
        filename = path + filename
    print filename

    _calibrator.calibrate([points[4]], filename, fake = True)

    i = 1
    while True:
        _calibrator.calibrate(points, filename)
        
        points = _calibrator.getMissingPoints(points, filename)
        if not perfect or not points or i >= 5:       #sollen alle punkte abgedeckt werden und sind welche über, widerhole mit diesen punkten
            break
        i += 1

    #starte das tracking wieder, falls es vorher schon lief
    if wasTracking:
        startTracking()
    if wasShowingDiscs:
        if isinstance(wasShowingDiscs, bool): 
            wasShowingDiscs = None
        showCalibrationResultPoints(wasShowingDiscs)
    if wasShowingNet:
        if isinstance(wasShowingNet, bool): 
            wasShowingNet = None
        showCalibrationResultNet(wasShowingNet)


def showCalibrationResultPoints(filename = None):
    '''
    Zeigt das Ergebnis der letzten Kalibrierung in Punkten.
    Falls ein Dateiname übergeben wird, wird diese Kalibrierung geladen.
    '''
    global _isShowingCalibrationResultPoints
    if filename:
        #path = './Data/'       #dateipfad herausfinden
        path = _filepath
        if not os.path.isdir(path):
            os.mkdir(path)
        filename = path + filename

    _isShowingCalibrationResultPoints = filename or True
    wasTracking = isTracking()
    if not filename and wasTracking:
        stopTracking()
    _calibVisualizer.showResultPoints(filename)
    if wasTracking:
        startTracking()


def hideCalibrationResultPoints():
    '''Versteckt das Ergebnis der letzten Kalibrierung.'''
    global _isShowingCalibrationResultPoints
    _isShowingCalibrationResultPoints = False
    _calibVisualizer.hideResultPoints()


def showCalibrationResultNet(filename = None):
    '''
    Zeigt das Ergebnis der letzten Kalibrierung als Netz.
    Falls ein Dateiname übergeben wird, wird diese Kalibrierung geladen.
    '''
    global _isShowingCalibrationResultNet
    if filename:
        #path = './Data/'       #dateipfad herausfinden
        path = _filepath
        if not os.path.isdir(path):
            os.mkdir(path)
        filename = path + filename

    _isShowingCalibrationResultNet = filename or True
    wastracking = isTracking()
    if not filename and wastracking:
        stopTracking()
    _calibVisualizer.showResultNet(filename)
    if wastracking:
        startTracking()


def hideCalibrationResultNet():
    '''Versteckt das Ergebnis der letzten Kalibrierung.'''
    global _isShowingCalibrationResultNet
    _isShowingCalibrationResultNet = False
    _calibVisualizer.hideResultNet()

    
def showGazePoint():
    '''Zeigt den aktuell betrachteten Punkt auf dem Bildschirm.'''
    global _isShowingGaze
    if not isTracking():
        startTracking()
    _isShowingGaze = True
    _gazeProcessor.showGazePoint()
    
    
def hideGazePoint():
    '''Versteckt den aktuell betrachteten Punkt auf dem Bildschirm.'''
    global _isShowingGaze
    _isShowingGaze = False
    _gazeProcessor.hideGazePoint()
    

def setTrigger(triggerNum):
    '''Speichert in den Ausgabedaten den übergebenen Trigger ab.'''
    _gazeProcessor.setTrigger(triggerNum)
    

def loadGazeData(filename = None):
    '''
    Lädt gespeicherte gaze-daten.
    Da der Puffer nur alle 0.5sek geschrieben wird, müssen alle Daten wieder zusammengesetzt werden.
    Rückgabe: [(time, data/trigger)] 
    '''
    if not filename:
        filename = _dataName + ".pic"
    
    try:
        inp = open(filename, "rb")  #daten sind binär gespeichert
    except:
        return None
    
    allData = []
    while True:
        try:
            data = pickle.load(inp) #probiere nächsten abschnitt zu laden
        except EOFError:
            break
        except:
            import traceback;traceback.print_exc()
            break
        allData.extend(data)    #füge abschnitt allem bisherigen hinzu
    
    inp.close()
    return allData


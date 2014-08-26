# -*- coding: iso-8859-15 -*-
'''
Created on 09.11.2010

@author: oskar
'''
from pyTobiiImports import TobiiConstants

fixationColor               = [-1, -1, -1]           #farbe des fixationskreuzes

calibPosis                  = [[-20.0, 13.0],     #links oben
                               [0, 13.0],      #mitte oben
                               [20.0, 13.0],      #rechts oben
                               [-20.0, 0],     #links mitte 
                               [0, 0],      #mitte mitte
                               [20.0, 0],      #rechts mitte
                               [-20.0, -13.0],    #links unten
                               [0, -13.0],     #mitte unten
                               [20.0, -13.0]]     #rechts unten

#verbindungsinfo f�r den tobii
connection                  = "localhost", TobiiConstants.TetConstants_DefaultServerPort, TobiiConstants.TetSynchronizationMode_Local

#puffergr��e und speicherintervall f�r blickdaten
gazeProcessorBuffersize     = 50*5      #5 sekunden
dataSaveIntervall           = 0.5       #alle wieviel sekunden daten rausgeschrieben werden 

#discs werden zur anzeige der kalibrations-, kamera-, und blickdaten genutzt
discRadius                  = 0.5    #radius in cm

#calibrationseisntellungen
calibrationNumGoodSamples   = 6     #anzahl der brauchbaren samples f�r die config (siehe handbuch)
calibrationShrinkSpeed      = 0.5   #wie lange das quadrat kleiner wird 
calibrationQuadSize         = 3  #gr��e der calibrierungsquadrate vor dem klein werden
calibrationCrossSize        = 0.3 #l�nge jedes kreuzstriches

leftColor = 0, 1, 0
rightColor = 1, 0, 0
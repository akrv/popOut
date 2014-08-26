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

#verbindungsinfo für den tobii
connection                  = "localhost", TobiiConstants.TetConstants_DefaultServerPort, TobiiConstants.TetSynchronizationMode_Local

#puffergröße und speicherintervall für blickdaten
gazeProcessorBuffersize     = 50*5      #5 sekunden
dataSaveIntervall           = 0.5       #alle wieviel sekunden daten rausgeschrieben werden 

#discs werden zur anzeige der kalibrations-, kamera-, und blickdaten genutzt
discRadius                  = 0.5    #radius in cm

#calibrationseisntellungen
calibrationNumGoodSamples   = 6     #anzahl der brauchbaren samples für die config (siehe handbuch)
calibrationShrinkSpeed      = 0.5   #wie lange das quadrat kleiner wird 
calibrationQuadSize         = 3  #größe der calibrierungsquadrate vor dem klein werden
calibrationCrossSize        = 0.3 #länge jedes kreuzstriches

leftColor = 0, 1, 0
rightColor = 1, 0, 0
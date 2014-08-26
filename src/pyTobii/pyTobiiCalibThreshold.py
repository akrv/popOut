'''
Created on 25.08.2014

@author: Aswin
'''

import numpy as np

class CalibratorThreshold:
    
    def __init__(self):
#         self.pyTobiiCalibrationVisualizer = pyTobiiCalibrationVisualizer.pyTobiiCalibrationVisualizer()
#         self.pyTobiiCalibrationVisualizer.processCalib(filename)
#        self.calibDataPoints = self.pyTobiiCalibrationVisualizer.calibData
        self.thresholdDistance = 5 #units
        self.thresCheck = {}
        
    def thresholdCheck(self,filename):
        try:
            calib = self.__tc.GetCalibrationResult(filename)
        except:
            raise Exception("Error in thresholdCheck(): A calibration must be set.")
        for i in range(calib.size):
            curData = calib.GetAt(i)
            if not (curData.leftValidity == 1 == curData.rightValidity): continue

            
            key = round(curData.truePointX, 2), round(curData.truePointY, 2)          
            value = curData.leftMapX, curData.leftMapY, curData.rightMapX, curData.rightMapY
            
            calibPointX = (curData.leftMapX + curData.rightMapX)/2
            calibPointY = (curData.leftMapY + curData.rightMapY)/2
            truePointX = curData.truePointX
            truePointY = curData.truePointY
            distCalibPoints = np.sqrt(((truePointX - calibPointX)*(truePointX - calibPointX))-((truePointY - calibPointY)*(truePointY - calibPointY)))
            if distCalibPoints < self.thresholdDistance:
                self.thresCheck[key].append(True)
            else:
                self.thresCheck[key].append(False)
        return len(set(distCalibPoints.values()))==True
            
            
#         if distCalibPoints >= self.thresholdDistance:
#             self.reCalibration = True
            
        
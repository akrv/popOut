# -*- coding: iso-8859-15 -*-
'''
Created on 08.11.2010

@author: Oskar
'''
from ctypes import *

class TobiiConstants:
    TetCalibPointSize_Large       =1          # from enum TetCalibPointSize
    TetCalibPointSize_Medium      =2          # from enum TetCalibPointSize
    TetCalibPointSize_Small       =3          # from enum TetCalibPointSize
    TetCalibPointSpeed_Fast       =1          # from enum TetCalibPointSpeed
    TetCalibPointSpeed_Medium     =3          # from enum TetCalibPointSpeed
    TetCalibPointSpeed_MediumFast =2          # from enum TetCalibPointSpeed
    TetCalibPointSpeed_MediumSlow =4          # from enum TetCalibPointSpeed
    TetCalibPointSpeed_Slow       =5          # from enum TetCalibPointSpeed
    TetCalibType_Calib            =1          # from enum TetCalibType
    TetCalibType_Recalib          =2          # from enum TetCalibType
    TetConstants_DefaultServerPort=4455       # from enum TetConstants
    TetEye_Both                   =3          # from enum TetEye
    TetEye_Left                   =1          # from enum TetEye
    TetEye_Right                  =2          # from enum TetEye
    TetGazeDataDelivery_Post      =4          # from enum TetGazeDataDelivery
    TetGazeDataDelivery_RealTime  =2          # from enum TetGazeDataDelivery
    ITF_E_CALIBMANAGER_CALIBNOTINIT=-2147220224 # from enum TetHResults
    ITF_E_CALIBMANAGER_FATALINTERNALERROR=-2147220222 # from enum TetHResults
    ITF_E_CALIBMANAGER_INVALIDPARAMETER=-2147220223 # from enum TetHResults
    ITF_E_CALIBPLOT_FATALINTERNALERROR=-2147220350 # from enum TetHResults
    ITF_E_CALIBPLOT_INVALIDPARAMETER=-2147220351 # from enum TetHResults
    ITF_E_CALIBPLOT_MANAGERNOTSET =-2147220352 # from enum TetHResults
    ITF_E_CALIBPROC_CALIBRES_FAILED=-2147220472 # from enum TetHResults
    ITF_E_CALIBPROC_CALIBRES_INTERRUPTED=-2147220471 # from enum TetHResults
    ITF_E_CALIBPROC_FATALINTERNALERROR=-2147220473 # from enum TetHResults
    ITF_E_CALIBPROC_INVALIDOPERATION=-2147220474 # from enum TetHResults
    ITF_E_CALIBPROC_INVALIDPARAMETER=-2147220475 # from enum TetHResults
    ITF_E_CALIBPROC_ISCALIBRATING =-2147220480 # from enum TetHResults
    ITF_E_CALIBPROC_ISNOTCALIBRATING=-2147220479 # from enum TetHResults
    ITF_E_CALIBPROC_MONITORNOTFOUND=-2147220478 # from enum TetHResults
    ITF_E_CALIBPROC_WINDOWNOTVISIBLE=-2147220476 # from enum TetHResults
    ITF_E_CALIBPROC_WINDOWVISIBLE =-2147220477 # from enum TetHResults
    ITF_E_CLIENT_ASYNCSTATE       =-2147220859 # from enum TetHResults
    ITF_E_CLIENT_CONNECTED        =-2147220864 # from enum TetHResults
    ITF_E_CLIENT_FATALINTERNALERROR=-2147220861 # from enum TetHResults
    ITF_E_CLIENT_INTERNALTIMEOUT  =-2147220860 # from enum TetHResults
    ITF_E_CLIENT_NOTCONNECTED     =-2147220863 # from enum TetHResults
    ITF_E_CLIENT_NOTTRACKING      =-2147220856 # from enum TetHResults
    ITF_E_CLIENT_STOPTRACKING     =-2147220862 # from enum TetHResults
    ITF_E_CLIENT_TRACKING         =-2147220859 # from enum TetHResults
    ITF_E_CLIENT_TTIMENOTSUPPORTED=-2147220858 # from enum TetHResults
    ITF_E_FAIL                    =-2147467259 # from enum TetHResults
    ITF_E_TET_CALIBABORTED        =-2147220964 # from enum TetHResults
    ITF_E_TET_CALIBINCOMPATIBLEDATAFORMAT=-2147220982 # from enum TetHResults
    ITF_E_TET_CALIBINSUFFICIENTDATA=-2147220981 # from enum TetHResults
    ITF_E_TET_CALIBNODATASET      =-2147220980 # from enum TetHResults
    ITF_E_TET_CAMERA              =-2147220985 # from enum TetHResults
    ITF_E_TET_CANNOTGETTLS        =-2147220969 # from enum TetHResults
    ITF_E_TET_CONFIGKEYNOTPRESENT =-2147220972 # from enum TetHResults
    ITF_E_TET_CONFIGKEYREADONLY   =-2147220971 # from enum TetHResults
    ITF_E_TET_DIODE               =-2147220984 # from enum TetHResults
    ITF_E_TET_FILEOPEN            =-2147220989 # from enum TetHResults
    ITF_E_TET_FILEREAD            =-2147220988 # from enum TetHResults
    ITF_E_TET_INCOMPATIBLESERVERVERSION=-2147220978 # from enum TetHResults
    ITF_E_TET_INTERNAL            =-2147220987 # from enum TetHResults
    ITF_E_TET_INVALIDSTATE        =-2147220979 # from enum TetHResults
    ITF_E_TET_LOCKEDSYSTEM        =-2147220983 # from enum TetHResults
    ITF_E_TET_MEMORY              =-2147220986 # from enum TetHResults
    ITF_E_TET_MISSINGDNSSDDLL     =-2147220960 # from enum TetHResults
    ITF_E_TET_MISSINGFIREWIRE     =-2147220974 # from enum TetHResults
    ITF_E_TET_MISSINGPROTOCOLEXTENSIONS=-2147220968 # from enum TetHResults
    ITF_E_TET_MISSINGUSBORSERIAL  =-2147220973 # from enum TetHResults
    ITF_E_TET_NOPRODUCTCONNECTED  =-2147220975 # from enum TetHResults
    ITF_E_TET_NOSUCHLOGGINGCHANNEL=-2147220970 # from enum TetHResults
    ITF_E_TET_NOTSUPPORTED        =-2147220967 # from enum TetHResults
    ITF_E_TET_PROBINGHARDWARE     =-2147220976 # from enum TetHResults
    ITF_E_TET_PROTOCOLEXTENSIONNOTSUPPORTED=-2147220966 # from enum TetHResults
    ITF_E_TET_SERVERCOMMUNICATION =-2147220990 # from enum TetHResults
    ITF_E_TET_SERVERISNOTCONNECTED=-2147220991 # from enum TetHResults
    ITF_E_TET_UNAUTHORIZED        =-2147220965 # from enum TetHResults
    ITF_E_TET_UNKNOWNAUTHALGORITHM=-2147220962 # from enum TetHResults
    ITF_E_TET_UNKNOWNAUTHREALM    =-2147220963 # from enum TetHResults
    ITF_E_TET_UNKNOWNEXPERIMENT   =-2147220961 # from enum TetHResults
    ITF_E_TET_UNKNOWNORINVALIDPARAMETER=-2147220977 # from enum TetHResults
    ITF_E_TRACKSTATUS_FATALINTERNALERROR=-2147220607 # from enum TetHResults
    ITF_E_TRACKSTATUS_INVALIDPARAMETER=-2147220608 # from enum TetHResults
    ITF_S_OK                      =0          # from enum TetHResults
    TetNumCalibPoints_2           =1          # from enum TetNumCalibPoints
    TetNumCalibPoints_5           =2          # from enum TetNumCalibPoints
    TetNumCalibPoints_9           =3          # from enum TetNumCalibPoints
    TetProtocolExtension_All      =65535      # from enum TetProtocolExtension
    TetProtocolExtension_Authorize=32         # from enum TetProtocolExtension
    TetProtocolExtension_Configuration=4          # from enum TetProtocolExtension
    TetProtocolExtension_Experimental=16         # from enum TetProtocolExtension
    TetProtocolExtension_FrameRate=128        # from enum TetProtocolExtension
    TetProtocolExtension_HotPlug  =2          # from enum TetProtocolExtension
    TetProtocolExtension_Logging  =8          # from enum TetProtocolExtension
    TetProtocolExtension_Naming   =64         # from enum TetProtocolExtension
    TetProtocolExtension_None     =0          # from enum TetProtocolExtension
    TetProtocolExtension_PayPerUse=256        # from enum TetProtocolExtension
    TetProtocolExtension_PowerState=1          # from enum TetProtocolExtension
    TetSynchronizationMode_Local  =3          # from enum TetSynchronizationMode
    TetSynchronizationMode_None   =1          # from enum TetSynchronizationMode
    TetSynchronizationMode_Server =2          # from enum TetSynchronizationMode


class Point(Structure):
    _fields_ = [("x", c_double),
                ("y", c_double),
                ("z", c_double)]

class InitValues(Structure):
    _fields_ = [("width",   c_float),
                ("height",  c_float),
                ("distance",c_float)]

class Threshold(Structure):
    _fields_ = [("SBDeg", c_float),
                ("SEDeg", c_float)]
    
class TetCalibAnalyzeData(Structure):
    _fields_ = [("truePointX",      c_float),
                ("truePointY",      c_float),
                ("leftMapX",        c_float),
                ("leftMapY",        c_float),
                ("rightMapX",       c_float),
                ("rightMapY",       c_float),
                ("leftValidity",    c_long),
                ("rightValidity",   c_long)]

class TetGazeData(Structure):
    _fields_ = [("diameter_pupil_lefteye",  c_float),
                ("diameter_pupil_righteye", c_float),
                ("distance_lefteye",        c_float),
                ("distance_righteye",       c_float),
                ("timestamp_microsec",      c_long),
                ("timestamp_sec",           c_long),
                ("validity_lefteye",        c_long),
                ("validity_righteye",       c_long),
                ("x_camerapos_lefteye",     c_float),
                ("x_camerapos_righteye",    c_float),
                ("x_gazepos_lefteye",       c_float),
                ("x_gazepos_righteye",      c_float),
                ("y_camerapos_lefteye",     c_float),
                ("y_camerapos_righteye",    c_float),
                ("y_gazepos_lefteye",       c_float),
                ("y_gazepos_righteye",      c_float)]

'''
validity:
0 - The eye tracker is certain that the data for this eye is right. There is no risk of
    confusing data from the other eye.
1 - The eye tracker has only recorded one eye, and has made some assumptions and
    estimations regarding which is the left and which is the right eye. However, it is still
    very likely that the assumption made is correct. The validity code for the other eye is
    in this case always set to 3.
2 - The eye tracker has only recorded one eye, and has no way of determining which
    one is left eye and which one is right eye. The validity code for both eyes is set to 2.
3 - The eye tracker is fairly confident that the actual gaze data belongs to the other
    eye. The other eye will always have validity code 1.
4 - The actual gaze data is missing or definitely belonging to the other eye.
'''
# -*- coding: iso-8859-15 -*-

import pyTobiiConfiguration
from psychopy import visual

class Cross:
    def __init__(self, window, width = 1, color = [-1,-1,-1]):
        self.__window       = window
        self.__width        = width
        self.__color        = color
        self.__scale        = 1
        
        x = visual.Line(win=self.__window, lineColor = self.__color, lineColorSpace='rgb', start=[self.__scale*(-1)*self.__width/2.0, 0], end=[self.__scale*self.__width/2.0, 0], interpolate=False)
        y = visual.Line(win=self.__window, lineColor = self.__color, lineColorSpace='rgb', start=[0, self.__scale*(-1)*self.__width/2.0], end=[0, self.__scale*self.__width/2.0], interpolate=False)
        self.__cross        = [x,y]

     
    def draw(self):
        self.__cross[0].draw()
        self.__cross[1].draw()


    def setPosition(self, posx, posy):
        self.__cross[0].pos = (posx, posy)
        self.__cross[1].pos = (posx, posy)

        
    def getPosition(self):
        return self.__cross[0].pos
    
    
    def color(self, color=None):
        if not color:
            return self.__color
        self.__color = color
        self.__cross[0].lineColor = color
        self.__cross[1].lineColor = color
    
    
    def scale(self, scale = None):
        if not scale:
            return self.__scale
        self.__scale = scale
        self.__cross[0].setStart([self.__scale*(-1)*self.__width/2, 0])
        self.__cross[0].setEnd([self.__scale*self.__width/2, 0])
        self.__cross[1].setStart([0, self.__scale*(-1)*self.__width/2])
        self.__cross[1].setEnd([0, self.__scale*self.__width/2])


    def setAutoDraw(self, val):
        self.__cross[0].setAutoDraw(val, False)
        self.__cross[1].setAutoDraw(val, False)



class Disc:
    def __init__(self, window, radius = -1, color = [-1,-1,-1]):
        self.__window       = window
        self.__radius       = radius == -1 and pyTobiiConfiguration.discRadius or radius
        self.__color        = color
        self.__scale        = 1
        
        self.__disc         = visual.Circle(win=self.__window, radius=self.__radius*self.__scale, lineColor=self.__color, lineColorSpace='rgb', fillColor=self.__color, fillColorSpace='rgb', interpolate=False)
        
    
    def draw(self): 
        self.__disc.draw()
        
        
    def setPosition(self, posx, posy):
        self.__disc.pos = (posx, posy)

        
    def getPosition(self):
        return self.__disc.pos
    
    
    def color(self, color=None):
        if not color:
            return self.__color
        self.__color = color
        self.__disc.fillColor = color
        self.__disc.lineColor = color
        
        
    def scale(self, scale = None):
        if not scale:
            return self.__scale
        self.__scale = scale
        self.__disc.setRadius(self.__radius*self.__scale)
        
        
    def copy(self):
        ret = Disc(self.__window, self.__radius, self.__color)
        ret.scale(self.scale())
        return ret
    
    
    def setAutoDraw(self, val):
        self.__disc.setAutoDraw(val, False)
        
        
        
class Quad:
    def __init__(self, window, width = -1, color = None):
        self.__window       = window
        self.__width        = width == -1 and pyTobiiConfiguration.calibrationQuadSize*3 or width
        self.__color        = color == None and pyTobiiConfiguration.fixationColor or color
        self.__scale        = 1
        
        self.__quad         = visual.Rect(win=self.__window, width=self.__width*self.__scale, height=self.__width*self.__scale, lineColor=self.__color, lineColorSpace='rgb', fillColor=self.__color, fillColorSpace='rgb', interpolate=False)
        
    
    def draw(self): 
        self.__quad.draw()
        
        
    def setPosition(self, posx, posy):
        self.__quad.pos = (posx, posy)

        
    def getPosition(self):
        return self.__quad.pos
    
    
    def color(self, color=None):
        if not color:
            return self.__color
        self.__color = color
        self.__quad.fillColor = color
        self.__quad.lineColor = color
        
        
    def scale(self, scale = None):
        if not scale:
            return self.__scale
        self.__scale = scale
        self.__quad.setWidth(self.__width*self.__scale)
        self.__quad.setHeight(self.__width*self.__scale)
        
        
    def setAutoDraw(self, val):
        self.__quad.setAutoDraw(val, False)
        
        
# -*- coding: iso-8859-15 -*-
'''
Created on 19.05.2014

@author: Aswin
'''
from __future__ import division
from psychopy import visual, core, event, monitors
import datetime
import numpy as np
import os
import pyTobii as tobii
import random
from collections import Counter


class Exp():
    def __init__ (self,config,resume):
        self.config = config
        self.resume = resume
        self.positions = self.config.xys
        self.counter = self.config.counter
        self.waitForKeys = True
        mon = monitors.Monitor('myMonitor')
        self.window = visual.Window(size=mon.getSizePix(), color=(1,1,1), colorSpace='rgb', fullscr=True, monitor=mon, units='cm')
        self.window.mouseVisible = False
        self.resultData = np.zeros(shape = (360,7),dtype=np.float64)
        if self.resume:
            self.loadExistingData()
        
        fixationX = visual.Line(win=self.window, lineColor=(-1,-1,-1), lineColorSpace='rgb', start=(-0.5,0), end=(0.5,0),lineWidth = 2.5, interpolate=False)
        fixationY = visual.Line(win=self.window, lineColor=(-1,-1,-1), lineColorSpace='rgb', start=(0,-0.5), end=(0,0.5),lineWidth = 2.5, interpolate=False)
        self.fixation = [fixationX, fixationY]
        
        
        self.text1 = visual.TextStim(win=self.window, text='Ist', color=(-1,-1,-1), colorSpace='rgb', height=2, bold=True, wrapWidth=50, pos=(0.0, 2))
        self.text3 = visual.TextStim(win=self.window, text='im folgenden Bild enthalten?', color=(-1,-1,-1), colorSpace='rgb', height=2, bold=True, wrapWidth=50, pos=(0.0, -2.0))
        
        
        imgStart1 = visual.SimpleImageStim(win=self.window, image="..\\img\\auftrag1.png")
        imgStart2 = visual.SimpleImageStim(win=self.window, image="..\\img\\aufgabe2.png")
        imgPractice1 = visual.SimpleImageStim(win=self.window, image="..\\img\\training1.png")
        imgExperiment = visual.SimpleImageStim(win=self.window, image="..\\img\\Versuch.jpg")
        thankyou = visual.SimpleImageStim(win=self.window, image="..\\img\\danke.jpg")
        
        # block slides
        block1 = visual.SimpleImageStim(win=self.window, image="..\\img\\Block_1.jpg")
        block2 = visual.SimpleImageStim(win=self.window, image="..\\img\\Block_2.jpg")
        block3 = visual.SimpleImageStim(win=self.window, image="..\\img\\Block_3.jpg")
        block4 = visual.SimpleImageStim(win=self.window, image="..\\img\\Block_4.jpg")
        block5 = visual.SimpleImageStim(win=self.window, image="..\\img\\Block_5.jpg")
        block6 = visual.SimpleImageStim(win=self.window, image="..\\img\\Block_6.jpg")
        
        'creating the stimulus'
        self.redCircle = visual.ImageStim(win=self.window, image="..\\img\\shapes_13.jpg", units = "cm", pos=(0,0), size = 3.4, contrast=1.0)
        self.greenCircle = visual.ImageStim(win=self.window, image="..\\img\\shapes_11.jpg", units = "cm", pos=(0,0), size = 3.4, contrast=1.0)
        self.redTriangle = visual.ImageStim(win=self.window, image="..\\img\\shapes_15.jpg", units = "cm", pos=(0,0), size = 3.4, ori = -90, contrast=1.0)
        self.greenTriangle = visual.ImageStim(win=self.window, image="..\\img\\shapes_17.png", units = "cm", pos=(0,0), size = 3.4, contrast=1.0)
        self.redSquare = visual.ImageStim(win=self.window, image="..\\img\\shapes_03.jpg", units = "cm", pos=(0,0), size = 3.4, contrast=1.0)
        self.greenSquare = visual.ImageStim(win=self.window, image="..\\img\\shapes_05.jpg", units = "cm", pos=(0,0), size = 3.4, contrast=1.0)
        self.greenRhombus = visual.ImageStim(win=self.window, image="..\\img\\shapes_07.jpg", units = "cm", pos=(0,0), size = 3.4, contrast=1.0)
        self.greenSquareOpen = visual.ImageStim(win=self.window, image="..\\img\\shapes_09.jpg", units = "cm", pos=(0,0), size = 3.4, contrast=1.0)
        self.star4 = visual.ImageStim(win=self.window, image="..\\img\\shapes_25.jpg", units = "cm", pos=(0,0), size = 3.4, contrast=1.0)
        self.star5 = visual.ImageStim(win=self.window, image="..\\img\\shapes_20.jpg", units = "cm", pos=(0,0), size = 3.4, contrast=1.0)
                
        self.instructions = {'start1': imgStart1,
                             'start2': imgStart2,
                             'practice1': imgPractice1,
                             'experiment': imgExperiment,
                             'danke': thankyou,
                             'block1': block1,
                             'block2': block2,
                             'block3': block3,
                             'block4': block4,
                             'block5': block5,
                             'block6': block6
                             }
        '''generating a dict with keys 1 to 60 of all the necessary images'''
        self.images = {} 
        for x in range(1,17):
            self.images[x] = self.redCircle
    
        x += 1
        self.images[x] = self.greenCircle
    
        for x in range (18,29):
            self.images[x] = self.redSquare
    
        for x in range (29,40):
            self.images[x] = self.greenSquare 
    
        x += 1
        self.images[x] = self.greenSquareOpen
    
        x += 1
        self.images[x] = self.greenRhombus 
    
        x += 1
        self.images[x] = self.redTriangle
    
        for x in range (43,59):
            self.images[x] = self.star4
    
        x += 1
        self.images[x] = self.star5
    
        x += 1
        self.images[x] = self.greenTriangle
        
        'tobii handling'
        tobiiFilename = str(self.config.subject)+'_tobii'
        if os.path.exists(self.config.outputFolder+"/vp"+str(self.config.subject)+"/"+tobiiFilename+".tob"):
            fileExists = True
            ext = 0
            while(fileExists):
                ext += 1
                tobiiFilename = str(self.config.subject)+'_tobii_'+str(ext)
                if not os.path.exists(self.config.outputFolder+"/vp"+str(self.config.subject)+"/"+tobiiFilename+".tob"):
                    fileExists = False
                    
                    
        #tobii.init(self.window, self.config.outputFolder+"/vp"+str(self.config.subject)+"/", tobiiFilename)
        #self.useTobii = True
        self.useTobii = False
        
    def TakeABreak(self):
        '''
        method called when the #blocks finished is 3.
        Its a simple method to countdown from 3 for every 60 seconds.
        core.wait(60) is used and the index in the for loop can be changed to increase the time of the break
        '''
        minsLeft = 3
        for y in range(0,3):
            breakText = 'PAUSE! \n' + str(minsLeft) + ' min'
            self.waitForKeys = False
            self.showCustomText(breakText)
            core.wait(60)
            
            minsLeft -= 1
            self.waitForKeys = True
        if self.useTobii:
            self.showCustomText("Kalibrierung")
            tobii.calibrate(perfect=True)
            tobii.showCalibrationResultNet()
            event.waitKeys()

        
     
    def showQuestionText(self, txt):
        '''
        This method will show the questions. The predefined text gives the question formation with the object of interest drawn dynamically.
        The object of interest for each trial is taken from the array self.config.questions in the predefined random order drawn from the dict self.config.orderBlock
        '''
        text2 = visual.TextStim(win=self.window, text= txt, color=(-1,-1,-1), colorSpace='rgb', height=2, bold=True, wrapWidth=50, pos=(0.0, 0.0))
        textObj = [self.text1, text2, self.text3]
        for text in textObj:
            text.draw()
        self.window.flip()
        #core.wait(self.config.questionDuration)
        key = event.waitKeys(keyList=['space','escape'])
        if key[0] == 'escape':
            self.quit()      
    
    def showCustomText(self,txt):
        '''
        Show any text by passing the variable to this method.
        This will be displayed in the middle of the screen.
        Method will wait for user input escape to quit and spacebar to proceed.
        '''
        text = visual.TextStim(win=self.window, text= txt, color=(-1,-1,-1), colorSpace='rgb', height=2, bold=True, wrapWidth=50, pos=(0.0, 0.0))
        text.draw()
        self.window.flip()
        if self.waitForKeys:
            key = event.waitKeys(keyList=['space','escape'])
            if key[0] == 'escape':
                self.quit()      
        
    def drawFixation(self):
        for f in self.fixation:
            f.draw()
        self.window.flip()
        core.wait(self.config.fixationDuration)
        
    def showImage(self, img):
        img.draw()
        self.window.flip()
        key = event.waitKeys(keyList=['space','escape'])
        if key[0] == 'escape':
            self.quit()

    def showAndSetImage(self,pointsPlot):
        for img in pointsPlot:
            self.counter += 1
            a = self.positions[self.counter - 1]
            self.images[img].setPos(a)
            self.images[img].draw()
        self.window.flip()
        self.counter = 0 
 
    def setImageFalse (self,imgIdx):
        
        if imgIdx == 0:
            self.greenCircle.setImage("..\\img\\shapes_13.jpg") #redCircle
        if imgIdx == 1:
            self.greenSquareOpen.setImage("..\\img\\shapes_05.jpg") #greenSqure
        if imgIdx == 2:
            self.greenRhombus.setImage("..\\img\\shapes_15.jpg") #redTriangle
        if imgIdx == 3:
            self.redTriangle.setImage("..\\img\\shapes_17.png") #greenTriangle
        if imgIdx == 4:
            self.star5.setImage("..\\img\\shapes_25.jpg") #star4

    def resetImageFalse (self,imgIdx):
        
        if imgIdx == 0:
            self.greenCircle.setImage("..\\img\\shapes_11.jpg") #redCircle
        if imgIdx == 1:
            self.greenSquareOpen.setImage("..\\img\\shapes_09.jpg") #greenSqure
        if imgIdx == 2:
            self.greenRhombus.setImage("..\\img\\shapes_07.jpg") #redTriangle
        if imgIdx == 3:
            self.redTriangle.setImage("..\\img\\shapes_15.jpg") #greenTriangle
        if imgIdx == 4:
            self.star5.setImage("..\\img\\shapes_20.jpg") #star4            
                 
    def tutorial(self):
        self.showImage(self.instructions["start1"])
        self.showImage(self.instructions["start2"])
        

     
    def practice(self):
        self.showImage(self.instructions["practice1"])
        order = range(0,10)
        self.trialPrac = 0
        random.shuffle(order)
        blockNoPrac = 0
        for y in order:
            
            if self.useTobii:
                tobii.setTrigger(self.trialPrac)
            self.showQuestionText(self.config.questions[self.config.questionIdxPrac[y,0]])
            if self.config.questionIdxPrac[y,1] == 0 :
                self.setImageFalse(self.config.questionIdxPrac[y,0])
            self.drawFixation()
            ''
            self.showAndSetImage(self.config.constellation[7])
            startTime = core.getTime()
            key = event.waitKeys(keyList=['y','n','escape'])
            ''
            if key[0] == 'escape':
                self.quit()
            'check for the answer'
            if key[0] == 'n' and self.config.questionIdxPrac[y,1] == 0:
                responsePrac = 1    
            if key[0] == 'y' and self.config.questionIdxPrac[y,1] == 1:
                responsePrac = 1
            else:
                responsePrac = 0
            
            'compute reaction time'
            reactionTimePrac = core.getTime() - startTime
            'details about the trial'
            objectTypePrac = self.config.questionIdxPrac[y,0]
            objectExistsPrac = self.config.questionIdxPrac[y,1]
            
            if self.save:
                self.resultData[self.trialPrac,:] = [self.config.subject, blockNoPrac, self.trialPrac, objectTypePrac, objectExistsPrac, responsePrac, reactionTimePrac]
                self.trialPrac += 1
                self.saveData()
                if self.resume:
                    self.resume = False

            self.resetImageFalse(self.config.questionIdxPrac[y,0])

    def runBlock (self,blockNo):
        """
        runBlock prepares the screen for that block.
        Plots the images required for the train.
        Sets the images that are true and at the end of the trail resets the image.
        Runs the trial and computes reactions time and logs the data to be written into the text file.
        self.resume is set to false in case it is true so that normal routine is followed after loadExistingData() method is called and initial values are reset to resume values
        blockNo is received by this method only for writing in the text file.
        """
        for y in self.orderBlock:

            if self.useTobii:
                tobii.setTrigger(self.trial)
            self.showQuestionText(self.config.questions[self.config.questionIdx[y,0]])
            #print self.trial
            if self.config.questionIdx[y,1] == 0 :
                self.setImageFalse(self.config.questionIdx[y,0])
            if self.useTobii:
                tobii.startTracking()
            self.drawFixation()
            self.showAndSetImage(self.config.constellation[blockNo])
            startTime = core.getTime() 
            key = event.waitKeys(keyList=['y','n','escape'])
            endTime = core.getTime()
            if self.useTobii:
                tobii.stopTracking()
            if key[0] == 'escape':
                '''Escape quits the program by calling the method self.quit()'''
                self.quit()
            
            if key[0] == 'n' and self.config.questionIdx[y,1] == 0:
                '''check for the answer NO is correct or not. If correct set 1 else 0'''
                self.response = 1    
            if key[0] == 'y' and self.config.questionIdx[y,1] == 1:
                '''check for the answer Yes is correct or not. If correct set 1 else 0'''
                self.response = 1
            else:
                self.response = 0
            
            'compute reaction time'
            reactionTime = endTime - startTime
            
            'details about the trial'
            objectType = self.config.questionIdx[y,0] # object type with 5 objects of interest. 0:Green Circle  1:OpenSquare 2:Rhombus 3:RedTriangle 4:Star(Five sided) 
            objectExists = self.config.questionIdx[y,1] # if the object exists in that trail. Can be used to evaluate it with the response.

            self.resetImageFalse(self.config.questionIdx[y,0])
            
            if self.save:
                self.resultData[self.trialIdx,:] = [self.config.subject, blockNo, self.trial, objectType, objectExists, self.response, reactionTime]
                self.trialIdx += 1
                self.trial += 1
                self.saveData()
                if self.resume:
                    self.resume = False
                    
                    
                    
    def showStat(self,statTime):
        '''
        Shows the statistics of the block. Total time elapsed from the start of the block and the number of correct answers
        '''
        
        blockData = self.resultData[self.trialIdx-60:self.trialIdx,:]
        correctAnswers = Counter(blockData[:,4] == blockData[:,5])
        amtAnswers = correctAnswers.values()
        amtAnswers.reverse()
        percentAnswers = round((amtAnswers[0] / 60) * 100, 2)
        amtAnswers = []
        statText = 'Zeit abgelaufen zu diesem Block:\t' + str(datetime.timedelta(seconds=statTime)) + '\n Prozent der richtigen Antworten:\t' + str(percentAnswers) + '%'
        self.showCustomText(statText)
        
        

        
    def run(self):
        
        if self.useTobii and not self.resume:
            
            self.showCustomText("Kalibrierung") 
            tobii.calibrate(perfect=True)
            tobii.showCalibrationResultNet()
            event.waitKeys()

        
        if not self.resume:
            self.trial = 1
            self.trialIdx = 0
            self.count = 1
            self.noOfBlocks = self.config.noOfBlocks
            random.shuffle(self.noOfBlocks)
            self.tutorial()
            self.save = False
            self.practice()
        
        if self.resume:
            self.save = True
            self.showCustomText("Versuch wird fortgesetzt")
            random.shuffle(self.noOfBlocks)
            if self.useTobii:
                self.showCustomText("Kalibrierung")
                tobii.calibrate(perfect=True)
                tobii.showCalibrationResultNet()
                event.waitKeys()
        self.showImage(self.instructions["experiment"])
        self.save = True
        
        
        
        for y in self.noOfBlocks:
            
            if not self.resume:
                self.orderBlock = self.config.orderBlock[y]
            
            if self.count == 4 and not self.resume:
                self.TakeABreak()
            blockName = 'block' + str(self.count)
            self.waitForKeys = True
            self.showImage(self.instructions[blockName])
            self.blockStartTime = core.getTime() #block starting time
            self.runBlock(y)
            self.blockEndTime = core.getTime() #block end time
            elapsedTime = self.blockEndTime - self.blockStartTime # time elapsed from the start till the end of the block
            self.showStat(elapsedTime)
            self.count += 1
        self.showImage(self.instructions["danke"])
        self.quit()
      
   
            

    def quit(self):
        self.window.close()
        
        if self.useTobii:
            tobii.stopTracking()
            tobii.kill()
            tobii._gazeProcessor.closeFiles()
        core.quit()
        
    def loadExistingData(self):
        exData = np.loadtxt(os.path.join(self.config.outputFolder, "vp"+str(self.config.subject), str(self.config.subject)+"_result_data.txt"), skiprows=1, dtype=np.float64)
        idx = np.nonzero(exData[:,1] != 0)[0]
        
        #if len(int(exData[idx[-1],2])) == 60*(len(self.noOfBlocksFinished)):
        # the above loop is to decide if the block is fully finished so that reset is not necessary for that block
        if np.size(idx) > 0:
            self.lastBlock = int(exData[idx[-1],1])
            self.resumeTrialIdx = int(exData[idx[-1],2])
            self.noOfBlocksFinished = np.unique(exData[idx,1])
            self.resumeNoOfBlocks = [x for x in self.config.noOfBlocks if x not in self.noOfBlocksFinished]
            self.noOfBlocks = np.append(self.resumeNoOfBlocks,self.lastBlock) 
            self.count = len(self.noOfBlocksFinished)
            self.trialIdx = (60*(len(self.noOfBlocksFinished)-1))
            self.trial = (60*(len(self.noOfBlocksFinished)-1)) +1
            self.orderBlock = self.config.orderBlock[self.lastBlock]
            self.resultData = exData
    
    def saveData(self):
        filename = os.path.join(self.config.outputFolder, "vp"+str(self.config.subject), str(self.config.subject)+"_result_data.txt")
        np.savetxt(filename,self.resultData,fmt='%-10.1i\t%-10.1i\t%-10.1i\t%-10.1i\t%-10.1i\t%-10.1i\t%-10.6f',
            delimiter='\t',header='Subject\tBlock\tTrial\tobjectType\tobjectExists\tresponse\treactionTime',comments='')
        
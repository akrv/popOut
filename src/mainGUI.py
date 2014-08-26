# -*- coding: iso-8859-15 -*-
"""
\mainpage PopOut Experiment using psychopy libraries

"""
from mainSeq import Exp
from mainConfig import Config

from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
import tkFont

import cPickle
import os


class GUI(Frame):
    """
    Class GUI starts the experiment runtime. 
    It creates a configuration box to add details and clicking the start button starts the program routine. 
    TKinter library is used for creating GUI interface for the dialogue box.
    """

    def __init__(self,parent):  
        """
        Initializes all the required variables. Default Python function
        """
        self.parent = parent
        self.configFile = "config.pkl" # 
        self.config = Config()
        self.loadConfig() # loads the configuration file from self.configFile
        
        self.startExpOnExit = False # Start experiment on exit of the dialogue box created by the GUI class. Set to True only after validating the inputs
        self.resume = False # Resume is used to continue in case the program crashes
        
        parent.columnconfigure(1, weight=1)       
        myFont = tkFont.Font(family="Arial", size=10, weight=tkFont.NORMAL)
        
        """
        Subject number is got as an input for every user who takes the experiment. 
        If the number is already found, it will be used to set self.resume.
        """
        self.labelSubject = Label(parent, text="VP", font=myFont)
        self.labelSubject.grid(row=0, column=0, sticky=W, padx=3, pady=3)

        self.subject = StringVar()
        self.inputSubject = Entry(parent, textvariable=self.subject, font=myFont)
        self.inputSubject.grid(row=0, column=1, sticky=W+E, padx=3, pady=3)
        
        
        """
        It helps the user to start the search from the centre of the screen for every question.
        """
        self.labelFixationDuration = Label(parent, text="Fixationsdauer [s]", font=myFont)
        self.labelFixationDuration.grid(row=9, column=0, sticky=W, padx=3, pady=3)
        
        self.fixationDuration = StringVar() # Fixation duration for centre bias that appears after every question. 
        self.inputFixationDuration = Entry(parent, textvariable=self.fixationDuration, font=myFont)
        self.inputFixationDuration.grid(row=9, column=1, sticky=W+E, padx=3, pady=3)
        self.fixationDuration.set(self.config.fixationDuration)
        
        
        #Question duration
#         self.labelQuestionDuration = Label(parent, text="Frage dauer [s]", font=myFont)
#         self.labelQuestionDuration.grid(row=10, column=0, sticky=W, padx=3, pady=3)
#          
#         self.questionDuration = StringVar()
#         self.inputQuestionDuration = Entry(parent, textvariable=self.questionDuration, font=myFont)
#         self.inputQuestionDuration.grid(row=10, column=1, sticky=W+E, padx=3, pady=3)
#         self.questionDuration.set(self.config.questionDuration)
        
        """
        Output folder for the experiment data.
        Two files will be saved, a text file with the details from the experiment
        .tob file which saves the eye data
        """
        self.labelOutputFolder = Label(parent, text="Ausgabeordner", font=myFont)
        self.labelOutputFolder.grid(row=14, column=0, sticky=W, padx=3, pady=3)
        
        self.frameFolder = Frame(parent)
        self.frameFolder.columnconfigure(0, weight=1)
        self.frameFolder.grid(row=14, column=1, sticky=W+E)
        
        self.outputFolder = StringVar()
        self.inputOutputFolder = Entry(self.frameFolder, textvariable=self.outputFolder, font=myFont)
        self.inputOutputFolder.grid(row=0, column=0, sticky=W+E, padx=3, pady=3)
        self.outputFolder.set(self.config.outputFolder)
        
        self.buttonOutputFolder = Button(self.frameFolder, text="Auswählen", font=myFont, command=self.getFolder, width=8)
        self.buttonOutputFolder.grid(row=0, column=1, sticky=E, padx=3, pady=3)
        
        """
        Start Button starts the experiment with the initial instructions.
        It also checks for the inputs to be valid. If they are not valid, the experiment routine is not started.
        """
        self.buttonStart = Button(parent, text="Start", font=myFont, command=self.exit, width=8)
        self.buttonStart.grid(row=15, column=0, sticky=W, padx=3, pady=3)
        

        
        
        
    def getFolder(self):
        """
        To set the output folder. The current directory is selected and set as the output folder. 
        Can be changed using the GUI browse option and set to a new folder.
        """
        folder = askdirectory(initialdir=".", title="Ausgabeordner für Experiment")
        if folder != "":
            self.outputFolder.set(folder)

    def loadConfig(self):
        """
        Loads configuration file from the folder
        """
        try:
            f = open(os.path.join(".",self.configFile),"rb")
            self.config = cPickle.load(f)
            f.close()          

            return True
        except:
            return False
        
    def saveConfig(self):
        """
        saveConfig saves the configuration
        """
        try:
            f = open(os.path.join(".",self.configFile),"wb")
            cPickle.dump(self.config,f)
            f.close()
            
            return True
        except:
            return False
        
    def checkInput(self):
        """
        Checks for the inputs if they are correct. When wrong, throws an exception.
        """
        errorString = ""
        try:
            subject = int(self.subject.get())
            if subject < 0:
                raise Exception()
        except:
            errorString += "Ungültige Vp-Nr.\n"
            
        try:
            fixD = float(self.fixationDuration.get())
            if fixD < 0:
                raise Exception()
        except:
            errorString += "Ungültige Fixationsdauer\n"
        
        try:
            folder = self.outputFolder.get()
            if not os.path.isdir(folder):
                raise Exception()
        except:
            errorString += "Ungültiger Ordner\n"
            
        if errorString == "":
            self.config.subject = subject
            self.config.fixationDuration = fixD
            self.config.outputFolder = folder
            
        return errorString

    def exit(self):
        """
        Return of error string contains if there are any errors in the input and shows them.
        If the inputs are correct, save the configuration using self.saveConfig()
        """
        errorMessage = self.checkInput()
        if errorMessage == "":
            self.saveConfig()
            if not os.path.exists(os.path.join(self.config.outputFolder, "vp"+str(self.config.subject))):
                os.makedirs(os.path.join(self.config.outputFolder, "vp"+str(self.config.subject)))
                self.startExpOnExit = True
            elif os.path.exists(os.path.join(self.config.outputFolder, "vp"+str(self.config.subject), str(self.config.subject)+"_result_data.txt")):
                ret = askquestion("Info", "Es wurden existierende Daten gefunden, Versuch fortsetzen?", icon=WARNING, type=YESNOCANCEL)
                if ret != 'cancel':
                    self.startExpOnExit = True
                if ret == 'yes':
                    self.resume = True
            else:
                self.startExpOnExit = True

            self.parent.destroy()
        else:
            showerror("Eingabefehler", errorMessage)

root = Tk() # starts Tk() library
root.wm_title("Konfiguration") # title for the GUI window
gui = GUI(root) # GUI(root) creates a instance of the GUI
root.mainloop() # refer Tkinter library

if gui.startExpOnExit:
    """
    experiment is started with self.resume set to True/False
    exp.run() is the instance that will be first executed.
    """
    exp = Exp(gui.config, gui.resume)
    exp.run()

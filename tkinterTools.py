"""
Angus Goody
tkinter module for SHED
module containing functions and classes for UI
"""

#--------Imports----------
from tkinter import *

#--------Classes----------

class mainFrame(Frame):
    """
    The MainFrame class is 
    based upton the tkinter
    frame class, it provides more 
    functionality and flexibility
    """
    def __init__(self,parent):
        Frame.__init__(self,parent)



class screenController(mainFrame):
    """
    Screen Controller
    will manage screens 
    in the program
    """
    def __init__(self,parent):
        mainFrame.__init__(self,parent)
        self.masterWindow=parent
        #Configure
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        #Attributes
        self.allScreens={}
        self.currentScreen=None

    def addScreen(self,screenObject):
        """
        Adds a Screen object to the screenController
        """
        #Place the screen
        screenObject.grid(row=0, column=0, sticky="nsew")
        #Add to dictionary
        self.allScreens[screenObject.name]=screenObject
        if self.currentScreen:
            self.showScreen(self.currentScreen)

    def showScreen(self,screenName):
        if screenName in self.allScreens:
            #Display
            self.allScreens[screenName].tkraise()
            #Update variable
            self.currentScreen=screenName

class screen(mainFrame):
    """
    A screen is area
    for content in a program
    """
    def __init__(self,master,name):
        mainFrame.__init__(self,master)
        #Attributes
        self.master=master
        self.name=name
        #Initalise with master
        self.master.addScreen(self)

    def show(self):
        """
        Method will show screen
        """
        self.master.showScreen(self.name)
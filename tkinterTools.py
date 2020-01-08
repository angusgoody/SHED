"""
Angus Goody
tkinter module for SHED
module containing functions and classes for UI
"""

#--------Imports----------
from tkinter import *

#--------Global Constants----------
globalButtonWidth=15
globalFont="system 13"
globalFontBig="system 16"

#--------Main Core Classes----------

class mainFrame(Frame):
    """
    The MainFrame class is 
    based upton the tkinter
    frame class, it provides more 
    functionality and flexibility
    """
    def __init__(self,parent):
        Frame.__init__(self,parent)

    def gridConfig(self,depth):
        """
        Will configure the columns
        and rows to a weight of 1 for
        the depth specified
        """
        for x in range(depth+1):
            self.grid_columnconfigure(x,weight=1)
            self.grid_rowconfigure(x,weight=1)

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
               
class advancedListbox(Listbox):
    """
    The advancedListbox is built on
    the tkinter listbox but offers
    built in methods to store objects
    etc
    """
    def __init__(self,parent):
        Listbox.__init__(self,parent)
        self.config(font="Avenir 15")

class mainTopLevel(Toplevel):
    """
    Core Top Level window
    that stays visible
    and in focus while in use
    """
    def __init__(self,root,title,**kwargs):
        Toplevel.__init__(self,root)
        #Variables
        self.master=root
        self.title=title
        #Configure window
        self.title=self.title
        self.geometry("400x300")

    def runWindow(self):
        """
        Running a window will
        set the program focus to the popup
        window so the user cannot interact with
        the program.
        """

        self.focus_set()
        self.grab_set()
        self.transient(self.master)
        self.resizable(width=False,height=False)

    def quit(self):
        """
        The quit method which
        will destroy the window
        and any saving etc.
        """
        self.destroy()
        
    
        
        
        


#--------Secondary Core Classes----------

class advancedLabel(Label):
    """
    The advancedLabel class
    is a modified label class 
    that offers more functionality
    """
    def __init__(self,parent,**kwargs):
        Label.__init__(self,parent,**kwargs)
        self.configure(font=globalFont)

class advancedEntry(Entry):
    """
    An advanced entry is a
    modified entry class and 
    can change colour and check
    for banned words etc
    """
    def __init__(self,parent):
        Entry.__init__(self,parent)
        self.config(font=globalFont,width=15)

#--------Child Classes----------

class dataSection(mainFrame):
    """
    The dataSection is a entry
    with a label for users
    to enter data
    """
    def __init__(self,parent,labelData):
        mainFrame.__init__(self,parent)
        self.labelText=StringVar()
        self.labelText.set(labelData)
        #Add Entry
        self.entry=advancedEntry(self)
        self.entry.grid(row=0,column=1,padx=5)
        #Add Label
        self.label=advancedLabel(self,textvariable=self.labelText)
        self.label.grid(row=0,column=0)

"""
Angus Goody
tkinter module for SHED
module containing functions and classes for UI
"""

#--------Imports----------
from tkinter import *
from tkinter import messagebox

#--------Global Constants----------
globalButtonWidth=15
globalFont="system 13"
globalFontBig="system 16"
globalFontTiny="system 9"
globalColours={
    "red":"#E58A8F",


}

#--------Functions----------

def showMessage(pre,message):
    """
    Function to show a tkinter
    message using messagebox
    """
    try:
        messagebox.showinfo(pre,message)
    except:
        print(message)
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
    An advanced listbox
    can store objects
    and has more functionality
    compared to a standard listbox
    """
    def __init__(self,parent):
        Listbox.__init__(self,parent)
        self.config(font=globalFontBig)
        self.objectDict={}
    def addObject(self,display,objectInstance):
        """
        Display data
        and have it reference an object
        """
        #Display
        self.insert(END,display)
        #Store
        self.objectDict[display]=objectInstance

    def getObject(self,name):
        """
        Will return the object
        given the name
        """
        if name in self.objectDict:
            return self.objectDict[name]

    def getCurrentItem(self):
        """
        Get the name of the item
        currently being selected
        """
        currentSelectionIndex=self.curselection()
        if len(currentSelectionIndex) > 0:
            return self.get(currentSelectionIndex[0])

    def getCurrentObject(self):
        """
        Return the object currently in
        selection
        """
        currentItem = self.getCurrentItem()
        if currentItem in self.objectDict:
            return self.objectDict[currentItem]

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

        #Store banned words
        self.bannedWords=["Bob","Angus"]
        self.blankAllowed=False
        self.contentValid=True
        self.reasonInvalid=""
        self.defaultColour=self.cget("bg")
        #Add the binding
        self.bind("<KeyRelease>",lambda event: self.checkContent())
        #Check content once to update
        self.checkContent()
        
    def checkContent(self):
        """
        Will check content of entry
        and change colour depending
        on if content is valid or not
        """
        entryContent=self.getContent().upper()
        #Check that there is content
        if len(entryContent.split()) < 1 and self.blankAllowed == False:
            self.contentValid=False
            self.reasonInvalid="Please enter something"
            self.configure(bg=self.defaultColour)
            return False
        #Check
        for item in self.bannedWords:
            if item.upper() == entryContent:
                self.contentValid=False
                self.reasonInvalid="This word is banned"
                self.configure(bg=globalColours["red"])
                return False
        self.resetSettings()

    def resetSettings(self):
        """
        Used to reset colour
        and variables, NOT content
        """
        self.configure(bg=self.defaultColour)
        self.contentValid=True
        self.reasonInvalid=""

    def getContent(self):
        """
        Will return the contents
        of the entry in plain 
        text
        """
        return self.get()

#--------Child Classes----------

class dataSection(mainFrame):
    """
    The dataSection is a entry
    with a label for users
    to enter data
    """
    def __init__(self,parent,labelData):
        mainFrame.__init__(self,parent)
        #Config
        self.labelText=StringVar()
        self.labelText.set(labelData)

        #Add Entry
        self.entry=advancedEntry(self)
        self.entry.grid(row=0,column=1,padx=5)
        #Add Label
        self.label=advancedLabel(self,textvariable=self.labelText)
        self.label.grid(row=0,column=0)

class buttonSection(mainFrame):
    """
    The ButtonSection is a frame
    that contains a row of buttons
    """
    def __init__(self,parent):
        mainFrame.__init__(self,parent)
        #Config
        self.gridConfig(0)
        #Store data
        self.buttonOrder=[]
        self.buttonDict={}
        #Add Center
        self.centerFrame=mainFrame(self)
        self.centerFrame.grid(row=0,column=0,pady=20)

    def addButton(self,name):
        """
        Add a button 
        to the frame
        """
        #Create the button
        newButton=Button(self.centerFrame,text=name,width=globalButtonWidth)
        #Display it
        newButton.grid(row=0,column=len(self.buttonOrder),padx=10)
        #Store it
        self.buttonOrder.append(name)
        self.buttonDict[name]=newButton

    def getButton(self,name):
        """
        Will return the button
        object given the name
        """
        if name in self.buttonDict:
            return self.buttonDict[name]
        

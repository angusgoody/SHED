"""
Angus Goody
tkinter module for SHED
module containing functions and classes for UI
"""

#--------Imports----------
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from shed.colourTools import getColourForBackground
#--------Global Constants----------
globalButtonWidth=15
globalFont="system 13"
globalFontBig="system 16"
gobalFontTitle="system 24"
globalFontMega="syetem 22"
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

def getAllChildren(widget):
    """
    Will recursivley get all the children
    of a widget
    """
    children=[]
    if "winfo_children" in dir(widget):
        for child in widget.winfo_children():
            children.append(child)
            results=getAllChildren(child)
            if results:
                children.extend(results)
    return children

def checkListInstanceOf(item,classList):
    """
    Will check if item belongs
    to any of the classes given
    in classlist
    """
    for i in classList:
        if isinstance(item,i):
            return True
    return False

def completeColour(widget,colour):
    """
    Will recursivley colour 
    a widget
    """
    allChildren=getAllChildren(widget)
    allChildren.append(widget)
    for child in allChildren:
        if "config" in dir(child):
            if "highlightbackground" in child.config() and checkListInstanceOf(child,[Frame,Label]) is False:
                print(type(child),"is background colour")
                child.config(highlightbackground=colour)
            else:
                try:
                    child.config(bg=colour)
                except Exception as e:
                    print("Error changing colour: ",e)
        if type(child) in [advancedLabel,Label]:
            newFg=getColourForBackground(colour)
            child.config(fg=newFg)

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

    def colour(self,colour):
        """
        Will recursivley change the
        colour of all the child
        widgets
        """
        completeColour(self,colour)

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
        self.config(font=globalFontMega)
        self.rowColour="#E1E0E2"
        self.rowCount=0
        self.objectDict={}
        #Add a scrollbar
        self.scrollBar=Scrollbar(self)
        self.scrollBar.pack(side=RIGHT,fill=Y)
        self.scrollBar.config(command=self.yview)
        self.config(yscrollcommand=self.scrollBar.set)
    
    def addObject(self,display,objectInstance):
        """
        Display data
        and have it reference an object
        """
        #Display
        paddedData=(" "*2)+str(display)
        self.insert(END,paddedData)
        self.rowCount+=1
        if self.rowCount % 2 == 0:
            self.itemconfig(END,bg=self.rowColour)
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
            return self.get(currentSelectionIndex[0]).lstrip()

    def getCurrentObject(self):
        """
        Return the object currently in
        selection
        """
        currentItem = self.getCurrentItem()
        if currentItem in self.objectDict:
            return self.objectDict[currentItem]

    def clear(self,**kwargs):
        """
        Will delete everything from
        the listbox and delete
        all objects stored

        retain = True: will keep objects
        """
        retain = kwargs.get("retain")
        #Delete everything
        self.delete(0,"end")
        if not(retain):
            #Clear all objects
            self.objectDict.clear()

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
        self.bannedWords=[]
        self.blankAllowed=False
        self.contentValid=True
        self.reasonInvalid=""
        self.defaultColour=self.cget("bg")
        #Add the binding
        self.bind("<KeyRelease>",lambda event: self.checkContent())
        #Check content once to update
        self.checkContent()
        
    def markInvalid(self):
        """
        Will change the colour to
        red to indicate a problem
        """
        self.configure(bg=globalColours["red"])

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
                self.markInvalid()
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

class advancedOptionMenu(OptionMenu):
    """
    Option Menu which allows
    the variable to accessed at any time
    """
    def __init__(self,parent,variable,*values,**kwargs):
        OptionMenu.__init__(self,parent,variable,*values,**kwargs)
        self.var=variable

class advancedTree(ttk.Treeview):
    """
    The advanced Tree class
    is a modified tree class
    which allows better control
    over colours and storing data
    etc
    """
    def __init__(self,parent,columns,**kwargs):
        ttk.Treeview.__init__(self,parent,show="headings",columns=columns)
        self.columns=columns
        for item in self.columns:
            self.addSection(item)
        #Add the scrollbar
        self.scroll=Scrollbar(self)
        self.scroll.pack(side=RIGHT,fill=Y)
        self.scroll.config(command=self.yview)
        self.config(yscrollcommand=self.scroll.set)

    def addSection(self,sectionName):
        """
        Add a section to the tree
        """
        self.column(sectionName,width=10,minwidth=45)
        self.heading(sectionName,text=sectionName)

    def insertData(self,values,tags):
        """
        Method to insert data into the treeview
        """
        #print("Inserting values",values)
        self.insert("" , 0,values=values,tags=tags)

    def addTag(self,tag,colour):
        self.tag_configure(tag,background=colour)

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
        self.label=advancedLabel(self,textvariable=self.labelText,width=14,anchor="w")
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
        
class optionMenuSection(mainFrame):
    """
    Similar to dataSection but
    optionMenu instead of entry
    """
    def __init__(self,parent,labelData):
        mainFrame.__init__(self,parent)
        #Config
        self.labelText=StringVar()
        self.labelText.set(labelData)
        #Add Label
        self.label=advancedLabel(self,textvariable=self.labelText)
        self.label.grid(row=0,column=0)
        #Add OptionMenu
        self.optionVar=StringVar()
        self.optionVar.set("None")
        self.optionMenu=advancedOptionMenu(self,self.optionVar,["None"])
        self.optionMenu.config(width=12)
        self.optionMenu.grid(row=0,column=1,padx=5)

class titleLabel(advancedLabel):
    """
    Label for displaying title sections
    """
    def __init__(self,parent,**kwargs):
        advancedLabel.__init__(self,parent,**kwargs)
        self.configure(font=gobalFontTitle)
        

class hiddenDataSection(dataSection):
    """
    Inherits from datasection but will
    have the ability to show and hide contents
    """
    def __init__(self,parent,labelData):
        dataSection.__init__(self,parent,labelData)
        #Conigure
        self.entry.config(show="•")
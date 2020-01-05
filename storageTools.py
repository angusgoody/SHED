
"""
Angus Goody
database module for SHED
module containing functions and classes for storing data
"""

#--------------Imports-----------
import os
import pickle
#--------------Functions-----------

#---Pickle---

def openPickle(fileName):
    """
    This function opens a pickle file
    and returns the content
    """
    try:
        content=pickle.load( open( fileName, "rb" ) )
    except Exception as e:
        print("No content found",e)
        return None
    else:
        return content

def savePickle(fileName,content):
    """
    This function will dump
    a pickle file to a directory
    """
    print("Dumping pickle with fileName...",fileName)
    pickle.dump(content, open( fileName, "wb" ) )

def writeFile(fileName,stringContent,mode):
    """
    Will write to file using plain text
    a = append
    w = write
    """
    file=open(fileName,mode)
    file.write(stringContent)
    file.close()

def readFile(fileName):
    """
    Will read contents from
    plain text file
    """
    try:
        content=open(fileName,"r")
    except Exception as e:
        print("Error opening file: ",e)
    else:
        return content
#---Directory Manipulation---

def getWorkingDirectory():
    """
    Will return the current working directory the program is in
    """
    return (os.path.dirname(os.getcwd()))

def createFileFolderPath(parentDir,folderOrFile):
    """
    Will take a parent directory
    and add the folder or file name to the end, this
    does not handle extensions
    """
    return os.path.join(parentDir,folderOrFile)

def createFolder(folderPath):
    """
    This function will create a folder
    in memory, if the folder already
    exists it will not create one
    """
    if not os.path.exists(folderPath):
        os.mkdir(folderPath)



#--------------Classes-----------

class smartDir:
    """
    A smart directory is a folder
    usually inside the datamanager
    that can save and retrieve files
    """
    def __init__(self,root,folderName):
        self.root=root
        self.folderName=folderName
        self.fullPath=createFileFolderPath(self.root,self.folderName)
        #Create location if it doesnt exist already
        createFolder(self.fullPath)

    def pickleData(self,fileName,content):
        """
        Will pickle the data to this
        smart directory
        """
        newPath=createFileFolderPath(self.fullPath,fileName)
        #Pickle
        savePickle(newPath,content)
        #Return path
        return newPath

    def unPickleData(self,baseName):
        """
        Will return the contents
        of the pickled file
        """
        newPath=createFileFolderPath(self.fullPath,baseName)
        return openPickle(newPath)


class dataManager(smartDir):
    """
    The Data manager will handle
    saving and retrieving all data
    for the program. It can create
    and save to folders and search
    for data.
    """
    def __init__(self,rootDir,name):
        smartDir.__init__(self,rootDir,name)
        self.name=name
        self.rootDir=rootDir
        self.subFolderDict={}

        #Find current folders
        self.findSubFolders()

    def findSubFolders():
        """
        Will scan root directory
        for sub folers
        """
        subFolders = [dI for dI in os.listdir('.') 
        if os.path.isdir(os.path.join('.',dI))]
        #Add each folder
        for folder in subFolders:
            self.addSubFolder(folder)

    def addSubFolder(folderName):
        """
        Will store a smart directory
        inside the data manager
        """
        #Create the smart directory
        newSmartDir=smartDir(self.rootDir,folderName)
        #Store smart directory
        self.subFolderDict[folderName]=newSmartDir

class projectManager:
    """
    The project manager
    will manage all project
    resources and settings
    """
    def __init__(self,rootDir,projectName):
        self.projectName=projectName
        self.rootDir=rootDir
        self.fileExtension=".txt"

        self.dataFolderName=projectName+" data"
        self.dataManager=dataManager(self.rootDir,
            self.dataFolderName)




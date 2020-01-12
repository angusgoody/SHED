
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
    return os.getcwd()

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
    print("Asked to create folder",folderPath)
    if not os.path.exists(folderPath):
        os.mkdir(folderPath)

def getAllFilesFromDir(directory,extension):
    """
    Will return the files with
    the extension from the given
    directory
    """
    results=[]
    for root, dirs, files in os.walk(directory):
        for file in files:
            #Add to list
            wholeFile=os.path.join(root,file)
            if file.endswith(extension):
                results.append(wholeFile)

    return results

def addExtensionToFile(fileName,extension):
    """
    Will add an extension to filename
    if there is not already one there.
    """
    if fileName.endswith(extension):
        return fileName
    else:
        return (fileName+extension)

def getFileWithoutExtension(fileName):
    return os.path.splitext(fileName)[0]

def getBasename(filePath):
    return os.path.basename(filePath)
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

    def privatePickleData(self,fileName,content):
        """
        Will pickle the data to this
        smart directory
        """
        newPath=createFileFolderPath(self.fullPath,fileName)
        #Pickle
        savePickle(newPath,content)
        #Return path
        return newPath

    def privateUnPickleData(self,baseName):
        """
        Will return the contents
        of the pickled file
        """
        newPath=createFileFolderPath(self.fullPath,baseName)
        return openPickle(newPath)

    def findFiles(self,extension):
        """
        Will search recursivley 
        for files inside the directory
        """
        return getAllFilesFromDir(self.fullPath,extension)

    def privateWriteFile(self,fileName,extension,content):
        """
        Will write file into the directory
        in plain text
        """
        #Create path
        fullPath = createFileFolderPath(self.fullPath,
            addExtensionToFile(fileName,extension))
        #Save the content
        writeFile(fullPath,content)

    def privateOpenFile(self,fileName):
        """
        Will open a plain txt file and
        return the contents
        """
        return openFile(createFileFolderPath(self.fullPath,fileName))

class dataManager(smartDir):
    """
    The Data manager will handle
    saving and retrieving all data
    for the program. It can create
    and save to folders and search
    for data.
    """
    def __init__(self,projectManager):
        smartDir.__init__(self,projectManager.projectRootDir,
            projectManager.dataFolderName)
        self.name=projectManager.dataFolderName
        self.rootDir=createFileFolderPath(projectManager.projectRootDir,self.name)
        self.projectManager=projectManager
        self.subFolderDict={}

        #Find current folders
        self.findSubFolders()

    def findSubFolders(self):
        """
        Will scan root directory
        for sub folers
        """
        subFolders = next(os.walk(self.rootDir))[1]
        #Add each folder
        for folder in subFolders:
            self.addSubFolder(folder)

    def addSubFolder(self,folderName):
        """
        Will store a smart directory
        inside the data manager
        """
        #Create the smart directory
        newSmartDir=smartDir(self.rootDir,folderName)
        #Store smart directory
        self.subFolderDict[folderName]=newSmartDir

    def pickleData(self,folder,fileName,content):
        """
        Will pickle data to a specified 
        folder, if the folder does not exist
        create one
        """
        #If the smart directory exists
        if folder in self.subFolderDict:
            self.subFolderDict[folder].privatePickleData(fileName,
                content)
        else:
            #Create one and call the function again
            self.addSubFolder(folder)
            self.pickleData(folder,fileName,content)

    def openPickle(self,folder,fileName):
        """
        Will open a pickle file
        in the specified directory
        """
        #Check folder exists
        if folder in self.subFolderDict:
            return self.subFolderDict[folder].privateUnPickleData(fileName)

class projectManager:
    """
    The project manager
    will manage all project
    resources and settings
    """
    def __init__(self,rootDir,projectName):
        self.projectName=projectName
        self.projectRootDir=rootDir
        self.dataFolderName=projectName+" data"
        self.dataManager=dataManager(self)
        #Store Template names
        self.userDataFolderName="UserData"
        self.fileExtension=".txt"

    def addFolder(self,folderName):
        """
        Will create a new smart folder in
        the data manager
        """
        self.dataManager.addSubFolder(folderName)

    def getFolder(self,folderName):
        """
        Will find the smart directory
        object and return in
        """
        if folderName in self.dataManager.subFolderDict:
            return self.dataManager.subFolderDict[folderName]
        else:
            print("Could not find core folder")
            return False

    def saveUserData(self,fileName,content):
        """
        Will take base file, add extension and
        then save it in the userDataFolderName folder,
        if this does not exist create it
        """
        #Create Filename with extension
        fullFileName=addExtensionToFile(fileName,self.fileExtension)
        #Save to this file
        self.dataManager.pickleData(self.userDataFolderName,fullFileName,content)

    def findAllFiles(self,extension):
        """
        Will locate all files
        in directory with extension
        """
        return getAllFilesFromDir(self.projectRootDir,extension)

    def findAllUserFiles(self):
        """
        Will locate all files with
        file extension
        """
        return self.findAllFiles(self.fileExtension)

    def loadAllUserFiles(self):
        """
        Will unpickle all the userdata
        and return it in a dictionary
        key = filename in dir
        value = object
        """
        allUserFiles=self.findAllUserFiles()
        contentDict={}
        for path in allUserFiles:
            path=getBasename(path)
            content=self.dataManager.openPickle(self.userDataFolderName,path)
            contentDict[getFileWithoutExtension(path)]=content
        return contentDict


        

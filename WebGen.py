import os
import re
import shutil

GEN = "GEN"
SRC = "SRC"

CSS = "CSS"
DATA = "Data"
TEMPLATES = "Templates"
GLOBALS = "Globals"

DELIMTER = "***"
Domain = "BurakBiyikli.com"

RunDir = os.getcwd() #Where The Shell is when the script is run
SaveDir = os.path.dirname(os.path.realpath(__file__)) #Saved Dir

GlobalSnippets = {}
GlobalSnippets["TestTag"] = "TestContent"

#Index is list of all pages
#CSS is list of all style sheets

#Take folder of txt files and process them into templates to be used
class Template():
	def __init__(self, FileName):
		self.Name = os.path.split(FileName)[1][:-4]
		self.SectionNames = [""]
		self.SectionSnippets = [""]
		self.tags = []
		self.processTemplateFile(FileName)
		
	def getName(self):
		return self.Name

	def processTemplateFile(self, FileName):
		try:
			with open(FileName, "r") as TemplateFile:
				Loc = 0
				for line in TemplateFile:
					if DELIMTER in line:
						LIndex = line.find(DELIMTER)+len(DELIMTER)
						RIndex = line.rfind(DELIMTER)
						if (LIndex == (RIndex+len(DELIMTER))):
							print("MALFORMED TEMPLATE!!! Line:"+line)
							print("MALFORMED TEMPLATE!!! File:"+FileName)
						Name = line[LIndex:RIndex]
						self.SectionNames.append( Name )
						self.SectionSnippets.append("")
						self.SectionNames.append("")
						self.SectionSnippets.append("")
						Loc = Loc + 2
					else:
						self.SectionSnippets[Loc] = "".join([self.SectionSnippets[Loc],line])
				TemplateFile.close()
		except:
			print("TEMPLATE READ FAILED!!! Failure processing "+FileName)
			print(self.SectionNames)

		
		for tag in self.SectionNames:
			if (tag!=""):
				self.tags.append(tag)

	def populateTemplate(self, GlobalSnippets, FileSnippets):
		for t in self.tags:
			if( t!="" ):
				if( not(t in GlobalSnippets or t in FileSnippets)):
					print("Warning! mismatched template data Length")
		OutStr = []
		for index, tag in enumerate(self.SectionNames):
			if (tag==""):
				OutStr.append(self.SectionSnippets[index])
			else:
				if (tag in GlobalSnippets):
					OutStr.append( GlobalSnippets[tag] )
				elif (tag in FileSnippets):
					OutStr.append( FileSnippets[tag] )
				else:
					print("Could not find tag: "+tag)
		return "".join(OutStr)

#Clear folder for new files assuming it is empty or contains a claimed token
def ClearOutputFolder(directory):
	print("Checking directory")
	FileNames = os.listdir(directory)
	if ( len(FileNames) != 0 ):
		if( not "delete.ok" in FileNames):
			print("Directory has files, operation deletes files in folder!")
			print("Override check by placing a file named delete.ok in folder")
			return False
		print("Operating on: "+ directory)
		print("")
		input("Operation will delete folders, press enter to continue...")
		for filename in FileNames:
			os.unlink(os.path.join(directory,filename))
		return True
	elif ( len(FileNames) == 0):
		return True
	return False

#Mark folder as used by script
def CreateClaimedFolderToken(directory):
	with open(os.path.join(directory,"delete.ok"), "w") as claim:
		claim.write("This directory is claimed and is subject to being deleted in full")

#Create a html snippet that will link in the template
def ProcessCSS(CSSdirectory, GENdirectory):
	global GlobalSnippets
	CSSFileNames = os.listdir(CSSdirectory)
	CSSString = ""
	for CSSFile in CSSFileNames:
		if ( not CSSFile[-4:].lower() == ".css"):
			continue
		CSSString = "".join( [CSSString, '<link rel="stylesheet" href=', CSSFile ,'>\n'] )
	GlobalSnippets["CSS"] = CSSString
	CopyCSS(CSSdirectory,GENdirectory)

#Move css files to GEN
def CopyCSS(CSSdirectory, GENdirectory):
	print("Copying CSS Files")
	CSSFileNames = os.listdir(CSSdirectory)
	for F in CSSFileNames:
		CSSFile = os.path.join(CSSdirectory, F)
		if (os.path.isfile( CSSFile )):
			shutil.copy(CSSFile, GENdirectory)

#Proccess all templates into template objects 
def ProcessIntoTemplates(directory):
	templates = []
	templateFiles = os.listdir(directory)
	for File in templateFiles:
		templates.append( Template( os.path.join(directory, File) ) )
	return templates

def ProccessGlobalSnippets(directory):
	global GlobalSnippets
	FileLists = os.listdir(directory)
	for file in FileLists:
		with open( os.path.join(directory,file), "r") as f:
			inData = False
			GSNewTag = None #Will be current tag
			for line in f:
				if (inData):
					if (DELIMTER in line):
						if ( not DELIMTER+"END"+DELIMTER in line):
							print("Unexpected Begin Format block, Potential Global snippet formating error")
						inData = False
					else:
						GlobalSnippets[GSNewTag] = "".join([GlobalSnippets[GSNewTag],line])
				else:
					if( DELIMTER in line ):
						if ( DELIMTER+"END"+DELIMTER in line): 
							print("Unexpected End Format block, Potential Global snippet formating error")
						LIndex = line.find(DELIMTER)+len(DELIMTER)
						RIndex = line.rfind(DELIMTER)
						if (LIndex == (RIndex+len(DELIMTER))):
							print("MALFORMED GlobalSnippet!!! Line:"+line)
							print("MALFORMED GlobalSnippet!!! File:"+file)
						GSNewTag = line[LIndex:RIndex]
						if (GSNewTag in GlobalSnippets.keys()):
							print("Warning, parsed data indicates doubley defined tag: "+GSNewTag)
						GlobalSnippets[GSNewTag] = ""
						inData = True

def InterpretDataSnippets(directory):
	FileList = os.listdir(directory)
	Snippets = []
	for file in FileList:
		if ( file[-4:] == ".txt"):
			Dict = InterpretDataSnippet(os.path.join(directory,file))
			Dict["TemplateName"] = file[:file.find("_")]
			Dict["LOC"]=Dict["LOC"].strip()
			Dict["TITLE"]=Dict["TITLE"].strip()
			Snippets.append(Dict)
	return Snippets

def InterpretDataSnippet(FilePath):
	DataSnippet = {}
	with open( FilePath, "r") as DataFile:
		inData = False
		NewTag = None #Will be current tag
		for line in DataFile:
			if (inData):
				if (DELIMTER in line):
					if ( not DELIMTER+"END"+DELIMTER in line):
						print("Unexpected Begin Format block, Potential Data snippet formating error in: "+FilePath)
					inData = False
				else:
					DataSnippet[NewTag] = "".join([DataSnippet[NewTag],line])

			else:
				if( DELIMTER in line ):
					if ( DELIMTER+"END"+DELIMTER in line): 
						print("Unexpected End Format block, Potential Data snippet formating error in: "+FilePath)
					LIndex = line.find(DELIMTER)+len(DELIMTER)
					RIndex = line.rfind(DELIMTER)
					if (LIndex == (RIndex+len(DELIMTER))):
						print("MALFORMED DataSnippet!!! Line:"+line)
						print("MALFORMED DataSnippet!!! File:"+FilePath)
					NewTag = line[LIndex:RIndex]
					if (NewTag in DataSnippet.keys()):
						print("Warning, parsed data indicates doubley defined tag: "+NewTag)
					DataSnippet[NewTag] = ""
					inData = True
		DataFile.close()
	return DataSnippet

def GenerateIndexElement(DataSnipets):
	global GlobalSnippets
	indexData = ""
	for Dict in DataSnippets:
		indexData = indexData + "<a href='"+ Domain+ "/"+ Dict["LOC"] + "'>"+Dict["TITLE"]+"</a>\n"
	GlobalSnippets["Index"] = indexData 

def GeneratePages(outPutdir, DataSnippets, templates):
	for DataSnippet in DataSnippets:
		print("Processing: "+DataSnippet["TITLE"] , end="")
		template = None
		#get template
		for t in templates:
			if( t.getName().lower() == DataSnippet["TemplateName"].lower() ):
				template = t
				break
		else:
			print("Could not find template: "+DataSnippet["TemplateName"])

		with open(os.path.join(outPutdir, DataSnippet["LOC"]), "w") as wf:
			wf.write( template.populateTemplate( GlobalSnippets, DataSnippet) )
			wf.close()
		print("\t\tSaved to: " + DataSnippet["LOC"])

if __name__ == "__main__":
	print("Run from: ", RunDir, "\tExececuting on: ", SaveDir) 

	if( ClearOutputFolder( os.path.join(SaveDir, GEN) ) ):
		print("Directory clear")
	else:
		print("Error clearing folder of contents")
		quit()

	print("Marking folder for future use")
	CreateClaimedFolderToken( os.path.join(SaveDir, GEN) )

	#Creates CSS Element
	print("Proccessing CSS Files")
	ProcessCSS( os.path.join(SaveDir, SRC, CSS), os.path.join(SaveDir, GEN) )

	print("Creating Templates from files in: " + os.path.join(SaveDir, GEN) )
	templates = ProcessIntoTemplates( os.path.join(SaveDir, SRC, TEMPLATES) )
	print( str(len(templates))+" template(s) created")
	for t in templates:
		print("\t"+t.getName())

	print("Creating Global Snippets from files in: " + os.path.join(SaveDir, SRC, GLOBALS))
	ProccessGlobalSnippets(os.path.join(SaveDir, SRC, GLOBALS))
	print("Global Snipets: "+ str(GlobalSnippets))

	print("Reading main data from: " + os.path.join(SaveDir, SRC, DATA))
	DataSnippets = InterpretDataSnippets( os.path.join(SaveDir, SRC, DATA) )
	print("DataSnippets: " +str(DataSnippets))

	print("Generating Index Element from snippets")
	GenerateIndexElement(DataSnippets)
	print("Global Snipets: "+ str(GlobalSnippets))

	print("Generating Web pages to: " + os.path.join(SaveDir, GEN))
	GeneratePages(os.path.join(SaveDir, GEN), DataSnippets, templates)
	print("Done. Exiting...")
	quit()
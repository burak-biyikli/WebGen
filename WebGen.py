#!/usr/bin/env python3

import os
import re
import shutil
from datetime import datetime

GEN = "GEN"
SRC = "SRC"

CSS = "CSS"
JS = "Scripts"
RES = "Resources"
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
			if "." in filename:
				os.unlink(os.path.join(directory,filename))
			else:
				shutil.rmtree( os.path.join(directory,filename) )
		return True
	elif ( len(FileNames) == 0):
		return True
	return False

#Mark folder as used by script
def CreateClaimedFolderToken(directory):
	with open(os.path.join(directory,"delete.ok"), "w") as claim:
		claim.write("This directory is claimed and is subject to being deleted in full")

#Create a html snippet that will link in the template
def ProcessCSS(CSSdirectory, GENDirectory):
	global GlobalSnippets
	CSSFileNames = os.listdir(CSSdirectory)
	CSSString = ""
	for CSSFile in CSSFileNames:
		if ( not CSSFile[-4:].lower() == ".css"):
			continue
		CSSString = "".join( [CSSString, '<link rel="stylesheet" href=', CSSFile ,'>\n'] )
	GlobalSnippets["CSS"] = CSSString
	CopyCSS(CSSdirectory,GENDirectory)

#Move css files to GEN
def CopyCSS(CSSdirectory, GENDirectory):
	print("Copying CSS Files")
	CSSFileNames = os.listdir(CSSdirectory)
	for F in CSSFileNames:
		CSSFile = os.path.join(CSSdirectory, F)
		if (os.path.isfile( CSSFile )):
			shutil.copy(CSSFile, GENDirectory)

def ProcessJS( JSdirectory, GENDirectory ):
	global GlobalSnippets
	JSFileNames = os.listdir(JSdirectory)
	JSString = ""
	for JSFile in JSFileNames:
		if ( not JSFile[-3:].lower() == ".js"):
			continue
		JSString = "".join([ JSString, '<script src="', JSFile ,'"></script>\n' ])
	GlobalSnippets["JS"] = JSString
	CopyJS( JSdirectory, GENDirectory )

def CopyJS( JSdirectory, GENDirectory ):
	print("Copying JS Files")
	JSFileNames = os.listdir(JSdirectory)
	for F in JSFileNames:
		JSFile = os.path.join(JSdirectory, F)
		if (os.path.isfile( JSFile )):
			shutil.copy(JSFile, GENDirectory)

# Recursively copies the entire contents of the resource directory.
# Asserts that the destination does not exist before copying.
def CopyRES(RESdirectory, GENDirectory):
   
	print("Copying Resource Files")
	# This assertion ensures we don't accidentally copy into an existing folder.
	# The ClearOutputFolder function should prevent this, but this is a good safeguard.
	assert not os.path.exists(GENDirectory), f"Fatal: Resource destination {GENDirectory} already exists. Aborting."
	
	shutil.copytree(RESdirectory, GENDirectory)


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


# Reads all .txt data files from a directory, sorts them by modification
# time (newest first), and processes them into a list of dictionaries.
def InterpretDataSnippets(directory: str) -> list:
	data_files = []
	for filename in os.listdir(directory):
		if filename.endswith(".txt"):
			file_path = os.path.join(directory, filename)
			# Get the modification time of the file
			mod_time = os.path.getmtime(file_path)
			data_files.append((mod_time, file_path, filename))

	# Sort the files by modification time in descending order (newest first)
	data_files.sort(key=lambda x: x[0], reverse=True)

	data_snippets = []
	# os.walk will traverse the directory tree for us
	for dirpath, _, filenames in os.walk(directory):
		for filename in filenames:
			if filename.endswith(".txt"):
				file_path = os.path.join(dirpath, filename)		
				snippet_dict = InterpretDataSnippet(file_path) # Ensure required keys exist and strip whitespace
				for key in ["LOC", "TITLE"]:
					assert key in snippet_dict, f"Error: Expected {key} in template file {filename}. Saw {snippet_dict}"
					snippet_dict[key] = snippet_dict[key].strip()
					
				#Add required attributes, then add to the data_snippets array
				snippet_dict["TemplateName"] = filename[:filename.find("_")]
				data_snippets.append(snippet_dict)

	# Sort the list of dictionaries by the MODTIME key in descending order
	data_snippets.sort(key=lambda x: x.get("MODTIME", datetime.min), reverse=True)

	return data_snippets

# Attempts to parse a timestamp string from one of two formats:
# 1. 'M/D/YYYY, HH:MM am/pm'
# 2. 'M/D/YYYY'
# Returns a datetime object or None if parsing fails.
def ParseTimestamp(time_str: str) -> datetime | None:
	time_str = time_str.strip()
	try:
		if ":" in time_str:
			return datetime.strptime(time_str, '%B %d, %Y, %I:%M %p')
		else:
			return datetime.strptime(time_str, '%B %d, %Y')
	except ValueError:
		return None
	
# Appends a MODTIME section to a data file. This needs to be readable by ParseTimestamp()
def AppendMissingTimestamp(file_path: str, mod_time: float):
	# Format the timestamp into a readable string
	timestamp_str = datetime.fromtimestamp(mod_time).strftime('%B %d, %Y, %I:%M %p')
	print(f"Info: '{os.path.basename(file_path)}' is missing a timestamp. Appending one now.")
	with open(file_path, 'a') as f:
		f.write(f"\n***MODTIME***\n{timestamp_str}\n***END***\n")
  

# Wraps text blocks in <p> tags, ignoring blocks that look like HTML.
# A block is any text separated by one or more blank lines (2+ \n).  
def AutoParagraph(text: str) -> str:
	if not text:
		return ""
	paragraphs = []
	blocks = re.split(r'\n\s*\n', text.strip())
	for block in blocks:
		stripped_block = block.strip()
		if stripped_block.startswith('<') or stripped_block.endswith('>'):
			paragraphs.append(stripped_block)
		else:
			paragraphs.append(f"<p>{stripped_block}</p>")
	return "\n\n".join(paragraphs)

	
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
	
	# Auto-paragraph the body text
	if "Body" in DataSnippet:
		DataSnippet["Body"] = AutoParagraph(DataSnippet["Body"])
			
	# After parsing, check for the MODTIME tag
	if "MODTIME" in DataSnippet:
		parsed_time = ParseTimestamp(DataSnippet["MODTIME"])
		assert not(parsed_time is None), f"Fatal: Could not parse MODTIME in {FilePath} saw {DataSnippet['MODTIME']}"
		DataSnippet["MODTIME"] = parsed_time
	else:
		mod_time = os.path.getmtime(FilePath)
		DataSnippet["MODTIME"] = datetime.fromtimestamp(mod_time)
		AppendMissingTimestamp(FilePath, mod_time) # The function we discussed before

	return DataSnippet

def GenerateIndexElement(DataSnipets):
	global GlobalSnippets
	indexData = ""
	for Dict in DataSnippets:
		indexData = indexData + "<a href='"+ "/"+ Dict["LOC"] + "'>"+Dict["TITLE"]+"</a> <br>"
	GlobalSnippets["Index"] = indexData 


# Removes HTML tags and comments from a string using regular expressions.
# Will remove items similar to <b> <div> </div> and &rarr;
def StripHTML(HTML_Text: str) -> str:	
	cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
	clean_text = re.sub(cleaner, '', HTML_Text)
	return clean_text

# Generates an HTML feed of the most recent pages. Expects DataSnippets to be in order from most to least recent
def GenerateFeedElement(DataSnippets: list, num_items: int = 5, max_length: int = 100):
	global GlobalSnippets
	feed_html = ""
	for i, snippet in enumerate(DataSnippets[:num_items]):
		
		# Get the body text, or an empty string if it doesn't exist
		base_text = snippet.get("Summary","") + snippet.get("Body", "")
		
		# Clean and truncate the body text for the preview
		plain_text = StripHTML(base_text).strip()
		plain_text = " ".join( plain_text.split() )
		
		if len(plain_text) == 0:
			preview_text = "No preview avalible for this page..."
		else:
			preview_text = (plain_text[:(max_length-3)] + '...')
		
		# Create the HTML for this feed item
		feed_html += f"""\
<div class="feed-item">
	<h4><a href="/{snippet['LOC']}">{snippet['TITLE']}</a></h4>
	<p>{preview_text}</p>
</div>
"""
	# Wrap the entire output in a container
	GlobalSnippets["Feed"] = f'<br><br><br><hr><div class="feed-container"><h3>Recent Updates</h3>{feed_html}</div>'


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

	#Creates JS Element
	print("Proccessing JS Files")
	ProcessJS( os.path.join(SaveDir, SRC, JS), os.path.join(SaveDir, GEN) )

	#Copy over Resources
	CopyRES( os.path.join(SaveDir, SRC, RES), os.path.join(SaveDir, GEN, RES) )

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
	print("Generating Feed Element from snippets")
	GenerateFeedElement(DataSnippets)
	print("Global Snipets: ")
	for s in GlobalSnippets:
		print(f"\t{s}:{str(GlobalSnippets[s])}")

	print("Generating Web pages to: " + os.path.join(SaveDir, GEN))
	GeneratePages(os.path.join(SaveDir, GEN), DataSnippets, templates)
	print("Done. Exiting...")
	quit()

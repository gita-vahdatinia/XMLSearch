##################################################################################
#Guita Vahdatinia
#7/19/16
#Parses through XML file and returns errors_(datasource).txt of unfound searches
##################################################################################

#!/usr/bin/python
import xml.etree.ElementTree as ET
import urllib 
import re
import itertools
import time

#Start Timer
start_time = time.time()

#User Input
print ("Enter the XML file you wish to search: (include full filepath) \n")
filename = raw_input()

tree = ET.parse(filename)
root = tree.getroot()
child = tree.getroot() 
#Gets subname for error file
for child in root.iter('header'):
	datasourcename = child.find('datasource').text
	
#Create Empty Errors_.txt
errorfile = open("errors_"+datasourcename+ ".txt", "w")
errorfile = open("errors_"+datasourcename+ ".txt", "a") #this is appending

#Constructing URL
EXP1 ="http://search.cpuc.ca.gov/search?q=" 
EXP4 = "&site=PUC_Website&client=puc_frontend&output=xml_no_dtd&"
EXP5 = "proxystylesheet=puc_frontend&filter=p&getfields=*"
EXP3 = EXP4 + EXP5 

#Scoring Errors
sublinkError, xmlError, manyresultsError, noresultError, NUM, totalrecord, counter, pagenum  = 0, 0, 0, 0, 1, 0, 0, 0

#Intiliazing Lists
titlelist = []
idlist = []
urllist = []
filelist = []
flag = True
for names in root.iter('meta'):
	(name, content) = names.get('name'), names.get('content')
	if ( name == "DocID"):
		docid = content
		idlist.append(docid)
	elif (name == "DocTitle"):
		doctitle = content.encode('utf-8')
		doctitle = doctitle.replace(".docx","")
		doctitle = doctitle.replace(".DOCX","")
		doctitle = doctitle.replace(".pdf","")
		doctitle = doctitle.replace(".PDF","")
		doctitle = doctitle.replace("..."," ")
		if doctitle.endswith('.'):
			doctitle = doctitle[:-1]
		titlelist.append(doctitle)
		totalrecord+=1
		EXP2 = urllib.quote(doctitle)
		#Create Full URL 
		URL = EXP1 + EXP2 + EXP3
		urllist.append(URL)
	elif (name == "FileName"):
		fileid = content
		fileid = fileid.replace(".DOCX","")
		fileid = fileid.replace(".PDF", "")
		filelist.append(fileid)
		
def writer(id, title, url, namefile):
	namefile.write("DOCTITLE: {}\n".format(title))
	namefile.write("DOCID: {}\n".format(id))
	namefile.write("URL: {}\n\n\n".format(url))

while counter < totalrecord:
	pagenum = 0
	DOCID = idlist.pop()
	DOCTITLE = titlelist.pop()
	URL = urllist.pop()
	FILEID = filelist.pop()
	searchpage = urllib.urlopen(URL).read()
	textfile = open("textfile.txt", "w")
	textfile.write(searchpage)
	page = open('textfile.txt').read()
	
	while DOCID not in page and FILEID not in page:
		if "No pages were found" in page:
			errorfile.write("No result: \n")
			writer(DOCID, DOCTITLE, URL, errorfile)
			break
		if "Next" not in page:
			errorfile.write("Error: Could not find \n")
			writer(DOCID, DOCTITLE, URL, errorfile)
			break
		if "Next" in page and pagenum < 5: 
			with open('textfile.txt') as myfile:
				data = page.replace('\n', '')
				r = re.compile('<td\s+nowrap\="1">&nbsp;<span\s+class\="s"><a\s+ctype\="nav\.next"\s+href\=(?:(?!>Next&nbsp;&gt;</a></span></td>\s+)(?:.|\n))*>Next&nbsp;&gt;</a></span></td>\s+')
				URL2 = r.findall(data)
			if URL2:
				URL_2 = URL2[0]
				URL_2 = URL_2[73:]
				URL_2 = URL_2[:-49]
				secondURL = EXP1 + URL_2 + str(10*pagenum)
				secondURL = secondURL.replace("amp;","")
				#urlpage = open("urlpage.txt", 'a')
				#urlpage.write(secondURL + "\n")
				#writer(DOCID, DOCTITLE, URL, urlpage)
				second_searchpage = urllib.urlopen(secondURL).read()
				textfile_2 = open('textfile2.txt','w')
				textfile_2.write(second_searchpage)
				#secondpage = open('textfile2.txt').read()
				if DOCID in open('textfile2.txt').read() or FILEID in open('textfile2.txt'):
					break
				if pagenum == 4:
					errorfile.write("Not in first 4 pages\n")
					writer(DOCID, DOCTITLE, URL, errorfile)
					break
				else:
					pagenum+=1
	counter+=1


	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

	
	

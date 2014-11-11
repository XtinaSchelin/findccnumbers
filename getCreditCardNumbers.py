import re
import os

# Some hard-coded defaults.
baseDir = r"C:\XScripts\findccnumbers\testfiles"
patt = r'(?=(\d{%s}))'
outFile = r"C:\Users\Public\possibles.txt"

# Function to return whether the line contains numbers of a certain length.
def findNum(ccnum):
	# Strip all non-numeric characters from the string.
	ccnum = re.sub("[^0-9]", "", ccnum)
	x = 13
	while x <= 19:
		tpat = patt % str(x)
		matches = re.finditer(tpat, ccnum)
		if len(list(matches)) > 0:
			# If it matches even once, it's fine.
			return True
		x = x + 1
	return False

# Function to check the lines in each file for CCness.
def fileCheck(path, file):
	f = open(path + file, "rb")
	for line in f:
		if findNum(line.strip()) == True:
			f.close()
			return True
	f.close()
	return False
	
# Open the output file.
o = open(outFile, "wb")
o.write("Path\tFilename\n")

# For each file, recursive, in the provided directory.
for root, dirs, files in os.walk(baseDir):
	wPath = root
	for file in files:
		if fileCheck(wPath + "\\", file) == True:
			# If there's a number anywhere in the file, write it out.
			o.write(wPath + "\t" + file + "\n")

o.close()
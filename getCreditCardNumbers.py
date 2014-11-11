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
	found = False
	while x <= 19:
		tpat = patt % str(x)
		matches = re.finditer(tpat, ccnum)
		if len(list(matches)) > 0:
			found = True
			# Why is anything.
			matches = re.finditer(tpat, ccnum)
			for match in matches:
				# Write every match out.
				o = open(outFile, "ab")
				o.write(wPath + "\t" + file + "\t" + match.group(1) + "\n")
				o.close()
		x = x + 1
	return found

# Function to check the lines in each file for CCness.
def fileCheck(path, file):
	f = open(path + file, "rb")
	for line in f:
		findNum(line.strip())
	f.close()
	
# Open the output file.
o = open(outFile, "wb")
o.write("Path\tFilename\tNumber\n")
o.close()

# For each file, recursive, in the provided directory.
for root, dirs, files in os.walk(baseDir):
	for file in files:
		fileCheck(root + "\\", file)

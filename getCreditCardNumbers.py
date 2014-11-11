import re, os, sys

# Some hard-coded defaults.
patt = r'(?=(\d{%s}))'

def luhn_checksum(card_number):
	def digits_of(n):
		return [int(d) for d in str(n)]
	digits = digits_of(card_number)
	odd_digits = digits[-1::-2]
	even_digits = digits[-2::-2]
	checksum = 0
	checksum += sum(odd_digits)
	for d in even_digits:
		checksum += sum(digits_of(d*2))
	return checksum % 10

def is_luhn_valid(card_number):
	return luhn_checksum(card_number) == 0

# Function to return whether the line contains numbers of a certain length.
def findNum(ccnum, path, filename):
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
				isLuhn = 'Yes' if is_luhn_valid(match.group(1)) == True else 'No'
				o.write(path + "\t" + filename + "\t" + match.group(1) + "\t" + isLuhn + "\n")
				o.close()
		x = x + 1
	return found

# Function to check the lines in each file for CCness.
def fileCheck(path, filename):
	f = open(path + filename, "rb")
	for line in f:
		findNum(line.strip(), path, filename)
	f.close()

# The main method, mainly.
def scanFiles():
	global outFile
	# Get to-scan directory.
	print "What directory would you like to scan?"
	scanDir = raw_input("> ").strip()
	if os.path.isdir(scanDir) == False:
		sys.exit("That is not a valid directory.")
	
	# Get output file.
	print "Enter an output directory and .txt filename to export to."
	outFile = raw_input("> ").strip()
	# Directory exists?
	if os.path.isdir(os.path.dirname(outFile)) == False:
		sys.exit("That directory doesn't even exist, come on.")
	# File type is correct?
	ext = os.path.splitext(outFile)[1].lower()
	if ext not in (".txt", ".csv", ".tsv"):
		sys.exit("Incorrect file type.")

	# Open the output file.
	o = open(outFile, "wb")
	o.write("Path\tFilename\tNumber\tLuhn\n")
	o.close()

	# For each file, recursive, in the provided directory.
	for root, dirs, files in os.walk(scanDir):
		for file in files:
			fileCheck(root + "\\", file)

if __name__ == "__main__":
	scanFiles()

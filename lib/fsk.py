#this is a simple fsk repo for sending text
#still to do is error correction possibly

#similar code copied from my rtty-email repo
import subprocess

def send_text(text, baud):
	proc = subprocess.Popen(
		['minimodem', '--tx', str(baud), '-8', '--tx-carrier'],
		stdin=subprocess.PIPE,
		stderr=subprocess.DEVNULL
	)
	try:
		proc.stdin.write(text) #encode the text as ascii and send it
		proc.stdin.close()
		proc.wait()
	finally:
		proc.terminate()

def recive_text(baud, confidence, end_marker, max_chars): #you can choose to make it stop recieving when a certain string is recieved or when a certain amount of characters are recieved
	proc = subprocess.Popen(
		['minimodem', '--rx', str(baud), '-8', '--confidence', str(float(confidence))], #ascii charset only
		stdout=subprocess.PIPE,
		stderr=subprocess.DEVNULL
	)
	i = 0
	char = ""
	while True:
		char = char + proc.stdout.read(1).decode("ascii", errors="replace") #decodes as ascii and replaces invalid chars with ?
#		print(char) #for debugging
		if end_marker != None and end_marker in char:
			return char
		if i == max_chars - 1: #otherwise we get an extra character
			return char
		i = i + 1

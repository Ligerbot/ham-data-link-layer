import local_libraries.tones as tones
import time
import reedsolo
import subprocess
rsc = reedsolo.RSCodec(10)
#file = True
def recieve():
	global proc
	global newframes
	newframes = []
	breaknow = False
	proc = subprocess.Popen(
		['minimodem', '--rx', '1200', '--confidence', '0.1', '-q'],
		stdout=subprocess.PIPE,
		stderr=subprocess.DEVNULL
	)
	while not breaknow:
		recieved = proc.stdout.readline()
#		print(recieved)
		message = unframe(recieved)
#		print(message)
		if message != None and message != "":
			return message
#		if frame != None:
#			newframes.append(frame)
#		if breaknow == True:
#			print("Newframes: " + str(newframes))
#			break
#	print(newframes)
###	proc.terminate()
#	proc.terminate()
#	proc.terminate()
#	proc.terminate()
#	return message
#	return newframes
def unframe(raw):
	global breaknow
	global newframes
	splitted = raw.split(b"{|{|{|")
#	print("Splitted: " + str(splitted))
#	breaknow = False
	breaknow = False
	for item in splitted:
		if breaknow:
			break
		if b"|}|}|}" in item or b"|||" in item:
#			print("Sending ackgnowledgement")
#			newframes.append(item)
			try:
				fixed = rsc.decode(b"{|{|{|" + item)[0]
				tones.play(1000, 500)
				newframes.append(fixed) #does this fix it?
#				print(fixed)
#				return fixed
			except Exception as e:
				print(e)
#			return b"{|{|{|" + item
		elif b"{OK}" in item:
			breaknow = True
			tones.play(1000, 500)
#			exit(1)
#			print("Exiting from recieve loop, recieving cconnection close")
#			print("Connection closed from remote end")
			content = ""
			i = 0
			for frame in newframes:
				frame = frame.replace(b"{|{|{|", b"")
				frame = frame.split(b"|}|}|}")[0] #this instead of the commented line below makes it so that there aren't extra parity bits messing stuff up
#				frame = frame.replace(b"|}|}|}", b"")
				text = frame.split(b"|||")[1]
				sequencenum = int(frame.split(b"|||")[0])
#				print("Frame sequence number: " + str(int(sequencenum)))
#				print("Frame content: " + str(text))
#				text = str(text).replace("bytearray'", "")
				text = text.decode("ascii", errors="ignore")
#				print(f"Sequencenum: {sequencenum}, i: {i}")
				if sequencenum == i:
					content = content + str(text)
#					i = i - 1
#					print(f"Sequencenum: {sequencenum}, i: {i}")
				else:
#					print("Recieved duplicate packet number with sequence id " + str(sequencenum))
					i = i - 1
#					while len(str(text)) >= 11:
#						text = str(text)[:-1] #claude says this deletes last char
#					content = content + str(text)
				i = i + 1
			#	print(content)
#					print("Length error")
#			print("Reassembled string: " + content)
#			print(newframes)
#			break
#			print("Content: " + content)
			return content
#			break
#		elif b"SYNCSYNCSYNC" in item:
#			print("Got sync")
#			tones.play(1000, duration_ms=500)
#			tones.play(2300, duration_ms=75)
#			tones.play(2600, duration_ms=75)
#			if tones.listen(1000, duration_ms=500):
#				print("Sync agreed, ready for data")

#		else:
#			print("Not a packet")
#		sine(500, 700) #ackgnowledge ment tone
#	intermediate = raw.replace(b"{|{|{|", b"")
#	intermediate = intermediate.replace(b"|}|}|}", b"")
#	
#	raw.split(b"{|")
#	parts = raw.split(b"{|{|{|")
#	parts = parts[1:]  # weird sorcery with the [1:]
#
#	frames = []
#	for part in parts:
#		sides = part.split(b"|}|}|}")
#		frame = sides[0]
#		check = sides[1]
#		frames.append(frame + check)
#
#	print(frames)
#broken function to fix character deletions and insertions
#still need to fix this to make the protocol more reliable
#		print(raw)
#	fixed = ""
#	for i in range(len(frames)):
#		frame = frames[i] + frames[i+1]
#		if len(frame) + 12 < int(str(frames[3]) + str(frames[4])):
#			while len(frame) + 12 < int(str(frames[3]) + str(frames[4])):
#				frame = frame + "?"
#		elif len(frame) + 12 > int(str(frames[3]) + str(frames[4])):
#			while len(frame) + 12 > int(str(frames[3]) + str(frames[4])):
#				frame = frame[:-1]
#		fixed = fixed + rsc.decode(frame)[0]
#	print(fixed)
def chonk(message):
	if len(message) <= 4:
		print("Message does not need to be chunked")
		oneitemarray = []
		oneitemarray.append(message)
		return oneitemarray
	else:
		chunks = []
		i = 0
		while i < len(message):
			start = i
			end = i + 10
			chunk = message[start:end]
			chunks.append(chunk)
			i += 10
#		print(chunks)
		return chunks
def format(message):
	chunks = chonk(message)
#	print(chunks)
	frames = []
	i = 0
	for chunk in chunks:
		thebytes = chunk.encode("ascii")
#		parity = rsc.encode(thebytes)
#		print("Parity: " + str(parity))

#		frame = b"{|{|{|" + b"??" + b"|" + thebytes + b"|||" + parity + b"|}|}|}"
#		if not(len(frame) <= 99 and len(frame) >=10):
#			print("Frame length error")
#			return
#		frame = b"{|{|{|" + bytes(str(len(frame)), "ascii") + b"|" + thebytes + b"|||" + parity + b"|}|}|}"
#		frames.append(frame)

		if i <= 9:
			padded = b"0" + bytes(str(i), "ascii")
#		template = b"{|{|{|" + b"??" + b"|||" + thebytes + b"|}|}|}"
#		if not(len(template) <= 99 and len(template) >=10):
#			print("Frame length error")
#			return
		frame = b"{|{|{|" + padded + b"|||" + thebytes + b"|}|}|}"
		frames.append(rsc.encode(frame))
		i = i + 1
#	print(frames)
	return frames

def send(message):
	global proc
#	print("Sending: " + str(message))
	proc = subprocess.Popen(
		['minimodem', '--tx', '1200', '--confidence', '0.3'],
		stdin=subprocess.PIPE,
		stderr=subprocess.DEVNULL
	)
	proc.stdin.write(message)
	proc.stdin.close()
	proc.wait()
	proc.terminate()
	proc.terminate()
	proc.terminate()
	proc.terminate()

def send_data(msg):
	frames = format(msg)
	for frame in frames:
		while True:
			send(b"\n" + bytes(frame) + b"\n")
			if tones.listen(1000, duration_ms=500):
				print("Ackgnowledged")
				break
			print("Resending frame")
	while True:
		if tones.listen(1000, duration_ms=500):
			print("Transmission done")
			break
		print("Retransmitting connection close signal")
		send(b"\n{OK}\n")

if __name__ == "__main__":
	try:
		role = input("Sender(1) or reciever(2): ")
		if role == "1":
			msg = input("Message: ")
			frames = format(msg)
	#raw = b""
#	send(b"\n") #start of new frame
#	while True:
#		send(b"SYNCSYNCSYNCSYNC\n")
#	time.sleep(0.5)
#		if tones.listen(1000, duration_ms=500):
#			if tones.listen(2300, duration_ms=75):
#				if tones.listen(2600, duration_ms=75)
#			print("Synced")
#			tones.play(1000, duration_ms=500)
#			break

			for frame in frames:
#		send(b"\n" + bytes(frame) + b"\n")
#		time.sleep(0.5)
#			send(b"\n" + bytes(frame) + b"\n")
				while True:
					send(b"\n" + bytes(frame) + b"\n")
					if tones.listen(1000, duration_ms=500):
						print("Got ackgnowledgement, continuing to next packet")
						break
					print("Didn't recieve ackgnowledgement. Resending the frame")
	#			time.sleep(1)
	#			send(b"\n" + bytes(frame) + b"\n")
			while True:
				if tones.listen(1000, duration_ms=500):
					print("Done")
					break
				print("Never recieved ack")
				send(b"\n{OK}\n{OK}\n")
#			time.sleep(0.5)
#		time.sleep(0.5)
	#	raw = raw + bytes(frame)
	#unframe(raw)
		elif role == "2":
			print(recieve())
		else:
			print("Invalid option")
	finally:
		proc.terminate()
		proc.terminate()
		proc.terminate()
		proc.terminate()
		proc.terminate()
		proc.terminate()
		print("Killed off minimodem")

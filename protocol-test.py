import local_libraries.tones as tones
import time
import reedsolo
import subprocess
rsc = reedsolo.RSCodec(10)
#file = True
def recieve():
	while True:
		proc = subprocess.Popen(
			['minimodem', '--rx', '300', '--confidence', '0.1', '-q'],
			stdout=subprocess.PIPE,
			stderr=subprocess.DEVNULL
		)
		recieved = proc.stdout.readline()
		proc.terminate()
		proc.terminate()
		proc.terminate()
		proc.terminate()
		print(recieved)
		frame = unframe(recieved)

def unframe(raw):
	splitted = raw.split(b"{|{|{|")

	print("Splitted: " + str(splitted))
	for item in splitted:
		if b"|}|}|}" in item or b"|||" in item:
			print("Sending ackgnowledgement")
			tones.play(1000, 500)
		else:
			print("Not a packet")
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
	print(chunks)
	frames = []
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

		template = b"{|{|{|" + b"??" + b"|||" + thebytes + b"|}|}|}"
		if not(len(template) <= 99 and len(template) >=10):
			print("Frame length error")
			return
		frame = b"{|{|{|" + bytes(str(len(template)), "ascii") + b"|||" + thebytes + b"|}|}|}"
		frames.append(rsc.encode(frame))
	print(frames)
	return frames

def send(message):
	print("Sending: " + str(message))
	proc = subprocess.Popen(
		['minimodem', '--tx', '300', '--confidence', '0.3'],
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
role = input("Sender(1) or reciever(2): ")
if role == "1":
	msg = input("Message: ")
	frames = format(msg)
	#raw = b""
#	send(b"\n") #start of new frame
	for frame in frames:
		send(b"\n" + bytes(frame) + b"\n")
		time.sleep(0.5)
		while True:
			if tones.listen(1000):
				print("Got ackgnowledgement, continuing to next packet")
				break
			print("Didn't recieve ackgnowledgement. Resending the frame")
			time.sleep(1)
			send(b"\n" + bytes(frame) + b"\n")
#			time.sleep(0.5)
#		time.sleep(0.5)
	#	raw = raw + bytes(frame)
	#unframe(raw)
elif role == "2":
	recieve()
else:
	print("Invalid option")

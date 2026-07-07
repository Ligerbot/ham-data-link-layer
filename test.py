import lib.fsk as FSK
import reedsolo
rsc = reedsolo.RSCodec(15, c_exp=7)

def chunker(message):
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
			end = i + 15
			chunk = message[start:end]
			chunks.append(chunk)
			i += 15
		return chunks
def sender(text):
	chunks = chunker(text)
	print("Sending the following packets:")
	for chunk in chunks:
		while len(chunk) <= 9:
			chunk = chunk + "."
#		print(chunk)
		packet = rsc.encode(chunk.encode("ascii"))
		print(packet)
		FSK.send_text(packet, 45)
		ack = FSK.recive_text(45, 3, None, 3)
		if "!" in ack:
			print("Success")
		else:
			print("Retry")

#		FSK.send_text("!!!".encode("ascii"), 45)
#	FSK.send_text("!!!", 45)
def reciever():
	recieved = FSK.recive_text(45, 3, None, 30)
	try:
		recieved = rsc.decode(recieved.encode("ascii"))[0].decode("ascii")
		print("Successfully decoded rtty: \n" + recieved)
		FSK.send_text("!!!", 45)
	except Exception as e:
		print("Error decoding: \n" + recieved)
		print(e)
if __name__ == "__main__":
	mode = input("Reciever(1) or sender(2)? ")
	if mode == "1":
		reciever()
	elif mode == "2":
		text = input("> ")
		sender(text)
	else:
		print("Invalid option")

# Ham Radio Data Link Layer

The goal of this project to to make my own data link layer protocol for ham radio. I've tried to use AX.25, but it is seemingly impossible to decode it using AFSK in python.

Eventually, when this is finished, the program will be importable to other python programs to be used as a library. I want to move my other repo rtty-email to use this protocol.

The goal of this is for reliable communications even when there is lots of noise. Currently, the program chunks the message to be sent into ten character long pieces. Then, it encapsulates it in a frame which looks something like this: `{|{|{|length of packet|||body|}|}|}error correcting bits`. I want to add functionality to make one side request a higher speed if there is less noise, or a lower speed if there is more noise.

import sys
import os
# Need to Cleanup this area
XORByte = ""
INPUTBye = ""
outbyte = ""
inputfile = ""
inputfilename = ""
inputstring = ""
XOR_operation_null = ""
XOR_operation_key = ""
xorkey = ""
outputfile = ""
outputfilename = ""
CurrentByte = 0
OffsetStart = 0
OffsetEnd = 0
StringFileFlag = 0
xorkeycount = 0
inputstringcount = 0

def HelpMSG(): #Maybe convert to argparse
    print \
	"""
	HALP!:
		XOR Script:
		This script will XOR a FILE or HEX STRING.
		Can specify specific offset range to apply key to.
		The Options will define how the key is applied.
		=====================================================================================================
		Usage: XOR_Null.py <input> <Start Offset> <Finish Offset> <option1> <option2> <hex key> <outputfile>
		=====================================================================================================
		Input: Raw File or Hex String.
		
		Start Offset: Hexadecimal value of the offset you want to start XORing (0 = Start of File)
		
		Finish Offset: Hexadecimal value of the offset you want to finish XORing (0 = End of File)
		
		Option1: (Skip Null Bytes)
			[0] Ignore this option.
			[1] XOR operation preserves null bytes (Does not increment XOR Key).
			[2] XOR operation preserves null bytes (Increments XOR Key).
			[3] XOR operation preserves null bytes (Decrements XOR Key).
			
		Option2: (Skip Byte When Key Byte Matches Input Byte)
			[0] Ignore this option.
			[1] XOR operation skips when Key matches byte (Does not increment XOR Key).
			[2] XOR operation skips when Key matches byte (Increments XOR Key).
			[3] XOR operation skips when Key matches byte (Decrements XOR Key).
			
		Hex Key: Hexadecimal value (in bytes) the Input will be XORed with.
		
		Output File: XORed file.
	"""

def InputValid(): #Need to maybe change this to argparse, and remove global variables
	global StringFileFlag
	global inputfilename
	global inputstring
	global XOR_operation_null
	global XOR_operation_key
	global xorkey
	global outputfilename
	global OffsetStart
	global OffsetEnd

	if len(sys.argv) < 5:
		HelpMSG()
		sys.exit()
	else:
		if len(sys.argv) != 8:
			HelpMSG()
			sys.exit()
		inputfilename = sys.argv[1]
		if inputfilename == None:
			print "Invalid Input. Please use a Filename or Hex string."
			HelpMSG()
			sys.exit()
		else:
			if os.path.exists(sys.argv[1]):
				StringFileFlag = 1
			elif not os.path.exists(sys.argv[1]):
				inputstring = int(sys.argv[1], 16)
				StringFileFlag = 2
			else:
				print "Invalid Input. Please use a Filename or Hex string."
				HelpMSG()
				sys.exit()

		OffsetStart = sys.argv[2]
		if OffsetStart == None:
			OffsetStart = 0
		elif OffsetStart == "0":
			OffsetStart = 0
		elif int(sys.argv[2], 16):
			OffsetStart = int(sys.argv[2], 16)
		else:
			print "Offset Start Invalid."
			HelpMSG()
			sys.exit()

		OffsetEnd = sys.argv[3]
		if OffsetEnd == None:
			OffsetEnd = 0
		elif OffsetEnd == "0":
			OffsetEnd = 0
		elif int(sys.argv[3], 16):
			OffsetEnd = int(sys.argv[3], 16)
		else:
			print "Offset End Invalid."
			HelpMSG()
			sys.exit()

		XOR_operation_null = sys.argv[4]
		if XOR_operation_null == None:
			XOR_operation_null = 0
		elif XOR_operation_null == "0":
			XOR_operation_null = 0
		elif XOR_operation_null == "1":
			XOR_operation_null = 1
		elif XOR_operation_null == "2":
			XOR_operation_null = 2
		elif XOR_operation_null == "3":
			XOR_operation_null = 3
		else:
			print "Option1 Invalid."
			HelpMSG()
			sys.exit()

		XOR_operation_key = sys.argv[5]
		if XOR_operation_key == None:
			XOR_operation_key = 0
		elif XOR_operation_key == "0":
			XOR_operation_key = 0
		elif XOR_operation_key == "1":
			XOR_operation_key = 1
		elif XOR_operation_key == "2":
			XOR_operation_key = 2
		elif XOR_operation_key == "3":
			XOR_operation_key = 3
		else:
			print "Option2 Invalid."
			HelpMSG()
			sys.exit()

		xorkey = int(sys.argv[6], 16)
		outputfilename = sys.argv[7]

		if StringFileFlag == 1:
			XORFile()
		elif StringFileFlag == 2:
			XORString()
			
def XORFile():
	inputfilename = sys.argv[1]
	inputfile = open(inputfilename, 'rb')
	outputfile = open(outputfilename, 'wb')
	byte = inputfile.read(1)
	xorkey, xorkeycount = sys.argv[6].decode("hex"), 0
	xorkeylength = len(str(xorkey.encode("hex")))

	while byte != "":
		if xorkeycount >= xorkeylength / 2:
			xorkeycount = 0

		XORByte = xorkey[xorkeycount:xorkeycount+1].encode("hex")
		byte = byte.encode("hex")
		CurrentByte = inputfile.tell()

		if CurrentByte <= OffsetEnd or CurrentByte >= OffsetStart:
			if byte == XORByte and XOR_operation_key != 0:
				if XOR_operation_key == 1:
					outbyte = chr(int(byte, 16))

				elif XOR_operation_key == 2:
					outbyte = chr(int(byte, 16))
					xorkeycount += 1

				elif XOR_operation_key == 3:
					if xorkeycount <= 0:
						xorkeycount = xorkeylength / 2
					else:
						outbyte = chr(int(byte, 16))
						xorkeycount -= 1

			elif byte == "00" and XOR_operation_null != 0:
				if XOR_operation_null == 1:
					outbyte = chr(int(byte, 16))

				elif XOR_operation_null == 2:
					outbyte = chr(int(byte, 16))
					xorkeycount += 1

				elif XOR_operation_null == 3:
					if xorkeycount <= 0:
						xorkeycount = xorkeylength / 2
					else:
						outbyte = chr(int(byte, 16))
						xorkeycount -= 1

			else:
				outbyte = int(byte, 16) ^ int(XORByte, 16)
				outbyte = chr(outbyte)
				xorkeycount += 1
		else:
			outbyte = chr(int(byte, 16))

		outputfile.write(bytes(outbyte))
		byte = inputfile.read(1)
		continue

	inputfile.close()
	outputfile.close()

def XORString():
	inputstring, inputstringcount = sys.argv[1].decode("hex"), 0
	inputstringlength = len(str(inputstring.encode("hex")))
	xorkey, xorkeycount = sys.argv[6].decode("hex"), 0
	xorkeylength = len(str(xorkey.encode("hex")))
	outputfile = open(outputfilename, 'wb')

	while int(inputstringcount) + 1 <= inputstringlength / 2:
		if xorkeycount >= xorkeylength / 2:
			xorkeycount = 0

		XORByte = xorkey[xorkeycount:xorkeycount+1].encode("hex")
		INPUTByte = inputstring[inputstringcount:inputstringcount+1].encode("hex")

		if inputstring[inputstringcount] <= OffsetEnd or inputstring[inputstringcount] >= OffsetStart:
			if INPUTByte == XORByte and XOR_operation_key != 0:
				if XOR_operation_key == 1:
					outbyte = chr(int(INPUTByte, 16))

				elif XOR_operation_key == 2:
					outbyte = chr(int(INPUTByte, 16))
					xorkeycount += 1

				elif XOR_operation_key == 3:
					if xorkeycount <= 0:
						xorkeycount = xorkeylength / 2
					else:
						outbyte = chr(int(INPUTByte, 16))
						xorkeycount -= 1

			elif INPUTByte == "00" and XOR_operation_null != 0:
				if XOR_operation_null == 1:
					outbyte = chr(int(INPUTByte, 16))

				elif XOR_operation_null == 2:
					outbyte = chr(int(INPUTByte, 16))
					xorkeycount += 1
				elif XOR_operation_null == 3:
					if xorkeycount <= 0:
						xorkeycount = xorkeylength / 2
					else:
						outbyte = chr(int(INPUTByte, 16))
						xorkeycount -= 1

			else:
				outbyte = int(INPUTByte, 16) ^ int(XORByte, 16)
				outbyte = chr(outbyte)
				xorkeycount += 1
		else:
			outbyte = chr(int(INPUTByte, 16))

		inputstringcount += 1
		outputfile.write(bytes(outbyte))
		continue

	outputfile.close()	
InputValid()
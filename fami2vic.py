#!/usr/bin/env python

import sys

with open(sys.argv[1], 'r') as my_file:
	LineCount = len(my_file.readlines(  ))
	
with open(sys.argv[1], 'r') as f:
	Lines = f.read().splitlines()	

BlankLine="..."
StopNote1="---"
StopNote2="==="

DataStartAddress="1D00"
DataStartAddrDec=int(DataStartAddress,16)

SwapS2S3=0

Square1NoteModifier=-24
Square2NoteModifier=-12
TriangleNoteModifier=-12

ABCList=["C0","C#0","D0","D#0","E0","F0","F#0","G0","G#0","A0","A#0","B0","C1","C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1","A#1","B1","C2","C#2","D2","D#2","E2","F2","F#2","G2","G#2","A2","A#2","B2","C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3","A#3","B3","C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4","C5","C#5","D5","D#5","E5","F5","F#5","G5","G#5","A5","A#5","B5"]
PercList=["0#","1#","2#","3#","4#","5#","6#","7#","8#","9#","A#","B#","C#","D#","E#","F#"]



ToneLowByte=[132,139,146,152,158,163,168,173,178,182,186,190,193,197,200,203,206,209,211,214,216,218,220,222,224,226,227,229,230,232,233,234,235,236,237,238,239,240,241,242,242,243,244,244,245,245,246,246,247,247,248,248,249,249,249,249,250,250,250,251,251,251,251,251,252,252,252,252,252,252,252,253]
ToneHighByte=[7,6,1,2,0,4,5,4,0,3,4,2,7,3,5,5,4,2,6,2,4,5,6,5,4,1,6,3,6,1,3,5,6,7,7,7,6,5,3,1,7,4,2,6,3,7,3,7,3,6,2,5,0,2,5,7,2,4,6,0,1,3,5,6,0,1,2,4,5,6,7,0]
PercTone=[135,147,151,159,163,167,175,179,183,187,191,195,199,201,203,207,209,212,215,217,219,221,223,225,227,228,229,231,232,233,235,236,237,238,239,240,241]

DurationModifier=-1

Lines.pop() #Remove last two lines from file
Lines.pop()

print "Searching for number of rows per pattern"
for n in range(LineCount):
	CurRowString=Lines[n]
	CurRowTest=CurRowString[0:5]
	if CurRowTest=="TRACK":
		BeatRow=n
		RowsPerPattern=int(CurRowString[6:9])
		break	
print "row information found on line ", BeatRow
print "There are ",RowsPerPattern, "rows per pattern"
PatternSize=RowsPerPattern+2
print "Total Pattern Size (with headers) is ",PatternSize
print ""

print "Searching for PATTERN 00"
for n in range(LineCount):
	CurRowString=Lines[n]
	CurRowTest=CurRowString[0:10]
	if CurRowTest=="PATTERN 00":
		DataStartRow=n-1
		break
print "Pattern data starts on line ",DataStartRow	

TotalLines=len(Lines)
TotalDataLines=(TotalLines-DataStartRow)
print "There are ",TotalDataLines," lines of data"
TotalPatterns=TotalDataLines/PatternSize
print "There are a total of ",TotalPatterns," total patterns"
print ""	

print "Searching for ORDER information..."
for n in range(LineCount):
	CurRowString=Lines[n]
	CurRowTest=CurRowString[0:5]
	if CurRowTest=="ORDER":
		OrderStartRow=n
		break	
print "ORDER information starts on row",OrderStartRow
for n in range(LineCount):
	CurRowString=Lines[n+OrderStartRow]
	CurRowTest=CurRowString[0:5]
	if CurRowTest=="":
		OrderEndRow=n+OrderStartRow-1
		break	
print "ORDER information ends on row",OrderEndRow
TotalOrders=OrderEndRow-OrderStartRow+1
print "There are ",TotalOrders," total ORDER rows"
print ""

print "Searching for information about effects per column..."
for n in range(LineCount):
	CurRowString=Lines[n]
	CurRowTest=CurRowString[0:7]
	if CurRowTest=="COLUMNS":
		ColumnRow=n
		break	
ColumnString=Lines[n]
Square1Columns=int(ColumnString[10:11])
Square2Columns=int(ColumnString[12:13])
TriangleColumns=int(ColumnString[14:15])
NoiseColumns=int(ColumnString[16:17])

Square1ColumnStart=9
Square2ColumnStart=Square1ColumnStart+15+4*(Square1Columns-1)
TriangleColumnStart=Square2ColumnStart+15+4*(Square2Columns-1)
NoiseColumnStart=TriangleColumnStart+15+4*(TriangleColumns-1)

print "Number of columsn per channel.  Square1:",Square1Columns," Square2:",Square2Columns," Triangle Columns:",TriangleColumns," Noise Columns:",NoiseColumns
print "Square1 starts at:",Square1ColumnStart," Square2 starts at:",Square2ColumnStart," Triangle starts at:",TriangleColumnStart," Noise starts at:",NoiseColumnStart

Square1Order=[]
Square2Order=[]
TriangleOrder=[]
NoiseOrder=[]

print "Extracting Order information into individual voice lists..."
for n in range(TotalOrders):
	
	CurRowString=Lines[n+OrderStartRow]
	Square1CurOrder=CurRowString[11:13]
	Square1Order.append(Square1CurOrder)
	
	Square2CurOrder=CurRowString[14:16]
	Square2Order.append(Square2CurOrder)
	
	TriangleCurOrder=CurRowString[17:19]
	TriangleOrder.append(TriangleCurOrder)
	
	NoiseCurOrder=CurRowString[20:22]
	NoiseOrder.append(NoiseCurOrder)
	
print "Here is the completed Square1 Order List"
print Square1Order

print "Here is the completed Square2 Order List"
print Square2Order

print "Here is the completed Triangle Order List"
print TriangleOrder

print "Here is the completed Noise Order List"
print NoiseOrder
print ""


Square1LastFrame=0
Square2LastFrame=0
TriangleLastFrame=0
N4LastFrame=0

Square1EndedOnD00=0
Square2EndedOnD00=0
TriangleEndedOnD00=0
NoiseEndedOnD00=0

S1Duration=0
S2Duration=0
S3Duration=0
N4Duration=0

Square1Pattern = [[] for _ in range(TotalPatterns)]
Square2Pattern = [[] for _ in range(TotalPatterns)]
TrianglePattern=[[] for _ in range(TotalPatterns)]
NoisePattern=[[] for _ in range(TotalPatterns)]

print "Now let's start extracting pattern data"

for n in range(TotalPatterns):
	for i in range(RowsPerPattern):

		CurRowString=Lines[n*PatternSize+DataStartRow+i+2]
		
		Square1CurString=CurRowString[Square1ColumnStart:Square1ColumnStart+3]
		Square1Cmd=CurRowString[Square1ColumnStart+9:Square1ColumnStart+12]
		
		Square2CurString=CurRowString[Square2ColumnStart:Square2ColumnStart+3]
		Square2Cmd=CurRowString[Square2ColumnStart+9:Square2ColumnStart+12]
		
		TriangleCurString=CurRowString[TriangleColumnStart:TriangleColumnStart+3]
		TriangleCmd=CurRowString[TriangleColumnStart+9:TriangleColumnStart+12]
		
		NoiseCurString=CurRowString[NoiseColumnStart:NoiseColumnStart+3]
		NoiseCmd=CurRowString[NoiseColumnStart+9:NoiseColumnStart+12]

###### Calculate Square1 Data ######	
		if Square1EndedOnD00==0:
		
			if i==0 and Square1CurString==BlankLine:  #Set as "Stop Note" if no data on the first line
				Square1Pattern[n].append(75)			#Code 75 is the "stop" note
				Square1LastFrame=i
				
			if Square1CurString!=BlankLine:
				Square1Note=Square1CurString.replace(".","")
				if Square1Note!=StopNote1 and Square1Note!=StopNote2:
					Square1Note=Square1Note.replace("-","")
					if i>0:				#append duration value only if this isn't the first note in the list
						Square1NoteDuration=i-Square1LastFrame
						Square1Pattern[n].append(Square1NoteDuration+DurationModifier)
					Square1Pattern[n].append(Square1Note)
					Square1LastFrame=i
					
				if Square1Note==StopNote1 or Square1Note==StopNote2:
					if i>0:
						Square1NoteDuration=i-Square1LastFrame
						Square1Pattern[n].append(Square1NoteDuration+DurationModifier)
					Square1Pattern[n].append(75)
					Square1LastFrame=i
	
	###### Calculate Square2 Data ######
		if Square2EndedOnD00==0:
			if i==0 and Square2CurString==BlankLine:  #Set as "Stop Note" if no data on the first line
				Square2Pattern[n].append(75)			#Code 75 is the "stop" note
				Square2LastFrame=i
				
			if Square2CurString!=BlankLine:
				Square2Note=Square2CurString.replace(".","")
				if Square2Note!=StopNote1 and Square2Note!=StopNote2:
					Square2Note=Square2Note.replace("-","")
					if i>0:				#append duration value only if this isn't the first note in the list
						Square2NoteDuration=i-Square2LastFrame
						Square2Pattern[n].append(Square2NoteDuration+DurationModifier)
					Square2Pattern[n].append(Square2Note)
					Square2LastFrame=i
					
				if Square2Note==StopNote1 or Square2Note==StopNote2:
					if i>0:
						Square2NoteDuration=i-Square2LastFrame
						Square2Pattern[n].append(Square2NoteDuration+DurationModifier)
					Square2Pattern[n].append(75)
					Square2LastFrame=i				

	###### Calculate Triangle Data ######		
		if TriangleEndedOnD00==0:
			if i==0 and TriangleCurString==BlankLine:  #Set as "Stop Note" if no data on the first line
				TrianglePattern[n].append(75)			#Code 75 is the "stop" note
				TriangleLastFrame=i
				
			if TriangleCurString!=BlankLine:
				TriangleNote=TriangleCurString.replace(".","")
				if TriangleNote!=StopNote1 and TriangleNote!=StopNote2:
					TriangleNote=TriangleNote.replace("-","")
					if i>0:				#append duration value only if this isn't the first note in the list
						TriangleNoteDuration=i-TriangleLastFrame
						TrianglePattern[n].append(TriangleNoteDuration+DurationModifier)
					TrianglePattern[n].append(TriangleNote)
					TriangleLastFrame=i
					
				if (TriangleNote==StopNote1) or (TriangleNote==StopNote2):
					if i>0:
						TriangleNoteDuration=i-TriangleLastFrame
						TrianglePattern[n].append(TriangleNoteDuration+DurationModifier)
					TrianglePattern[n].append(75)
					TriangleLastFrame=i
				
	###### Calculate Noise Data ######		
		if NoiseEndedOnD00==0:
			if i==0 and NoiseCurString==BlankLine:  #Set as "Stop Note" if no data on the first line
				NoisePattern[n].append(75)			#Code 75 is the "stop" note
				NoiseLastFrame=i
				
			if NoiseCurString!=BlankLine:
				NoiseNote=NoiseCurString.replace(".","")
				if (NoiseNote!=StopNote1) and (NoiseNote!=StopNote2):
					NoiseNote=NoiseNote.replace("-","")
					if i>0:				#append duration value only if this isn't the first note in the list
						NoiseNoteDuration=i-NoiseLastFrame
						NoisePattern[n].append(NoiseNoteDuration+DurationModifier)
		
						
					NoisePattern[n].append(NoiseNote)
					NoiseLastFrame=i
					
				if (NoiseNote==StopNote1) or (NoiseNote==StopNote2):
					if i>0:
						NoiseNoteDuration=i-NoiseLastFrame
						NoisePattern[n].append(NoiseNoteDuration+DurationModifier)
					NoisePattern[n].append(75)
					NoiseLastFrame=i
		
		if Square1Cmd=="D00":
			print "D00 detected in line",(n*PatternSize+DataStartRow+i+2),", terminating Square 1 pattern"
			Square1EndedOnD00=1
			Square1NoteDuration=i-Square1LastFrame
			Square1Pattern[n].append(Square1NoteDuration)
			
		if Square2Cmd=="D00":
			print "D00 detected in line",(n*PatternSize+DataStartRow+i+2),", terminating Square 2 pattern"
			Square2EndedOnD00=1
			Square2NoteDuration=i-Square2LastFrame
			Square2Pattern[n].append(Square2NoteDuration)
		if TriangleCmd=="D00":
			TriangleEndedOnD00=1
			print "D00 detected in line",(n*PatternSize+DataStartRow+i+2),", terminating Triangle pattern"
			TriangleNoteDuration=i-TriangleLastFrame
			TrianglePattern[n].append(TriangleNoteDuration)
		if NoiseCmd=="D00":
			NoiseEndedOnD00=1
			print "D00 detected in line",(n*PatternSize+DataStartRow+i+2),", terminating Noise pattern"
			NoiseNoteDuration=i-NoiseLastFrame
			NoisePattern[n].append(NoiseNoteDuration)
			

	Square1NoteDuration=RowsPerPattern-Square1LastFrame
	Square1Pattern[n].append(Square1NoteDuration+DurationModifier)
	
	Square2NoteDuration=RowsPerPattern-Square2LastFrame
	Square2Pattern[n].append(Square2NoteDuration+DurationModifier)
	
	TriangleNoteDuration=RowsPerPattern-TriangleLastFrame
	TrianglePattern[n].append(TriangleNoteDuration+DurationModifier)
	
	NoiseNoteDuration=RowsPerPattern-NoiseLastFrame
	NoisePattern[n].append(NoiseNoteDuration+DurationModifier)

	Square1LastFrame=0
	Square2LastFrame=0
	TriangleLastFrame=0
	NoiseLastFrame=0
	Square1EndedOnD00=0
	Square2EndedOnD00=0
	TriangleEndedOnD00=0
	NoiseEndedOnD00=0
	
print "NoisePattern is",NoisePattern
	
#############################################	
######## Build out note data for VIC ########
#############################################
print ""
print "Recostructing sequential note data for the VIC-20"


#with open("asmPlayer_template.txt", 'r') as f:
#	program_data_out = f.read().splitlines()

program_data_out=[] #array to store all the note and duration data
address_header_out=[] #array to store the address start locations for each of the voices
bytestr="		byte "	
TotalLength=0

s3addr=hex(DataStartAddrDec)
s3highstr=s3addr[2:4]
s3lowstr=s3addr[4:6]

program_data_out.append("; S3 Note Data   ")	
for n in range(TotalOrders):
	
	CurrentOrder=int(Square1Order[n], 16)
	CurrentPattern=Square1Pattern[CurrentOrder]
	
	#print "Current Section is ",n,", loading in Pattern number ",CurrentOrder
	CurrentPatternLen=len(CurrentPattern)
	print "Current Pattern is :",CurrentPattern
	
	for i in range(CurrentPatternLen/2):
		CurrentNoteEng=CurrentPattern[i*2]
		CurrentDuration=CurrentPattern[i*2+1]
		
		if ((CurrentNoteEng != 75) and (CurrentNoteEng != 80)):  #Normal note positions
			CurrentNotePos=ABCList.index(CurrentNoteEng)
			ToneLow=ToneLowByte[CurrentNotePos+Square1NoteModifier]
			ToneHigh=ToneHighByte[CurrentNotePos+Square1NoteModifier]
			buildstr=bytestr + str(ToneLow) + "; S3 Low Byte Data"
			program_data_out.append(buildstr)
			buildstr=bytestr + str(ToneHigh) + "; S3 Low Byte Data"
			program_data_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; S3 Duration Data"
			program_data_out.append(buildstr)
			
		if CurrentNoteEng==75:		#Stop Code
			ToneHigh=0
			ToneLow=0	
			buildstr=bytestr + str(ToneLow) + "; S3 Low Byte Data"
			program_data_out.append(buildstr)
			buildstr=bytestr + str(ToneHigh) + "; S3 Low Byte Data"
			program_data_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; S3 Duration Data"
			program_data_out.append(buildstr)
			
		DataStartAddrDec=DataStartAddrDec+3
			
buildstr=bytestr + str(80) + "; S3 End of Song code"
program_data_out.append(buildstr)

DataStartAddrDec=DataStartAddrDec+1
s2addr=hex(DataStartAddrDec)
s2highstr=s2addr[2:4]
s2lowstr=s2addr[4:6]

program_data_out.append("; S2 Note Data   ")		
print "Square1 data compiled, starting Square2..."
print ""

for n in range(TotalOrders):
	CurrentOrder=int(Square2Order[n], 16)
	CurrentPattern=Square2Pattern[CurrentOrder]
	CurrentPatternLen=len(CurrentPattern)
	
	for l in range(CurrentPatternLen/2):
		TotalLength=TotalLength+int(CurrentPattern[2*l+1])
	TotalLength=TotalLength+CurrentPatternLen/2
	print "Section",n,", Pattern number",CurrentOrder, ":",CurrentPattern," legth:",TotalLength
	TotalLength=0
	
	
	for i in range(CurrentPatternLen/2):
		CurrentNoteEng=CurrentPattern[i*2]
		CurrentDuration=CurrentPattern[i*2+1]
		
		if ((CurrentNoteEng != 75) and (CurrentNoteEng != 80)):  #Normal note positions
			CurrentNotePos=ABCList.index(CurrentNoteEng)
			ToneLow=ToneLowByte[CurrentNotePos+Square2NoteModifier]
			ToneHigh=ToneHighByte[CurrentNotePos+Square2NoteModifier]
			buildstr=bytestr + str(ToneLow) + "; S2 Low Byte Data"
			program_data_out.append(buildstr)
			buildstr=bytestr + str(ToneHigh) + "; S2 Low Byte Data"
			program_data_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; S2 Duration Data"
			program_data_out.append(buildstr)
			
		if CurrentNoteEng==75:		#Stop Code
			ToneHigh=0
			ToneLow=0	
			buildstr=bytestr + str(ToneLow) + "; S2 Low Byte Data"
			program_data_out.append(buildstr)
			buildstr=bytestr + str(ToneHigh) + "; S2 Low Byte Data"
			program_data_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; S2 Duration Data"
			program_data_out.append(buildstr)
			
		DataStartAddrDec=DataStartAddrDec+3
buildstr=bytestr + str(80) + "; S2 End of Song code"
program_data_out.append(buildstr)
		
print "Square2 data compiled, starting Square2..."
print ""	

DataStartAddrDec=DataStartAddrDec+1
s1addr=hex(DataStartAddrDec)
s1highstr=s1addr[2:4]
s1lowstr=s1addr[4:6]

program_data_out.append("; S1 Note Data   ")		
			
for n in range(TotalOrders):
	CurrentOrder=int(TriangleOrder[n], 16)
	CurrentPattern=TrianglePattern[CurrentOrder]
	#print "Current Section is ",n,", loading in Pattern number ",CurrentOrder
	CurrentPatternLen=len(CurrentPattern)
	
	for i in range(CurrentPatternLen/2):
		CurrentNoteEng=CurrentPattern[i*2]
		CurrentDuration=CurrentPattern[i*2+1]
		
		if ((CurrentNoteEng != 75) and (CurrentNoteEng != 80)):  #Normal note positions
			CurrentNotePos=ABCList.index(CurrentNoteEng)
			ToneLow=ToneLowByte[CurrentNotePos+TriangleNoteModifier]
			ToneHigh=ToneHighByte[CurrentNotePos+TriangleNoteModifier]
			buildstr=bytestr + str(ToneLow) + "; S1 Low Byte Data"
			program_data_out.append(buildstr)
			buildstr=bytestr + str(ToneHigh) + "; S1 Low Byte Data"
			program_data_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; S1 Duration Data"
			program_data_out.append(buildstr)
			
		if CurrentNoteEng==75:		#Stop Code
			ToneHigh=0
			ToneLow=0	
			buildstr=bytestr + str(ToneLow) + "; S1 Low Byte Data"
			program_data_out.append(buildstr)
			buildstr=bytestr + str(ToneHigh) + "; S1 Low Byte Data"
			program_data_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; S1 Duration Data"
			program_data_out.append(buildstr)
			
		DataStartAddrDec=DataStartAddrDec+3
		
print "Triangle data compiled, starting Noise..."
print ""	

n4addr=hex(DataStartAddrDec)
n4highstr=n4addr[2:4]
n4lowstr=n4addr[4:6]	

program_data_out.append("; N4 Note Data   ")		
			
for n in range(TotalOrders):
	CurrentOrder=int(NoiseOrder[n], 16)
	CurrentPattern=NoisePattern[CurrentOrder]
	#print "Current Section is ",n,", loading in Pattern number ",CurrentOrder
	CurrentPatternLen=len(CurrentPattern)
	#print "CurrentPatternLen is ",CurrentPatternLen
	for i in range(CurrentPatternLen/2):
		CurrentNoteEng=CurrentPattern[i*2]
		CurrentDuration=CurrentPattern[i*2+1]
		print "CurrentNoteEng for Noise is",CurrentNoteEng," and duration is ",CurrentDuration
		
		if ((CurrentNoteEng != 75) and (CurrentNoteEng != 80)):  #Normal note positions
			CurrentNotePos=PercList.index(CurrentNoteEng)
			Tone=CurrentNotePos*6+128
			buildstr=bytestr + str(Tone) + "; N4 Low Byte Data"
			program_data_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; N4 Duration Data"
			program_data_out.append(buildstr)
			
		if CurrentNoteEng==75:		#Stop Code
			Tone=0	
			buildstr=bytestr + str(Tone) + "; N4 Low Byte Data"
			program_data_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; N4 Duration Data"
			program_data_out.append(buildstr)
print "Noise data compiled!  All done!"
print ""	
	
print "Noise Pattern 1 is ",NoisePattern[1]

if SwapS2S3==0:
	address_header_out.append("s3addrhighconst     byte $" + s3highstr)
	address_header_out.append("s3addrlowconst     byte $" + s3lowstr)
	address_header_out.append("s2addrhighconst     byte $" + s2highstr)
	address_header_out.append("s2addrlowconst     byte $" + s2lowstr)
	
if SwapS2S3==1:
	address_header_out.append("s3addrhighconst     byte $" + s2highstr)
	address_header_out.append("s3addrlowconst     byte $" + s2lowstr)
	address_header_out.append("s2addrhighconst     byte $" + s3highstr)
	address_header_out.append("s2addrlowconst     byte $" + s3lowstr)

address_header_out.append("s1addrhighconst     byte $" + s1highstr)
address_header_out.append("s1addrlowconst     byte $" + s1lowstr)
address_header_out.append("n4addrhighconst     byte $" + n4highstr)
address_header_out.append("n4addrlowconst     byte $" + n4lowstr)
address_header_out.append("")
address_header_out.append("*=$"+DataStartAddress)
address_header_out.append("")
address_header_out.append("sounddata")

print address_header_out

program_out=[]
program_out=address_header_out
program_out=program_out+program_data_out

			
with open('program_out.txt', 'w') as f:
			for item in program_out:
				print >> f, item
					



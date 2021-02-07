#!/usr/bin/env python

import sys

with open(sys.argv[1], 'r') as my_file:
	LineCount = len(my_file.readlines(  ))
	
with open(sys.argv[1], 'r') as f:
	Lines = f.read().splitlines()	

BlankLine="..."
StopNote="---"
#StopNote="==="

ABCList=["C0","C#0","D0","D#0","E0","F0","F#0","G0","G#0","A0","A#0","B0","C1","C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1","A#1","B1","C2","C#2","D2","D#2","E2","F2","F#2","G2","G#2","A2","A#2","B2","C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3","A#3","B3","C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4","C5","C#5","D5","D#5","E5","F5","F#5","G5","G#5","A5","A#5","B5"]
PercList=["C2","D2","D#2","E2","F2","F#2","G2","G#2","A2","A#2","B2","C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3","A#3","B3","C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4","C5","C#5"]



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
		Square1CurString=CurRowString[9:12]
		Square2CurString=CurRowString[32:35]
		TriangleCurString=CurRowString[55:58]
		NoiseCurString=CurRowString[78:81]

###### Calculate Square1 Data ######		
		if i==0 and Square1CurString==BlankLine:  #Set as "Stop Note" if no data on the first line
			Square1Pattern[n].append(75)			#Code 75 is the "stop" note
			Square1LastFrame=i
			
		if Square1CurString!=BlankLine:
			Square1Note=Square1CurString.replace(".","")
			if Square1Note!=StopNote:
				Square1Note=Square1Note.replace("-","")
				if i>0:				#append duration value only if this isn't the first note in the list
					Square1NoteDuration=i-Square1LastFrame
					Square1Pattern[n].append(Square1NoteDuration+DurationModifier)
				Square1Pattern[n].append(Square1Note)
				Square1LastFrame=i
				
			if Square1Note==StopNote:
				if i>0:
					Square1NoteDuration=i-Square1LastFrame
					Square1Pattern[n].append(Square1NoteDuration+DurationModifier)
				Square1Pattern[n].append(75)
				Square1LastFrame=i
	
	###### Calculate Square2 Data ######		
		if i==0 and Square2CurString==BlankLine:  #Set as "Stop Note" if no data on the first line
			Square2Pattern[n].append(75)			#Code 75 is the "stop" note
			Square2LastFrame=i
			
		if Square2CurString!=BlankLine:
			Square2Note=Square2CurString.replace(".","")
			if Square2Note!=StopNote:
				Square2Note=Square2Note.replace("-","")
				if i>0:				#append duration value only if this isn't the first note in the list
					Square2NoteDuration=i-Square2LastFrame
					Square2Pattern[n].append(Square2NoteDuration+DurationModifier)
				Square2Pattern[n].append(Square2Note)
				Square2LastFrame=i
				
			if Square2Note==StopNote:
				if i>0:
					Square2NoteDuration=i-Square2LastFrame
					Square2Pattern[n].append(Square2NoteDuration+DurationModifier)
				Square2Pattern[n].append(75)
				Square2LastFrame=i				

	###### Calculate Triangle Data ######		
		if i==0 and TriangleCurString==BlankLine:  #Set as "Stop Note" if no data on the first line
			TrianglePattern[n].append(75)			#Code 75 is the "stop" note
			TriangleLastFrame=i
			
		if TriangleCurString!=BlankLine:
			TriangleNote=TriangleCurString.replace(".","")
			if TriangleNote!=StopNote:
				TriangleNote=TriangleNote.replace("-","")
				if i>0:				#append duration value only if this isn't the first note in the list
					TriangleNoteDuration=i-TriangleLastFrame
					TrianglePattern[n].append(TriangleNoteDuration+DurationModifier)
				TrianglePattern[n].append(TriangleNote)
				TriangleLastFrame=i
				
			if TriangleNote==StopNote:
				if i>0:
					TriangleNoteDuration=i-TriangleLastFrame
					TrianglePattern[n].append(TriangleNoteDuration+DurationModifier)
				TrianglePattern[n].append(75)
				TriangleLastFrame=i
				
	###### Calculate Noise Data ######		
		if i==0 and NoiseCurString==BlankLine:  #Set as "Stop Note" if no data on the first line
			NoisePattern[n].append(75)			#Code 75 is the "stop" note
			NoiseLastFrame=i
			
		if NoiseCurString!=BlankLine:
			NoiseNote=NoiseCurString.replace(".","")
			if NoiseNote!=StopNote:
				NoiseNote=NoiseNote.replace("-","")
				if i>0:				#append duration value only if this isn't the first note in the list
					NoiseNoteDuration=i-NoiseLastFrame
					NoisePattern[n].append(NoiseNoteDuration+DurationModifier)
					
				if NoiseNote=="D#":
					NoisePattern[n].append(151)
				if NoiseNote=="8#":
					NoisePattern[n].append(236)
					
				#NoisePattern[n].append(NoiseNote)
				NoiseLastFrame=i
				
			if NoiseNote==StopNote:
				if i>0:
					NoiseNoteDuration=i-NoiseLastFrame
					NoisePattern[n].append(NoiseNoteDuration+DurationModifier)
				NoisePattern[n].append(75)
				NoiseLastFrame=i
		
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
	
#############################################	
######## Build out note data for VIC ########
#############################################
print ""
print "Recostructing sequential note data for the VIC-20"


with open("asmPlayer_template.txt", 'r') as f:
	program_out = f.read().splitlines()

#program_out=[]
bytestr="		byte "	

program_out.append("; S3 Note Data   ")	
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
			ToneLow=ToneLowByte[CurrentNotePos-12]
			ToneHigh=ToneHighByte[CurrentNotePos-12]
			buildstr=bytestr + str(ToneLow) + "; S3 Low Byte Data"
			program_out.append(buildstr)
			buildstr=bytestr + str(ToneHigh) + "; S3 Low Byte Data"
			program_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; S3 Duration Data"
			program_out.append(buildstr)
			
		if CurrentNoteEng==75:		#Stop Code
			ToneHigh=0
			ToneLow=0	
			buildstr=bytestr + str(ToneLow) + "; S3 Low Byte Data"
			program_out.append(buildstr)
			buildstr=bytestr + str(ToneHigh) + "; S3 Low Byte Data"
			program_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; S3 Duration Data"
			program_out.append(buildstr)
			
			
buildstr=bytestr + str(80) + "; S3 End of Song code"
program_out.append(buildstr)

program_out.append("; S2 Note Data   ")		
print "Square1 data compiled, starting Square2..."
print ""

for n in range(TotalOrders):
	CurrentOrder=int(Square2Order[n], 16)
	CurrentPattern=Square2Pattern[CurrentOrder]
	#print "Current Section is ",n,", loading in Pattern number ",CurrentOrder
	CurrentPatternLen=len(CurrentPattern)
	
	for i in range(CurrentPatternLen/2):
		CurrentNoteEng=CurrentPattern[i*2]
		CurrentDuration=CurrentPattern[i*2+1]
		
		if ((CurrentNoteEng != 75) and (CurrentNoteEng != 80)):  #Normal note positions
			CurrentNotePos=ABCList.index(CurrentNoteEng)
			ToneLow=ToneLowByte[CurrentNotePos]
			ToneHigh=ToneHighByte[CurrentNotePos]
			buildstr=bytestr + str(ToneLow) + "; S2 Low Byte Data"
			program_out.append(buildstr)
			buildstr=bytestr + str(ToneHigh) + "; S2 Low Byte Data"
			program_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; S2 Duration Data"
			program_out.append(buildstr)
			
		if CurrentNoteEng==75:		#Stop Code
			ToneHigh=0
			ToneLow=0	
			buildstr=bytestr + str(ToneLow) + "; S2 Low Byte Data"
			program_out.append(buildstr)
			buildstr=bytestr + str(ToneHigh) + "; S2 Low Byte Data"
			program_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; S2 Duration Data"
			program_out.append(buildstr)
print "Square2 data compiled, starting Square2..."
print ""	

program_out.append("; S1 Note Data   ")		
			
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
			ToneLow=ToneLowByte[CurrentNotePos-24]
			ToneHigh=ToneHighByte[CurrentNotePos-24]
			buildstr=bytestr + str(ToneLow) + "; S1 Low Byte Data"
			program_out.append(buildstr)
			buildstr=bytestr + str(ToneHigh) + "; S1 Low Byte Data"
			program_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; S1 Duration Data"
			program_out.append(buildstr)
			
		if CurrentNoteEng==75:		#Stop Code
			ToneHigh=0
			ToneLow=0	
			buildstr=bytestr + str(ToneLow) + "; S1 Low Byte Data"
			program_out.append(buildstr)
			buildstr=bytestr + str(ToneHigh) + "; S1 Low Byte Data"
			program_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; S1 Duration Data"
			program_out.append(buildstr)
print "Triangle data compiled, starting Noise..."
print ""		

program_out.append("; N4 Note Data   ")		
			
for n in range(TotalOrders):
	CurrentOrder=int(NoiseOrder[n], 16)
	CurrentPattern=NoisePattern[CurrentOrder]
	print "Current Section is ",n,", loading in Pattern number ",CurrentOrder
	CurrentPatternLen=len(CurrentPattern)
	print "CurrentPatternLen is ",CurrentPatternLen
	
	for i in range(CurrentPatternLen/2):
		CurrentNoteEng=CurrentPattern[i*2]
		
		
		CurrentDuration=CurrentPattern[i*2+1]
		print "CurrentNoteEng for Noise is",CurrentNoteEng," and duration is ",CurrentDuration
		
		if ((CurrentNoteEng != 75) and (CurrentNoteEng != 80)):  #Normal note positions
			#CurrentNotePos=PercList.index(CurrentNoteEng)
			#Tone=PercTone[CurrentNotePos]
			Tone=CurrentNoteEng
			buildstr=bytestr + str(Tone) + "; N4 Low Byte Data"
			program_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; N4 Duration Data"
			program_out.append(buildstr)
			
		if CurrentNoteEng==75:		#Stop Code
			Tone=0	
			buildstr=bytestr + str(Tone) + "; N4 Low Byte Data"
			program_out.append(buildstr)
			buildstr=bytestr + str(CurrentDuration) + "; N4 Duration Data"
			program_out.append(buildstr)
print "Noise data compiled!  All done!"
print ""	
	
print "Noise Pattern 1 is ",NoisePattern[1]
			
with open('program_out.txt', 'w') as f:
			for item in program_out:
				print >> f, item
					



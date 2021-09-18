#!/usr/bin/env python

import sys

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-i", "--input", dest="input_file",
                    help="input famitracker text export", metavar="FILE")					
parser.add_argument("-o", "--output", dest="output_file", default="program_out.txt",
					help="destination text file with asm code", metavar="FILE")
parser.add_argument("-S1", "--square1", dest="square1",
					help="Square1 Note position modifier (default=-24)", metavar="INTEGER")
parser.add_argument("-S2", "--square2", dest="square2",
					help="Square2 Note position modifier (default=-12)", metavar="INTEGER")
parser.add_argument("-T", "--triangle", dest="triangle",
					help="Triangle Note position modifier (default=-12)", metavar="INTEGER")
parser.add_argument("-V", "--volume", dest="volume",
					help="Volume Mute Cutoff Level (default=-1)", metavar="INTEGER")
parser.add_argument("-NC", "--nvolume", dest="noisevolume",
					help="Noise Channel Volume Mute Cutoff Level (default=4)", metavar="INTEGER")
parser.add_argument("-D", "--data", dest="datastart",
					help="Data Start Address (HEX)(default=2110)", metavar="STRING")
parser.add_argument("-SW", "--swap",
                    action="store_true", dest="swaps2s3", default=False,
                    help="Assign Square1 to S2 and Square2 to S3")
parser.add_argument("-I", "--ignore",
                    action="store_true", dest="ignoreall", default=True,
                    help="Ignore all errors due to over/underflow and replace with stop notes instead")
parser.add_argument("-CU", "--correct-underflow",
                    action="store_true", dest="correctunderflow", default=False,
                    help="Attempt to correct underflowed (too low) notes by shifting them up 1 octave")
parser.add_argument("-CO", "--correct-overflow",
                    action="store_true", dest="correctoverflow", default=False,
                    help="Attempt to correct overflowed (too high) notes by shifting them down 1 octave")
parser.add_argument("-F", "--full",
                    action="store_true", dest="full", default=False,
                    help="Output full ASM program using asmPlayer_template.txt")
parser.add_argument("-C64", "--commodore64",
                    action="store_true", dest="c64mode", default=False,
                    help="Compile PRG for Commodore 64")
					

args = parser.parse_args()

if args.input_file==None:
	print "No Input file specified!  Exiting..."
	sys.exit()

if args.swaps2s3==False:
	SwapS2S3=0
else:
	SwapS2S3=1
	
if args.c64mode==False:
	c64mode=0
else:
	c64mode=1
	
if c64mode==1:
	mute_note=97
	max_note=96
else:
	mute_note=73
	max_note=72
	
	

if SwapS2S3==0 and c64mode==0:
	if args.square1==None:
		print "No Square1 Modifier specified, defaulting to -24"
		Square1NoteModifier=-24
	else:
		Square1NoteModifier=int(args.square1)
		
	if args.square2==None:
		print "No Square2 Modifier specified, defaulting to -12"
		Square2NoteModifier=-12
	else:
		Square2NoteModifier=int(args.square2)
		
	if args.triangle==None:
		print "No Triangle Modifier specified, defaulting to -12"
		TriangleNoteModifier=-12
	else:
		TriangleNoteModifier=int(args.triangle)
		
if SwapS2S3==1 and c64mode==0:
	if args.square1==None:
		print "No Square1 Modifier specified, defaulting to -12"
		Square1NoteModifier=-12
	else:
		Square1NoteModifier=int(args.square1)
		
	if args.square2==None:
		print "No Square2 Modifier specified, defaulting to -24"
		Square2NoteModifier=-24
	else:
		Square2NoteModifier=int(args.square2)
		
	if args.triangle==None:
		print "No Triangle Modifier specified, defaulting to -12"
		TriangleNoteModifier=-12
	else:
		TriangleNoteModifier=int(args.triangle)
		
if c64mode==1:
	if args.square1==None:
		print "No Square1 Modifier specified, defaulting to 12"
		Square1NoteModifier=12
	else:
		Square1NoteModifier=int(args.square1)
		
	if args.square2==None:
		print "No Square2 Modifier specified, defaulting to 12"
		Square2NoteModifier=12
	else:
		Square2NoteModifier=int(args.square2)
		
	if args.triangle==None:
		print "No Triangle Modifier specified, defaulting to 0"
		TriangleNoteModifier=0
	else:
		TriangleNoteModifier=int(args.triangle)
			
		
if args.datastart==None and c64mode==0:
	print "No data start address specified, using 2110 (HEX)"
	DataStartAddress="2110"
elif args.datastart==None and c64mode==1:
	print "No data start address specified, using 5110 (HEX)"
	DataStartAddress="5400"
else:
	DataStartAddress=args.datastart
		
DataStartAddrDec=int(DataStartAddress,16)

if args.volume==None:
	print "No Voice Channel Volume Cutoff Specified, volume cutoff ignored"
	VolumeCutoff=-1
else:
	VolumeCutoff=int(args.volume)
	
if args.noisevolume==None:
	print "No Noise Channel Volume Cutoff Specified, defaulting to 8"
	NoiseVolumeCutoff=8
else:
	NoiseVolumeCutoff=int(args.noisevolume)

print "DataStartAddrDec is", DataStartAddrDec

input_file=args.input_file
output_file=args.output_file

with open(input_file, 'r') as my_file:
	LineCount = len(my_file.readlines(  ))
	
with open(input_file, 'r') as f:
	Lines = f.read().splitlines()	

BlankLine="..."
StopNote1="---"
StopNote2="==="
BlankVol="."

Square1VolMuted=0
Square1LastMutedNote=0
Square2VolMuted=0
Square2LastMutedNote=0
TriangleVolMuted=0
TriangleLastMutedNote=0


IgnoreUnderflowErrors=args.ignoreall
IgnoreOverflowErrors=args.ignoreall

CorrectUnderflowErrors=args.correctunderflow
CorrectOverflowErrors=args.correctoverflow

NoiseMutedNotes=0
TriangleMutedNotes=0
Square2MutedNotes=0
Square1MutedNotes=0

Square1NumOverNotes=0
Square1NumUnderNotes=0
Square1NumCorrectedNotes=0
Square2NumOverNotes=0
Square2NumUnderNotes=0
Square2NumCorrectedNotes=0
TriangleNumOverNotes=0
TriangleNumUnderNotes=0
TriangleNumCorrectedNotes=0
NoiseNumOverNotes=0
NoiseNumUnderNotes=0
NoiseNumCorrectedNotes=0


LoopPoint=0

ABCList=["C0","C#0","D0","D#0","E0","F0","F#0","G0","G#0","A0","A#0","B0","C1","C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1","A#1","B1","C2","C#2","D2","D#2","E2","F2","F#2","G2","G#2","A2","A#2","B2","C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3","A#3","B3","C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4","C5","C#5","D5","D#5","E5","F5","F#5","G5","G#5","A5","A#5","B5","C6","C#6","D6","D#6","E6","F6","F#6","G6","G#6","A6","A#6","B6","C7","C#7","D7","D#7","E7","F7","F#7","G7","G#7","A7","A#7","B7",108]
PercList=["0#","1#","2#","3#","4#","5#","6#","7#","8#","9#","A#","B#","C#","D#","E#","F#"]


PercTone=[135,147,151,159,163,167,173,179,183,187,191,195,199,201,203,207,209,212,215,217,219,221,223,225,227,228,229,231,232,233,235,236,237,238,239,240,241]


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

print "Number of columns per channel.  Square1:",Square1Columns," Square2:",Square2Columns," Triangle Columns:",TriangleColumns," Noise Columns:",NoiseColumns
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

Square1Mute=0
Square2Mute=0
TriangleMute=0

Square1LastNote=mute_note
Square2LastNote=mute_note
TriangleLastNote=mute_note
NoiseLastNote=mute_note

Square1EndedOnD00=0
Square2EndedOnD00=0
TriangleEndedOnD00=0
NoiseEndedOnD00=0

Square1Highest=0
Square1Lowest=max_note
Square2Highest=0
Square2Lowest=max_note
TriangleHighest=0
TriangleLowest=max_note

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
		Square1Vol=CurRowString[Square1ColumnStart+7:Square1ColumnStart+8]
		
		Square2CurString=CurRowString[Square2ColumnStart:Square2ColumnStart+3]
		Square2Cmd=CurRowString[Square2ColumnStart+9:Square2ColumnStart+12]
		Square2Vol=CurRowString[Square2ColumnStart+7:Square2ColumnStart+8]
		
		TriangleCurString=CurRowString[TriangleColumnStart:TriangleColumnStart+3]
		TriangleCmd=CurRowString[TriangleColumnStart+9:TriangleColumnStart+12]
		TriangleVol=CurRowString[TriangleColumnStart+7:TriangleColumnStart+8]
		
		NoiseCurString=CurRowString[NoiseColumnStart:NoiseColumnStart+3]
		NoiseCmd=CurRowString[NoiseColumnStart+9:NoiseColumnStart+12]
		NoiseVol=CurRowString[NoiseColumnStart+7:NoiseColumnStart+8]

###### Calculate Square1 Data ######	
		if Square1EndedOnD00==0:	
			if i==0 and Square1CurString==BlankLine:  #Set as "Stop Note" if no data on the first line
				if Square1Vol!=BlankVol:
					Square1VolDec=int(Square1Vol,16)
					if (Square1VolMuted==0 and Square1VolDec<VolumeCutoff) or (Square1VolMuted==1 and Square1VolDec>=VolumeCutoff):
						print "Ignoring beginning of pattern blank note, due to previous mute/unmute condition"
					else:
						#Square1Pattern[n].append(Square1LastNote)
						Square1Pattern[n].append(108)						
						#print "No beginning note detected (with volume parameter), appending code 108"
				else:
					#Square1Pattern[n].append(Square1LastNote)
					Square1Pattern[n].append(108)
					#print "No beginning note detected (with no volume), appending code 108"
				Square1LastFrame=i
				
			if Square1CurString!=BlankLine:
				Square1Note=Square1CurString.replace(".","")
				if Square1Note!=StopNote1 and Square1Note!=StopNote2:
					Square1Note=Square1Note.replace("-","")
					if i>0:				#append duration value only if this isn't the first note in the list
						Square1NoteDuration=i-Square1LastFrame
						Square1Pattern[n].append(Square1NoteDuration-1)
					Square1Pattern[n].append(Square1Note)
					Square1LastFrame=i
					
					Square1LastNote=Square1Note
					Square1VolMuted=0

					
				if Square1Note==StopNote1 or Square1Note==StopNote2:
					if i>0:
						Square1NoteDuration=i-Square1LastFrame
						Square1Pattern[n].append(Square1NoteDuration-1)
					Square1Pattern[n].append(mute_note)
					Square1LastFrame=i
					Square1LastNote=mute_note
					Square1VolMuted=0
					
###### Mute/Unmute notes based on volume cutoff ##########					
			if (Square1CurString==BlankLine) and (Square1Vol!=BlankVol):
				Square1VolDec=int(Square1Vol,16)
				if Square1VolDec<VolumeCutoff and Square1VolMuted==0:
					Square1LastMutedNote=Square1LastNote
					
					if i>0:
						Square1NoteDuration=i-Square1LastFrame
						Square1Pattern[n].append(Square1NoteDuration-1)
					Square1Pattern[n].append(mute_note)
					Square1LastFrame=i
					Square1LastNote=mute_note
					
					Square1VolMuted=0	
#					print "Found volume cutoff (",Square1VolDec,") at Pattern",n,", row",i,".  Muting note",Square1LastMutedNote,"duration:",Square1NoteDuration
					Square1VolMuted=1
									
				if Square1VolDec>=VolumeCutoff and Square1VolMuted:
				
					if i>0:				#append duration value only if this isn't the first note in the list
						Square1NoteDuration=i-Square1LastFrame
						Square1Pattern[n].append(Square1NoteDuration-1)
					Square1Pattern[n].append(Square1LastMutedNote)
					Square1LastFrame=i
					
					Square1LastNote=Square1LastMutedNote
#					print "Volume Muted note has risen above cutoff (",Square1VolDec,") level at Pattern",n,", row",i,".  Unmuting note",Square1LastMutedNote,"duration:",Square1NoteDuration
					Square1VolMuted=0
											
					
	
	###### Calculate Square2 Data ######
		if Square2EndedOnD00==0:	
			if i==0 and Square2CurString==BlankLine:  #Set as "Stop Note" if no data on the first line
				if Square2Vol!=BlankVol:
					Square2VolDec=int(Square2Vol,16)
					if (Square2VolMuted==0 and Square2VolDec<VolumeCutoff) or (Square2VolMuted==1 and Square2VolDec>=VolumeCutoff):
						print "Ignoring beginning of pattern blank note, due to previous mute/unmute condition"
					else:
						#Square2Pattern[n].append(Square2LastNote)
						Square2Pattern[n].append(108)						
						#print "No beginning note detected (with volume parameter), appending code 108"
				else:
					#Square2Pattern[n].append(Square2LastNote)
					Square2Pattern[n].append(108)
					#print "No beginning note detected (with no volume), appending code 108"
				Square2LastFrame=i
				
			if Square2CurString!=BlankLine:
				Square2Note=Square2CurString.replace(".","")
				if Square2Note!=StopNote1 and Square2Note!=StopNote2:
					Square2Note=Square2Note.replace("-","")
					if i>0:				#append duration value only if this isn't the first note in the list
						Square2NoteDuration=i-Square2LastFrame
						Square2Pattern[n].append(Square2NoteDuration-1)
					Square2Pattern[n].append(Square2Note)
					Square2LastFrame=i
					
					Square2LastNote=Square2Note
					Square2VolMuted=0

					
				if Square2Note==StopNote1 or Square2Note==StopNote2:
					if i>0:
						Square2NoteDuration=i-Square2LastFrame
						Square2Pattern[n].append(Square2NoteDuration-1)
					Square2Pattern[n].append(mute_note)
					Square2LastFrame=i	
					Square2LastNote=mute_note
					Square2VolMuted=0
					
					
					###### Mute/Unmute notes based on volume cutoff ##########					
			if (Square2CurString==BlankLine) and (Square2Vol!=BlankVol):
				Square2VolDec=int(Square2Vol,16)
				if Square2VolDec<VolumeCutoff and Square2VolMuted==0:
					Square2LastMutedNote=Square2LastNote
					
					if i>0:
						Square2NoteDuration=i-Square2LastFrame
						Square2Pattern[n].append(Square2NoteDuration-1)
					Square2Pattern[n].append(mute_note)
					Square2LastFrame=i
					Square2LastNote=mute_note
					
					Square2VolMuted=0	
#					print "Found volume cutoff (",Square2VolDec,") at Pattern",n,", row",i,".  Muting note",Square2LastMutedNote,"duration:",Square2NoteDuration
					Square2VolMuted=1
									
				if Square2VolDec>=VolumeCutoff and Square2VolMuted:
				
					if i>0:				#append duration value only if this isn't the first note in the list
						Square2NoteDuration=i-Square2LastFrame
						Square2Pattern[n].append(Square2NoteDuration-1)
					Square2Pattern[n].append(Square2LastMutedNote)
					Square2LastFrame=i
					
					Square2LastNote=Square2LastMutedNote
#					print "Volume Muted note has risen above cutoff (",Square2VolDec,") level at Pattern",n,", row",i,".  Unmuting note",Square2LastMutedNote,"duration:",Square2NoteDuration
					Square2VolMuted=0


	###### Calculate Triangle Data ######
		if TriangleEndedOnD00==0:	
			if i==0 and TriangleCurString==BlankLine:  #Set as "Stop Note" if no data on the first line
				if TriangleVol!=BlankVol:
					TriangleVolDec=int(TriangleVol,16)
					if (TriangleVolMuted==0 and TriangleVolDec<VolumeCutoff) or (TriangleVolMuted==1 and TriangleVolDec>=VolumeCutoff):
						print "Ignoring beginning of pattern blank note, due to previous mute/unmute condition"
					else:
						#TrianglePattern[n].append(TriangleLastNote)
						TrianglePattern[n].append(108)						
						#print "No beginning note detected (with volume parameter), appending code 108"
				else:
					#TrianglePattern[n].append(TriangleLastNote)
					TrianglePattern[n].append(108)
					#print "No beginning note detected (with no volume), appending code 108"
				TriangleLastFrame=i
				
			if TriangleCurString!=BlankLine:
				TriangleNote=TriangleCurString.replace(".","")
				if TriangleNote!=StopNote1 and TriangleNote!=StopNote2:
					TriangleNote=TriangleNote.replace("-","")
					if i>0:				#append duration value only if this isn't the first note in the list
						TriangleNoteDuration=i-TriangleLastFrame
						TrianglePattern[n].append(TriangleNoteDuration-1)
					TrianglePattern[n].append(TriangleNote)
					TriangleLastFrame=i
					
					TriangleLastNote=TriangleNote
					TriangleVolMuted=0
					
				if (TriangleNote==StopNote1) or (TriangleNote==StopNote2):
					if i>0:
						TriangleNoteDuration=i-TriangleLastFrame
						TrianglePattern[n].append(TriangleNoteDuration-1)
					TrianglePattern[n].append(mute_note)
					TriangleLastNote=mute_note					
					TriangleLastFrame=i
					TriangleVolMuted=0
					
					
			###### Mute/Unmute notes based on volume cutoff ##########					
			if (TriangleCurString==BlankLine) and (TriangleVol!=BlankVol):
				TriangleVolDec=int(TriangleVol,16)
				if TriangleVolDec<VolumeCutoff and TriangleVolMuted==0:
					print "Triangle Volume passed below threshhold"
					TriangleLastMutedNote=TriangleLastNote
					
					if i>0:
						TriangleNoteDuration=i-TriangleLastFrame
						TrianglePattern[n].append(TriangleNoteDuration-1)
					TrianglePattern[n].append(mute_note)
					TriangleLastFrame=i
					TriangleLastNote=mute_note
					print "Found volume cutoff (",TriangleVolDec,") at Pattern",n,", row",i,".  Muting note",TriangleLastMutedNote,"duration:",TriangleNoteDuration
					TriangleVolMuted=1
									
				if TriangleVolDec>=VolumeCutoff and TriangleVolMuted:
					print "Triangle Volume passed above threshhold"
					if i>0:				#append duration value only if this isn't the first note in the list
						TriangleNoteDuration=i-TriangleLastFrame
						TrianglePattern[n].append(TriangleNoteDuration-1)
					TrianglePattern[n].append(TriangleLastMutedNote)
					TriangleLastFrame=i
					
					TriangleLastNote=TriangleLastMutedNote
					print "Volume Muted note has risen above cutoff (",TriangleVolDec,") level at Pattern",n,", row",i,".  Unmuting note",TriangleLastMutedNote,"duration:",TriangleNoteDuration
					TriangleVolMuted=0
				
	###### Calculate Noise Data ######
		if NoiseEndedOnD00==0:	
			if i==0 and NoiseCurString==BlankLine:  #Set as "Stop Note" if no data on the first line
				if NoiseVol!=BlankVol:
					NoiseVolDec=int(NoiseVol,16)
					if (NoiseVolMuted==0 and NoiseVolDec<NoiseVolumeCutoff) or (NoiseVolMuted==1 and NoiseVolDec>=NoiseVolumeCutoff):
						print "Ignoring beginning of pattern blank note, due to previous mute/unmute condition"
					else:
						NoisePattern[n].append(mute_note)
				else:
					NoisePattern[n].append(mute_note)
				NoiseLastFrame=i
				
			if NoiseCurString!=BlankLine:
				NoiseNote=NoiseCurString.replace(".","")
				if NoiseNote!=StopNote1 and NoiseNote!=StopNote2:
					NoiseNote=NoiseNote.replace("-","")
					if i>0:				#append duration value only if this isn't the first note in the list
						NoiseNoteDuration=i-NoiseLastFrame
						NoisePattern[n].append(NoiseNoteDuration-1)
					NoisePattern[n].append(NoiseNote)
					NoiseLastFrame=i
					
					NoiseLastNote=NoiseNote
					NoiseVolMuted=0
					
				if (NoiseNote==StopNote1) or (NoiseNote==StopNote2):
					if i>0:
						NoiseNoteDuration=i-NoiseLastFrame
						NoisePattern[n].append(NoiseNoteDuration-1)
					NoisePattern[n].append(mute_note)
					NoiseLastNote=mute_note
					NoiseLastFrame=i
					NoiseVolMuted=0
					
					
			###### Mute/Unmute notes based on volume cutoff ##########					
			if (NoiseCurString==BlankLine) and (NoiseVol!=BlankVol):
				NoiseVolDec=int(NoiseVol,16)
				if NoiseVolDec<NoiseVolumeCutoff and NoiseVolMuted==0:
					NoiseLastMutedNote=NoiseLastNote
					
					if i>0:
						NoiseNoteDuration=i-NoiseLastFrame
						NoisePattern[n].append(NoiseNoteDuration-1)
					NoisePattern[n].append(mute_note)
					NoiseLastFrame=i
					NoiseLastNote=mute_note	
#					print "Found volume cutoff (",NoiseVolDec,") at Pattern",n,", row",i,".  Muting note",NoiseLastMutedNote,"duration:",NoiseNoteDuration
					NoiseVolMuted=1
									
				if NoiseVolDec>=NoiseVolumeCutoff and NoiseVolMuted:
				
					if i>0:				#append duration value only if this isn't the first note in the list
						NoiseNoteDuration=i-NoiseLastFrame
						NoisePattern[n].append(NoiseNoteDuration-1)
					NoisePattern[n].append(NoiseLastMutedNote)
					NoiseLastFrame=i
					
					NoiseLastNote=NoiseLastMutedNote
#					print "Volume Muted note has risen above cutoff (",NoiseVolDec,")(current volume:",NoiseVolDec,") level at Pattern",n,", row",i,".  Unmuting note",NoiseLastMutedNote,"duration:",NoiseNoteDuration
					NoiseVolMuted=0
		
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
			
		if Square1Cmd[0:1]=="B":
			LoopPointStr=Square1Cmd[1:3]
			LoopPoint=int(LoopPointStr,16)
			print "Loop point found at", LoopPoint,"!"
			
		if Square2Cmd[0:1]=="B":
			LoopPointStr=Square2Cmd[1:3]
			LoopPoint=int(LoopPointStr,16)
			print "Loop point found at", LoopPoint,"!"
		if TriangleCmd[0:1]=="B":
			LoopPointStr=TriangleCmd[1:3]
			LoopPoint=int(LoopPointStr,16)
			print "Loop point found at", LoopPoint,"!"
			
		if NoiseCmd[0:1]=="B":
			LoopPointStr=NoiseCmd[1:3]
			LoopPoint=int(LoopPointStr,16)
			print "Loop point found at", LoopPoint,"!"
			
			

	Square1NoteDuration=RowsPerPattern-Square1LastFrame
	Square1Pattern[n].append(Square1NoteDuration-1)
	
	Square2NoteDuration=RowsPerPattern-Square2LastFrame
	Square2Pattern[n].append(Square2NoteDuration-1)
	
	TriangleNoteDuration=RowsPerPattern-TriangleLastFrame
	TrianglePattern[n].append(TriangleNoteDuration-1)
	
	NoiseNoteDuration=RowsPerPattern-NoiseLastFrame
	NoisePattern[n].append(NoiseNoteDuration-1)

	Square1LastFrame=0
	Square2LastFrame=0
	TriangleLastFrame=0
	NoiseLastFrame=0
	Square1EndedOnD00=0
	Square2EndedOnD00=0
	TriangleEndedOnD00=0
	NoiseEndedOnD00=0
	
	
#############################################	
######## Build out note data for VIC ########
#############################################
print ""
print "Recostructing sequential note data for the VIC-20"

program_data_out=[] #array to store all the note and duration data
address_header_out=[] #array to store the address start locations for each of the voices
bytestr="		byte "	
TotalLength=0


s3Orders=[]
s2Orders=[]
s1Orders=[]
n4Orders=[]

s3usedpatterns=[]
s3addrhighlist=[]
s3addrlowlist=[]
S3usedaddresseshigh=[]
S3usedaddresseslow=[]

program_data_out.append("; S3 Note Data   ")


for n in range(TotalOrders):

	
	CurrentOrder=int(Square1Order[n], 16)
	
	CurrentPattern=Square1Pattern[CurrentOrder]
	
	CurrentPatternLen=len(CurrentPattern)
	
#	print "CurrentOrder is:",CurrentOrder
#	print "CurrentPattern is:",CurrentPattern
	
	
	if CurrentOrder in s3usedpatterns:
#		print "Current Order is",CurrentOrder," and it has already been compiled, adding its address to the address list"
		OrderIndex=s3usedpatterns.index(CurrentOrder)
		s3addrhighstr=S3usedaddresseshigh[OrderIndex]
		s3addrlowstr=S3usedaddresseslow[OrderIndex]
		s3addrhighlist.append(s3addrhighstr)
		s3addrlowlist.append(s3addrlowstr)
		
	
	
	
	if CurrentOrder not in s3usedpatterns:  #Check to see if the pattern has already been compiled
		
#		print "Current Order is:", CurrentOrder," and it has not yet been compiled.  Compiling..."
	
		s3addr=hex(DataStartAddrDec)
		s3addrhighlist.append("$"+s3addr[2:4])
		s3addrlowlist.append("$"+s3addr[4:6])
		buildstr="; S3 Pattern " + str(CurrentOrder)
		program_data_out.append(buildstr)
		
		
		for i in range(CurrentPatternLen/2):
			CurrentNoteEng=CurrentPattern[i*2]
			CurrentDuration=CurrentPattern[i*2+1]
			
			if ((CurrentNoteEng != mute_note) and (CurrentNoteEng != 108)):  #Normal note positions
				CurrentNotePos=ABCList.index(CurrentNoteEng)
				if ((CurrentNotePos + Square1NoteModifier)) >= max_note:
					print "Square 1 exceeded array.  Value=", ABCList.index(CurrentNoteEng),"Note was", CurrentNoteEng
					if IgnoreOverflowErrors==0:
						sys.exit()
					else:
						if CorrectOverflowErrors and ((CurrentNotePos + Square1NoteModifier-12)) < max_note:
							print "Adjusting",CurrentNoteEng,"down one octave"
							Square1NumCorrectedNotes=Square1NumCorrectedNotes+1
							buildstr=bytestr + str(CurrentNotePos+Square1NoteModifier-12) + "," + str(CurrentDuration) + "; S3 note and duration"
						else:
							print "Muting note"
							Square1NumOverNotes=Square1NumOverNotes+1
							buildstr=bytestr + str(mute_note) + "," + str(CurrentDuration) + "; S3 note and duration"
							Square1MutedNotes=1
					
				else:	
					buildstr=bytestr + str(CurrentNotePos+Square1NoteModifier) + "," + str(CurrentDuration) + "; S3 note and duration"
										
				
				if CurrentNotePos+Square1NoteModifier<0:
					print "Square1 offset is too much!  Array underflowed.  Value=", str(CurrentNotePos+Square1NoteModifier),"Note was", CurrentNoteEng
					
					if IgnoreUnderflowErrors==0:
						sys.exit()
					else:
						if CorrectUnderflowErrors and ((CurrentNotePos+Square1NoteModifier+12)>=0):
							print "Adjusting",CurrentNoteEng,"up one octave"
							Square1NumCorrectedNotes=Square1NumCorrectedNotes+1
							buildstr=bytestr + str(CurrentNotePos+Square1NoteModifier+12) + "," + str(CurrentDuration) + "; S3 note and duration"
						else:	
							print "Muting note"
							Square1NumUnderNotes=Square1NumUnderNotes+1
							buildstr=bytestr + str(mute_note) + "," + str(CurrentDuration) + "; S3 note and duration"
							Square1MutedNotes=1
						

				if CurrentNotePos>Square1Highest:
					Square1Highest=CurrentNotePos
				if CurrentNotePos<Square1Lowest:
					Square1Lowest=CurrentNotePos
					
			if CurrentNoteEng==mute_note:		#Stop Code
				buildstr=bytestr + str(mute_note) + "," + str(CurrentDuration) + "; S3 note and duration"
				
			if CurrentNoteEng==108:		#Transparent Note
				buildstr=bytestr + str(108) + "," + str(CurrentDuration) + "; S3 transparent note and duration"
				
			DataStartAddrDec=DataStartAddrDec+2
			program_data_out.append(buildstr)
		
		s3usedpatterns.append(CurrentOrder)
		S3usedaddresseshigh.append("$"+s3addr[2:4])
		S3usedaddresseslow.append("$"+s3addr[4:6])
		
		
		buildstr=bytestr + str(109) + "; S3 End Pattern Code"
		program_data_out.append(buildstr)
		DataStartAddrDec=DataStartAddrDec+1
		
		
		
	s3Orders.append(CurrentOrder)
	
s3addrhighlist.append(80) # append exit code, so the player knows when to stop playing
		
S2usedpatterns=[]
S2addrhighlist=[]
S2addrlowlist=[]
S2usedaddresseshigh=[]
S2usedaddresseslow=[]
program_data_out.append("; S2 Note Data   ")	
	
for n in range(TotalOrders):

	CurrentOrder=int(Square2Order[n], 16)
	CurrentPattern=Square2Pattern[CurrentOrder]
	CurrentPatternLen=len(CurrentPattern)
	
	
	if CurrentOrder in S2usedpatterns:
		OrderIndex=S2usedpatterns.index(CurrentOrder)
		S2addrhighstr=S2usedaddresseshigh[OrderIndex]
		S2addrlowstr=S2usedaddresseslow[OrderIndex]
		S2addrhighlist.append(S2addrhighstr)
		S2addrlowlist.append(S2addrlowstr)
		
	
	
	
	if CurrentOrder not in S2usedpatterns:  #Check to see if the pattern has already been compiled
		
	
		S2addr=hex(DataStartAddrDec)
		S2addrhighlist.append("$"+S2addr[2:4])
		S2addrlowlist.append("$"+S2addr[4:6])
		buildstr="; S2 Pattern " + str(CurrentOrder)
		program_data_out.append(buildstr)
		
		
		
		for i in range(CurrentPatternLen/2):
			CurrentNoteEng=CurrentPattern[i*2]
			CurrentDuration=CurrentPattern[i*2+1]
			
			if ((CurrentNoteEng != mute_note) and (CurrentNoteEng != 108)):  #Normal note positions
				CurrentNotePos=ABCList.index(CurrentNoteEng)
				if ((CurrentNotePos + Square2NoteModifier)) >= max_note:
					print "Square 2 exceeded array.  Value=", ABCList.index(CurrentNoteEng),"Note was", CurrentNoteEng
					if IgnoreOverflowErrors==0:
						sys.exit()
					else:
						if CorrectOverflowErrors and ((CurrentNotePos + Square2NoteModifier-12)) < max_note:
							print "Adjusting",CurrentNoteEng,"down one octave"
							Square2NumCorrectedNotes=Square2NumCorrectedNotes+1
							buildstr=bytestr + str(CurrentNotePos+Square2NoteModifier-12) + "," + str(CurrentDuration) + "; S2 note and duration"
						else:
							print "Muting note"
							Square2NumOverNotes=Square2NumOverNotes+1
							buildstr=bytestr + str(mute_note) + "," + str(CurrentDuration) + "; S2 note and duration"
							Square2MutedNotes=1
				
				else:
					buildstr=bytestr + str(CurrentNotePos+Square2NoteModifier) + "," + str(CurrentDuration) + "; S2 stop note and duration"						
				
				if CurrentNotePos+Square2NoteModifier<0:
					print "Square2 offset is too much!  Array underflowed.  Value=", str(CurrentNotePos+Square2NoteModifier),"Note was", CurrentNoteEng
					
					if IgnoreUnderflowErrors==0:
						sys.exit()
					else:
						if CorrectUnderflowErrors and ((CurrentNotePos+Square2NoteModifier+12)>=0):
							print "Adjusting",CurrentNoteEng,"up one octave"
							Square2NumCorrectedNotes=Square2NumCorrectedNotes+1
							buildstr=bytestr + str(CurrentNotePos+Square2NoteModifier+12) + "," + str(CurrentDuration) + "; S2 note and duration"
						else:	
							print "Muting note"
							Square2NumUnderNotes=Square2NumUnderNotes+1
							buildstr=bytestr + str(mute_note) + "," + str(CurrentDuration) + "; S2 note and duration"
							Square2MutedNotes=1
					
					
				if CurrentNotePos>Square2Highest:
					Square2Highest=CurrentNotePos
				if CurrentNotePos<Square2Lowest:
					Square2Lowest=CurrentNotePos
					
			if CurrentNoteEng==mute_note:		#Stop Code
				buildstr=bytestr + str(mute_note) + "," + str(CurrentDuration) + "; S2 stop note and duration"
				
			if CurrentNoteEng==108:		#Transparent Note
				buildstr=bytestr + str(108) + "," + str(CurrentDuration) + "; S2 transparent note and duration"
				
			DataStartAddrDec=DataStartAddrDec+2
			program_data_out.append(buildstr)
		
		S2usedpatterns.append(CurrentOrder)
		S2usedaddresseshigh.append("$"+S2addr[2:4])
		S2usedaddresseslow.append("$"+S2addr[4:6])
		
		
		buildstr=bytestr + str(109) + "; S2 End Pattern Code"
		program_data_out.append(buildstr)
		DataStartAddrDec=DataStartAddrDec+1
		
	s2Orders.append(CurrentOrder)

		
S1usedpatterns=[]
S1addrhighlist=[]
S1addrlowlist=[]
S1usedaddresseshigh=[]
S1usedaddresseslow=[]
program_data_out.append("; S1 Note Data   ")	
	
for n in range(TotalOrders):

	CurrentOrder=int(TriangleOrder[n], 16)
	CurrentPattern=TrianglePattern[CurrentOrder]
	CurrentPatternLen=len(CurrentPattern)
	
	
	if CurrentOrder in S1usedpatterns:
		OrderIndex=S1usedpatterns.index(CurrentOrder)
		S1addrhighstr=S1usedaddresseshigh[OrderIndex]
		S1addrlowstr=S1usedaddresseslow[OrderIndex]
		S1addrhighlist.append(S1addrhighstr)
		S1addrlowlist.append(S1addrlowstr)
	
	
	
	if CurrentOrder not in S1usedpatterns:  #Check to see if the pattern has already been compiled
		
		#print "Current Order is:", CurrentOrder," and it has not yet been compiled.  Compiling..."
	
		S1addr=hex(DataStartAddrDec)
		S1addrhighlist.append("$"+S1addr[2:4])
		S1addrlowlist.append("$"+S1addr[4:6])
		buildstr="; S1 Pattern " + str(CurrentOrder) + " " + S1addr
		program_data_out.append(buildstr)
		
		
		for i in range(CurrentPatternLen/2):
			CurrentNoteEng=CurrentPattern[i*2]
			CurrentDuration=CurrentPattern[i*2+1]
			
			if ((CurrentNoteEng != mute_note) and (CurrentNoteEng != 108)):  #Normal note positions
				if ((CurrentNotePos + Square2NoteModifier)) >= max_note:
					print "Triangle Note exceeded array.  Value=", ABCList.index(CurrentNoteEng),"Note was", CurrentNoteEng
					if IgnoreOverflowErrors==0:
						sys.exit()
					else:
						if CorrectOverflowErrors and ((CurrentNotePos + TriangleNoteModifier-12)) < max_note:
							print "Adjusting",CurrentNoteEng,"down one octave"
							TriangleNumCorrectedNotes=TriangleNumCorrectedNotes+1
							buildstr=bytestr + str(CurrentNotePos+TriangleNoteModifier-12) + "," + str(CurrentDuration) + "; S1 note and duration"
						else:
							print "Muting note"
							TriangleNumOverNotes=TriangleNumOverNotes+1
							buildstr=bytestr + str(mute_note) + "," + str(CurrentDuration) + "; S1 note and duration"
							TriangleMutedNotes=1
				
				else:
					CurrentNotePos=ABCList.index(CurrentNoteEng)
					buildstr=bytestr + str(CurrentNotePos+TriangleNoteModifier) + "," + str(CurrentDuration) + "; S1 note and duration"					
				
				if CurrentNotePos+TriangleNoteModifier<0:
					print "Triangle offset is too much!  Array underflowed.  Value=", str(CurrentNotePos+TriangleNoteModifier),"Note was", CurrentNoteEng
					
					if IgnoreUnderflowErrors==0:
						sys.exit()
					else:
						if CorrectUnderflowErrors and ((CurrentNotePos+TriangleNoteModifier+12)>=0):
							print "Adjusting",CurrentNoteEng,"up one octave"
							TriangleNumCorrectedNotes=TriangleNumCorrectedNotes+1
							buildstr=bytestr + str(CurrentNotePos+TriangleNoteModifier+12) + "," + str(CurrentDuration) + "; S1 note and duration"
						else:	
							print "Muting note"
							TriangleNumUnderNotes=TriangleNumUnderNotes+1
							buildstr=bytestr + str(mute_note) + "," + str(CurrentDuration) + "; S1 note and duration"
							TriangleMutedNotes=1
					
				if CurrentNotePos>TriangleHighest:
					TriangleHighest=CurrentNotePos
				if CurrentNotePos<TriangleLowest:
					TriangleLowest=CurrentNotePos
					
			if CurrentNoteEng==mute_note:		#Stop Code
				buildstr=bytestr + str(mute_note) + "," + str(CurrentDuration) + "; S1 stop note and duration"
				
			if CurrentNoteEng==108:		#Transparent note
				buildstr=bytestr + str(108) + "," + str(CurrentDuration) + "; S1 transparent note and duration"
				
			DataStartAddrDec=DataStartAddrDec+2
			program_data_out.append(buildstr)
		
		S1usedpatterns.append(CurrentOrder)
		S1usedaddresseshigh.append("$"+S1addr[2:4])
		S1usedaddresseslow.append("$"+S1addr[4:6])
		
		
		
	s1Orders.append(CurrentOrder)
		
N4usedpatterns=[]
N4addrhighlist=[]
N4addrlowlist=[]
N4usedaddresseshigh=[]
N4usedaddresseslow=[]

program_data_out.append("; N4 Note Data   ")	
	
for n in range(TotalOrders):

	CurrentOrder=int(NoiseOrder[n], 16)
	CurrentPattern=NoisePattern[CurrentOrder]
	CurrentPatternLen=len(CurrentPattern)
	#print "Current Pattern (",CurrentOrder,")is:", CurrentPattern
	
	
	if CurrentOrder in N4usedpatterns:
		#print "Current Order is",CurrentOrder," and it has already been compiled, adding its address to the address list"
		OrderIndex=N4usedpatterns.index(CurrentOrder)
		N4addrhighstr=N4usedaddresseshigh[OrderIndex]
		N4addrlowstr=N4usedaddresseslow[OrderIndex]
		N4addrhighlist.append(N4addrhighstr)
		N4addrlowlist.append(N4addrlowstr)
		
		#print "Adding addresses $",N4addrhighstr,",",N4addrlowstr
	
	
	if CurrentOrder not in N4usedpatterns:  #Check to see if the pattern has already been compiled
		
		#print "Current Order is:", CurrentOrder," and it has not yet been compiled.  Compiling..."
		
		N4addr=hex(DataStartAddrDec)
		N4addrhighlist.append("$"+N4addr[2:4])
		N4addrlowlist.append("$"+N4addr[4:6])
		buildstr="; N4 Pattern " + str(CurrentOrder)
		program_data_out.append(buildstr)
#		print "Current Order:",CurrentOrder,"Current Note:",CurrentNoteEng
		
		for i in range(CurrentPatternLen/2):
			CurrentNoteEng=CurrentPattern[i*2]
			CurrentDuration=CurrentPattern[i*2+1]
			
			if ((CurrentNoteEng != mute_note)):  #Normal note positions
				CurrentNotePos=PercList.index(CurrentNoteEng)
				Tone=CurrentNotePos*8+128
				if Tone>=256:
					Tone=255
				buildstr=bytestr + str(Tone) + "," + str(CurrentDuration) + "; N4 low and duration"
				program_data_out.append(buildstr)
				
			if CurrentNoteEng==mute_note:		#Stop Code
				Tone=0	
				buildstr=bytestr + str(Tone) + "," + str(CurrentDuration) + "; N4 low and duration"
				program_data_out.append(buildstr)
					
			DataStartAddrDec=DataStartAddrDec+2
		
		N4usedpatterns.append(CurrentOrder)
		
		
		

		n4Orders.append(CurrentOrder)
		N4usedaddresseshigh.append("$"+N4addr[2:4])
		N4usedaddresseslow.append("$"+N4addr[4:6])


address_header_out.append("SwapS2S3        byte " + str(SwapS2S3))

if LoopPoint==0: #Starting point of 255 starts the song back at 0 in the VICplayer
	LoopPoint=256
	

address_header_out.append("LoopPoint        byte " + str(LoopPoint-1))

s3addrhighliststr=str(s3addrhighlist)
s3addrhighliststr=s3addrhighliststr.replace("[","")
s3addrhighliststr=s3addrhighliststr.replace("]","")
s3addrhighliststr=s3addrhighliststr.replace("'","")
s3addrhighliststr="S3addrhighlist	" + bytestr + s3addrhighliststr
s3addrlowliststr=str(s3addrlowlist)
s3addrlowliststr=s3addrlowliststr.replace("[","")
s3addrlowliststr=s3addrlowliststr.replace("]","")
s3addrlowliststr=s3addrlowliststr.replace("'","")
s3addrlowliststr="S3addrlowlist	" + bytestr + s3addrlowliststr
S2addrhighliststr=str(S2addrhighlist)
S2addrhighliststr=S2addrhighliststr.replace("[","")
S2addrhighliststr=S2addrhighliststr.replace("]","")
S2addrhighliststr=S2addrhighliststr.replace("'","")
S2addrhighliststr="S2addrhighlist	" + bytestr + S2addrhighliststr
S2addrlowliststr=str(S2addrlowlist)
S2addrlowliststr=S2addrlowliststr.replace("[","")
S2addrlowliststr=S2addrlowliststr.replace("]","")
S2addrlowliststr=S2addrlowliststr.replace("'","")
S2addrlowliststr="S2addrlowlist	" + bytestr + S2addrlowliststr



S1addrhighliststr=str(S1addrhighlist)
S1addrhighliststr=S1addrhighliststr.replace("[","")
S1addrhighliststr=S1addrhighliststr.replace("]","")
S1addrhighliststr=S1addrhighliststr.replace("'","")
S1addrhighliststr="S1addrhighlist	" + bytestr + S1addrhighliststr
S1addrlowliststr=str(S1addrlowlist)
S1addrlowliststr=S1addrlowliststr.replace("[","")
S1addrlowliststr=S1addrlowliststr.replace("]","")
S1addrlowliststr=S1addrlowliststr.replace("'","")
S1addrlowliststr="S1addrlowlist	" + bytestr + S1addrlowliststr
N4addrhighliststr=str(N4addrhighlist)
N4addrhighliststr=N4addrhighliststr.replace("[","")
N4addrhighliststr=N4addrhighliststr.replace("]","")
N4addrhighliststr=N4addrhighliststr.replace("'","")
N4addrhighliststr="N4addrhighlist	" + bytestr + N4addrhighliststr
N4addrlowliststr=str(N4addrlowlist)
N4addrlowliststr=N4addrlowliststr.replace("[","")
N4addrlowliststr=N4addrlowliststr.replace("]","")
N4addrlowliststr=N4addrlowliststr.replace("'","")
N4addrlowliststr="N4addrlowlist	" + bytestr + N4addrlowliststr


address_header_out.append(s3addrhighliststr)
address_header_out.append(s3addrlowliststr)
address_header_out.append(S2addrhighliststr)
address_header_out.append(S2addrlowliststr)
address_header_out.append(S1addrhighliststr)
address_header_out.append(S1addrlowliststr)
address_header_out.append(N4addrhighliststr)
address_header_out.append(N4addrlowliststr)

address_header_out.append("*=$"+DataStartAddress)
address_header_out.append("")
address_header_out.append("sounddata")

program_out=[]
if args.full:
	with open("asmPlayer_template.txt", 'r') as f:
		program_out = f.read().splitlines()
	
program_out=program_out + address_header_out
program_out=program_out+program_data_out

print "S3 Order List:",s3Orders
print "S2 Order List:",s2Orders
print "S1 Order List:",s1Orders
print "N4 Order List:",n4Orders

print "Square1 Range:", Square1Lowest, ":", Square1Highest
print "Square2 Range:", Square2Lowest, ":", Square2Highest
print "Triangle Range:", TriangleLowest, ":", TriangleHighest

if Square1MutedNotes:
	print "Offset on Square1 caused some notes to be muted (",Square1NumUnderNotes,"due to underflow and",Square1NumOverNotes,"due to overflow)"
if Square1NumCorrectedNotes>0:
	print Square1NumCorrectedNotes,"notes in Square1 were adjusted"
if Square2MutedNotes:
	print "Offset on Square2 caused some notes to be muted (",Square2NumUnderNotes,"due to underflow and",Square2NumOverNotes,"due to overflow)"
if Square2NumCorrectedNotes>0:
	print Square2NumCorrectedNotes,"notes in Square2 were adjusted"
if TriangleMutedNotes:
	print "Offset on Triangle caused some notes to be muted (",TriangleNumUnderNotes,"due to underflow and",TriangleNumOverNotes,"due to overflow)"
if TriangleNumCorrectedNotes>0:
	print TriangleNumCorrectedNotes,"notes in Triangle were adjusted"

			
with open(output_file, 'w') as f:
			for item in program_out:
				print >> f, item
	


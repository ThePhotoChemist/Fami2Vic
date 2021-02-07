# Fami2Vic
Software to convert FamiTracker .txt exports to a playable PRG on a VIC-20

I just slapped this thing together not too long ago, so the python script will probably fail on most other txt exports from FamiTracker.  I will continue working with other files to identify problems along the way.  Mind the dust!

To use:

$python fami2vic.py "/path/to/text/file.txt"

The script will spit out ASM source that can be compiled in CBM Studio.  

The compiled PRG file of "Wily's Castle 2" is included in the repo, and can be loaded on to a VIC-20 with an sd2iec, etc.  It requires an 8k RAM expansion to function properly.  

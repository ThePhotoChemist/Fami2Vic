# Fami2Vic
Software to convert FamiTracker .txt exports to a playable PRG on a VIC-20

This is a work in progress, but nearly complete!  Mind the dust!

To use:

$python fami2vic.py -i /path/to/text/file.txt

The script will spit out ASM source that can be compiled in CBM Studio.  It will also print out diagnostic information regarding note mapping.  Due to the VIC's 3 square wave voices (S1, S2 and S3 from lowest to highest) each being offset one octave from each other, Square1, Square2 and Triangle from the NES side each require their own pitch offsets to stay at the right pitch.  

If you're compiling for a Commodore 64, use -C64.  Otherwise, it will default to VIC-20 mode.  Most of the following arguments are VIC-20 specific.  

Default configuration maps Square1 to S3, Square2 to S2 and Triangle to S1.  The offsets are -24, -12 and -12.  

Try --swap to change the mapping to Square2 to S3, Square1 to S2, and Triangle to S1.  Default offsets are -12, -24 and -12.

Individual channel offsets can be modified with -S1, -S2 or -T.  Typically, this is only needed when melodies from non-triangle channels are copy/pasted into the triangle channel in Famitracker/Famistudio.  If that's the case, try -T 0

If Famitracker notes aren't able to be assigned to a channel due to being too high or too low for the VIC voice, they are muted by default.  Running the script with and without the --swap option will report how many notes don't make it.  Usually the option where the least amount of notes are muted is the best. 

--CU and --CO will attempt to correct notes that were too low (underflow) and too high (overflow) by adjusting them an octave in the right direction.  If they still aren't able to be assigned a VIC note value, they stay muted.  

-V and -NC specify volume cutoff threshholds for the 3 square voices and noise voice, respectively.  Sometimes multiple notes are played repeatedly in one Famitracker note with no "stop note" in between, using volume decay instead to differentiate notes.  When the script detects the volume has passed below the cutoff threshhold, it will mute the channel, only unmuting when the volume has returned back to the threshhold.

-o specifies output file.  If not specified, the script defaults output to a file called "program_out.txt"

-F outputs a full ASM program using the asmPlayerTemplate.txt file to the specified output location.  If not specified, the script only outputs the VIC sound data.

-D specifies the sound data start address.  If not specified, it defaults to hex 2110.  This is useful if you're trying to move the sound data around to try and make a more compact PRG.  

The compiled PRG file of "Wily's Castle 2" is included in the repo, and can be loaded on to a VIC-20 with an sd2iec, etc.  It requires an 8k RAM expansion to function properly.  

Many thanks goes to Aleksi Eeben, for publishing his code for 10-bit oscillator resolution.  Without his work, the music from this script would sound about 500 times worse.  https://aleksieeben.wordpress.com/portfolio/tools-hacks/

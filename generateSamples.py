import numpy as np
import os
import sys, getopt
import wave
from pydub import AudioSegment

def detect_silence(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms
    
def split_stereo_file_into_left_right(fn, wav, channel):
    '''
    Take Wave_read object as an input and save one of its
    channels into a separate .wav file.
    '''
    
    # Read data
    nch   = wav.getnchannels()
    depth = wav.getsampwidth()
    wav.setpos(0)
    sdata = wav.readframes(wav.getnframes())

    # Extract channel data (24-bit data not supported)
    typ = { 1: np.uint8, 2: np.uint16, 4: np.uint32 }.get(depth)
    if not typ:
        raise ValueError("sample width {} not supported".format(depth))
    if channel >= nch:
        raise ValueError("cannot extract channel {} out of {}".format(channel+1, nch))
    print ("Extracting channel {} out of {} channels, {}-bit depth".format(channel+1, nch, depth*8))
    data = np.fromstring(sdata, dtype=typ)
    ch_data = data[channel::nch]
    outwav = wave.open(fn, 'w')
    outwav.setparams(wav.getparams())
    outwav.setnchannels(1)
    outwav.writeframes(ch_data.tostring())
    outwav.close()
    
def processAndExportWav(directory, filename, wav, channel):
    '''
    Main processing flow
    '''
    split_stereo_file_into_left_right(filename + '.wav', wav, channel)
    sound = AudioSegment.from_file('.\\' + filename + '.wav', format="wav")
    start_trim = 0
    end_trim = detect_silence(sound.reverse())
    duration = len(sound)    
    trimmed_sound = sound[start_trim:duration-end_trim]
    trimmed_sound.export(outputDir + "\\" + filename + '.wav', format="wav")

if len(sys.argv) != 3:
    print('Invalid arg length. Usage: generateSamples.py [inputDir] [outputDir]')
    sys.exit(2)

inputDir = sys.argv[1]
outputDir = sys.argv[2]

if not os.path.isdir(inputDir):
    print('Input path is not a valid directory')
    sys.exit(2)
if not os.path.isdir(outputDir):
    print('Output path is not a valid directory')
    sys.exit(2)

index = 1
for filename in os.listdir(inputDir):
    if filename.endswith(".wav"):
        wavfile = wave.open(os.path.join(sys.argv[1], filename))
        processAndExportWav(inputDir, 'LEFT_' + str(index), wavfile, 0)
        processAndExportWav(inputDir, 'RIGHT_' + str(index), wavfile, 1)
        index += 1
        continue
    else:
        continue

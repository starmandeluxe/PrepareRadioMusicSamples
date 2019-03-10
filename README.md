# PrepareRadioMusicSamples
Provides a script that will split stereo .wav files into separate mono left and right .wav files as well as trims the trailing silence in the audio

To use it, run `python generateSamples.py [inputDirectory] [outputDirectory]` where `inputDirectory` is a path storing one or more stereo .wav files. The output will be files in numbered order of the format LEFT_<index>.wav and RIGHT_<index>.wav. The index corresponds to the original source .wav file, split into LEFT and RIGHT channels.

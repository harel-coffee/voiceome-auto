
## Getting started
To clean an entire folder of .WAV files, you can run:

```
cd ~ 
cd allie/cleaning/audio_cleaning
python3 cleaning.py /Users/jimschwoebel/allie/load_dir
```

### [Audio](https://github.com/jim-schwoebel/allie/tree/master/cleaning/audio_cleaning)
* [clean_getfirst3secs](https://github.com/jim-schwoebel/allie/blob/master/cleaning/audio_cleaning/clean_getfirst3secs.py) - gets the first 3 seconds of the audio file
* [clean_keyword](https://github.com/jim-schwoebel/allie/blob/master/cleaning/audio_cleaning/clean_keyword.py) - keeps only keywords that are spoken based on a transcript (from the default_audio_transcriber)
* [clean_mono16hz](https://github.com/jim-schwoebel/allie/blob/master/cleaning/audio_cleaning/clean_mono16hz.py) - converts all audio to mono 16000 Hz for analysis (helps prepare for many preprocessing techniques)
* [clean_towav](https://github.com/jim-schwoebel/allie/blob/master/cleaning/audio_cleaning/clean_towav.py) - converts all audio files to wav files
* [clean_multispeaker](https://github.com/jim-schwoebel/allie/blob/master/cleaning/audio_cleaning/clean_multispeaker.py) - deletes audio files from a dataset that have been identified as having multiple speakers from a deep learning model
* [clean_normalizevolume](https://github.com/jim-schwoebel/allie/blob/master/cleaning/audio_cleaning/clean_normalizevolume.py) - normalizes the volume of all audio files using peak normalization methods from ffmpeg-normalize
* [clean_opus](https://github.com/jim-schwoebel/allie/blob/master/cleaning/audio_cleaning/clean_opus.py) - converts an audio file to .OPUS audio file format then back to wav (a lossy conversion) - narrowing in more on voice signals over noise signals.
* [clean_randomsplice](https://github.com/jim-schwoebel/allie/blob/master/cleaning/audio_cleaning/clean_randomsplice.py) - take a random splice (time specified in the script) from the audio file.
* [clean_removenoise](https://github.com/jim-schwoebel/allie/blob/master/cleaning/audio_cleaning/clean_removenoise.py) - removes noise from the audio file using SoX program and noise floors.
* [clean_removesilence](https://github.com/jim-schwoebel/allie/blob/master/cleaning/audio_cleaning/clean_removesilence.py) - removes silence from an audio file using voice activity detectors.
* [clean_rename](https://github.com/jim-schwoebel/allie/blob/master/cleaning/audio_cleaning/clean_rename.py) - renames all the audio files in the current directory with a new UUID
* [clean_utterances](https://github.com/jim-schwoebel/allie/blob/master/cleaning/audio_cleaning/clean_utterances.py) - converts all audio files into unique utterances (1 .WAV file --> many .WAV file utterances) for futher analysis.

### Settings

Here are some default settings relevant to this section of Allie's API:

| setting | description | default setting | all options | 
|------|------|------|------| 
| clean_data | whether or not to clean datasets during the model training process via default cleaning scripts. | False | True, False | 
| [default_audio_cleaners](https://github.com/jim-schwoebel/allie/tree/master/cleaning/audio_cleaning) | the default cleaning strategies used during audio modeling if clean_data == True | ["clean_mono16hz"] | ["clean_getfirst3secs", "clean_keyword", "clean_mono16hz", "clean_towav", "clean_multispeaker", "clean_normalizevolume", "clean_opus", "clean_randomsplice", "clean_removenoise", "clean_removesilence", "clean_rename", "clean_utterances"] |

'''
               AAA               lllllll lllllll   iiii                      
              A:::A              l:::::l l:::::l  i::::i                     
             A:::::A             l:::::l l:::::l   iiii                      
            A:::::::A            l:::::l l:::::l                             
           A:::::::::A            l::::l  l::::l iiiiiii     eeeeeeeeeeee    
          A:::::A:::::A           l::::l  l::::l i:::::i   ee::::::::::::ee  
         A:::::A A:::::A          l::::l  l::::l  i::::i  e::::::eeeee:::::ee
        A:::::A   A:::::A         l::::l  l::::l  i::::i e::::::e     e:::::e
       A:::::A     A:::::A        l::::l  l::::l  i::::i e:::::::eeeee::::::e
      A:::::AAAAAAAAA:::::A       l::::l  l::::l  i::::i e:::::::::::::::::e 
     A:::::::::::::::::::::A      l::::l  l::::l  i::::i e::::::eeeeeeeeeee  
    A:::::AAAAAAAAAAAAA:::::A     l::::l  l::::l  i::::i e:::::::e           
   A:::::A             A:::::A   l::::::ll::::::li::::::ie::::::::e          
  A:::::A               A:::::A  l::::::ll::::::li::::::i e::::::::eeeeeeee  
 A:::::A                 A:::::A l::::::ll::::::li::::::i  ee:::::::::::::e  
AAAAAAA                   AAAAAAAlllllllllllllllliiiiiiii    eeeeeeeeeeeeee  


/  __ \ |                (_)              / _ \ | ___ \_   _|  _ 
| /  \/ | ___  __ _ _ __  _ _ __   __ _  / /_\ \| |_/ / | |   (_)
| |   | |/ _ \/ _` | '_ \| | '_ \ / _` | |  _  ||  __/  | |      
| \__/\ |  __/ (_| | | | | | | | | (_| | | | | || |    _| |_   _ 
 \____/_|\___|\__,_|_| |_|_|_| |_|\__, | \_| |_/\_|    \___/  (_)
                                   __/ |                         
                                  |___/                          
  ___            _ _       
 / _ \          | (_)      
/ /_\ \_   _  __| |_  ___  
|  _  | | | |/ _` | |/ _ \ 
| | | | |_| | (_| | | (_) |
\_| |_/\__,_|\__,_|_|\___/ 
                           

This section of Allie's API cleans folders of audio files
using the default_audio_cleaners.

Usage: python3 clean.py [folder] [cleantype]

All cleantype options include:
["clean_getfirst3secs", "clean_keyword", "clean_mono16hz", "clean_towav", 
"clean_multispeaker", "clean_normalizevolume", "clean_opus", "clean_randomsplice",
"clean_removenoise", "clean_removesilence", "clean_rename", "clean_utterances"]

Read more @ https://github.com/jim-schwoebel/allie/tree/master/cleaning/audio_cleaning
'''

################################################
##              IMPORT STATEMENTS             ##
################################################
import json, os, sys, time, random, uuid
import numpy as np 
# import helpers.transcribe as ts
# import speech_recognition as sr
from tqdm import tqdm

def prev_dir(directory):
    g=directory.split('/')
    dir_=''
    for i in range(len(g)):
        if i != len(g)-1:
            if i==0:
                dir_=dir_+g[i]
            else:
                dir_=dir_+'/'+g[i]
    # print(dir_)
    return dir_

################################################
##              Helper functions              ##
################################################

def transcribe(file, default_audio_transcriber, settingsdir):
    # create all transcription methods here
    print('%s transcribing: %s'%(default_audio_transcriber, file))

    # use the audio file as the audio source
    r = sr.Recognizer()
    transcript_engine = default_audio_transcriber

    with sr.AudioFile(file) as source:
        audio = r.record(source)  # read the entire audio file

    if transcript_engine == 'pocketsphinx':

        # recognize speech using Sphinx
        try:
            transcript= r.recognize_sphinx(audio)
        except sr.UnknownValueError:
            transcript=''
        except sr.RequestError as e:
            transcript=''

    elif transcript_engine == 'deepspeech_nodict':

        curdir=os.getcwd()
        os.chdir(settingsdir+'/features/audio_features/helpers')
        listdir=os.listdir()
        deepspeech_dir=os.getcwd()

        # download models if not in helper directory
        if 'deepspeech-0.7.0-models.pbmm' not in listdir:
            os.system('wget https://github.com/mozilla/DeepSpeech/releases/download/v0.7.0/deepspeech-0.7.0-models.pbmm')

        # initialize filenames
        textfile=file[0:-4]+'.txt'
        newaudio=file[0:-4]+'_newaudio.wav'
        
        if deepspeech_dir.endswith('/'):
            deepspeech_dir=deepspeech_dir[0:-1]

        # go back to main directory
        os.chdir(curdir)

        # convert audio file to 16000 Hz mono audio 
        os.system('ffmpeg -i "%s" -acodec pcm_s16le -ac 1 -ar 16000 "%s" -y'%(file, newaudio))
        command='deepspeech --model %s/deepspeech-0.7.0-models.pbmm --audio "%s" >> "%s"'%(deepspeech_dir, newaudio, textfile)
        print(command)
        os.system(command)

        # get transcript
        transcript=open(textfile).read().replace('\n','')

        # remove temporary files
        os.remove(textfile)
        os.remove(newaudio)

    elif transcript_engine == 'deepspeech_dict':

        curdir=os.getcwd()
        os.chdir(settingsdir+'/features/audio_features/helpers')
        listdir=os.listdir()
        deepspeech_dir=os.getcwd()

        # download models if not in helper directory
        if 'deepspeech-0.7.0-models.pbmm' not in listdir:
            os.system('wget https://github.com/mozilla/DeepSpeech/releases/download/v0.7.0/deepspeech-0.7.0-models.pbmm')
        if 'deepspeech-0.7.0-models.scorer' not in listdir:
            os.system('wget https://github.com/mozilla/DeepSpeech/releases/download/v0.7.0/deepspeech-0.7.0-models.scorer')

        # initialize filenames
        textfile=file[0:-4]+'.txt'
        newaudio=file[0:-4]+'_newaudio.wav'
        
        if deepspeech_dir.endswith('/'):
            deepspeech_dir=deepspeech_dir[0:-1]

        # go back to main directory
        os.chdir(curdir)

        # convert audio file to 16000 Hz mono audio 
        os.system('ffmpeg -i "%s" -acodec pcm_s16le -ac 1 -ar 16000 "%s" -y'%(file, newaudio))
        command='deepspeech --model %s/deepspeech-0.7.0-models.pbmm --scorer %s/deepspeech-0.7.0-models.scorer --audio "%s" >> "%s"'%(deepspeech_dir, deepspeech_dir, newaudio, textfile)
        print(command)
        os.system(command)

        # get transcript
        transcript=open(textfile).read().replace('\n','')

        # remove temporary files
        os.remove(textfile)
        os.remove(newaudio)

    elif transcript_engine == 'google':

        # recognize speech using Google Speech Recognition
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`

        # recognize speech using Google Cloud Speech
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        print(GOOGLE_CLOUD_SPEECH_CREDENTIALS)

        try:
            transcript=r.recognize_google_cloud(audio, credentials_json=open(GOOGLE_CLOUD_SPEECH_CREDENTIALS).read())
        except sr.UnknownValueError:
            transcript=''
        except sr.RequestError as e:
            transcript=''

    elif transcript_engine == 'wit':

        # recognize speech using Wit.ai
        WIT_AI_KEY = os.environ['WIT_AI_KEY']

        try:
            transcript=r.recognize_wit(audio, key=WIT_AI_KEY)
        except sr.UnknownValueError:
            transcript=''
        except sr.RequestError as e:
            transcript=''

    elif transcript_engine == 'azure':

        # recognize speech using Microsoft Azure Speech
        AZURE_SPEECH_KEY = os.environ['AZURE_SPEECH_KEY']
        print(AZURE_SPEECH_KEY)
        try:
            transcript=r.recognize_azure(audio, key=AZURE_SPEECH_KEY)
        except sr.UnknownValueError:
            transcript=''
        except sr.RequestError as e:
            transcript=''

    elif transcript_engine == 'bing':
        # recognize speech using Microsoft Bing Voice Recognition
        BING_KEY = os.environ['BING_KEY']
        try:
            transcript=r.recognize_bing(audio, key=BING_KEY)
        except sr.UnknownValueError:
            transcript=''
        except sr.RequestError as e:
            transcript=''

    elif transcript_engine == 'houndify':
        # recognize speech using Houndify
        HOUNDIFY_CLIENT_ID = os.environ['HOUNDIFY_CLIENT_ID']  
        HOUNDIFY_CLIENT_KEY = os.environ['HOUNDIFY_CLIENT_KEY']  
        try:
            transcript=r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
        except sr.UnknownValueError:
            transcript=''
        except sr.RequestError as e:
            transcript=''

    elif transcript_engine == 'ibm':
        # recognize speech using IBM Speech to Text
        IBM_USERNAME = os.environ['IBM_USERNAME']
        IBM_PASSWORD = os.environ['IBM_PASSWORD']

        try:
            transcript=r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
        except sr.UnknownValueError:
            transcript=''
        except sr.RequestError as e:
            transcript=''

    else:
        print('no transcription engine specified')
        transcript=''

    # show transcript
    print(transcript_engine.upper())
    print('--> '+ transcript)

    return transcript 

def audio_clean(cleaning_set, audiofile, basedir):

    # long conditional on all the types of features that can happen and featurizes accordingly.
    if cleaning_set == 'clean_getfirst3secs':
        audiofile=clean_getfirst3secs.clean_getfirst3secs(audiofile)
    elif cleaning_set == 'clean_mono16hz':
        audiofile=clean_mono16hz.clean_mono16hz(audiofile)
    elif cleaning_set == 'clean_towav':
        audiofile=clean_towav.clean_towav(audiofile)
    elif cleaning_set == 'clean_keyword':
        audiofile=clean_keyword.clean_keyword(audiofile,'coconut')
    elif cleaning_set == 'clean_multispeaker':
        modeldir=basedir+'/helpers'
        audiofile=clean_multispeaker.clean_multispeaker(audiofile,modeldir)
    elif cleaning_set == 'clean_normalizevolume':
        audiofile=clean_normalizevolume.clean_normalizevolume(audiofile)
    elif cleaning_set == 'clean_opus':
        audiofile=clean_opus.clean_opus(audiofile,basedir+'/helpers/opustools/')
    elif cleaning_set == 'clean_randomsplice':
        audiofile=clean_randomsplice.clean_randomsplice(audiofile,20)
    elif cleaning_set == 'clean_removenoise':
        audiofile=clean_removenoise.clean_removenoise(audiofile)
    elif cleaning_set == 'clean_removesilence':
        audiofile=clean_removesilence.clean_removesilence(audiofile)
    elif cleaning_set == 'clean_rename':
        audiofile=clean_rename.clean_rename(audiofile)
    elif cleaning_set == 'clean_utterances':
        audiofile=clean_utterances.clean_utterances(audiofile)
    # transcripts = can look for hotwords and remove
    return audiofile

################################################
##              Load main settings            ##
################################################

# directory=sys.argv[1]
basedir=os.getcwd()
settingsdir=prev_dir(basedir)
settingsdir=prev_dir(settingsdir)
settings=json.load(open(settingsdir+'/settings.json'))
os.chdir(basedir)

audio_transcribe=settings['transcribe_audio']
default_audio_transcribers=settings['default_audio_transcriber']
try:
    # assume 1 type of feature_set 
    cleaning_sets=[sys.argv[2]]
except:
    # if none provided in command line, then load deafult features 
    cleaning_sets=settings['default_audio_cleaners']

################################################
##          Import According to settings      ##
################################################
# only load the relevant featuresets for featurization to save memory
if 'clean_getfirst3secs' in cleaning_sets:
    import clean_getfirst3secs
if 'clean_mono16hz' in cleaning_sets:
    import clean_mono16hz
if 'clean_towav' in cleaning_sets:
    import clean_towav
if 'clean_keyword' in cleaning_sets:
    import clean_keyword
if 'clean_multispeaker' in cleaning_sets:
    import clean_multispeaker
if 'clean_opus' in cleaning_sets:
    import clean_opus
if 'clean_normalizevolume' in cleaning_sets:
    import clean_normalizevolume
if 'clean_randomsplice' in cleaning_sets:
    import clean_randomsplice
if 'clean_rename' in cleaning_sets:
    import clean_rename
if 'clean_removenoise' in cleaning_sets:
    import clean_removenoise
if 'clean_removesilence' in cleaning_sets:
    import clean_removesilence
if 'clean_utterances' in cleaning_sets:
    import clean_utterances

################################################
##          Get featurization folder          ##
################################################

foldername=sys.argv[1]
os.chdir(foldername)
listdir=os.listdir() 
random.shuffle(listdir)
cur_dir=os.getcwd()
help_dir=basedir+'/helpers/'

# get class label from folder name 
labelname=foldername.split('/')
if labelname[-1]=='':
    labelname=labelname[-2]
else:
    labelname=labelname[-1]

################################################
##        REMOVE JSON AND DUPLICATES          ##
################################################

deleted_files=list()

# rename files appropriately
for i in range(len(listdir)):
    os.rename(listdir[i],listdir[i].replace(' ',''))

# remove duplicates / json files
for i in tqdm(range(len(listdir)), desc=labelname):
    file=listdir[i]
    listdir2=os.listdir()
    #now sub-loop through all files in directory and remove duplicates 
    for j in range(len(listdir2)):
        try:
            if listdir2[j]==file:
                pass
            elif listdir2[j]=='.DS_Store':
                pass 
            else:
                if filecmp.cmp(file, listdir2[j])==True:
                    print('removing duplicate: %s ____ %s'%(file,listdir2[j]))
                    deleted_files.append(listdir2[j])
                    os.remove(listdir2[j])
                else:
                    pass
        except:
            pass 
            
print('deleted the files below')
print(deleted_files)

listdir=os.listdir() 
for i in tqdm(range(len(listdir))):
    # remove .JSON files
    if listdir[i].endswith('.json'):
        os.remove(listdir[i])

# now rename files with UUIDs
listdir=os.listdir()
for i in range(len(listdir)):
    file=listdir[i]
    os.rename(file, str(uuid.uuid4())+file[-4:])
    
################################################
##                NOW CLEAN!!                 ##
################################################

listdir=os.listdir()
random.shuffle(listdir)

# featurize all files accoridng to librosa featurize
for i in tqdm(range(len(listdir)), desc=labelname):
    if listdir[i][-4:] in ['.wav', '.mp3', '.m4a']:
        filename=[listdir[i]]
        for j in range(len(cleaning_sets)):
            for k in range(len(filename)):
                cleaning_set=cleaning_sets[j]
                filename=audio_clean(cleaning_set, filename[k], basedir)

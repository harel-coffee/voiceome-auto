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

______         _                          ___  ______ _____     
|  ___|       | |                        / _ \ | ___ \_   _|  _ 
| |_ ___  __ _| |_ _   _ _ __ ___  ___  / /_\ \| |_/ / | |   (_)
|  _/ _ \/ _` | __| | | | '__/ _ \/ __| |  _  ||  __/  | |      
| ||  __/ (_| | |_| |_| | | |  __/\__ \ | | | || |    _| |_   _ 
\_| \___|\__,_|\__|\__,_|_|  \___||___/ \_| |_/\_|    \___/  (_)
                                                                
                                                                
 _____                           
|_   _|                          
  | | _ __ ___   __ _  __ _  ___ 
  | || '_ ` _ \ / _` |/ _` |/ _ \
 _| || | | | | | (_| | (_| |  __/
 \___/_| |_| |_|\__,_|\__, |\___|
                       __/ |     
                      |___/      

Featurize folders of images with the default_image_features.

Usage: python3 featurize.py [folder] [featuretype]

All featuretype options include:
["image_features", "inception_features", "resnet_features", "squeezenet_features", 
"tesseract_features", "vgg16_features", "vgg19_features", "xception_features"]

Read more @ https://github.com/jim-schwoebel/allie/tree/master/features/image_features
'''
import helpers.audio_plot as ap 
import numpy as np 
import os, json, sys
from tqdm import tqdm

##################################################
##				Helper functions.    			##
##################################################

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

def image_featurize(feature_set, imgfile, cur_dir, haar_dir):

	if feature_set == 'image_features':
		features, labels=imf.image_featurize(cur_dir, haar_dir, imgfile)
	elif feature_set == 'vgg16_features':
		features, labels=v16f.vgg16_featurize(imgfile)
	elif feature_set == 'inception_features':
		features, labels=incf.inception_featurize(imgfile)
	elif feature_set == 'xception_features':
		features, labels=xf.xception_featurize(imgfile)
	elif feature_set == 'resnet_features':
		features, labels=rf.resnet_featurize(imgfile)
	elif feature_set == 'vgg19_features':
		features, labels=v19f.vgg19_featurize(imgfile)
	elif feature_set == 'tesseract_features':
		transcript, features, labels = tf.tesseract_featurize(imgfile)
	elif feature_set == 'squeezenet_features':
		features, labels=sf.squeezenet_featurize(imgfile, cur_dir)
		
	# make sure all the features do not have any infinity or NaN
	features=np.nan_to_num(np.array(features))
	features=features.tolist()

	return features, labels 

##################################################
##				   Main script  		    	##
##################################################

# directory=sys.argv[1]
basedir=os.getcwd()
haar_dir=basedir+'/helpers/haarcascades'
foldername=sys.argv[1]
os.chdir(foldername)
cur_dir=os.getcwd()
listdir=os.listdir() 

# settings directory 
settingsdir=prev_dir(basedir)
sys.path.append(settingsdir)
from standard_array import make_features
settings=json.load(open(prev_dir(settingsdir)+'/settings.json'))
os.chdir(basedir)

image_transcribe=settings['transcribe_image']
default_image_transcriber=settings['default_image_transcriber']
try:
	feature_sets=[sys.argv[2]]
except:
	feature_sets=settings['default_image_features']

##################################################
##	         Only load relevant features     	##
##################################################

if 'vgg16_features' in feature_sets:
	import vgg16_features as v16f
if 'image_features' in feature_sets:
	import image_features as imf 
if 'inception_features' in feature_sets:
	import inception_features as incf 
if 'xception_features' in feature_sets:
	import xception_features as xf 
if 'resnet_features' in feature_sets:
	import resnet_features as rf 
if 'vgg19_features' in feature_sets:
	import vgg19_features as v19f
if 'squeezenet_features' in feature_sets:
	import squeezenet_features as sf
if image_transcribe == True or 'tesseract_features' in feature_sets:
	import tesseract_features as tf

# get class label from folder name 
labelname=foldername.split('/')
if labelname[-1]=='':
	labelname=labelname[-2]
else:
	labelname=labelname[-1]

##################################################
##	         		Main loop     				##
##################################################

# featurize all files accoridng to librosa featurize
for i in tqdm(range(len(listdir)), desc=labelname):
	os.chdir(cur_dir)
	if listdir[i][-4:] in ['.jpg', '.png']:
		try:
			imgfile=listdir[i]
			sampletype='image'

			# I think it's okay to assume audio less than a minute here...
			if listdir[i][0:-4]+'.json' not in listdir:

				# make new .JSON if it is not there with base array schema.
				basearray=make_features(sampletype)

				if image_transcribe==True:
					for j in range(len(default_image_transcriber)):
						transcript, features, labels = tf.tesseract_featurize(imgfile)
						transcript_list=basearray['transcripts']
						transcript_list['image'][default_image_transcriber[j]]=transcript 
						basearray['transcripts']=transcript_list
				
				# featurize the image file with specified featurizers 
				for j in range(len(feature_sets)):
					feature_set=feature_sets[j]
					features, labels = image_featurize(feature_set, imgfile, cur_dir, haar_dir)
					print(features)
					try:
						data={'features':features.tolist(),
							  'labels': labels}
					except:
						data={'features':features,
							  'labels': labels}

					image_features=basearray['features']['image']
					image_features[feature_set]=data
					basearray['features']['image']=image_features

				basearray['labels']=[labelname]

				# write to .JSON 
				jsonfile=open(listdir[i][0:-4]+'.json','w')
				json.dump(basearray, jsonfile)
				jsonfile.close()

			elif listdir[i][0:-4]+'.json' in listdir:
				# overwrite existing .JSON if it is there.
				basearray=json.load(open(listdir[i][0:-4]+'.json'))
				transcript_list=basearray['transcripts']

				# only re-transcribe if necessary 
				if image_transcribe==True:
					for j in range(len(default_image_transcriber)):
						if default_image_transcriber[j] not in list(transcript_list['image']):
							transcript, features, labels = tf.tesseract_featurize(imgfile)
							transcript_list['image'][default_image_transcriber[j]]=transcript 
							basearray['transcripts']=transcript_list

				# only re-featurize if necessary (checks if relevant feature embedding exists)
				for j in range(len(feature_sets)):
					# load feature set 
					feature_set=feature_sets[j]
					# only add in if it is not in the image feature list array 
					if feature_set not in list(basearray['features']['image']):
						features, labels = image_featurize(feature_set, imgfile, cur_dir, haar_dir)
						try:
							data={'features':features.tolist(),
								  'labels': labels}
						except:
							data={'features':features,
								  'labels': labels}
						print(features)
						basearray['features']['image'][feature_set]=data

				# only add label if necessary 
				label_list=basearray['labels']
				if labelname not in label_list:
					label_list.append(labelname)
				basearray['labels']=label_list

				# overwrite .JSON file 
				jsonfile=open(listdir[i][0:-4]+'.json','w')
				json.dump(basearray, jsonfile)
				jsonfile.close()
		except:
			print('error')

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

|  \/  |         | |    | |    
| .  . | ___   __| | ___| |___ 
| |\/| |/ _ \ / _` |/ _ \ / __|
| |  | | (_) | (_| |  __/ \__ \
\_|  |_/\___/ \__,_|\___|_|___/

Make model predictions using this load.py script. This loads in all models in this 
directory and makes predictions on a target folder. Note that files in this target
directory will be featurized with the default features as specified by the settings.json.

Usage: python3 load.py [target directory] [sampletype] [target model directory]

Example: python3 load.py /Users/jim/desktop/allie/load_dir audio /Users/jim/desktop/gender_tpot_classifier

Alt Usage: python3 load.py
--> this just loads all the models and makes predictions in the ./load_dir
'''

import os, json, pickle, time, sys, shutil
import pandas as pd
import numpy as np

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

def most_common(lst):
	'''
	get most common item in a list
	'''
	return max(set(lst), key=lst.count)

def model_schema():
	models={'audio': dict(),
			'text': dict(),
			'image': dict(),
			'video': dict(),
			'csv': dict()
			}
	return models 

def classifyfolder(listdir):

	filetypes=list()

	for i in range(len(listdir)):
		if listdir[i].endswith(('.mp3', '.wav')):
			filetypes.append('audio')
		elif listdir[i].endswith(('.png', '.jpg')):
			filetypes.append('image')
		elif listdir[i].endswith(('.txt')):
			filetypes.append('text')
		elif listdir[i].endswith(('.mp4', '.avi')):
			filetypes.append('video')
		elif listdir[i].endswith(('.csv')):
			filetypes.append('csv')

	filetypes=list(set(filetypes))

	return filetypes

def get_features(models, actual_model_dir, sampletype):
	models=models['%s_models'%(sampletype)]
	features=list()
	for i in range(len(models)):
		os.chdir(actual_model_dir+'/'+models[i])
		temp_settings=json.load(open('settings.json'))
		features=features+temp_settings['default_%s_features'%(sampletype)]
	# get only the necessary features for all models
	default_features=list(set(features))

	return default_features

def featurize(features_dir, load_dir, model_dir, filetypes, models):

	# contextually load the proper features based on the model information
	actual_model_dir=prev_dir(features_dir)+'/models/'+model_dir
	
	# get default features
	sampletype=model_dir.split('_')[0]
	default_features=get_features(models, actual_model_dir, sampletype)

	# now change to proper directory for featurization
	if model_dir=='audio_models' and 'audio' in filetypes:
		os.chdir(features_dir+'/audio_features')
	elif model_dir=='text_models' and 'text' in filetypes:	
		models=models['text_models']
		os.chdir(features_dir+'/text_features')
	elif model_dir=='image_models' and 'image' in filetypes:
		models=models['image_models']
		os.chdir(features_dir+'/image_features')
	elif model_dir=='video_models' and 'video' in filetypes:
		models=models['video_models']	
		os.chdir(features_dir+'/video_features')
	elif model_dir=='csv_models' and 'csv' in filetypes:
		models=models['csv_models']
		os.chdir(features_dir+'/csv_features')

	# call featurization API via default features
	for i in range(len(default_features)):
		print(os.getcwd())
		os.system('python3 featurize.py %s %s'%(load_dir, default_features[i]))


def find_files(model_dir):

	print(model_dir)
	jsonfiles=list()
	csvfiles=list()
	
	if model_dir == 'audio_models':
		listdir=os.listdir()
		print(listdir)
		for i in range(len(listdir)):
			jsonfile=listdir[i][0:-4]+'.json'
			if listdir[i].endswith('.wav') and jsonfile in listdir:
				jsonfiles.append(jsonfile)

	elif model_dir == 'text_models':
		listdir=os.listdir()
		for i in range(len(listdir)):
			jsonfile=listdir[i][0:-4]+'.json'
			if listdir[i].endswith('.txt') and jsonfile in listdir:
				jsonfiles.append(jsonfile)

	elif model_dir == 'image_models':
		listdir=os.listdir()
		for i in range(len(listdir)):
			jsonfile=listdir[i][0:-4]+'.json'
			if listdir[i].endswith('.png') and jsonfile in listdir:
				jsonfiles.append(jsonfile)

	elif model_dir == 'video_models':
		listdir=os.listdir()
		for i in range(len(listdir)):
			jsonfile=listdir[i][0:-4]+'.json'
			if listdir[i].endswith('.mp4') and jsonfile in listdir:
				jsonfiles.append(jsonfile)

	elif model_dir =='csv_models':
		# csv files are a little different here 
		listdir=os.listdir()
		for i in range(len(listdir)):
			csvfile='featurized_'+listdir[i]
			if listdir[i].endswith('.csv') and csvfile in listdir:
				csvfiles.append(csvfile)

	else:
		jsonfiles=[]

	print(jsonfiles)
	return jsonfiles, csvfiles

def make_predictions(sampletype, transformer, clf, modeltype, jsonfiles, csvfiles, default_features, classes, modeldata, model_dir):
	'''
	get the metrics associated iwth a classification and regression problem
	and output a .JSON file with the training session.
	'''

	sampletype=sampletype.split('_')[0]

	if sampletype != 'csv':
		for k in range(len(jsonfiles)):
			try:
				g=json.load(open(jsonfiles[k]))
				print(sampletype)
				print(g)
				features=list()
				print(default_features)
				for j in range(len(default_features)):
					print(sampletype)
					features=features+g['features'][sampletype][default_features[j]]['features']
				
				labels=g['features'][sampletype][default_features[0]]['labels']
				print(transformer)

				print(features)
				if transformer != '':
						features=np.array(transformer.transform(np.array(features).reshape(1, -1))).reshape(1, -1)
				else:
						features=np.array(features).reshape(1,-1)
				print(features)
				metrics_=dict()

				print(modeltype)

				if modeltype not in ['autogluon', 'autokeras', 'autopytorch', 'alphapy', 'atm', 'keras', 'devol', 'ludwig', 'safe', 'neuraxle']:
						y_pred=clf.predict(features)

				elif modeltype=='alphapy':
						# go to the right folder 
						curdir=os.getcwd()
						print(os.listdir())
						os.chdir(common_name+'_alphapy_session')
						alphapy_dir=os.getcwd()
						os.chdir('input')
						os.rename('test.csv', 'predict.csv')
						os.chdir(alphapy_dir)
						os.system('alphapy --predict')
						os.chdir('output')
						listdir=os.listdir()
						for k in range(len(listdir)):
								if listdir[k].startswith('predictions'):
										csvfile=listdir[k]
						y_pred=pd.read_csv(csvfile)['prediction']
						os.chdir(curdir)

				elif modeltype == 'autogluon':
						curdir=os.getcwd()
						os.chdir(model_dir+'/model/')
						from autogluon import TabularPrediction as task
						print(os.getcwd())
						
						if transformer != '':
							new_features=dict()
							for i in range(len(features[0])):
								new_features['feature_%s'%(str(i))]=[features[0][i]]
							print(new_features)
							df=pd.DataFrame(new_features)
						else:
							df=pd.DataFrame(features, columns=labels)
						y_pred=clf.predict(df)
						os.chdir(curdir)

				elif modeltype == 'autokeras':
						curdir=os.getcwd()
						os.chdir(model_dir+'/model')
						print(os.getcwd())
						y_pred=clf.predict(features).flatten()
						os.chdir(curdir)
				elif modeltype == 'autopytorch':
						y_pred=clf.predict(features).flatten()

				elif modeltype == 'atm':
						curdir=os.getcwd()
						os.chdir('atm_temp')
						data = pd.read_csv('test.csv').drop(labels=['class_'], axis=1)
						y_pred = clf.predict(data)
						os.chdir(curdir)

				elif modeltype == 'ludwig':
						data=pd.read_csv('test.csv').drop(labels=['class_'], axis=1)
						pred=clf.predict(data)['class__predictions']
						y_pred=np.array(list(pred), dtype=np.int64)

				elif modeltype== 'devol':
						features=features.reshape(features.shape+ (1,)+ (1,))
						y_pred=clf.predict_classes(features).flatten()

				elif modeltype=='keras':
						if mtype == 'c':
							y_pred=clf.predict_classes(features).flatten()
						elif mtype == 'r':
								y_pred=clf.predict(feaures).flatten()

				elif modeltype =='neuraxle':
						y_pred=clf.transform(features)

				elif modeltype=='safe':
						# have to make into a pandas dataframe
						test_data=pd.read_csv('test.csv').drop(columns=['class_'], axis=1)
						y_pred=clf.predict(test_data)
						# update model in schema

				# except:
					# print('error %s'%(modeltype.upper()))

				# try:
				# get class from classes (assuming classification)
				'''
				X={'male': [1],
					'female': [2],
					'other': [3]}

				then do a search of the values
				names=list(X) --> ['male', 'female', 'other']		
				i1=X.values().index([1]) --> 0 
				names[i1] --> male 
				'''
				
				# print(modeldata)
				outputs=dict()
				for i in range(len(classes)):
					outputs[classes[i]]=[i]

				names=list(outputs)
				i1=list(outputs.values()).index(y_pred)
				class_=classes[i1]

				print(y_pred)
				print(outputs)
				print(i1)
				print(class_)

				try:
					models=g['models']
				except:
					models=models=model_schema()

				temp=models[sampletype]

				if class_ not in list(temp):
					temp[class_]= [modeldata]
				else:
					tclass=temp[class_]
					try:
						# make a list if it is not already to be compatible with deprecated versions
						tclass.append(modeldata)
					except:
						tclass=[tclass]
						tclass.append(modeldata)
					temp[class_]=tclass
					
				models[sampletype]=temp
				g['models']=models
				print(class_)

				# update database
				jsonfilename=open(jsonfiles[k],'w')
				json.dump(g,jsonfilename)
				jsonfilename.close()
			except:
				print('error making jsonfile %s'%(jsonfiles[k].upper()))
	else:
		try:
			for k in range(len(csvfiles)):
				
				if len(csvfiles[k].split('featurized')) == 2:
					features=pd.read_csv(csvfiles[k])
					oldfeatures=features
					print(features)
					if transformer != '':
							features=np.array(transformer.transform(np.array(features)))
					else:
							features=np.array(features)
					print(features)
					metrics_=dict()

					print(modeltype)

					if modeltype not in ['autogluon', 'autokeras', 'autopytorch', 'alphapy', 'atm', 'keras', 'devol', 'ludwig', 'safe', 'neuraxle']:
							y_pred=clf.predict(features)

					elif modeltype=='alphapy':
							# go to the right folder 
							curdir=os.getcwd()
							print(os.listdir())
							os.chdir(common_name+'_alphapy_session')
							alphapy_dir=os.getcwd()
							os.chdir('input')
							os.rename('test.csv', 'predict.csv')
							os.chdir(alphapy_dir)
							os.system('alphapy --predict')
							os.chdir('output')
							listdir=os.listdir()
							for k in range(len(listdir)):
									if listdir[k].startswith('predictions'):
											csvfile=listdir[k]
							y_pred=pd.read_csv(csvfile)['prediction']
							os.chdir(curdir)

					elif modeltype == 'autogluon':
							curdir=os.getcwd()
							os.chdir(model_dir+'/model/')
							from autogluon import TabularPrediction as task
							print(os.getcwd())
							
							if transformer != '':
								new_features=dict()
								for i in range(len(features[0])):
									new_features['feature_%s'%(str(i))]=[features[0][i]]
								print(new_features)
								df=pd.DataFrame(new_features)
							else:
								df=pd.DataFrame(features, columns=labels)
							y_pred=clf.predict(df)
							os.chdir(curdir)

					elif modeltype == 'autokeras':
							curdir=os.getcwd()
							os.chdir(model_dir+'/model')
							print(os.getcwd())
							y_pred=clf.predict(features).flatten()
							os.chdir(curdir)
					elif modeltype == 'autopytorch':
							y_pred=clf.predict(features).flatten()

					elif modeltype == 'atm':
							curdir=os.getcwd()
							os.chdir('atm_temp')
							data = pd.read_csv('test.csv').drop(labels=['class_'], axis=1)
							y_pred = clf.predict(data)
							os.chdir(curdir)

					elif modeltype == 'ludwig':
							data=pd.read_csv('test.csv').drop(labels=['class_'], axis=1)
							pred=clf.predict(data)['class__predictions']
							y_pred=np.array(list(pred), dtype=np.int64)

					elif modeltype== 'devol':
							features=features.reshape(features.shape+ (1,)+ (1,))
							y_pred=clf.predict_classes(features).flatten()

					elif modeltype=='keras':
							if mtype == 'c':
								y_pred=clf.predict_classes(features).flatten()
							elif mtype == 'r':
									y_pred=clf.predict(feaures).flatten()

					elif modeltype =='neuraxle':
							y_pred=clf.transform(features)

					elif modeltype=='safe':
							# have to make into a pandas dataframe
							test_data=pd.read_csv('test.csv').drop(columns=['class_'], axis=1)
							y_pred=clf.predict(test_data)
							# update model in schema

					y_pred=pd.DataFrame(y_pred)
					oldfeatures['class_']=y_pred
					print(type(y_pred))	
					oldfeatures.to_csv(csvfiles[k].replace('featurized','predictions'), index=False)
		except:
			pass

def load_model(folder_name):

	listdir=os.listdir()
	# load in a transform if necessary
	for i in range(len(listdir)):
		if listdir[i].endswith('transform.pickle'):
			print(listdir[i])
			transform_=open(listdir[i],'rb')
			transformer=pickle.load(transform_)
			transform_.close()
			break
		else:
			transformer=''

	jsonfile=open(folder_name+'.json')
	g=json.load(jsonfile)
	jsonfile.close()

	# get model name
	modelname=g['model name']
	classes=g['classes']
	model_type=g['model type']
	print(model_type)
	# g['model type']

	# load model for getting metrics
	if model_type not in ['alphapy', 'atm', 'autokeras', 'autopytorch', 'ludwig', 'keras', 'devol']:
		loadmodel=open(modelname, 'rb')
		clf=pickle.load(loadmodel)
		loadmodel.close()
	elif model_type == 'atm':
		from atm import Model
		clf=Model.load(modelname)
	elif model_type == 'autokeras':
		import tensorflow as tf
		import autokeras as ak
		clf = pickle.load(open(modelname, 'rb'))
	elif model_type=='autopytorch':
		import torch
		clf=torch.load(modelname)
	elif model_type == 'ludwig':
		from ludwig.api import LudwigModel
		clf=LudwigModel.load('ludwig_files/experiment_run/model/')
	elif model_type in ['devol', 'keras']: 
		from keras.models import load_model
		clf = load_model(modelname)
	else: 
		clf=''

	return transformer, clf, model_type, classes, g

def find_models(target_model_dir, sampletype):

	curdir=os.getcwd()

	if sampletype == False:
		listdir=os.listdir()
		directories=['audio_models', 'text_models', 'image_models', 'video_models', 'csv_models']
		models_=dict()

		for i in range(len(directories)):
			model_names=list()
			try:
				os.chdir(curdir)
				os.chdir(directories[i])
				listdir=os.listdir()

				folders=list()
				for j in range(len(listdir)):
					if listdir[j].find('.') < 0:
						folders.append(listdir[j])

				print(folders)
				curdir2=os.getcwd()

				for j in range(len(folders)):
					try:
						os.chdir(curdir2)
						os.chdir(folders[j])
						os.chdir('model')
						listdir2=os.listdir()
						jsonfile=folders[j]+'.json'
						for k in range(len(listdir2)):
							if listdir2[k] == jsonfile:
								g=json.load(open(jsonfile))
								model_names.append(jsonfile[0:-5])
					except:
						pass
				print(model_names)
			except:
				print('error')

			models_[directories[i]]=model_names
	else:
		# copy the target_model_dir to the right folder
		models_=dict()
		models_['audio_models']=list()
		models_['text_models']=list()
		models_['text_models']=list()
		models_['image_models']=list()
		models_['csv_models']=list()

		try:
			shutil.copytree(target_model_dir, curdir+'/'+sampletype+'_models/'+target_model_dir.split('/')[-1])
		except:
			pass

		models_[sampletype+'_models']=[target_model_dir.split('/')[-1]]

	print('------------------------------')
	print('	      IDENTIFIED MODELS      ')
	print('------------------------------')

	print(models_)

	# time.sleep(50)
	return models_

# get folders
curdir=os.getcwd()
basedir=prev_dir(curdir)
os.chdir(basedir)

# load settings 
settings=json.load(open('settings.json'))

# get the base audio, text, image, and video features from required models
default_audio_features=settings['default_audio_features']
default_text_features=settings['default_text_features']
default_image_features=settings['default_image_features']
default_video_features=settings['default_video_features']
default_csv_features=settings['default_csv_features']

features_dir=basedir+'/features'
model_dir=basedir+'/models'

try:
	# specify a specific model to make a prediction around 
	# e.g. /Users/jim/desktop/audiofiles
	load_dir=sys.argv[1]
except:
	# if not specified, defaults to the ./load_dir folder
	load_dir=basedir+'/load_dir'
try:
	# get the sampletype, for example 'audio'
	sampletype = sys.argv[2]
except:	
	# if no sampletype specified, it will discover all file types
	sampletype=False
try:

	target_model_dir=sys.argv[3]
except:
	target_model_dir=False

# now get all the filetypes if not specified 
os.chdir(load_dir)
listdir=os.listdir()

if sampletype != False and sampletype in ['audio','image','text','image','video','csv']:
	# e.g. sampletype =='audio'
	filetypes=[sampletype]
else:
	# get file tyes ['audio','image','text','image','video','csv']
	filetypes=classifyfolder(listdir)

# find all machine learning models
os.chdir(model_dir)
models=find_models(target_model_dir, sampletype)
model_dirs=list(models)

# now that we have all the models we can begin to load all of them 
for i in range(len(model_dirs)):
	if model_dirs[i].split('_')[0] in filetypes:
		print('-----------------------')
		print('FEATURIZING %s'%(model_dirs[i].upper()))
		print('-----------------------')
		# Note this contextually featurizes based on all the models and the 
		# minimum number of featurizations necessary to accomodate all model predictions
		featurize(features_dir, load_dir, model_dirs[i], filetypes, models)

# now model everything
for i in range(len(model_dirs)):
	# try:
	if model_dirs[i].split('_')[0] in filetypes:

		print('-----------------------')
		print('MODELING %s'%(model_dirs[i].upper()))
		print('-----------------------')
		os.chdir(model_dir)
		os.chdir(model_dirs[i])
		models_=models[model_dirs[i]]

		# get default features
		print(model_dirs[i])
		if model_dirs[i] == 'audio_models':
			default_features =default_audio_features
		elif model_dirs[i] == 'text_models':
			default_features = default_text_features
		elif model_dirs[i] == 'image_models':
			default_features = default_image_features
		elif model_dirs[i] == 'video_models':
			default_features = default_video_features
		elif model_dirs[i] == 'csv_models':
			default_features = default_csv_features

		# loop through models
		for j in range(len(models_)):
			os.chdir(model_dir)
			os.chdir(model_dirs[i])
			print('--> predicting %s'%(models_[j]))
			os.chdir(models_[j])
			os.chdir('model')
			transformer, clf, modeltype, classes, modeldata = load_model(models_[j])
			os.chdir(load_dir)
			jsonfiles, csvfiles=find_files(model_dirs[i])
			make_predictions(model_dirs[i], transformer, clf, modeltype, jsonfiles, csvfiles, default_features, classes, modeldata, model_dir+'/'+model_dirs[i]+'/'+models_[j])
	# except:
		# print('error')
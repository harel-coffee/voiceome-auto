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
                                                                
                                                                
 _____         _   
|_   _|       | |  
  | | _____  _| |_ 
  | |/ _ \ \/ / __|
  | |  __/>  <| |_ 
  \_/\___/_/\_\\__|
                   
Featurize folders of text files with the default_text_features.

Usage: python3 featurize.py [folder] [featuretype]

All featuretype options include:
["bert_features", "fast_features", "glove_features", "grammar_features", 
"nltk_features", "spacy_features", "text_features", "w2v_features"]

Read more @ https://github.com/jim-schwoebel/allie/tree/master/features/text_features
'''
##################################################
##				Import statements   			##
##################################################

import numpy as np
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from tqdm import tqdm
import helpers.transcribe as ts
import json, os, sys
import os, wget, zipfile, uuid
import shutil

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

def text_featurize(feature_set, transcript, glovemodel, w2vmodel, fastmodel, bert_model):

	if feature_set == 'nltk_features':
		features, labels = nf.nltk_featurize(transcript)
	elif feature_set == 'spacy_features':
		features, labels = sf.spacy_featurize(transcript)
	elif feature_set == 'glove_features':
		features, labels=gf.glove_featurize(transcript, glovemodel)
	elif feature_set == 'w2v_features':
		features, labels=w2v.w2v_featurize(transcript, w2vmodel)
	elif feature_set == 'fast_features':
		features, labels=ff.fast_featurize(transcript, fastmodel)
	elif feature_set == 'text_features':
		features, labels=textf.text_featurize(transcript)
	elif feature_set == 'grammar_features':
		features, labels=grammarf.grammar_featurize(transcript)
	elif feature_set == 'bert_features':
		features, labels=bertf.bert_featurize(transcript, bert_model)
	elif feature_set == 'blabla_feature':
		features, labels=bbf.blabla_featurize(transcript)
	
	# make sure all the features do not have any infinity or NaN
	features=np.nan_to_num(np.array(features))
	features=features.tolist()

	return features, labels 

def transcribe_text(default_text_transcriber, transcript):
	## create a simple function to expand into the future
	if default_text_transcriber == 'raw text':
		transcript=transcript
	else:
		transcript=''
	return transcript

# type in folder before downloading and loading large files.
foldername=sys.argv[1]

# get class label from folder name 
labelname=foldername.split('/')
if labelname[-1]=='':
	labelname=labelname[-2]
else:
	labelname=labelname[-1]

##################################################
##				   Main script  		    	##
##################################################

basedir=os.getcwd()

# directory=sys.argv[1]
settingsdir=prev_dir(basedir)
sys.path.append(settingsdir)
from standard_array import make_features
settingsdir=prev_dir(settingsdir)
settings=json.load(open(settingsdir+'/settings.json'))
os.chdir(basedir)
try:
	feature_sets=[sys.argv[2]]
except:
	feature_sets=settings['default_text_features']
default_text_transcribers=settings['default_text_transcriber']
text_transcribe=settings['transcribe_text']

# contextually load repositories here
if 'blabla_features' in feature_sets:
	import blabla_features as bbf
if 'nltk_features' in feature_sets:
	import nltk_features as nf
if 'spacy_features' in feature_sets:
	import spacy_features as sf
if 'glove_features' in feature_sets:
	import glove_features as gf 
if 'w2v_features' in feature_sets:
	import w2v_features as w2v
if 'fast_features' in feature_sets:
	import fast_features as ff
if 'text_features' in feature_sets:
	import text_features as textf 
if 'grammar_features' in feature_sets:
	import grammar_features as grammarf
if 'bert_features' in feature_sets:
	import bert_features as bertf
	from sentence_transformers import SentenceTransformer
	bert_model=SentenceTransformer('bert-base-nli-mean-tokens')
else:
	bert_model=[]

# can specify many types of features...
for j in range(len(feature_sets)):
	feature_set=feature_sets[j]
	glovemodel=[]
	w2vmodel=[]
	fastmodel=[]

	if feature_set in ['nltk_features', 'spacy_features']:
		# save memory by not loading any models that are not necessary.
		glovemodel=[]
		w2vmodel=[]
		fastmodel=[]

	else:
		##################################################
		##				Load ML models					##
		##################################################

		# load GloVE model
		if feature_set == 'glove_features':

			from gensim.scripts.glove2word2vec import glove2word2vec

			if 'glove.6B' not in os.listdir(os.getcwd()+'/helpers'):
				curdir=os.getcwd()
				print('downloading GloVe model...')
				wget.download("http://neurolex.co/uploads/glove.6B.zip", "./helpers/glove.6B.zip")
				print('extracting GloVe model')
				zip_ref = zipfile.ZipFile(os.getcwd()+'/helpers/glove.6B.zip', 'r')
				zip_ref.extractall(os.getcwd()+'/helpers/glove.6B')
				zip_ref.close()
				os.chdir(os.getcwd()+'/helpers/glove.6B')
				glove_input_file = 'glove.6B.100d.txt'
				word2vec_output_file = 'glove.6B.100d.txt.word2vec'
				glove2word2vec(glove_input_file, word2vec_output_file)
				os.chdir(curdir)

			glovemodelname = 'glove.6B.100d.txt.word2vec'
			print('-----------------')
			print('loading GloVe model...')
			glovemodel = KeyedVectors.load_word2vec_format(os.getcwd()+'/helpers/glove.6B/'+glovemodelname, binary=False)
			print('loaded GloVe model...')

		# load Google W2V model
		elif feature_set == 'w2v_features':

			if 'GoogleNews-vectors-negative300.bin' not in os.listdir(os.getcwd()+'/helpers'):
				print('downloading Google W2V model...')
				wget.download("http://neurolex.co/uploads/GoogleNews-vectors-negative300.bin", "./helpers/GoogleNews-vectors-negative300.bin")

			w2vmodelname = 'GoogleNews-vectors-negative300.bin'
			print('-----------------')
			print('loading Google W2V model...')
			w2vmodel = KeyedVectors.load_word2vec_format(os.getcwd()+'/helpers/'+w2vmodelname, binary=True)
			print('loaded Google W2V model...')

		# load facebook FastText model
		elif feature_set == 'fast_features':

			from gensim.models.fasttext import FastText

			if 'wiki-news-300d-1M' not in os.listdir(os.getcwd()+'/helpers'):
				print('downloading Facebook FastText model...')
				wget.download("https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip", "./helpers/wiki-news-300d-1M.vec.zip")
				zip_ref = zipfile.ZipFile(os.getcwd()+'/helpers/wiki-news-300d-1M.vec.zip', 'r')
				zip_ref.extractall(os.getcwd()+'/helpers/wiki-news-300d-1M')
				zip_ref.close()

			print('-----------------')
			print('loading Facebook FastText model...')
			# Loading fasttext model 
			fastmodel = KeyedVectors.load_word2vec_format(os.getcwd()+'/helpers/wiki-news-300d-1M/wiki-news-300d-1M.vec')
			print('loaded Facebook FastText model...')


# # rename files appropriately to eliminate ( and ) 
# os.chdir(foldername)
# listdir=os.listdir()
# for i in range(len(listdir)):
# 	if listdir[i].endswith('.txt'):
# 		id_=str(uuid.uuid4())
# 		os.rename(listdir[i], id_+'.txt')
# 		if listdir[i][0:-4]+'.json' in listdir:
# 			os.rename(listdir[i][0:-4]+'.json', id_+'.json')

# now get files and directory
os.chdir(foldername)
listdir=os.listdir()
cur_dir=os.getcwd()

# featurize all files accoridng to librosa featurize
for i in tqdm(range(len(listdir)), desc=labelname):
	if listdir[i][-4:] in ['.txt']:
		try:
			sampletype='text'
			os.chdir(cur_dir)
			transcript=open(listdir[i]).read()

			# I think it's okay to assume audio less than a minute here...
			if listdir[i][0:-4]+'.json' not in listdir:

				# make new .JSON if it is not there with base array schema.
				basearray=make_features(sampletype)

				# assume text_transcribe==True and add to transcript list
				if text_transcribe==True: 
					transcript_list=basearray['transcripts']
					for j in range(len(default_text_transcribers)):
						default_text_transcriber=default_text_transcribers[j]
						transcript_=transcribe_text(default_text_transcriber, transcript)
						transcript_list['text'][default_text_transcriber]=transcript_
						basearray['transcripts']=transcript_list

				for j in range(len(feature_sets)):
					feature_set=feature_sets[j]
					# featurize the text file 
					features, labels = text_featurize(feature_set, transcript, glovemodel, w2vmodel, fastmodel, bert_model)
					print(features)

					try:
						data={'features':features.tolist(),
							  'labels': labels}
					except:
						data={'features':features,
							  'labels': labels}

					text_features=basearray['features']['text']
					text_features[feature_set]=data
					basearray['features']['text']=text_features

				basearray['labels']=[foldername]
				jsonfile=open(listdir[i][0:-4]+'.json','w')
				json.dump(basearray, jsonfile)
				jsonfile.close()

			elif listdir[i][0:-4]+'.json' in listdir:
				
				# load base array 
				basearray=json.load(open(listdir[i][0:-4]+'.json'))

				# get transcript and update if necessary 
				transcript_list=basearray['transcripts']

				# assume text_transcribe==True and add to transcript list 
				if text_transcribe==True:
					for j in range(len(default_text_transcribers)):
						default_text_transcriber=default_text_transcribers[j]
						if default_text_transcriber not in list(transcript_list['text']):
							transcript_=transcribe_text(default_text_transcriber, transcript)
							transcript_list['text'][default_text_transcriber]=transcript_
							basearray['transcripts']=transcript_list

				for j in range(len(feature_sets)):
					feature_set=feature_sets[j]
					# re-featurize only if necessary 
					if feature_set not in list(basearray['features']['text']):

						features, labels = text_featurize(feature_set, transcript, glovemodel, w2vmodel, fastmodel, bert_model)
						print(features)

						try:
							data={'features':features.tolist(),
								  'labels': labels}
						except:
							data={'features':features,
								  'labels': labels}

						basearray['features']['text'][feature_set]=data

				# only add the label if necessary 
				label_list=basearray['labels']
				if labelname not in label_list:
					label_list.append(labelname)
				basearray['labels']=label_list

				# overwrite existing .JSON
				jsonfile=open(listdir[i][0:-4]+'.json','w')
				json.dump(basearray, jsonfile)
				jsonfile.close()

		except:
			print('error')

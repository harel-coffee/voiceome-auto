# Datasets

![](https://github.com/jim-schwoebel/allie/blob/master/annotation/helpers/assets/datasets.png)

You can quickly download any of these datasets with the download.py script. This uses fuzzy search to figure out what dataset you are trying to find. 
```
cd allie/datasets/downloads
python3 download.py 
```

An exhaustive list of all the audio, text, image, and video datasets are listed below.

You can also search for more datasets using Google DataSet search @ https://toolbox.google.com/datasetsearch or Kaggle @ https://www.kaggle.com/datasets.

You can always create datasets with [mTurk](https://towardsdatascience.com/how-i-created-a-40-000-labeled-audio-dataset-in-4-hours-of-work-and-500-17ad9951b180), [YouTube Scrape](https://github.com/jim-schwoebel/youtube_scrape/tree/b030d65277626ee01bea0fd98cee2d1ffafee8bb), and/or [SurveyLex](https://surveylex.com) as well.

## Standard feature dictionary 

After much trial and error, this standard feature dictionary schema seemed the most appropriate for defining data samples (audio, text, image, video, or CSV samples):

```python3
def make_features(sampletype):

	# only add labels when we have actual labels.
	features={'audio':dict(),
		  'text': dict(),
		  'image':dict(),
		  'video':dict(),
		  'csv': dict()}

	transcripts={'audio': dict(),
		     'text': dict(),
		     'image': dict(),
		     'video': dict(),
		     'csv': dict()}

	models={'audio': dict(),
		 'text': dict(),
		 'image': dict(),
		 'video': dict(),
		 'csv': dict()}

	data={'sampletype': sampletype,
	      'transcripts': transcripts,
	      'features': features,
	      'models': models,
	      'labels': [],
	      'errors': []}

	return data
```

There are many advantages for having this schema including:
- **sampletype definition flexibility** - flexible to 'audio' (.WAV / .MP3), 'text' (.TXT / .PPT / .DOCX), 'image' (.PNG / .JPG), 'video' (.MP4), and 'csv' (.CSV). This format can also can adapt into the future to new sample types, which can also tie to new featurization scripts. By defining a sample type, it can help guide how data flows through model training and prediction scripts. 
- **transcript definition flexibility** - transcripts can be audio, text, image, video, and csv transcripts. The image and video transcripts use OCR to characterize text in the image, whereas audio transcripts are transcipts done by traditional speech-to-text systems (e.g. Pocketsphinx). You can also add multiple transcripts (e.g. Google and PocketSphinx) for the same sample type.
- **featurization flexibility** - many types of features can be put into this array of the same data type. For example, an audio file can be featurized with 'standard_features' and 'praat_features' without really affecting anything. This eliminates the need to re-featurize and reduces time to sort through multiple types of featurizations during the data cleaning process.
- **label annotation flexibility** - can take the form of ['classname_1', 'classname_2', 'classname_N...'] - classification problems and [{classname1: 'value'}, {classname2: 'value'}, ... {classnameN: 'valueN'}] where values are between [0,1] for regression problems. 
- **model predictions** - one survey schema can be used for making model predictions and updating the schema with these predictions. Note that any model that is used for training can be used to make predictions in the load_dir. 
- **visualization flexibility** - can easily visualize features of any sample type through Allie's [visualization script](https://github.com/jim-schwoebel/allie/tree/master/visualize) (e.g. tSNE plots, correlation matrices, and more).
- **error tracing** - easily trace errors associated with featurization and/or modeling to review what is happening during a session.

This schema is inspired by [D3M-schema](https://github.com/mitll/d3m-schema/blob/master/documentation/datasetSchema.md) by the MIT media lab.

## Seeding sample data 

To illustrate a quick example, we can pull some sample audio data from this GitHub repository, separating males (x50) from females (x50). 

This [seed_test.py script](https://github.com/jim-schwoebel/allie/blob/master/datasets/seed_test.py) creates two datasets in the train_dir folder, one full of audio files of males and the other full of audio files of females. This data will be used for the rest of the demo sections listed here.

```python3
cd /Users/jim/desktop/allie
cd datasets
python3 seed_test.py
---------------
Cloning into 'sample_voice_data'...
remote: Enumerating objects: 119, done.
remote: Counting objects: 100% (119/119), done.
remote: Compressing objects: 100% (115/115), done.
remote: Total 119 (delta 5), reused 108 (delta 2), pack-reused 0
Receiving objects: 100% (119/119), 18.83 MiB | 7.43 MiB/s, done.
Resolving deltas: 100% (5/5), done.
```
You can easily test if the files are in there with:
```
cd ..
cd train_dir
ls
```
Which should output:
```
jim@Jims-MBP train_dir % ls
README.md		delete_json.py		females
delete_features.py	featurize_csv.py	males
```

Click the .GIF below for a quick tutorial and example.

[![](https://github.com/jim-schwoebel/allie/blob/master/annotation/helpers/assets/collecting.gif)](https://drive.google.com/file/d/1YYniwEJWZFpxTFNwJSGYGP0eeCAgxcvU/view?usp=sharing)

## Audio datasets 
There are two main types of audio datasets: speech datasets and audio event/music datasets. 

### Speech datasets 
* [2000 HUB5 English](https://catalog.ldc.upenn.edu/LDC2002T43) - The Hub5 evaluation series focused on conversational speech over the telephone with the particular task of transcribing conversational speech into text. Its goals were to explore promising new areas in the recognition of conversational speech, to develop advanced technology incorporating those ideas and to measure the performance of new technology.
* [Arabic Speech Corpus](http://en.arabicspeechcorpus.com/) - The Arabic Speech Corpus (1.5 GB) is a Modern Standard Arabic (MSA) speech corpus for speech synthesis. The corpus contains phonetic and orthographic transcriptions of more than 3.7 hours of MSA speech aligned with recorded speech on the phoneme level. The annotations include word stress marks on the individual phonemes. 
* [AudioMNIST](https://github.com/soerenab/AudioMNIST) - The dataset consists of 30000 audio samples of spoken digits (0-9) of 60 different speakers
* [Common Voice](https://voice.mozilla.org/) - Common Voice is Mozilla's initiative to help teach machines how real people speak. 12GB in size; spoken text based on text from a number of public domain sources like user-submitted blog posts, old books, movies, and other public speech corpora.
* [CHIME](https://archive.org/details/chime-home) - This is a noisy speech recognition challenge dataset (~4GB in size). The dataset contains real simulated and clean voice recordings. Real being actual recordings of 4 speakers in nearly 9000 recordings over 4 noisy locations, simulated is generated by combining multiple environments over speech utterances and clean being non-noisy recordings. 
* [CMU Wilderness](http://festvox.org/cmu_wilderness/) - (noncommercial) - not available but a great speech dataset many accents reciting passages from the Bible.
* [Emotional Voices Database](https://github.com/numediart/EmoV-DB) - various emotions with 5 voice actors (amused, angry, disgusted, neutral, sleepy).
* [Emotional Voice dataset - Nature](https://www.nature.com/articles/s41562-019-0533-6) -  2,519 speech samples produced by 100 actors from 5 cultures. With large-scale statistical inference methods, we find that prosody can communicate at least 12 distinct kinds of emotion that are preserved across the 2 cultures. 
* [Free Spoken Digit Dataset](https://github.com/Jakobovski/free-spoken-digit-dataset) -4 speakers, 2,000 recordings (50 of each digit per speaker), English pronunciations.
* [Flickr Audio Caption](https://groups.csail.mit.edu/sls/downloads/flickraudio/) - 40,000 spoken captions of 8,000 natural images, 4.2 GB in size.
* [ISOLET Data Set](https://data.world/uci/isolet) - This 38.7 GB dataset helps predict which letter-name was spoken — a simple classification task.
* [Librispeech](https://www.openslr.org/12) - LibriSpeech is a corpus of approximately 1000 hours of 16Khz read English speech derived from read audiobooks from the LibriVox project.
* [LJ Speech](https://keithito.com/LJ-Speech-Dataset/) - This is a public domain speech dataset consisting of 13,100 short audio clips of a single speaker reading passages from 7 non-fiction books. A transcription is provided for each clip. Clips vary in length from 1 to 10 seconds and have a total length of approximately 24 hours.
* [Multimodal EmotionLines Dataset (MELD)](https://github.com/SenticNet/MELD) - Multimodal EmotionLines Dataset (MELD) has been created by enhancing and extending EmotionLines dataset. MELD contains the same dialogue instances available in EmotionLines, but it also encompasses audio and visual modality along with text. MELD has more than 1400 dialogues and 13000 utterances from Friends TV series. Each utterance in a dialogue has been labeled with— Anger, Disgust, Sadness, Joy, Neutral, Surprise and Fear. 
* [Noisy Dataset](https://datashare.is.ed.ac.uk/handle/10283/2791)- Clean and noisy parallel speech database. The database was designed to train and test speech enhancement methods that operate at 48kHz. 
* [Parkinson's speech dataset](https://archive.ics.uci.edu/ml/datasets/Parkinson+Speech+Dataset+with++Multiple+Types+of+Sound+Recordings) - The training data belongs to 20 Parkinson’s Disease (PD) patients and 20 healthy subjects. From all subjects, multiple types of sound recordings (26) are taken for this 20 MB set.
* [Persian Consonant Vowel Combination (PCVC) Speech Dataset](https://github.com/S-Malek/PCVC) - The Persian Consonant Vowel Combination (PCVC) Speech Dataset is a Modern Persian speech corpus for speech recognition and also speaker recognition. This dataset contains 23 Persian consonants and 6 vowels. The sound samples are all possible combinations of vowels and consonants (138 samples for each speaker) with a length of 30000 data samples.
* [Speech Accent Archive](https://www.kaggle.com/rtatman/speech-accent-archive/version/1) - For various accent detection tasks.
* [Speech Commands Dataset](http://ai.googleblog.com/2017/08/launching-speech-commands-dataset.html) - The dataset (1.4 GB) has 65,000 one-second long utterances of 30 short words, by thousands of different people, contributed by members of the public through the AIY website.
* [Spoken Commands dataset](https://github.com/JohannesBuchner/spoken-command-recognition) - A large database of free audio samples (10M words), a test bed for voice activity detection algorithms and for recognition of syllables (single-word commands). 3 speakers, 1,500 recordings (50 of each digit per speaker), English pronunciations. This is a really small set- about 10 MB in size.
* [Spoken Wikipeida Corpora](https://nats.gitlab.io/swc/) - 38 GB in size available in both audio and without audio format.
* [Tatoeba](https://tatoeba.org/eng/downloads) - Tatoeba is a large database of sentences, translations, and spoken audio for use in language learning. This download contains spoken English recorded by their community.
* [Ted-LIUM](https://www.openslr.org/51/) - The TED-LIUM corpus was made from audio talks and their transcriptions available on the TED website (noncommercial).
* [TIMIT dataset](https://catalog.ldc.upenn.edu/LDC93S1) - TIMIT contains broadband recordings of 630 speakers of eight major dialects of American English, each reading ten phonetically rich sentences. It includes time-aligned orthographic, phonetic and word transcriptions as well as a 16-bit, 16 kHz speech waveform file for each utterance (have to pay).
* [VoxCeleb](https://github.com/andabi/voice-vector) - VoxCeleb is a large-scale speaker identification dataset. It contains around 100,000 utterances by 1,251 celebrities, extracted from You Tube videos. The data is mostly gender balanced (males comprise of 55%). The celebrities span a diverse range of accents, professions, and age. There is no overlap between the development and test sets. It’s an intriguing use case for isolating and identifying which superstar the voice belongs to.
* [VoxForge](http://www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/) - VoxForge was set up to collect transcribed speech for use with Free and Open Source Speech Recognition Engines.
* [Zero Resource Speech Challenge](https://github.com/bootphon/zerospeech2017) - The ultimate goal of the Zero Resource Speech Challenge is to construct a system that learns an end-to-end Spoken Dialog (SD) system, in an unknown language, from scratch, using only information available to a language learning infant. “Zero resource” refers to zero linguistic expertise (e.g., orthographic/linguistic transcriptions), not zero information besides audio (visual, limited human feedback, etc). The fact that 4-year-olds spontaneously learn a language without supervision from language experts show that this goal is theoretically reachable.

### Audio events and music 
* [AudioSet](https://research.google.com/audioset/) - An expanding ontology of 632 audio event classes and a collection of 2,084,320 human-labeled 10-second sound clips drawn from YouTube videos. 
* [Bird audio detection challenge](http://machine-listening.eecs.qmul.ac.uk/bird-audio-detection-challenge/) -  This challenge contained new datasets (5.4 GB) collected in real live bio-acoustics monitoring projects, and an objective, standardized evaluation framework.
* [Environmental audio dataset](http://www.cs.tut.fi/~heittolt/datasets) - Audio data collection and manual data annotation both are tedious processes, and lack of proper development dataset limits fast development in the environmental audio research.
* [Free Music Archive](https://github.com/mdeff/fma) - FMA is a dataset for music analysis. 1000 GB in size.
* [Freesound dataset](https://www.kaggle.com/c/freesound-audio-tagging-2019/data) - many different sound events. https://annotator.freesound.org/ and https://annotator.freesound.org/fsd/explore/ - The AudioSet Ontology is a hierarchical collection of over 600 sound classes and we have filled them with 297,159 audio samples from Freesound. This process generated 678,511 candidate annotations that express the potential presence of sound sources in audio clips.
* [Karoldvl-ESC](https://github.com/karoldvl/ESC-50) - The ESC-50 dataset is a labeled collection of 2000 environmental audio recordings suitable for benchmarking methods of environmental sound classification.
* [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/) - The Million Song Dataset is a freely-available collection of audio features and meta-data for a million contemporary popular music tracks. 280 GB in size.
* [Urban Sound Dataset](https://urbansounddataset.weebly.com/) - two datasets and a taxonomy for urban sound research.

## Text datasets

Text datasets mostly separated by language.
* [TBA] - standard dataset used for text classification 

### Datasets (English, multilang)
*   [Apache Software Foundation Public Mail Archives](http://aws.amazon.com/de/datasets/apache-software-foundation-public-mail-archives/): all publicly available Apache Software Foundation mail archives as of July 11, 2011 (200 GB)
*   [Blog Authorship Corpus](http://u.cs.biu.ac.il/~koppel/BlogCorpus.htm): consists of the collected posts of 19,320 bloggers gathered from blogger.com in August 2004. 681,288 posts and over 140 million words. (298 MB)
*   [Amazon Fine Food Reviews [Kaggle]](https://www.kaggle.com/snap/amazon-fine-food-reviews): consists of 568,454 food reviews Amazon users left up to October 2012. [Paper](http://i.stanford.edu/~julian/pdfs/www13.pdf). (240 MB)
*   [Amazon Reviews](https://snap.stanford.edu/data/web-Amazon.html): Stanford collection of 35 million amazon reviews. (11 GB)
*   [ArXiv](http://arxiv.org/help/bulk_data_s3): All the Papers on archive as fulltext (270 GB) + sourcefiles (190 GB).
*   [ASAP Automated Essay Scoring [Kaggle]](https://www.kaggle.com/c/asap-aes/data): For this competition, there are eight essay sets. Each of the sets of essays was generated from a single prompt. Selected essays range from an average length of 150 to 550 words per response. Some of the essays are dependent upon source information and others are not. All responses were written by students ranging in grade levels from Grade 7 to Grade 10. All essays were hand graded and were double-scored. (100 MB)
*   [ASAP Short Answer Scoring [Kaggle]](https://www.kaggle.com/c/asap-sas/data): Each of the data sets was generated from a single prompt. Selected responses have an average length of 50 words per response. Some of the essays are dependent upon source information and others are not. All responses were written by students primarily in Grade 10. All responses were hand graded and were double-scored. (35 MB)
*   [Classification of political social media](https://www.crowdflower.com/data-for-everyone/): Social media messages from politicians classified by content. (4 MB)
*   [CLiPS Stylometry Investigation (CSI) Corpus](http://www.clips.uantwerpen.be/datasets/csi-corpus): a yearly expanded corpus of student texts in two genres: essays and reviews. The purpose of this corpus lies primarily in stylometric research, but other applications are possible. (on request)
*   [ClueWeb09 FACC](http://lemurproject.org/clueweb09/FACC1/): [ClueWeb09](http://lemurproject.org/clueweb09/) with Freebase annotations (72 GB)
*   [ClueWeb11 FACC](http://lemurproject.org/clueweb12/FACC1/): [ClueWeb11](http://lemurproject.org/clueweb12/) with Freebase annotations (92 GB)
*   [Common Crawl Corpus](http://aws.amazon.com/de/datasets/common-crawl-corpus/): web crawl data composed of over 5 billion web pages (541 TB)
*   [Cornell Movie Dialog Corpus](http://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html): contains a large metadata-rich collection of fictional conversations extracted from raw movie scripts: 220,579 conversational exchanges between 10,292 pairs of movie characters, 617 movies (9.5 MB)
*   [Corporate messaging](http://aws.amazon.com/de/datasets/common-crawl-corpus/): A data categorization job concerning what corporations actually talk about on social media. Contributors were asked to classify statements as information (objective statements about the company or it’s activities), dialog (replies to users, etc.), or action (messages that ask for votes or ask users to click on links, etc.). (600 KB)
*   [Crosswikis](http://nlp.stanford.edu/data/crosswikis-data.tar.bz2/): English-phrase-to-associated-Wikipedia-article database. Paper. (11 GB) 
*   [DBpedia](http://aws.amazon.com/de/datasets/dbpedia-3-5-1/?tag=datasets%23keywords%23encyclopedic): a community effort to extract structured information from Wikipedia and to make this information available on the Web (17 GB)
*   [Death Row](http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html): last words of every inmate executed since 1984 online (HTML table)
*   [Del.icio.us](http://arvindn.livejournal.com/116137.html): 1.25 million bookmarks on delicious.com (170 MB)
*   [Disasters on social media](https://www.crowdflower.com/data-for-everyone/): 10,000 tweets with annotations whether the tweet referred to a disaster event (2 MB).
*   [Economic News Article Tone and Relevance](https://www.crowdflower.com/data-for-everyone/): News articles judged if relevant to the US economy and, if so, what the tone of the article was. Dates range from 1951 to 2014. (12 MB)
*   [Enron Email Data](http://aws.amazon.com/de/datasets/enron-email-data/): consists of 1,227,255 emails with 493,384 attachments covering 151 custodians (210 GB)
*   [Event Registry](http://eventregistry.org/): Free tool that gives real time access to news articles by 100.000 news publishers worldwide. [Has API](https://github.com/gregorleban/EventRegistry/). (query tool)
*   [Examiner.com - Spam Clickbait News Headlines [Kaggle]](https://www.kaggle.com/therohk/examine-the-examiner): 3 Million crowdsourced News headlines published by now defunct clickbait website The Examiner from 2010 to 2015. (200 MB)
*   [Federal Contracts from the Federal Procurement Data Center (USASpending.gov)](http://aws.amazon.com/de/datasets/federal-contracts-from-the-federal-procurement-data-center-usaspending-gov/): data dump of all federal contracts from the Federal Procurement Data Center found at USASpending.gov (180 GB)
*   [Flickr Personal Taxonomies](http://www.isi.edu/~lerman/downloads/flickr/flickr_taxonomies.html): Tree dataset of personal tags (40 MB)
*   [Freebase Data Dump](http://aws.amazon.com/de/datasets/freebase-data-dump/): data dump of all the current facts and assertions in Freebase (26 GB) 
*   [Freebase Simple Topic Dump](http://aws.amazon.com/de/datasets/freebase-simple-topic-dump/): data dump of the basic identifying facts about every topic in Freebase (5 GB)
*   [Freebase Quad Dump](http://aws.amazon.com/de/datasets/freebase-quad-dump/): data dump of all the current facts and assertions in Freebase (35 GB)
*   [GigaOM Wordpress Challenge [Kaggle]](https://www.kaggle.com/c/predict-wordpress-likes/data): blog posts, meta data, user likes (1.5 GB)
*   [Google Books Ngrams](http://storage.googleapis.com/books/ngrams/books/datasetsv2.html): available also in hadoop format on amazon s3 (2.2 TB)
*   [Google Web 5gram](https://catalog.ldc.upenn.edu/LDC2006T13): contains English word n-grams and their observed frequency counts (24 GB)
*   [Gutenberg Ebook List](http://www.gutenberg.org/wiki/Gutenberg:Offline_Catalogs): annotated list of ebooks (2 MB)
*   [Hansards text chunks of Canadian Parliament](http://www.isi.edu/natural-language/download/hansard/): 1.3 million pairs of aligned text chunks (sentences or smaller fragments) from the official records (Hansards) of the 36th Canadian Parliament. (82 MB)
*   [Harvard Library](http://library.harvard.edu/open-metadata#Harvard-Library-Bibliographic-Dataset): over 12 million bibliographic records for materials held by the Harvard Library, including books, journals, electronic resources, manuscripts, archival materials, scores, audio, video and other materials. (4 GB)
*   [Hate speech identification](https://github.com/t-davidson/hate-speech-and-offensive-language): Contributors viewed short text and identified if it a) contained hate speech, b) was offensive but without hate speech, or c) was not offensive at all. Contains nearly 15K rows with three contributor judgments per text string. (3 MB)
*   [Hillary Clinton Emails [Kaggle]](https://www.kaggle.com/kaggle/hillary-clinton-emails): nearly 7,000 pages of Clinton's heavily redacted emails (12 MB)
*   [Historical Newspapers Yearly N-grams and Entities Dataset](https://data.bris.ac.uk/data/dataset/dobuvuu00mh51q773bo8ybkdz): Yearly time series for the usage of the 1,000,000 most frequent 1-, 2-, and 3-grams from a subset of the British Newspaper Archive corpus, along with yearly time series for the 100,000 most frequent named entities linked to Wikipedia and a list of all articles and newspapers contained in the dataset (3.1 GB)
*   [Historical Newspapers Daily Word Time Series Dataset](https://datadryad.org/resource/doi:10.5061/dryad.nh775): Time series of daily word usage for the 25,000 most frequent words in 87 years of UK and US historical newspapers between 1836 and 1922. (2.7GB)
*   [Home Depot Product Search Relevance [Kaggle]](https://www.kaggle.com/c/home-depot-product-search-relevance/data): contains a number of products and real customer search terms from Home Depot's website. The challenge is to predict a relevance score for the provided combinations of search terms and products. To create the ground truth labels, Home Depot has crowdsourced the search/product pairs to multiple human raters. (65 MB)
*   [Identifying key phrases in text](https://www.crowdflower.com/data-for-everyone/): Question/Answer pairs + context; context was judged if relevant to question/answer. (8 MB)
*   [Jeopardy](http://www.reddit.com/r/datasets/comments/1uyd0t/200000_jeopardy_questions_in_a_json_file/): archive of 216,930 past Jeopardy questions (53 MB)
*   [200k English plaintext jokes](https://github.com/taivop/joke-dataset): archive of 208,000 plaintext jokes from various sources.
*   [Machine Translation of European Languages](http://statmt.org/wmt11/translation-task.html#download): (612 MB)
*   [Material Safety Datasheets](http://aws.amazon.com/de/datasets/material-safety-data-sheets/): 230,000 Material Safety Data Sheets. (3 GB)
*   [Million News Headlines - ABC Australia [Kaggle]](https://www.kaggle.com/therohk/million-headlines): 1.3 Million News headlines published by ABC News Australia from 2003 to 2017. (56 MB)
*   [Millions of News Article URLs](https://datadryad.org/resource/doi:10.5061/dryad.p8s0j): 2.3 million URLs for news articles from the frontpage of over 950 English-language news outlets in the six month period between October 2014 and April 2015. (101MB)
*   [MCTest](http://research.microsoft.com/en-us/um/redmond/projects/mctest/index.html): a freely available set of 660 stories and associated questions intended for research on the machine comprehension of text; for question answering (1 MB)
*   [News Headlines of India - Times of India [Kaggle]](https://www.kaggle.com/therohk/india-headlines-news-dataset): 2.7 Million News Headlines with category published by Times of India from 2001 to 2017. (185 MB)
*   [News article / Wikipedia page pairings](https://www.crowdflower.com/data-for-everyone/): Contributors read a short article and were asked which of two Wikipedia articles it matched most closely. (6 MB)
*   [NIPS2015 Papers (version 2) [Kaggle]](https://www.kaggle.com/benhamner/nips-2015-papers/version/2): full text of all NIPS2015 papers (335 MB)
*   [NYTimes Facebook Data](http://minimaxir.com/2015/07/facebook-scraper/): all the NYTimes facebook posts (5 MB)
*   [One Week of Global News Feeds [Kaggle]](https://www.kaggle.com/therohk/global-news-week): News Event Dataset of 1.4 Million Articles published globally in 20 languages over one week of August 2017. (115 MB)
*   [Objective truths of sentences/concept pairs](https://www.crowdflower.com/data-for-everyone/): Contributors read a sentence with two concepts. For example “a dog is a kind of animal” or “captain can have the same meaning as master.” They were then asked if the sentence could be true and ranked it on a 1-5 scale. (700 KB)
*   [Open Library Data Dumps](https://openlibrary.org/developers/dumps): dump of all revisions of all the records in Open Library. (16 GB)
*   [Personae Corpus](http://www.clips.uantwerpen.be/datasets/personae-corpus): collected for experiments in Authorship Attribution and Personality Prediction. It consists of 145 Dutch-language essays by 145 different students. (on request)
*   [Reddit Comments](https://www.reddit.com/r/datasets/comments/3bxlg7/i_have_every_publicly_available_reddit_comment/): every publicly available reddit comment as of july 2015. 1.7 billion comments (250 GB)
*   [Reddit Comments (May ‘15) [Kaggle]](https://www.kaggle.com/reddit/reddit-comments-may-2015): subset of above dataset (8 GB)
*   [Reddit Submission Corpus](https://www.reddit.com/r/datasets/comments/3mg812/full_reddit_submission_corpus_now_available_2006/): all publicly available Reddit submissions from January 2006 - August 31, 2015). (42 GB)
*   [Reuters Corpus](http://trec.nist.gov/data/reuters/reuters.html): a large collection of Reuters News stories for use in research and development of natural language processing, information retrieval, and machine learning systems. This corpus, known as "Reuters Corpus, Volume 1" or RCV1, is significantly larger than the older, well-known Reuters-21578 collection heavily used in the text classification community. Need to sign agreement and sent per post to obtain. (2.5 GB)
*   [SMS Spam Collection](http://www.dt.fee.unicamp.br/~tiago/smsspamcollection/): 5,574 English, real and non-enconded SMS messages, tagged according being legitimate (ham) or spam.  (200 KB) 
*   [SouthparkData](https://github.com/BobAdamsEE/SouthParkData): .csv files containing script information including: season, episode, character, & line. (3.6 MB)
* [Stanford Question Answering Dataset (SQUAD 2.0)](https://rajpurkar.github.io/SQuAD-explorer/): a reading comprehension dataset, consisting of questions posed by crowdworkers on a set of Wikipedia articles, where the answer to every question is a segment of text, or span, from the corresponding reading passage, or the question might be unanswerable.
*   [Stackoverflow](http://data.stackexchange.com/): 7.3 million stackoverflow questions + other stackexchanges (query tool)
*   [Twitter Cheng-Caverlee-Lee Scrape](https://archive.org/details/twitter_cikm_2010): Tweets from September 2009 - January 2010, geolocated. (400 MB)
*   [Twitter New England Patriots Deflategate sentiment](https://www.crowdflower.com/data-for-everyone/): Before the 2015 Super Bowl, there was a great deal of chatter around deflated footballs and whether the Patriots cheated. This data set looks at Twitter sentiment on important days during the scandal to gauge public sentiment about the whole ordeal. (2 MB)
*   [Twitter Progressive issues sentiment analysis](https://www.crowdflower.com/data-for-everyone/): tweets regarding a variety of left-leaning issues like legalization of abortion, feminism, Hillary Clinton, etc. classified if the tweets in question were for, against, or neutral on the issue (with an option for none of the above). (600 KB)
*   [Twitter Sentiment140](http://help.sentiment140.com/for-students/): Tweets related to brands/keywords. Website includes papers and research ideas. (77 MB)
*   [Twitter sentiment analysis: Self-driving cars](https://www.crowdflower.com/data-for-everyone/): contributors read tweets and classified them as very positive, slightly positive, neutral, slightly negative, or very negative. They were also prompted asked to mark if the tweet was not relevant to self-driving cars. (1 MB)
*   [Twitter Elections Integrity](https://about.twitter.com/en_us/values/elections-integrity.html#data): All suspicious tweets and media from 2016 US election. (1.4 GB)
*   [Twitter Tokyo Geolocated Tweets](http://followthehashtag.com/datasets/200000-tokyo-geolocated-tweets-free-twitter-dataset/): 200K tweets from Tokyo. (47 MB)
*   [Twitter UK Geolocated Tweets](http://followthehashtag.com/datasets/170000-uk-geolocated-tweets-free-twitter-dataset/): 170K tweets from UK. (47 MB)
*   [Twitter USA Geolocated Tweets](http://followthehashtag.com/datasets/free-twitter-dataset-usa-200000-free-usa-tweets/): 200k tweets from the US (45MB)
*   [Twitter US Airline Sentiment [Kaggle]](https://www.kaggle.com/crowdflower/twitter-airline-sentiment): A sentiment analysis job about the problems of each major U.S. airline. Twitter data was scraped from February of 2015 and contributors were asked to first classify positive, negative, and neutral tweets, followed by categorizing negative reasons (such as "late flight" or "rude service"). (2.5 MB)
*   [U.S. economic performance based on news articles](https://www.crowdflower.com/data-for-everyone/): News articles headlines and excerpts ranked as whether relevant to U.S. economy. (5 MB)
*   [Urban Dictionary Words and Definitions [Kaggle]](https://www.kaggle.com/therohk/urban-dictionary-words-dataset): Cleaned CSV corpus of 2.6 Million of all Urban Dictionary words, definitions, authors, votes as of May 2016. (238 MB)
*   [Wesbury Lab Usenet Corpus](http://aws.amazon.com/de/datasets/the-westburylab-usenet-corpus/): anonymized compilation of postings from 47,860 English-language newsgroups from 2005-2010 (40 GB)
*   [Wesbury Lab Wikipedia Corpus](http://www.psych.ualberta.ca/~westburylab/downloads/westburylab.wikicorp.download.html) Snapshot of all the articles in the English part of the Wikipedia that was taken in April 2010. It was processed, as described in detail below, to remove all links and irrelevant material (navigation text, etc) The corpus is untagged, raw text. Used by [Stanford NLP](https://scholar.google.com/scholar?oi=bibs&hl=en&cites=9060444488071171966&as_sdt=5) (1.8 GB).
*   [WorldTree Corpus of Explanation Graphs for Elementary Science Questions](http://cognitiveai.org/explanationbank/): a corpus of manually-constructed explanation graphs, explanatory role ratings, and associated semistructured tablestore for most publicly available elementary science exam questions in the US (8 MB)
*   [Wikipedia Extraction (WEX)](http://aws.amazon.com/de/datasets/wikipedia-extraction-wex/): a processed dump of english language wikipedia (66 GB)
*   [Wikipedia XML Data](http://aws.amazon.com/de/datasets/wikipedia-xml-data/): complete copy of all Wikimedia wikis, in the form of wikitext source and metadata embedded in XML. (500 GB)
*   [Yahoo! Answers Comprehensive Questions and Answers](http://webscope.sandbox.yahoo.com/catalog.php?datatype=l): Yahoo! Answers corpus as of 10/25/2007. Contains 4,483,032 questions and their answers. (3.6 GB)
*   [Yahoo! Answers consisting of questions asked in French](http://webscope.sandbox.yahoo.com/catalog.php?datatype=l): Subset of the Yahoo! Answers corpus from 2006 to 2015 consisting of 1.7 million questions posed in French, and their corresponding answers. (3.8 GB)
*   [Yahoo! Answers Manner Questions](http://webscope.sandbox.yahoo.com/catalog.php?datatype=l): subset of the Yahoo! Answers corpus from a 10/25/2007 dump, selected for their linguistic properties. Contains 142,627 questions and their answers. (104 MB)
*   [Yahoo! HTML Forms Extracted from Publicly Available Webpages](http://webscope.sandbox.yahoo.com/catalog.php?datatype=l): contains a small sample of pages that contain complex HTML forms, contains 2.67 million complex forms. (50+ GB)
*   [Yahoo! Metadata Extracted from Publicly Available Web Pages](http://webscope.sandbox.yahoo.com/catalog.php?datatype=l): 100 million triples of RDF data (2 GB)
*   [Yahoo N-Gram Representations](http://webscope.sandbox.yahoo.com/catalog.php?datatype=l): This dataset contains n-gram representations. The data may serve as a testbed for query rewriting task, a common problem in IR research as well as to word and sentence similarity task, which is common in NLP research. (2.6 GB)
*   [Yahoo! N-Grams, version 2.0](http://webscope.sandbox.yahoo.com/catalog.php?datatype=l): n-grams (n = 1 to 5), extracted from a corpus of 14.6 million documents (126 million unique sentences, 3.4 billion running words) crawled from over 12000 news-oriented sites (12 GB)
*   [Yahoo! Search Logs with Relevance Judgments](http://webscope.sandbox.yahoo.com/catalog.php?datatype=l): Annonymized Yahoo! Search Logs with Relevance Judgments (1.3 GB)
*   [Yahoo! Semantically Annotated Snapshot of the English Wikipedia](http://webscope.sandbox.yahoo.com/catalog.php?datatype=l): English Wikipedia dated from 2006-11-04 processed with a number of publicly-available NLP tools. 1,490,688 entries. (6 GB)
*   [Yelp](https://www.yelp.com/academic_dataset): including restaurant rankings and 2.2M reviews (on request)
*   [Youtube](https://www.reddit.com/r/datasets/comments/3gegdz/17_millions_youtube_videos_description/): 1.7 million youtube videos descriptions (torrent)

### Arabic datasets
*   [SaudiNewsNet](https://github.com/ParallelMazen/SaudiNewsNet): 31,030 Arabic newspaper articles alongwith metadata, extracted from various online Saudi newspapers. (2 MB)

### German datasets 
*   [German Political Speeches Corpus](http://purl.org/corpus/german-speeches): collection of recent speeches held by top German representatives (25 MB, 11 MTokens)
*   [NEGRA](http://www.coli.uni-saarland.de/projects/sfb378/negra-corpus/negra-corpus.html): A Syntactically Annotated Corpus of German Newspaper Texts. Available for free for all Universities and non-profit organizations. Need to sign and send form to obtain. (on request)
*   [Ten Thousand German News Articles Dataset](https://tblock.github.io/10kGNAD/): 10273 german language news articles categorized into nine classes for topic classification. (26.1 MB)

### Other datasets
*   [Awesome public datasets/NLP](https://github.com/caesar0301/awesome-public-datasets#natural-language) (includes more lists)
*   [AWS Public Datasets](http://aws.amazon.com/de/datasets/)
*   [CrowdFlower: Data for Everyone](https://www.crowdflower.com/data-for-everyone/) (lots of little surveys they conducted and data obtained by crowdsourcing for a specific task)
*   [Kaggle 1](https://www.kaggle.com/datasets), [2](https://www.kaggle.com/competitions) (make sure though that the kaggle competition data can be used outside of the competition!)
*   [Open Library](https://openlibrary.org/developers/dumps)
*   [Quora](https://www.quora.com/Datasets-What-are-the-major-text-corpora-used-by-computational-linguists-and-natural-language-processing-researchers-and-what-are-the-characteristics-biases-of-each-corpus) (mainly annotated corpora)
*   [/r/datasets](https://www.reddit.com/r/datasets) (endless list of datasets, most is scraped by amateurs though and not properly documented or licensed)
*   [rs.io](http://rs.io/100-interesting-data-sets-for-statistics/) (another big list)
*   [Stackexchange: Opendata](http://opendata.stackexchange.com/)
*   [Stanford NLP group](http://www-nlp.stanford.edu/links/statnlp.html) (mainly annotated corpora and TreeBanks or actual NLP tools)
*   [Yahoo! Webscope](http://webscope.sandbox.yahoo.com/) (also includes papers that use the data that is provided)


## Image datasets

Standard image datasets, alphabetized. 
* [MNIST](http://yann.lecun.com/exdb/mnist/) - standard dataset used for image classification / regression. 

### Common image datasets 
* [MNIST](http://yann.lecun.com/exdb/mnist/) - hand-written image dataset, standard to measure accuracy from Yan Lecun @ NYU.
* [MS-COCO](http://cocodataset.org/#download) - COCO is a large-scale object detection, segmentation, and captioning dataset. 330K images (>200K labeled), 1.5 million object instances, 80 object categories, 91 stuff categories, 5 captions per image, 250,000 people with keypoints.
* [ImageNet](http://www.image-net.org/) - ImageNet is an image database organized according to the WordNet hierarchy (currently only the nouns), in which each node of the hierarchy is depicted by hundreds and thousands of images. 
* [Open Images Dataset](https://storage.googleapis.com/openimages/web/index.html) - 15,851,536 boxes on 600 categories, 2,785,498 instance segmentations on 350 categories, 36,464,560 image-level labels on 19,959 categories, 391,073 relationship annotations of 329 relationships, Extension - 478,000 crowdsourced images with 6,000+ categories.
* [VisualQA](https://visualqa.org/) - VQA is a new dataset containing open-ended questions about images. These questions require an understanding of vision, language and commonsense knowledge to answer. 265,016 images (COCO and abstract scenes)
At least 3 questions (5.4 questions on average) per image, 10 ground truth answers per question, 3 plausible (but likely incorrect) answers per question, Automatic evaluation metric.
* [The Street View House Numbers (SVHN)](http://ufldl.stanford.edu/housenumbers/) - 10 classes, 1 for each digit. Digit '1' has label 1, '9' has label 9 and '0' has label 10. 73257 digits for training, 26032 digits for testing, and 531131 additional, somewhat less difficult samples, to use as extra training data.
* [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) - The CIFAR-10 dataset consists of 60000 32x32 colour images in 10 classes, with 6000 images per class. There are 50000 training images and 10000 test images. 

## Video datasets

Standard video datasets, alphabetized. 
* [MNIST](http://yann.lecun.com/exdb/mnist/) - standard dataset used for video classification / regression. 

### Common video datasets 
* [20BN-JESTER](https://www.twentybn.com/datasets/jester) - Human Hand Gestures Dataset. 148000 videos	27 classes	pre-defined classes.
* [20BN-SOMETHING-SOMETHING](https://www.twentybn.com/datasets/something-something) - The 20BN-SOMETHING-SOMETHING dataset is a large collection of densly-labeled video clips that show humans performing predefined basic actions with every day objects. 108000 videos, 174 classes	pre-defined classes.
* [ActivityNet](http://activity-net.org/) - A Large-Scale Video Benchmark for Human Activity Understanding. 28000 videos,	203 classes	pre-defined classes.
* [ActivityNet Captions](http://cs.stanford.edu/people/ranjaykrishna/densevid/) - a large-scale benchmark for dense-captioning events.	20000	videos, 100k Aligned captions	text.
* [ASLAN](http://www.openu.ac.il/home/hassner/data/ASLAN/ASLAN.html) - ASLAN. The Action Similarity Labeling dataset. 1571	videos, 432 action classes, 3697 action samples	pre-defined classes
* [AVA](https://research.google.com/ava/) - A Video Dataset of Spatio-temporally Localized Atomic Visual Actions. 57600 videos, 210k action labels, 80 atomic visual actions, spatio-temporal annotations	pre-defined classes, text, spatio-temporal annotation.
* [Charades](http://allenai.org/plato/charades/) - This dataset guides our research into unstructured video activity recognition and commonsense reasoning for daily human activities. 9848	 videos, 157 action labels, 27847 Free-text descriptions, action intervals, classes of interacted objects	pre-defined classes, text, intervals.
* [DALY](http://thoth.inrialpes.fr/daly/) - Daily Action Localization in Youtube videos. 8100 videos, 3.6k spatio-temporal action annotation	pre-defined classes, spatio-temporal annotation
* [DAVIS](http://davischallenge.org/) - Densely Annotated VIdeo Segmentation. 50	videos 3455 annotated frames	Segmentation mask.
* [DiDeMo dataset](https://people.eecs.berkeley.edu/~lisa_anne/didemo.html) - the Distinct Describable Moments (DiDeMo) dataset consists of over 10,000 unedited, personal videos in diverse visual settings with pairs of localized video segments and referring expressions. 10000 videos,	40000 aligned captions	captions
* [Kinetics](https://deepmind.com/research/open-source/open-source-datasets/kinetics/) - Kinetics is a large-scale, high-quality dataset of YouTube video URLs which include a diverse range of human focused actions. 500000	videos, 600 action classes	pre-defined classes.
* [HMDB51](http://serre-lab.clps.brown.edu/resource/hmdb-a-large-human-motion-database/) - HMDB: A Large Video Database for Human Motion Recognition - Action recognition	6766 videos,	51 action classes	pre-defined classes.
* [Hollywood2](http://www.di.ens.fr/~laptev/actions/hollywood2/) - Human actions and scenes dataset. 3669 videos, 12 human action classes, 10 classes of scene	pre-defined classes
* [Instruction Video Dataset](http://www.di.ens.fr/willow/research/instructionvideos/) - A new challenging dataset of real-world instruction videos from the Internet. 150	videos, 5 different instructional tasks with subtitles	pre-defined classes, captions
* [Lip reading dataset](http://www.robots.ox.ac.uk/~vgg/data/lip_reading/) - LRW, LRS2 and LRS3 are audio-visual speech recognition datasets collected from in the wild videos. 6M+ word instances, 800+ hours, 5,000+ identities
* [LSMDC](http://www.mpi-inf.mpg.de/departments/computer-vision-and-multimodal-computing/research/vision-and-language/mpii-movie-description-dataset/) - Large-Scale Movie Understanding Dataset. 118000 videos, Aligned captions	text.
* [Moments in Time](http://moments.csail.mit.edu/) - Moments in Time Dataset: one million videos for event understanding. 1000000	videos, 339 action classes	pre-defined classes
* [MovieQA](http://movieqa.cs.toronto.edu/home/) - Movie Understanding	140	15k Question-Answer, 408 movie plots, 408 subtitles	Question-Answer, text.
* [MPII-Cooking](https://www.mpi-inf.mpg.de/departments/computer-vision-and-multimodal-computing/research/human-activity-recognition/mpii-cooking-2-dataset/) - MPII Cooking dataset. 273	videos, 78 classes, 13k labelled instances	pre-defined classes, text.
* [MSR-VTT](https://www.microsoft.com/en-us/research/publication/msr-vtt-a-large-video-description-dataset-for-bridging-video-and-language/) - A Large Video Description Dataset for Bridging Video and Language. 10000	videos, 200000 aligned captions	captions.
* [SLAC](http://slac.csail.mit.edu/) - A Sparsely Labeled ACtions Dataset. 520000	videos, 200 action classes, 1.75M clip annotations	pre-defined classes.
* [Sports-1M](http://cs.stanford.edu/people/karpathy/deepvideo/) - The YouTube Sports-1M Dataset. 1100000	videos, 487 sports classes pre-defined classes.
* [TGIF](http://raingo.github.io/TGIF-Release/) - TUMBLR GIF captioning	125781	videos, 125781 captions	
* [UCF101](https://www.crcv.ucf.edu/data/UCF101.php) - UCF101: A Dataset of 101 Human Actions Classes From Videos in The Wild. 	13320	videos, 101 action classes	pre-defined classes
* [VGG Human Pose](https://www.robots.ox.ac.uk/~vgg/data/pose/index.html) - The VGG Human Pose Estimation datasets is a set of large video datasets annotated with human upper-body pose. 152	videos Hours of human upper-body pose	human pose.
* [VideoMCC](http://videomcc.org/) - 272000	videos, 10 topics and Video captions	Question-Answer, text.
* [VLOG](https://people.eecs.berkeley.edu/~dfouhey/2017/VLOG/index.html) - VLOG From Lifestyle VLOGs to Everyday Interactions: The VLOG Dataset. 114000 videos	pre-defined classes.
* [YFCC100M](http://yfcc100m.appspot.com/?) - YFCC100M: The New Data in Multimedia Research. 800000	videos, 1570 tags, captions and diverse metadata	Captions, pre-defined classes.
* [YouTube 8M](https://research.google.com/youtube8m/download.html) - YouTube-8M is a large-scale labeled video dataset that consists of millions of YouTube video IDs and associated labels from a diverse vocabulary of 4700+ visual entities. 8000000 videos,	4716 classes	pre-defined classes.
* [Youtube BoundingBoxes](https://research.google.com/youtube-bb/) - YouTube-BoundingBoxes Dataset. 240000 videos 5.6M Bouding boxes, 23 objects	Bounding boxes.

## CSV datasets 
* see [PyDataset](https://github.com/iamaziz/PyDataset)

## References
* [Audio datasets](https://towardsdatascience.com/a-data-lakes-worth-of-audio-datasets-b45b88cd4ad) 
* [Bokeh](https://bokeh.pydata.org/en/latest/) 
* [Common Voice](https://voice.mozilla.org/) 
* [Datasets-natural-language-processing](https://machinelearningmastery.com/datasets-natural-language-processing/) 
* [Download AudioSet](https://github.com/jim-schwoebel/download_audioset) 
* [Google Dataset Search](https://toolbox.google.com/datasetsearch)
* [Kaggle](https://kaggle.com)
* [Matplotlib](https://matplotlib.org/) 
* [NP Datasets](https://github.com/niderhoff/nlp-datasets)
* [PyDataset](https://github.com/iamaziz/PyDataset)
* [Video datasets](https://www.di.ens.fr/~miech/datasetviz/)
* [Voicebook repository](https://github.com/jim-schwoebel/voicebook)
* [Yellowbrick](https://www.scikit-yb.org/en/latest/)

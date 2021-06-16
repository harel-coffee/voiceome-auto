# Voiceome
The [Voiceome Study](https://www.voiceome.org/) is the world’s largest clinical study to collect voice information labeled with health traits. The goal is to recruit between 10,000-100,000 patients into the study and track them at multiple time points to advance scientific understanding for vocal biomarkers and speed up the process for its commercialization.

[![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/voiceome.png?raw=true)](https://www.youtube.com/watch?v=lCk_mffvJ0A&feature=emb_logo)

More information about the Voiceome study can be found @ [the wiki](https://github.com/jim-schwoebel/voiceome/wiki) and [website](https://voiceome.org).

## Background/goals
One of the primary causes of slow translation of voice biomarker research is a result of small datasets. There have been many research studies that have shown that acoustic or linguistic voice features relate to health conditions like stress, schizophrenia, depression, bipolar disorder, stroke, and cardiovascular diseases. However, many of these studies have relatively small sample sizes (N<1,000 patients in each class), suffer from poor audio quality (e.g. use of different microphones and data collection techniques), and are difficult to access (e.g. large licensing fees to corporations and/or difficulty obtaining IRB access without close academic ties). These factors dramatically limit the ability to model the underlying data and correlate voice data to health traits, replicate peer-reviewed publications, as well as open up this work to the broader scientific community.

![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/confounds.png?raw=true)

Therefore, the main goals of the Voiceome Study include:

- **Standardizing collection tools and features** - Standardize the tools and techniques used to collect and featurize voice samples for use in health-related research. <em> We have done this by building [SurveyLex](https://surveylex.com), a web-enabled survey tool for vocal biomarker research.</em>
- **Establishing reference ranges** - Create a standard set of normative ranges of [acoustic](https://github.com/jim-schwoebel/voiceome/tree/main/assets/references/A/acoustics) and [linguistic](https://github.com/jim-schwoebel/voiceome/tree/main/assets/references/A/linguistics) features across various ages, genders, microphone types, and dialects labeled with health information. <em>These are provided as [tables](https://github.com/jim-schwoebel/voiceome/tree/main/assets/references/A/acoustics) and standardized scripts with the [command line interface](https://github.com/jim-schwoebel/voiceome/blob/main/cli.py) in this repository</em>.
- **Standardizing voice protocols** - Standardize the series of voice tasks used to collect speech samples for use in the voiceome. <em>These voice protocols can be found in the [wiki](https://github.com/jim-schwoebel/voiceome/wiki), and includes novel tasks like automated confrontational naming tasks and nonword tasks.</em>
- **Standardizing health trait labels** - Standardize the type of health trait labels tied to voice information to emit the most signal from the voice. <em>These are provided [here](https://github.com/jim-schwoebel/voiceome/wiki/16.-Health-labels#lichert-questions-custom-made).</em>
- **Creating machine learning models** - From Voiceome Study dataset, build and optimize novel machine learning models; to publish this work in academic journals openly. <em>These models will be published on in follow-on publications into the future.</em>
- **Creating an ethics framework** - Create a venue for legal, ethical, and security considerations for collecting voice data for health-related purposes. <em>This can be read in the [Voiceome strategic plan](https://drive.google.com/file/d/1Dme9tUq0eCepja_7Yg9sNqn_JWKaJxJm/view).</em>
- **Build a lasting community** - The Voiceome project will foster a lasting community and enthusiasm for the field of vocal biomarkers in general. <em>We do this through writing textbooks like [Voice Computing in Python](https://neurolex.ai/voicebook), collaborating with research organizations like the University of Washington and Biogen, and through training fellows through the [Innovation Fellows Program](http://neurolex.ai/research).</em>

## Clinical trial design
Anyone >18 years of age that could speak English was eligible to participate in the Voiceome Study (>6,000 participants completed the first survey). Each participant was randomly assigned one of three tracks (AAAA, ABAB, ABCD, or ACBD) and could participate in follow-on surveys separated by roughly three weeks in these tracks. Subjects were primarily recruited on Amazon Mechanical Turk with a paid incentive ($5-20/session), and anyone who completed 4 surveys was eligible to receive a health report.

| Overvew    |    Locations   |   
| ----------- | ----------- | 
|  ![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/overview.png) | ![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/locations.png) |

## Getting started
This assumes you are using a MacOS-related computer.

### MacOS
To get started, clone this repository in a virtual environment and install requirements.txt (note this can take 10 minutes):
```
git clone git@github.com:jim-schwoebel/voiceome.git
cd voiceome
pip3 install virtualenv
virtualenv env 
source env/bin/activate
pip3 install -r requirements.txt
```

Now install various libraries with Homebrew (if you don't have Homebrew, install it before this step [following these instructions](https://brew.sh/)):
```
brew install ffmpeg sox autoconf automake m4 libtool autoconf gcc portaudio lasound
```

Next, install OpenSMILE:
```
cd scripts/features/helpers/opensmile/opensmile-2.3.0
bash autogen.sh
bash autogen.sh
./configure
make -j4 ; make
make install
```

Optionally, if you want to transcribe data with Microsoft Azure (this was the transcriber used in the Voiceome paper), update the ['settings.json'](https://github.com/jim-schwoebel/voiceome/blob/main/settings.json) Azure Key:
```
{"AzureKey": "KEY_GOES_HERE",...}
```

You can now use the convenient Voiceome CLI tool for [a few things](https://github.com/jim-schwoebel/voiceome#using-the-cli):
```
Usage: cli.py [options]

Options:
  -h, --help            show this help message and exit
  --c=command, --command=command
                        the target command (cleaning API = 'clean',  features
                        API = 'features',  quality API = 'quality',
                        references API = 'reference',  samples API = 'sample',
                        testing API = 'test',  urls API = 'urls',  visualize
                        API = 'visualize',  list/change default settings =
                        'settings')
  --a=age_gender, --agegender=age_gender
                        specify the age and gender in CamelCase for references
                        ('TwentiesMale' =  male aged 20s); if not used will
                        default to settings.json value.
  --d=dir, --dir=dir    an array of the target directory (or directories) that
                        contains sample files all APIs (e.g.
                        '/Users/jim/desktop/allie/train_dir/teens/')
  --e=feature_embedding, --embedding=feature_embedding
                        the feature embedding to use for reference ranges
                        (e.g. 'OpenSmile'); if not used it will default to
                        settings.json value.
  --f=feature, --feature=feature
                        the feature value in a feature embedding to use for a
                        reference range (e.g.
                        'F0semitoneFrom27.5Hz_sma3nz_amean'); if not used it
                        will default to settings.json value.
  --fi=file, --file=file
                        an audio file to extract relevant quality metrics and
                        transcribe (e.g. 'test.wav')
  --t=task, --task=task
                        the task type to focus on (e.g. 'microphone_task'); if
                        not used it will default to settings.json value.
  --v=visualizationtype, --vtype=visualizationtype
                        the visualization type that you'd like to use - two
                        options: ['bar', 'bar_cohorts']
  --verbosity=verbosity
                        whether or not to display visualizations/charts on the
                        screen ([True or False]).
  --u=urls, --urls=urls
                        the url links for surveys in the Voiceome Study
                        (useful for cloning surveys via the SurveyLex
                        interface).
```

## Using the CLI 

There are many things you can do with the Voiceome CLI. Primarily, you can use it to extract feautures and references, as well as make cool visualizations to do quick experiments from the means and standard deviations of the features. A full list of things is below:
* [cleaning data]()
* [featurizing data]()
* [extracting quality metrics]()
* [querying reference ranges]()
* [visualizing data cohorts]()
* [changing settings]()
* [get survey URLs]()
* [running unit tests]()

If you have any thing else you'd find valuable - feel free to [suggest some new features here!](https://github.com/jim-schwoebel/voiceome/issues/new)

### cleaning data
You can clean data with the CLI by specifying the command and directory of interest. This will clean files to mono 16000 Hz:
```
python3 cli.py --command clean --dir /Users/jimschwoebel/desktop/files
```
### featurizing data
You can also featurize a folder of files with OpenSmileFeatures, ProsodyFeatures, PauseFeatures, and AudioText features with:
```
python3 cli.py --command features --dir /Users/jimschwoebel/desktop/files
```
### extracting quality metrics 
You can featurize an audio file and get back quality metrics with:
```
python3 cli.py --command quality --file test.wav
```
### querying references 
You can get a reference feature with a specified age and gender (e.g. TwentiesMale) with:
```
python3 cli.py --command reference --vtype table_by_feature --agegender TwentiesMale
```
You can get a reference table for a speech task (e.g. microphone task) and feature embedding (e.g. OpensmileFeatures) with:
```
python3 cli.py --command reference --vtype table_by_embedding --agegender TwentiesMale
```
You can get a reference table across sample tasks while keeping a feature constant with:
```
python3 cli.py --command reference --vtype table_across_tasks --agegender TwentiesMale
```
### visualizing data
Visualize the means and standard deviations for a feature with a bar chart:
```
python3 cli.py --command visualize --agegender FourtiesMale] 
```
Visualize multiple features and references next to each other in a bar chart:
```
python3 cli.py --command visualize --agegender FourtiesMale] --vtype bar_cohorts --agegender ThirtiesMale --agegender FiftiesMale
```

### changing settings
You can change settings.json file with the API with:

```
python3 cli.py --command settings 
```

[Settings.json](https://github.com/jim-schwoebel/voiceome/blob/main/settings.json) specifies various settings for the API. The configuration options are listed in the table below. Note all possible options are listed out in the [options folder](https://github.com/jim-schwoebel/voiceome/tree/main/data/options) as .JSON files.

| Setting     |    Default option   |  All Options | Description |
| ----------- | ----------- | ----------- | ----------- |
| 'AzureKey' | 'TEST' | Any string related to the Azure string | Azure key for API usage in transcription. | 
| 'Features' | 'opensmile_features' | ['opensmile_features', 'prosody_features' 'pause_features', 'audiotext_features'] | The default feature embedding to use to calculate features/references. |
| 'FeatureType' | 'F0semitoneFrom27.5Hz_sma3nz_amean' |  ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'space', 'numbers', 'capletters', 'cc', 'cd', 'dt', 'ex', 'in', 'jj', 'jjr', 'jjs', 'ls', 'md', 'nn', 'nnp', 'nns', 'pdt', 'pos', 'prp', 'prp2', 'rbr', 'rbs', 'rp', 'to', 'uh', 'vb', 'vbd', 'vbg', 'vbn', 'vbp', 'vbz', 'wdt', 'wp', 'wrb', 'polarity', 'subjectivity', 'repeat', 'uniquewords', 'n_sents', 'n_words', 'n_chars', 'n_syllables', 'n_unique_words', 'n_long_words', 'n_monosyllable_words', 'n_polysyllable_words', 'flesch_kincaid_grade_level', 'flesch_reading_ease', 'smog_index', 'gunning_fog_index', 'coleman_liau_index', 'automated_readability_index', 'lix', 'gulpease_index', 'wiener_sachtextformel', 'PROPN', 'ADP', 'DET', 'NUM', 'PUNCT', 'SPACE', 'VERB', 'NOUN', 'ADV', 'CCONJ', 'PRON', 'ADJ', 'SYM', 'PART', 'INTJ', 'X', 'pos_other', 'NNP', 'IN', 'DT', 'CD', 'NNPS', ',', '_SP', 'VBZ', 'NN', 'RB', 'CC', '', 'NNS', '.', 'PRP', 'MD', 'VB', 'HYPH', 'VBD', 'JJ', ':', '-LRB-', '$', '-RRB-', 'VBG', 'VBN', 'NFP', 'RBR', 'POS', 'VBP', 'RP', 'JJS', 'PRP$', 'EX', 'JJR', 'WP', 'WDT', 'TO', 'WRB', 'PDT', 'AFX', 'RBS', 'UH', 'WP$', 'FW', 'XX', 'LS', 'ADD', 'tag_other', 'compound', 'ROOT', 'prep', 'det', 'pobj', 'nummod', 'punct', 'nsubj', 'advmod', 'conj', 'aux', 'dobj', 'nmod', 'acl', 'appos', 'npadvmod', 'amod', 'agent', 'case', 'intj', 'prt', 'pcomp', 'ccomp', 'attr', 'dep', 'acomp', 'poss', 'auxpass', 'expl', 'mark', 'nsubjpass', 'quantmod', 'advcl', 'relcl', 'oprd', 'neg', 'xcomp', 'csubj', 'predet', 'parataxis', 'dative', 'preconj', 'csubjpass', 'meta', 'dep_other', 'shape_other', 'mean sentence polarity', 'std sentence polarity', 'max sentence polarity', 'min sentence polarity', 'median sentence polarity', 'mean sentence subjectivity', 'std sentence subjectivity', 'max sentence subjectivity', 'min sentence subjectivity', 'median sentence subjectivity', 'character count', 'word count', 'sentence number', 'words per sentence', 'unique chunk noun text', 'unique chunk root text', 'unique chunk root head text', 'chunkdep ROOT', 'chunkdep pobj', 'chunkdep nsubj', 'chunkdep dobj', 'chunkdep conj', 'chunkdep appos', 'chunkdep attr', 'chunkdep nsubjpass', 'chunkdep dative', 'chunkdep pcomp', 'number of named entities', 'PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL', 'filler ratio', 'type token ratio', 'standardized word entropy', 'question ratio', 'number ratio', 'Brunets Index', 'Honores statistic', 'datewords freq', 'word number', 'five word count', 'max word length', 'min word length', 'variance of vocabulary', 'std of vocabulary', 'sentencenum', 'periods', 'questions', 'interjections', 'repeatavg', 'filler_ratio', 'type_token_ratio', 'standardized_word_entropy', 'question_ratio', 'number_ratio', 'brunets_index', 'honores_statistic', 'pronoun_to_noun_ratio', 'F0semitoneFrom27.5Hz_sma3nz_amean', 'F0semitoneFrom27.5Hz_sma3nz_stddevNorm', 'F0semitoneFrom27.5Hz_sma3nz_percentile20.0', 'F0semitoneFrom27.5Hz_sma3nz_percentile50.0', 'F0semitoneFrom27.5Hz_sma3nz_percentile80.0', 'F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2', 'F0semitoneFrom27.5Hz_sma3nz_meanRisingSlope', 'F0semitoneFrom27.5Hz_sma3nz_stddevRisingSlope', 'F0semitoneFrom27.5Hz_sma3nz_meanFallingSlope', 'F0semitoneFrom27.5Hz_sma3nz_stddevFallingSlope', 'loudness_sma3_amean', 'loudness_sma3_stddevNorm', 'loudness_sma3_percentile20.0', 'loudness_sma3_percentile50.0', 'loudness_sma3_percentile80.0', 'loudness_sma3_pctlrange0-2', 'loudness_sma3_meanRisingSlope', 'loudness_sma3_stddevRisingSlope', 'loudness_sma3_meanFallingSlope', 'loudness_sma3_stddevFallingSlope', 'jitterLocal_sma3nz_amean', 'jitterLocal_sma3nz_stddevNorm', 'shimmerLocaldB_sma3nz_amean', 'shimmerLocaldB_sma3nz_stddevNorm', 'HNRdBACF_sma3nz_amean', 'HNRdBACF_sma3nz_stddevNorm', 'logRelF0-H1-H2_sma3nz_amean', 'logRelF0-H1-H2_sma3nz_stddevNorm', 'logRelF0-H1-A3_sma3nz_amean', 'logRelF0-H1-A3_sma3nz_stddevNorm', 'F1frequency_sma3nz_amean', 'F1frequency_sma3nz_stddevNorm', 'F1bandwidth_sma3nz_amean', 'F1bandwidth_sma3nz_stddevNorm', 'F1amplitudeLogRelF0_sma3nz_amean', 'F1amplitudeLogRelF0_sma3nz_stddevNorm', 'F2frequency_sma3nz_amean', 'F2frequency_sma3nz_stddevNorm', 'F2amplitudeLogRelF0_sma3nz_amean', 'F2amplitudeLogRelF0_sma3nz_stddevNorm', 'F3frequency_sma3nz_amean', 'F3frequency_sma3nz_stddevNorm', 'F3amplitudeLogRelF0_sma3nz_amean', 'F3amplitudeLogRelF0_sma3nz_stddevNorm', 'alphaRatioV_sma3nz_amean', 'alphaRatioV_sma3nz_stddevNorm', 'hammarbergIndexV_sma3nz_amean', 'hammarbergIndexV_sma3nz_stddevNorm', 'slopeV0-500_sma3nz_amean', 'slopeV0-500_sma3nz_stddevNorm', 'slopeV500-1500_sma3nz_amean', 'slopeV500-1500_sma3nz_stddevNorm', 'alphaRatioUV_sma3nz_amean', 'hammarbergIndexUV_sma3nz_amean', 'slopeUV0-500_sma3nz_amean', 'slopeUV500-1500_sma3nz_amean', 'loudnessPeaksPerSec', 'VoicedSegmentsPerSec', 'MeanVoicedSegmentLengthSec', 'StddevVoicedSegmentLengthSec', 'MeanUnvoicedSegmentLength', 'StddevUnvoicedSegmentLength', 'Speech_Time_VADInt_1', 'Total_Time_VADInt_1', 'Pause_Time_VADInt_1', 'Pause_Percentage_VADInt_1', 'Pause_Speech_Ratio_VADInt_1', 'Mean_Pause_Length_VADInt_1', 'Pause_Variability_VADInt_1', 'Speech_Time_VADInt_2', 'Total_Time_VADInt_2', 'Pause_Time_VADInt_2', 'Pause_Percentage_VADInt_2', 'Pause_Speech_Ratio_VADInt_2', 'Mean_Pause_Length_VADInt_2', 'Pause_Variability_VADInt_2', 'Speech_Time_VADInt_3', 'Total_Time_VADInt_3', 'Pause_Time_VADInt_3', 'Pause_Percentage_VADInt_3', 'Pause_Speech_Ratio_VADInt_3', 'Mean_Pause_Length_VADInt_3', 'Pause_Variability_VADInt_3', 'UtteranceNumber', 'PauseNumber', 'AveragePauseLength', 'StdPauseLength', 'TimeToFirstPhonation', 'TimeToLastPhonation', 'UtterancePerMin', 'WordsPerMin', 'Duration'] | The default feature label for sorting data. |
| 'Task' | 'microphone_task' | ['microphone_task', 'freespeech_task', 'picture_task', 'category_task', 'letterf_task', 'paragraph_task', 'ahh_task', 'papapa_task', 'pataka_task', 'confrontational_task', 'nonword_task', 'recall_mandog_task', 'recall_tourbus_task', 'diagnosis_task', 'medication_task'] | The default task to customize API usage. | 
| 'TranscriptEngine' | "azure" | ["azure", "deepspeech_dict", "deepspeech_nodict", "wav2vec"] | The default transcription engine to use for audiotext_features. | 
| 'CleanAudio' | True | [True, False] | Whether or not you should clean audio files during featurization to mono16000Hz. | 
| 'DefaultAgeGender' | 'all' | ['TwentiesMale', 'TwentiesFemale', 'ThirtiesMale', 'ThirtiesFemale', 'FourtiesMale]', 'FourtiesFemale', 'FiftiesMale', 'FiftiesFemale', 'SixtiesMale', 'SixtiesFemale', 'AllAgesGenders'] | The default age and gender to use for reference ranges. | 

### get survey urls 

You can get the survey urls with:
```
python3 cli.py --command urls
```

This is useful for cloning surveys on the SurveyLex interface.

### running unit tests
You can run unit tests with:
```
python3 cli.py --command test 
```

## surveys 
Here are the 4 main surveys used in the Voiceome clinical study:

| Survey     |    Link    |   Number of completions |
| ----------- | ----------- | ----------- |
| Survey A      | [https://app.surveylex.com/surveys/8a32cbb0-cc8a-11eb-9ea3-938cc8b6d71e](https://app.surveylex.com/surveys/8a32cbb0-cc8a-11eb-9ea3-938cc8b6d71e), but for new studies recommend a slightly altered survey [here](https://app.surveylex.com/surveys/2f5b97d0-cc94-11eb-8595-0ba9699e9d53).      | 6,426     |
| Survey B  | [https://app.surveylex.com/surveys/061da3f0-a637-11eb-bcc9-eba67643f616](https://app.surveylex.com/surveys/061da3f0-a637-11eb-bcc9-eba67643f616) | 1400 |
| Survey C | [https://app.surveylex.com/surveys/a66494c0-a824-11ea-88c1-ab37bac1e1d4](https://app.surveylex.com/surveys/a66494c0-a824-11ea-88c1-ab37bac1e1d4) | 800 |
| Survey D | [https://app.surveylex.com/surveys/53737620-a637-11eb-bcc9-eba67643f616](https://app.surveylex.com/surveys/53737620-a637-11eb-bcc9-eba67643f616) | 100 |

Previews for each of these surveys are provided below as .GIFs so that you can quickly visualize the survey experience for clinical study participants.

Note you can clone these surveys @ https://surveylex.com and replicate our work in other patient populations.

### [Survey A](https://app.surveylex.com/surveys/8a32cbb0-cc8a-11eb-9ea3-938cc8b6d71e)
![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/A/A.gif)

| Survey fragment    |    Description   | Sample Audio |   
| ----------- | ----------- |  ----------- | 
| [Consent form](https://github.com/jim-schwoebel/voiceome/wiki/0.-Consent-form) | A standard consent form to opt into the Voiceome study. | n/a | 
| [Microphone check](https://github.com/jim-schwoebel/voiceome/wiki/00.-Microphone-check-task)| A fragment and information screen to test that a microphone is able to collect voice input from a browser. | [![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/play.svg)](https://drive.google.com/file/d/1c54zKMuBxCririQrrbvKBuJG6c0UpgOK/view?usp=sharing) |
| [Free speech task](https://github.com/jim-schwoebel/voiceome/wiki/01.-Free-speech-task) | A free speech prompt to collect extemporaneous speech from clinical study participants. | [![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/play.svg)](https://drive.google.com/file/d/1RcC8PY84rPg7qZKA6BFMXc2XmBElXM6e/view?usp=sharing) |
| [Category Naming Task](https://github.com/jim-schwoebel/voiceome/wiki/03.-Category-naming-task) | A prompt that asks participants to name as many animals as they can in one minute. | [![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/play.svg)](https://drive.google.com/file/d/114XDxQwd621pQM5JYukXPRm5QONTpaGW/view?usp=sharing) |
| [Letter F Task](https://github.com/jim-schwoebel/voiceome/wiki/04.-Letter-%7BFAS%7D-Tasks) | A prompt that asks participants to name as many words that start with the letter F as they can in one minute. | [![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/play.svg)](https://drive.google.com/file/d/1m-gRiiaPS4m7bFx7B22rgC5ZsBsejaZ9/view?usp=sharing) |
| [Paragraph Reading Task](https://github.com/jim-schwoebel/voiceome/wiki/05.-Paragraph-reading-task) | A prompt that asks participants to read the Caterpillar passage. | [![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/play.svg)](https://drive.google.com/file/d/1pF4Jw6vTL3GOewZOn-dceD4z645ACEzg/view?usp=sharing) |
| [Sustained Phonation Task](https://github.com/jim-schwoebel/voiceome/wiki/06.-Sustained-phonation-('ahh')) | A prompt to ask users to hold a sustained phonation of 'ahh' for as long as they can in 30 seconds. | [![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/play.svg)](https://drive.google.com/file/d/1XUrfVM_dnDeA21jaHRXtn6guspZczTeV/view?usp=sharing) |
| [Papapa Task](https://github.com/jim-schwoebel/voiceome/wiki/07.-Pa-pa-pa-task) | A voice task to say puh-puh-puh as many times as a clinical study participant can in 10 seconds. | [![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/play.svg)](https://drive.google.com/file/d/1nqknAogTF90Zw6Cckcg85CjObVoYSpBG/view?usp=sharing) |
| [Pa-ta-ka Task](https://github.com/jim-schwoebel/voiceome/wiki/08.-Pa-ta-ka-task) | A voice task to say puh-tah-kah as many times as a clinical study participant can in 10 seconds. | [![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/play.svg)](https://drive.google.com/file/d/1WFlkKbyUCREtyhybN-TFVGs3h8-Yj4nc/view?usp=sharing) |
| [Confrontational Naming Task](https://github.com/jim-schwoebel/voiceome/wiki/09.-Confrontational-naming-task) | Name 25 images back-to-back in a session. | [![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/play.svg)](https://drive.google.com/file/d/1HgPxr0Kiz2z5PNtJ10iXAZnN0dnxhQJQ/view?usp=sharing) |
| [Nonword Naming Task](https://github.com/jim-schwoebel/voiceome/wiki/10.-Nonword-task) | Name a series of 10 nonsense words in a session. | [![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/play.svg)](https://drive.google.com/file/d/1yaKH85Gm6kvuSjThKMkWnofWUS-VvMkG/view?usp=sharing) |
| [Immediate Recall Tasks](https://github.com/jim-schwoebel/voiceome/wiki/11.-Immediate-recall-task) | Recall 2 sentences played back in the browser immediately to test memory. | [![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/play.svg)](https://drive.google.com/file/d/1OpNdamMRar9eJx2q3iouzKVZf02nCyLB/view?usp=sharing) |
| [Spoken Diagnosis Task](https://github.com/jim-schwoebel/voiceome/wiki/12.-Spoken-diagnosis-task) | Asks individuals to name their clinical diagnoses (optional speech task). | [![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/play.svg)](https://drive.google.com/file/d/13v6Sj5GB6dDUWWTBaIbG2qGX9pWDjbEM/view?usp=sharing) |
| [Spoken Medication Task](https://github.com/jim-schwoebel/voiceome/wiki/13.-Spoken-medication-task) | Asks individuals to name their current medications that they are taking (optional speech task). | [![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/play.svg)](https://drive.google.com/file/d/1I7PwZbK2xu9PPNyYoJ8qyW1bWk2qlyFC/view?usp=sharing) |
| [Confounding Questions](https://github.com/jim-schwoebel/voiceome/wiki/14.-Confounding-questions) | Survey section asking confounding questions like smoking histories, visual acuity, and other impairments. | n/a|
| [Demographic Questions](https://github.com/jim-schwoebel/voiceome/wiki/15.-Demographic-questions) | A standard list of demographic questions | n/a |
| [Health Labels](https://github.com/jim-schwoebel/voiceome/wiki/16.-Health-labels) | A standard list of health questionnaires that can be used as self-reported labels for vocal biomarker research. | n/a |
| [Fun Facts](https://github.com/jim-schwoebel/voiceome/wiki/17.-Fun-Facts) | Fun facts and other fragments in the survey that can be used to increase user engagement. | n/a |

### [Survey B](https://app.surveylex.com/surveys/061da3f0-a637-11eb-bcc9-eba67643f616)
![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/B/B.gif)

### [Survey C](https://app.surveylex.com/surveys/a66494c0-a824-11ea-88c1-ab37bac1e1d4)
![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/C/C.gif)

### [Survey D](https://app.surveylex.com/surveys/53737620-a637-11eb-bcc9-eba67643f616)
![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/D/D.gif)

## Cite us
If you incorporate our work in your research, feel free to reference us with the APA format below:
```
Schwoebel, James, et al. "The Voiceome Study: A Longitudinal Normative Dataset and Protocol for Speech and Language Biomarker Research." Nature Methods. 2021.
```

## Data access
We have tried to make acoustic and linguistic feature reference ranges for each task as open as possible. These are available in this repository under an Apache 2.0 license.

The sample audio and spreadsheets released in this repository are also released under an Apache 2.0 license. They were recorded by Jim Schwoebel in a controlled setting, cloning the protocol on the SurveyLex product. We did not use any sample data from participants here to protect their identities.

Also, note that OpenSMILE GeMAPS features are for research-only use. Keep this in mind if you are working on commercial deployments. Read more about their dual licensing model [here](https://github.com/audeering/opensmile). Since this repository was in the scope of research, we fall within this dual license model and can publish these references openly.

Raw audio data and .CSV labels for the Voiceome Study is accessible via a commercial license. If you are interested to license or access the Voiceome dataset, please reach out to Jim Schwoebel (VP of Data and Research @ Sonde) @ jim.schwoebel@gmail.com.

## Collaborators
[![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/sonde.png)](https://sondehealth.com)
[![](https://github.com/jim-schwoebel/voiceome/blob/main/assets/images/thumbnails/collaborators.png)](https://voiceome.org)

## References
Voice Protocols
- [00. Microphone check task](https://github.com/jim-schwoebel/voiceome/wiki/00.-Microphone-check-task)
- [01. Free speech task](https://github.com/jim-schwoebel/voiceome/wiki/01.-Free-speech-task)
- [02. Picture description task](https://github.com/jim-schwoebel/voiceome/wiki/02.-Picture-description-task)
- [03. Category naming task](https://github.com/jim-schwoebel/voiceome/wiki/03.-Category-naming-task)
- [04. Letter {FAS} Tasks](https://github.com/jim-schwoebel/voiceome/wiki/04.-Letter-%7BFAS%7D-Tasks)
- [05. Paragraph reading task](https://github.com/jim-schwoebel/voiceome/wiki/05.-Paragraph-reading-task)
- [06. Sustained phonation ('ahh')](https://github.com/jim-schwoebel/voiceome/wiki/06.-Sustained-phonation-('ahh'))
- [07. Pa pa pa task](https://github.com/jim-schwoebel/voiceome/wiki/07.-Pa-pa-pa-task)
- [08. Pa ta ka task](https://github.com/jim-schwoebel/voiceome/wiki/08.-Pa-ta-ka-task)
- [09. Confrontational naming task](https://github.com/jim-schwoebel/voiceome/wiki/09.-Confrontational-naming-task)
- [10. Nonword task](https://github.com/jim-schwoebel/voiceome/wiki/10.-Nonword-task)
- [11. Immediate recall task](https://github.com/jim-schwoebel/voiceome/wiki/11.-Immediate-recall-task)
- [12. Spoken diagnosis task](https://github.com/jim-schwoebel/voiceome/wiki/12.-Spoken-diagnosis-task)
- [13. Spoken medication task](https://github.com/jim-schwoebel/voiceome/wiki/13.-Spoken-medication-task)

Health questionniares 
- [Confounding questions](https://github.com/jim-schwoebel/voiceome/wiki/14.-Confounding-questions)
- [Demographic questions](https://github.com/jim-schwoebel/voiceome/wiki/15.-Demographic-questions)
- [Custom lichert scales](https://github.com/jim-schwoebel/voiceome/wiki/16.-Health-labels#lichert-questions-custom-made)
- [PHQ-9](https://www.mdcalc.com/phq-9-patient-health-questionnaire-9)
- [GAD-7](https://patient.info/doctor/generalised-anxiety-disorder-assessment-gad-7)
- [Altman Self-rating scale](https://psychology-tools.com/test/altman-self-rating-mania-scale)
- [Audit-C](https://www.mdcalc.com/audit-c-alcohol-use)
- [Sheehan disability scale](http://memorialparkpsychiatry.com/doc/sheehan_disability_scale.pdf)
- [ADHD Self-rating Scale - Part A](https://psychology-tools.com/test/adult-adhd-self-report-scale)
- [Insomnia Severity Index](https://www.ons.org/sites/default/files/InsomniaSeverityIndex_ISI.pdf)
- [Stanford Sleepiness Scale](https://www.med.upenn.edu/cbti/assets/user-content/documents/Stanford%20Sleepiness%20Scale.pdf)
- [PTSD-5](https://www.ptsd.va.gov/professional/assessment/documents/pc-ptsd5-screen.pdf)

Other references 
- [Allie ML repository](https://github.com/jim-schwoebel/allie)
- [Voicebook](https://github.com/jim-schwoebel/voicebook)
- [SurveyLex](https://surveylex.com)
- [OpenSmile GeMAPS](https://sail.usc.edu/publications/files/eyben-preprinttaffc-2015.pdf)
- [Voiceome strategic plan](https://drive.google.com/file/d/1Dme9tUq0eCepja_7Yg9sNqn_JWKaJxJm/view)
- [Voice_datasets repo](https://github.com/jim-schwoebel/voice_datasets)
- [Amazon Mechanical Turk](https://www.mturk.com/)

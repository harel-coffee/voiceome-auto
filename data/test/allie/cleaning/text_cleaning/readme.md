
## Getting started
To clean an entire folder of .TXT files, you can run:

```
cd ~ 
cd allie/cleaning/text_cleaning
python3 cleaning.py /Users/jimschwoebel/allie/load_dir
```

### [Text](https://github.com/jim-schwoebel/allie/tree/master/cleaning/text_cleaning)
* [clean_summary](https://github.com/jim-schwoebel/allie/blob/master/cleaning/text_cleaning/clean_summary.py) - extracts a 100 word summary of a long piece of text and deletes the original work (using [Text rank summarization](https://github.com/davidadamojr/TextRank))
* [clean_textacy](https://github.com/jim-schwoebel/allie/blob/master/cleaning/text_cleaning/clean_textacy.py) - removes punctuation and a variety of other operations to clean a text (uses [Textacy](https://chartbeat-labs.github.io/textacy/build/html/api_reference/text_processing.html))

### Settings

Here are some default settings relevant to this section of Allie's API:

| setting | description | default setting | all options | 
|------|------|------|------| 
| clean_data | whether or not to clean datasets during the model training process via default cleaning scripts. | False | True, False | 
| [default_text_cleaners](https://github.com/jim-schwoebel/allie/tree/master/cleaning/text_cleaning) | the default cleaning techniques used during model training on text data if clean_data == True| ["clean_textacy"] | ["clean_summary", "clean_textacy"]  | 

## Getting started
This is a console program for learning words (e.g. in English). 

[![Build Status](https://travis-ci.org/oyyablokov/lemys.svg?branch=develop)](https://travis-ci.org/oyyablokov/lemys)

## Features
- Support for favorite words lists;
- Integration with [Google Translator](https://translate.google.com/);
- Integration with [wordsapi](https://www.wordsapi.com/);

## Install & run
```shell
cd /path/to/lemys/                          # Go to your Lemys directory
pip install -r requirements                 # Install the required packages
cd /your/directory/for/working/with/lemys   # For convenience*
python /path/to/lemys/lemys                 # Run the program
```
\* I advise to work in a separate directory as Lemys will create some files in it (e.g. settings files and dictionary/ directory with translations downloaded from wordsapi)

## Integration with Google Translator
Lemys can import translations from your Google Translate Phrasebook:
1. Download the \*.csv file with translations from your Phrasebook (consult Google Help to learn how to do this);
2. Move the file to any directory;
3. Run the program from this directory.

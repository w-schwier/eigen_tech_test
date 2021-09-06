# Eigen Tech Test

### What is it?

A small python package that will process a series of documents to produce a dictionary of interesting words, the number of occurrences and where each sentence containing that word can be found. The words in question can either be explicitly defined or will be determined automatically.

### Installation and Usage

You will need to have pipenv installed and the code locally. Navigate into the main directory (where src and tests are).

Install required dependencies by running ```pipenv install --dev```. Once that finishes running, start up the shell with ```pipenv shell```.

To change the documents being processed, either edit the `docs` directory to contain the desired .txt files, set the FOLDER_PATH variable to their location in the .env file, or pass it as an option when running in the terminal (see below).

To run the app: ```python -m src.cli```

You can also interact directly with the dictionary returned by using ```python``` to open an interactive shell, then as an example with "interesting" and "another" being used as the interesting words:
```
from src import cli

word_stats = cli.run(["-iw", "interesting", "another"])
print(word_stats["another"])
```

There are various optional params that can be appended to the run command as needed:
- -fp - path to folder containing documents to process
- -iw - interesting words to use instead of automatically finding them
- -mwl - if automatically finding words, the min length of word that will be used
- -wl - the limit for the number of automatically found words
- -q - quieten the printing of the dictionary of word statistics
- -t - print a table containing the word stats dictionary, recommended to use with quieten
- -tw - max width for table, fine tune to format table nicely for your screen size

One easy way to interact with the outputted data is to copy the response without quieten or table to https://jsonformatter.curiousconcept.com. This allows you to minimise the location portion of the dict, which can be quite long.

#### Debugging:
Can't find a word you're expecting to see - Ensure that `min_word_length` isn't higher than the number of characters in the word, and that the word isn't in the list of stop words found in `lib/nltk_data/corpora/stopwords/english`

#### Tests:
Test can be run with ```python -m pytest```

### Future Features

In future iterations, I would ensure both flake8 and mypy were appeased as they currently aren't very happy. I'd also extend the tests to cover the table functionality. There would also be the potential to wrap this code in a RESTFUL api, or as a PyPI package. The CLI wrapper could also be expanded to be a bit more interactive, taking inputs as a series of questions.

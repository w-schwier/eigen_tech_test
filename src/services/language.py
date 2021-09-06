import glob
import os
from typing import List, Tuple, Union

from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize as get_sentences
from nltk.tokenize import word_tokenize as get_words


class LanguageService:
    def __init__(self, path_to_docs: str):
        self.path_to_docs = path_to_docs
        self.word_stats = {}

    def get_interesting_words(self, min_word_length: int = 5, word_limit: int = 50) -> dict:
        interesting_words = {}
        for filepath in glob.glob(f"{self.path_to_docs}/*.txt"):
            for x, y in _get_freq_dist(filepath, min_word_length):
                interesting_words.update({x: y + interesting_words.get(x, 0)})

        return dict(sorted(interesting_words.items(), key=lambda item: item[1], reverse=True)[:word_limit])

    def get_word_statistics(self, interesting_words: Union[dict, List[str]]) -> dict:
        self.word_stats = {}
        for file_name in os.listdir(self.path_to_docs):
            self._add_word_stats_for_filepath(file_name, interesting_words)

        return dict(sorted(self.word_stats.items(), key=lambda item: item[1]["count"], reverse=True))

    def _update_word_stats(self, word, count, document, sentence):
        if self.word_stats.get(word):
            self.word_stats[word]["locations"] += [{"document": document, "sentence": sentence}]
            self.word_stats[word]["count"] += count
        else:
            self.word_stats[word] = {"count": count, "locations": [{"document": document, "sentence": sentence}]}

    def _add_word_stats_for_filepath(self, file_name: str, interesting_words: dict):
        with open(f"{self.path_to_docs}/{file_name}") as f:
            for sentence in get_sentences(f.read()):
                sentence_words = get_words(sentence.lower())
                for word in [substring for substring in interesting_words if substring.lower() in sentence_words]:
                    self._update_word_stats(word.lower(), sentence_words.count(word.lower()), file_name, sentence)


def _remove_small_and_stop_words(words_to_filter: List[str], min_word_length: int) -> List[str]:
    stop_words = set(stopwords.words("english"))
    return [w.lower() for w in words_to_filter if len(w) >= min_word_length and w.lower() not in stop_words]


def _get_freq_dist(filepath: str, min_word_length: int = 0) -> List[Tuple]:
    with open(filepath) as f:
        words = get_words(f.read())
        filtered_words = _remove_small_and_stop_words(words, min_word_length)
        freq_dist = FreqDist(filtered_words)

    return freq_dist.most_common()

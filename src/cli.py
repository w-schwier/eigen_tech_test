import argparse

from src.core.settings import get_settings
from src.services.language import LanguageService
from src.services.table import get_table_from_dict


def run(argv=None):
    args, language_service, interesting_words = _setup(argv)
    word_stats = language_service.get_word_statistics(interesting_words)
    if not args.quieten:
        print(word_stats)
    if args.table:
        print(get_table_from_dict(word_stats, args.table_width))
    return word_stats


def _add_arguments(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-fp", "--folder_path", default=get_settings().FOLDER_PATH)
    parser.add_argument("-iw", "--interesting_words", nargs='*', default=None)
    parser.add_argument("-mwl", "--min_word_length", type=int, default=5)
    parser.add_argument("-wl", "--word_limit", type=int, default=50)
    parser.add_argument("-q", "--quieten", action="store_true", default=False)
    parser.add_argument("-t", "--table", action="store_true")
    parser.add_argument("-tw", "--table_width", type=int, default=140)
    return parser.parse_args(argv)


def _setup(argv=None):
    args = _add_arguments(argv)
    language_service = LanguageService(args.folder_path)
    if args.interesting_words:
        interesting_words = args.interesting_words
    else:
        interesting_words = language_service.get_interesting_words(args.min_word_length, args.word_limit)
    return args, language_service, interesting_words


if __name__ == "__main__":
    run()

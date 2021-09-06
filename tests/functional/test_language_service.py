import pytest

from src.core.settings import get_settings
from src.services.language import LanguageService

FOLDER_PATH = get_settings().FOLDER_PATH


@pytest.fixture(scope="module")
def language_service() -> LanguageService:
    return LanguageService(FOLDER_PATH)


@pytest.mark.parametrize(
    ["word_limit", "texts_to_file", "expected_response"],
    [
        (
            1,
            ["This sentence contains the word interesting twice, interesting."],
            {"interesting": 2},
        ),
        (
            4,
            ["This sentence contains the word interesting twice, interesting."],
            {"interesting": 2, "contains": 1, "sentence": 1, "twice": 1},
        ),
        (
            3,
            [
                "This doc contains the word interesting twice. Interesting!",
                "Another doc also contains interesting twice. Also interesting.",
            ],
            {"interesting": 4, "contains": 2, "twice": 2},
        ),
        (
            1,
            [
                "This sentence has a word above the min word length a few times, that's above interesting... above",
                "Above all else, remember to be interesting; and that above is a stop word."
            ],
            {"interesting": 2},
        ),
        (
            1,
            [
                "Look, this sentence is set to look like it is going to contain the word look a lot, interesting...?",
                "Look isn't a stop word, but it is less than the default min word length; now that is interesting!"
            ],
            {"interesting": 2},
        ),
    ],
)
def test_get_interesting_words(language_service, word_limit, expected_response, with_auto_files):
    # GIVEN
    # WHEN
    response = language_service.get_interesting_words(word_limit=word_limit)

    # THEN
    assert response == expected_response


@pytest.mark.parametrize(
    ["interesting_words", "texts_to_file", "expected_response"],
    [
        (
            ["interesting"],
            ["This sentence contains the word interesting."],
            {
                "interesting": {
                    "count": 1,
                    "locations": [
                        {
                            "document": "doc1.txt",
                            "sentence": "This sentence contains the word interesting."
                        },
                    ],
                },
            },
        ),
        (
            {"interesting": 1},
            ["This sentence contains the word interesting."],
            {
                "interesting": {
                    "count": 1,
                    "locations": [
                        {
                            "document": "doc1.txt",
                            "sentence": "This sentence contains the word interesting."
                        },
                    ],
                },
            },
        ),
        (
            ["interesting"],
            ["This sentence contains the word Interesting with a capital I."],
            {
                "interesting": {
                    "count": 1,
                    "locations": [
                        {
                            "document": "doc1.txt",
                            "sentence": "This sentence contains the word Interesting with a capital I."
                        },
                    ],
                },
            },
        ),
        (
            ["interesting"],
            ["This sentence contains the word interesting, but also a name like Dr. Smith."],
            {
                "interesting": {
                    "count": 1,
                    "locations": [
                        {
                            "document": "doc1.txt",
                            "sentence": "This sentence contains the word interesting, but also a name like Dr. Smith."
                        },
                    ],
                },
            },
        ),
        (
            ["interesting"],
            ["This sentence contains the word interesting. This one also contains interesting."],
            {
                "interesting": {
                    "count": 2,
                    "locations": [
                        {
                            "document": "doc1.txt",
                            "sentence": "This sentence contains the word interesting."
                        },
                        {
                            "document": "doc1.txt",
                            "sentence": "This one also contains interesting."
                        },
                    ],
                },
            },
        ),
        (
            ["interesting"],
            ["This sentence contains the word interesting twice, isn't that interesting."],
            {
                "interesting": {
                    "count": 2,
                    "locations": [
                        {
                            "document": "doc1.txt",
                            "sentence": ""
                                        "This sentence contains the word interesting twice, isn't that interesting."
                        },
                    ],
                },
            },
        ),
        (
            ["interesting"],
            ["This sentence contains the word interesting.", "This one in a different doc also contains interesting."],
            {
                "interesting": {
                    "count": 2,
                    "locations": [
                        {
                            "document": "doc1.txt",
                            "sentence": "This sentence contains the word interesting."
                        },
                        {
                            "document": "doc2.txt",
                            "sentence": "This one in a different doc also contains interesting."
                        },
                    ],
                },
            },
        ),
        (
            ["interesting", "hypothetical"],
            ["This sentence contains the word interesting. This one contains hypothetical."],
            {
                "interesting": {
                    "count": 1,
                    "locations": [
                        {
                            "document": "doc1.txt",
                            "sentence": "This sentence contains the word interesting."
                        },
                    ],
                },
                "hypothetical": {
                    "count": 1,
                    "locations": [
                        {
                            "document": "doc1.txt",
                            "sentence": "This one contains hypothetical."
                        },
                    ],
                },
            },
        ),
        (
            ["interesting", "hypothetical"],
            ["This sentence contains the word interesting and hypothetical."],
            {
                "interesting": {
                    "count": 1,
                    "locations": [
                        {
                            "document": "doc1.txt",
                            "sentence": "This sentence contains the word interesting and hypothetical."
                        },
                    ],
                },
                "hypothetical": {
                    "count": 1,
                    "locations": [
                        {
                            "document": "doc1.txt",
                            "sentence": "This sentence contains the word interesting and hypothetical."
                        },
                    ],
                },
            },
        ),
    ],
)
def test_with_given_words(language_service, interesting_words, expected_response, with_auto_files):
    # GIVEN
    # WHEN
    response = language_service.get_word_statistics(interesting_words)

    # THEN
    assert response == expected_response

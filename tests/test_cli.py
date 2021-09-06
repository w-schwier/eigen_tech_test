import pytest

from src import cli


@pytest.mark.parametrize(
    ["texts_to_file", "interesting_words", "expected_response"],
    [
        (
            ["This sentence contains the word interesting."],
            ["interesting"],
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
    ],
)
def test_cli(capsys, interesting_words, expected_response, with_auto_files):
    # GIVEN
    # WHEN
    cli.run(["-iw", *interesting_words])
    out, err = capsys.readouterr()

    # THEN
    assert out == f"{expected_response}\n"

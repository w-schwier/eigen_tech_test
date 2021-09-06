from dotenv import load_dotenv, find_dotenv
import glob
import os
import pytest

from src.core.settings import get_settings

load_dotenv(verbose=True)

load_dotenv(find_dotenv("test.env", raise_error_if_not_found=True), override=True)


@pytest.fixture()
def with_auto_files(texts_to_file):
    folder_path = get_settings().FOLDER_PATH
    _create_files(folder_path, texts_to_file)
    yield
    _remove_files(folder_path)


def _create_files(folder_path, input_texts):
    for i in range(0, len(input_texts)):
        with open(f"{folder_path}/doc{i + 1}.txt", 'w') as f:
            f.write(input_texts[i])


def _remove_files(folder_path):
    for f in glob.glob(f"{folder_path}/*.txt"):
        os.remove(f)

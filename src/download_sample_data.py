import os
import wget
from src.settings import RAW_DATA_PATH, example_file_name


def download_sample_data():
    url = 'https://aepinilla.com/sample_data/PJGHY.xdf'
    # output_path = RAW_DATA_PATH + sample_file_name
    filename = RAW_DATA_PATH + '/' + os.path.basename(example_file_name)
    if os.path.exists(filename):
        os.remove(filename)
    print('Downloading example data...')
    wget.download(url, out=filename)
    print(f"File downloaded: {filename}")


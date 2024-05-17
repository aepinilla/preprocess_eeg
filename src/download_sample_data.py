import os
import wget
from src.settings import RAW_DATA_PATH, sample_file_name


def download_sample_data():
    url = 'https://drive.google.com/file/d/1WyPQ0vTpahdP6-6c2KKoEvAV8T-6s0Ur'
    output_path = RAW_DATA_PATH + sample_file_name
    filename = RAW_DATA_PATH + '/' + os.path.basename(sample_file_name)
    if os.path.exists(filename):
        os.remove(filename)
    wget.download(url, out=filename)
    print(f"File downloaded: {filename}")


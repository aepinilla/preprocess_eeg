import pickle as pkl
import numpy as np

from src.preprocess_eeg import preprocessing_pipeline
from src.create_data_folder import create_data_folder
from src.download_sample_data import download_sample_data
from src.settings import TRIALS_DATA_PATH, data_paths, example_file_name, output_file_name


def main(file_name: str, sample_data: bool):
    # Create data folder if it does not exist
    for d in data_paths:
        create_data_folder(d)
    # Download sample data
    if sample_data:
        download_sample_data()
    # Preprocess data and extract trials
    trials = preprocessing_pipeline(file_name)
    # Save preprocessed trials to NPY format
    with open(TRIALS_DATA_PATH + output_file_name, 'wb') as f:
        pkl.dump(trials, f)


if __name__ == "__main__":
    # The name of the XDF file
    filename = example_file_name
    main(file_name=filename, sample_data=True)
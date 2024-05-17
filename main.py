from src.preprocess_eeg import preprocessing_pipeline
from src.create_data_folder import create_data_folder
from src.download_sample_data import download_sample_data
from src.settings import data_paths, sample_file_name, trials_file_name


def main(file_name: str):
    # Create data folder if it does not exist
    for d in data_paths:
        create_data_folder(d)
    # Download sample data
    download_sample_data()
    # Preprocess data and extract trials
    trials = preprocessing_pipeline(file_name)
    # Save preprocessed trials to NPY format
    np.save(TRIALS_DATA_PATH + trials_file_name, np.array(trials, dtype=object), allow_pickle=True)


if __name__ == "__main__":
    # The name of the XDF file
    filename = sample_file_name
    main(file_name=filename)
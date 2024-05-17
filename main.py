from src.preprocess_eeg import preprocessing_pipeline
from src.create_data_folder import create_data_folder
from src.settings import data_paths


def main(file_name: str):
    for d in data_paths:
        create_data_folder(d)
    # Preprocess data and extract trials
    trials = preprocessing_pipeline(file_name)
    # Save preprocessed trials to NPY format
    np.save(TRIALS_DATA_PATH + 'trials.npy', np.array(a, dtype=object), allow_pickle=True)

    print(trials)


if __name__ == "__main__":
    # The name of the XDF file
    filename = "PJGHY.xdf"
    main(file_name=filename)
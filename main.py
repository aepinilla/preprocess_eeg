from src.preprocess_eeg import *

def main(file_name):
    t = PreprocessEEG(file_name)
    t._find_indexes()
    t._clean_signal()
    trials = t.extract_trials()

    return trials


if __name__ == "__main__":
    file_name = "PJGHY.xdf"
    main(file_name)
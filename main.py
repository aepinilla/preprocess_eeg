from src.preprocess_eeg import preprocessing_pipeline
from src.settings import filename


def main(file_name: str):
    return preprocessing_pipeline(file_name)


if __name__ == "__main__":
    main(file_name = filename)
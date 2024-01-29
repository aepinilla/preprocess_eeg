from src.preprocess_eeg import preprocessing_pipeline


def main(file_name: str):
    return preprocessing_pipeline(file_name)


if __name__ == "__main__":
    file_name = "PJGHY.xdf"
    main(file_name = file_name)
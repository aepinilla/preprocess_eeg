from src.read_xdf import read_xdf
from src.preprocess import preprocess
from src.extract_trials import extract_trials
from src.settings import DATA_PATH

def main(file_name):
    streams, streams_index = read_xdf(DATA_PATH + file_name)
    preprocessed = preprocess(streams, streams_index)
    trials = extract_trials(preprocessed, streams, streams_index)

    print('Preprocessing is complete')
    print(len(trials), 'trials have been extracted')

if __name__ == "__main__":
    file_name = 'PJGHY.xdf'
    main(file_name)
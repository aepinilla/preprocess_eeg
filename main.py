from src.read_xdf import read_xdf
from src.settings import DATA_PATH

def main(file_name):
    streams, streams_index = read_xdf(DATA_PATH + file_name)
    print(streams_index)

if __name__ == "__main__":
    file_name = 'PJGHY.xdf'
    main(file_name)
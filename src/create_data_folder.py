import os


def create_data_folder(path: str) -> None:
    os.path.exists(path)
    if not os.path.exists(path):
        os.makedirs(path)

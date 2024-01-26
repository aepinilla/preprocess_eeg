import pyxdf
from .settings import *

def read_xdf(file_path):
    # Obtain streams and header from XDF file
    streams, header = pyxdf.load_xdf(file_path)
    # Find stream indices
    ecg_index = -1
    eeg_index = -1
    markers_index = -1
    for index in range(len(streams)):
        if streams[index]['info']['name'][0] == ecg_stream_name:
            ecg_index = index
        elif streams[index]['info']['name'][0] == marker_stream_name:
            markers_index = index
        elif streams[index]['info']['name'][0] == eeg_stream_name:
            eeg_index = index

        if ecg_index >= 0 and eeg_index >= 0 and markers_index >= 0:
            break

    streams_index = {
        'ecg': ecg_index,
        'eeg': eeg_index,
        'markers': markers_index
    }

    return streams, streams_index
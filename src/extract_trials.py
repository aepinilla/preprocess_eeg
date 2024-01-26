import numpy as np
from .settings import trial_start_marker, trial_len

def extract_trials(downsampled, streams, streams_index):
    # Get index of EEG and markers streams
    eeg_index = streams_index['eeg']
    markers_index = streams_index['markers']

    # Get sampling frequency of EEG stream
    sfreq = int(streams[eeg_index]['info']['nominal_srate'][0])

    # Align timestamps of EEG and markers streams
    eeg_data = downsampled.get_data().astype("float")
    eeg_time_zero_ref = streams[eeg_index]["time_stamps"] - streams[eeg_index]["time_stamps"][0]
    marker_data = streams[markers_index]["time_series"]
    marker_time_zero_ref = streams[markers_index]["time_stamps"] - streams[markers_index]["time_stamps"][0]

    # Get index of relevant markers (trial start)
    markers_list = list(np.where(marker_data == trial_start_marker))[0]

    # Slice trials data
    trials = []
    for m in markers_list:
        # Trial start timestamp
        marker_start_time = marker_time_zero_ref[m]
        # Index of the EEG sample recorded immediately after the marker was received
        eeg_start_idx = np.where(eeg_time_zero_ref >= marker_start_time)
        eeg_start_idx = eeg_start_idx[0][0]
        # Index of trial end
        eeg_end_idx = eeg_start_idx + (trial_len * sfreq)
        # Subset trial
        trial = np.array([channel[eeg_start_idx:eeg_end_idx] for channel in eeg_data])
        # TODO: Handle time difference between marker timestamp and EEG timestamp
        # time_offset = EEG_start - marker_start_time
        trials.append(trial)

    return trials
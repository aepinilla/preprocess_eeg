import pyxdf
import mne
from asrpy import ASR
import numpy as np

from settings import *


class PreprocessEEG:
    def __init__(self, file_name: str):
        # Define file path
        self.file = DATA_PATH + file_name
        # Obtain streams and header from XDF file
        self.streams, self.header = pyxdf.load_xdf(self.file)
        # Initialize streams index dictionary
        self.streams_index = {'ecg': -1, 'eeg': -1, 'markers': -1}
        # Initialize empty variable with downsample data
        self.down_sampled = []

    def _find_indexes(self):
        # Find stream indexes
        for i in range(len(self.streams)):
            match self.streams[i]['info']['name'][0]:
                case streams_names.ecg:
                    self.streams_index['ecg'] = i
                case streams_names.eeg:
                    self.streams_index['eeg'] = i
                case streams_names.markers:
                    self.streams_index['markers'] = i

            # If all streams indexes are equal or greater than zero, exit the for loop
            if all(i >= 0 for i in list(self.streams_index.values())):
                break

    def _clean_signal(self):
        # Get sampling frequency of the EEG stream
        eeg_index = self.streams_index['eeg']
        sfreq = int(self.streams[eeg_index]['info']['nominal_srate'][0])
        # Create MNE object
        info = mne.create_info(ch_names=eeg_ch_names, sfreq=sfreq, ch_types=ch_types)
        eeg_data = self.streams[eeg_index]["time_series"][:, :len(eeg_ch_names)].T
        raw = mne.io.RawArray(eeg_data, info)
        # Remove powerline and low frequency noise
        notched = raw.notch_filter([50, 60])
        filtered_low_frequency = notched.filter(0.75, None, fir_design='firwin')
        # Remove artifacts using ASR
        asr = ASR(sfreq=filtered_low_frequency.info["sfreq"], cutoff=13)
        asr.fit(filtered_low_frequency)
        artifacts_removed = asr.transform(filtered_low_frequency)
        # Common-average referencing
        referenced = mne.set_eeg_reference(artifacts_removed, ref_channels='average')
        # Band-pass filter
        band_passed = referenced[0].filter(4, 45, fir_design='firwin')
        # Downsample for faster processing
        self.down_sampled = band_passed.copy().resample(sfreq=downsample_sfreq)

    def extract_trials(self):
        # Get index of EEG and markers streams
        eeg_index = self.streams_index['eeg']
        markers_index = self.streams_index['markers']
        # Get sampling frequency of EEG stream
        sfreq = int(self.streams[eeg_index]['info']['nominal_srate'][0])
        # Align timestamps of EEG and markers streams
        eeg_data = self.down_sampled.get_data().astype("float")
        eeg_time_zero_ref = self.streams[eeg_index]["time_stamps"] - self.streams[eeg_index]["time_stamps"][0]
        marker_data = self.streams[markers_index]["time_series"]
        marker_time_zero_ref = self.streams[markers_index]["time_stamps"] - self.streams[markers_index]["time_stamps"][0]
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



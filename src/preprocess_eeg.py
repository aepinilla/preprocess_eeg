import pyxdf
import mne
import numpy as np
import numpy.typing as npt
from asrpy import ASR
from dataclasses import dataclass


from src.settings import STREAMS_NAMES, stream_types, eeg_ch_names, trial_len, downsample_sfreq, trial_start_marker

# Path to folder with XDF files
DATA_PATH = 'data/'
# Channel types. Required for building MNE object
CH_TYPES = "eeg"

class PreprocessEEG:

    def __init__(self, file_name: str):
        self.file = DATA_PATH + file_name
        # Obtain streams and header from XDF file
        self.streams, self.header = pyxdf.load_xdf(self.file)
        # Initialize streams index dictionary
        self.streams_index = {key: -1 for key in stream_types}
        # Initialize empty variable with down sampled data
        self.down_sampled = []

    def find_indexes(self):
        for i in range(len(self.streams)):
            match self.streams[i]['info']['name'][0]:
                # EDIT ACCORDING TO THE NUMBER OF STREAMS STORED IN YOUR XDF FILE
                case STREAMS_NAMES.ecg:
                    self.streams_index['ecg'] = i
                case STREAMS_NAMES.eeg:
                    self.streams_index['eeg'] = i
                case STREAMS_NAMES.markers:
                    self.streams_index['markers'] = i

            # If all streams indexes have been found, exit the for loop
            if all(i >= 0 for i in list(self.streams_index.values())):
                break

    def clean_signal(self):
        # Get sampling frequency of the EEG stream
        eeg_index = self.streams_index['eeg']
        sfreq = int(self.streams[eeg_index]['info']['nominal_srate'][0])

        # Create MNE object
        info = mne.create_info(ch_names=eeg_ch_names, sfreq=sfreq, ch_types=CH_TYPES)
        eeg_data = self.streams[eeg_index]["time_series"][:, :len(eeg_ch_names)].T
        raw = mne.io.RawArray(eeg_data, info)
        raw.set_eeg_reference(ref_channels=['REF'])
        fig = raw.plot(start= 100, duration=3, scalings=1.0)
        fig.savefig('figures/1-raw.png', bbox_inches='tight')

        # Remove powerline
        notched = raw.notch_filter([50, 60])
        notched.plot(start= 100, duration=3, scalings=1.0)
        fig = notched.plot(start=100, duration=3, scalings=1.0)
        fig.savefig('figures/2-notched.png', bbox_inches='tight')

        # Remove low frequency noise
        filtered_low_frequency = notched.filter(1, None, fir_design='firwin')
        fig = filtered_low_frequency.plot(start=100, duration=3, scalings=1.0)
        fig.savefig('figures/3-filtered_low_frequency.png', bbox_inches='tight')

        # Remove artifacts using ASR
        asr = ASR(sfreq=filtered_low_frequency.info["sfreq"], cutoff=13)
        asr.fit(filtered_low_frequency)
        artifacts_removed = asr.transform(filtered_low_frequency)
        fig = artifacts_removed.plot(start=100, duration=3, scalings=1.0)
        fig.savefig('figures/4-artifacts_removed.png', bbox_inches='tight')

        # Common-average referencing
        referenced = mne.set_eeg_reference(artifacts_removed, ref_channels='average')
        referenced = referenced[0].drop_channels('REF')
        fig = referenced.plot(start=100, duration=3, scalings=1.0)
        fig.savefig('figures/5-referenced.png', bbox_inches='tight')

        # Band-pass filter
        band_passed = referenced.filter(1, 45, fir_design='firwin')
        fig = band_passed.plot(start=100, duration=3, scalings=1.0)
        fig.savefig('figures/6-band_passed.png', bbox_inches='tight')

        # Downsample for faster processing
        self.down_sampled = band_passed.copy().resample(sfreq=downsample_sfreq)

    def extract_trials(self):
        # Get index of EEG and markers streams
        type(self.streams)
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


def preprocessing_pipeline(file_name: str) -> list[npt.NDArray[np.float64]]:
    file = PreprocessEEG(file_name)
    file.find_indexes()
    file.clean_signal()
    trials = file.extract_trials()
    return trials
import mne
from asrpy import ASR

from .settings import eeg_ch_names, ch_types, downsample_sfreq

def preprocess(streams, streams_index):
    # Get sampling frequency of the EEG stream
    eeg_index = streams_index['eeg']
    sfreq = int(streams[eeg_index]['info']['nominal_srate'][0])

    # Create MNE object
    info = mne.create_info(ch_names=eeg_ch_names, sfreq=sfreq, ch_types=ch_types)
    EEG_channels = streams[eeg_index]["time_series"][:, :len(eeg_ch_names)].T
    raw = mne.io.RawArray(EEG_channels, info)
    raw = raw.drop_channels(['REF'])

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
    bandpassed = referenced[0].filter(4, 45, fir_design='firwin')

    # Downsample
    downsampled = bandpassed.copy().resample(sfreq=downsample_sfreq)

    return downsampled
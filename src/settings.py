# Path to folder with XDF files
DATA_PATH = 'data/'

# Names of EEG channels
eeg_ch_names = ["REF", "F3", "F4", "P3", "P4", "T7", "T8", "CZ"]

# Channel types. Required for building MNE object
ch_types = "eeg"

# Length of each trial in seconds
trial_len = 60

# Names of LabStreamingLayer (LSL) streams
ecg_stream_name = 'BrainVision RDA'
marker_stream_name = 'psychopy_marker_oddball'
eeg_stream_name = 'g.USBamp'

# Target frequency for downsampling data after preprocessing
downsample_sfreq = 128

# The marker that was triggered when each trial started
trial_start_marker = 7
import types
# Path to folder with XDF files
RAW_DATA_PATH = 'data/raw/'
# Path to folder with preprocessed trials
TRIALS_DATA_PATH = 'data/preprocessed/'
#
data_paths = [RAW_DATA_PATH, TRIALS_DATA_PATH]
# Channel types. Required for building MNE object
CH_TYPES = "eeg"

# Create object compatible with Match-Case Statement
STREAMS_NAMES = types.SimpleNamespace()

# Names of LabStreamingLayer (LSL) streams
STREAMS_NAMES.ecg = 'BrainVision RDA'
STREAMS_NAMES.markers = 'psychopy_marker_oddball'
STREAMS_NAMES.eeg = 'g.USBamp'

# Stream types
stream_types = ['ecg', 'eeg', 'markers']

# Names of EEG channels
eeg_ch_names = ["REF", "F3", "F4", "P3", "P4", "T7", "T8", "CZ"]

# Length of each trial in seconds
trial_len = 60

# Target frequency for downsampling data after preprocessing
downsample_sfreq = 128

# The marker that was triggered when each trial started
trial_start_marker = 7
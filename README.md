# Preprocess EEG

## Description
This is a simple Python script for preprocessing EEG signals stored in a XDF file, the format
commonly used to store data streamed using [LabStreamingLayer (LSL)](https://github.com/sccn/labstreaminglayer).

![alt text](https://github.com/aepinilla/preprocess_eeg/blob/main/figures/gif.gif)

The preprocessing steps are the following:
1. Apply notch filter (50 or 60 Hz, depending on which country was the data recorded).
2. TODO: Remove bad channels.
3. High-pass filter at 1Hz to remove low frequency drifts.
4. Remove artifacts using [Artifact Subspace Reconstruction (ASR)](https://patents.google.com/patent/US20160113587A1/en).
5. Common-average referencing.
6. Apply band-pass filter to remove frequencies below 1 Hz and above 45 Hz.
7. Down-sample to 128 Hz.

The order of the preprocessing steps is based on recommendations taken from [Makoto's preprocessing pipeline](https://sccn.ucsd.edu/wiki/Makoto%27s_preprocessing_pipeline), and requirements to use ASR taken from [this PDF](https://sccn.ucsd.edu/githubwiki/files/asr-final-export.pdf) by Christian Kothe.

## Cite the research paper
An earlier version of this preprocessing pipeline was used in [this](https://www.frontiersin.org/articles/10.3389/frvir.2022.964754/full) research paper. Please feel free to use it for any academic or commercial projects, and consider citing the paper:

Pinilla, A., Voigt-Antons, J. N., Garcia, J., Raffe, W., & Möller, S. (2023). Real-time affect detection in virtual reality: a technique based on a three-dimensional model of affect and EEG signals. Frontiers in Virtual Reality, 3, 964754. https://doi.org/10.3389/frvir.2022.964754

```
@article{pinilla_real-time_2023,
	title = {Real-time affect detection in virtual reality: a technique based on a three-dimensional model of affect and {EEG} signals},
	volume = {3},
	issn = {2673-4192},
	shorttitle = {Real-time affect detection in virtual reality},
	url = {https://www.frontiersin.org/articles/10.3389/frvir.2022.964754/full},
	doi = {10.3389/frvir.2022.964754},
	urldate = {2024-01-29},
	journal = {Frontiers in Virtual Reality},
	author = {Pinilla, Andres and Voigt-Antons, Jan-Niklas and Garcia, Jaime and Raffe, William and Möller, Sebastian},
	month = jan,
	year = {2023},
	pages = {964754},
	file = {Full Text:/Users/aepinilla/Zotero/storage/XF5NBVSX/Pinilla et al. - 2023 - Real-time affect detection in virtual reality a t.pdf:application/pdf},
}
```

## Installation
1. Clone this repository
```
git clone git@github.com:aepinilla/preprocess_eeg.git
```
2. Install the required libraries
```
poetry install
```
5. Download the data folder to the root of the project. The data folder is available [here](https://drive.google.com/drive/folders/1tCpIKOqNX8GkNTFijNCGq36yR6OsGGYl?usp=share_link).
6. Run the script using the following command:
```
python main.py
```

## Settings
The default settings of this script work with a sample XDF file taken from the paper mentioned above. You can change
the settings to use it with your XDF files.

To customise it, please do the following:
1. Go to src/settings.py and adjust the values according to the characteristics of your XDF file. 
```
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

# The name of the XDF file (usually generated with LSL LabRecorder)
file_name = "PJGHY.xdf"
```

2. Go to src/preprocess_eeg.py and customise the Match-Case statement according to your streams.
```
match self.streams[i]['info']['name'][0]:
    # EDIT ACCORDING TO THE NUMBER OF STREAMS STORED IN YOUR XDF FILE
    case STREAMS_NAMES.ecg:
        self.streams_index['ecg'] = i
    case STREAMS_NAMES.eeg:
        self.streams_index['eeg'] = i
    case STREAMS_NAMES.markers:
        self.streams_index['markers'] = i
```

## Python version
Tested on Python 3.11.7

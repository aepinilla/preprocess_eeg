# Preprocess EEG
Simple Python script for preprocessing EEG signals stored in an XDF file


## Introduction
This is a simple Python project that demonstrates how to conduct basic signal
preprocessing steps on data stored in a XDF file. XDF is the file format
commonly used to store data streamed over LabStreamingLayer (LSL). 

## Installation
1. Clone this repository
```
git clone git@github.com:aepinilla/preprocess_eeg.git
```
2. Install the required libraries
```
pip install -r requirements. txt
```
3. Go to the folder where the libraries are stored in your computer. For example, if you are using Conda, they 
should be stored in:
```
/Users/USERNAME/anaconda3/envs/preprocess_eeg/lib/python3.11/site-packages 
```
4. Go to the folder "asrpy" and replace the files "asr_utils.py" and "asr.py" with the files in this fork: https://github.com/aepinilla/asrpy/tree/main/asrpy
5. Download the data folder to the root of the project. The data folder is available [here](https://drive.google.com/drive/folders/1tCpIKOqNX8GkNTFijNCGq36yR6OsGGYl?usp=share_link) 
6. Run the project using the following command:
```
python main.py
```
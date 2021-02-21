# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:42:25 2020

@author: leojack
"""
from tkinter import filedialog 
import mne
import matplotlib.pyplot as plt
import seaborn as sns
import math
import pandas as pd
import numpy as np
#### IMPORT BRAINVISION DATA
data = filedialog.askopenfilename()
raw = mne.io.read_raw_brainvision(data,  preload=True)

######## COMMANDS TO CHECK UP
#raw.ch_names
#%matplotlib auto 
#raw.plot()
#raw.plot_psd()
#epochs['rest'].plot_psd(fmax=30, average=False)
#raw.plot_sensors(show_names=True, to_sphere=True)
################

##### RENAME CHANNELS
def renamer(raw):
    a = raw.ch_names
    b = ['F3','F4','FC5', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4','FC6','C5','C3','C1','Cz', 'C2', 'C4', 'C6', 'CP5', 'CP3','CP1', 'CPz','CP2','CP4','CP6', 'P5', 'P3', 'P1', 'Pz', 'P2','P4', 'P6']
    newch ={}
    for i in range(30):
        ch = {a[i]:b[i]}
        newch.update(ch)
    raw.rename_channels(newch)
    return raw
renamer()

#### PREPROCESSING
montage = mne.channels.make_standard_montage('standard_1020')
raw.set_montage(montage);
raw.filter(0.1, 30, fir_design='firwin', skip_by_annotation='edge')

events, ids = mne.events_from_annotations(raw)
events = mne.pick_events(events, exclude=[99999])
del ids['New Segment/']
ids['vibro'] = ids.pop('1/Key Space')
ids['rest'] = ids.pop('2/cond2')

epochs = mne.Epochs(raw, events, event_id=ids, tmin=0.0, tmax=5.0, baseline=(0, 0), preload=True)      

##### SPECTRAL ANALISYS
psds_rst_full, ffreqs = mne.time_frequency.psd_welch(epochs['rest'],fmin = 1, fmax = 30, n_fft=500, n_overlap=500*0.8)
psds_ts_full, ffreqs = mne.time_frequency.psd_welch(epochs['vibro'], fmin = 1, fmax = 30, n_fft=500, n_overlap=500*0.8)

#### TOPOMAP
psds_rst, freqs = mne.time_frequency.psd_welch(epochs['rest'],fmin = 11, fmax = 13, n_fft=500, n_overlap=500*0.8)
psds_ts, freqs = mne.time_frequency.psd_welch(epochs['vibro'], fmin = 11, fmax = 13, n_fft=500, n_overlap=500*0.8)


rst_mean = psds_rst.mean(0).mean(1)
vibro_mean = psds_ts.mean(0).mean(1)
erd = (rst_mean-vibro_mean)/rst_mean*100
mne.viz.plot_topomap(erd,raw.info)

#### SPECTRUM
sns.lineplot(x=ffreqs, y=psds_rst_full.mean(0)[10],color='black', label="rest", linewidth=1.5)
sns.lineplot(x=ffreqs, y=psds_ts_full.mean(0)[10], color='red', label="tactile_stimulation", linewidth=1.5)






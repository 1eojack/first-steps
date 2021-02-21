# -*- coding: utf-8 -*-
"""
for 1 REC ANALYSIS
@author: leoja
"""
from BCI2kReader import BCI2kReader as b2k
from tkinter import filedialog
import numpy as np
import pandas as pd
import mne
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
#### LEGO
def dat2mne (data):
    dat = b2k.BCI2kReader(data)
    eeg = dat.signals
    meta = dat.states
    trig = meta['StimulusCode']
    raweeg = np.concatenate((trig, eeg), axis=0);
    ch_names = ['st','F3','F4','FC5', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4','FC6','C5','C3','C1','Cz', 'C2', 'C4', 'C6', 'CP5', 'CP3','CP1', 'CPz','CP2','CP4','CP6', 'P5', 'P3', 'P1', 'Pz', 'P2','P4', 'P6']
    ch_type = ['stim'] + ['eeg']*30
    info = mne.create_info(ch_names,montage = 'easycap-M1', sfreq=500.0, ch_types=ch_type)
    raweeg = mne.io.RawArray(raweeg,info,verbose=False)
    return raweeg
#### OPENING
rec1 = filedialog.askopenfilename() #запросить файл
print('File_1 is opened')
#### CREATING RAW
raweeg = dat2mne(rec1)
##### PREPROC
mne.set_eeg_reference(raweeg);
raweeg.filter(0.1, 30, fir_design='firwin', skip_by_annotation='edge')
events = mne.find_events(raweeg, initial_event = True);
event_id = dict(fes=1, rest=2, before=3, after=4)
epochs1 = mne.Epochs(raweeg, events, event_id, tmin=0.0, tmax=3.0, baseline=(0, 0), preload=True)      
####### MULTITAPER FULL SPECTRUM
def multitaper(eeg):
    for key in event_id:
        psds, freqs = mne.time_frequency.psd_multitaper(eeg[key],fmin = 1, fmax = 30, picks=[10])
        psds = 10. * np.log10(psds)
        aver = psds.mean(0).mean(0)
        t = sns.lineplot(x=freqs, y=aver, label=key)
    return t
####### SPECTRAL ANALYSIS ERD 
def welch():
    rst, freqs = mne.time_frequency.psd_welch(epochs1['rest'],fmin = 7, fmax = 15, n_fft=500, n_overlap=500*0.9, picks=[11])
    rst = rst.mean(0).mean(0)
#   spectrum=np.array([[rst],[freqs]])
    w = sns.lineplot(x=freqs, y=rst, color='black', label='REST')
    return w

plt.subplots()
t = multitaper(epochs1)
plt.subplots()
w = welch()

def erdmaker(data, fmin, fmax):    
    psds_rst, freqs = mne.time_frequency.psd_welch(data['rest'],fmin = fmin, fmax = fmax, n_fft=500, n_overlap=500*0.9)
    psds_b, freqs = mne.time_frequency.psd_welch(data['before'], fmin = fmin, fmax = fmax, n_fft=500, n_overlap=500*0.9)
    psds_a, freqs = mne.time_frequency.psd_welch(data['after'], fmin = fmin, fmax = fmax, n_fft=500, n_overlap=500*0.9)
    psds_f, freqs = mne.time_frequency.psd_welch(data['fes'], fmin = fmin, fmax = fmax, n_fft=500, n_overlap=500*0.9)
    ####### AVERAGING
    rst_mean = psds_rst.mean(0)
    before_mean = psds_b.mean(0)
    after_mean = psds_a.mean(0)
    fes_mean = psds_f.mean(0)
    ####### ERD 
    erd_b = (rst_mean-before_mean)/rst_mean*100
    erd_a = (rst_mean-after_mean)/rst_mean*100
    erd_f = (rst_mean-fes_mean)/rst_mean*100
    erds = np.concatenate((erd_b,erd_f,erd_a), axis=1)
    return erds
erds1 = erdmaker(epochs1,11,11)
def map(ERD):
    conds = ['mi_before', 'mi_fes', 'mi_after']
    fig, axes = plt.subplots(figsize=(7.5, 2.5), ncols=3)
    for ax, i, extr in zip(axes, range(3), conds):
        mne.viz.plot_topomap(ERD[:,i],raweeg.info, axes=ax, show = True)
        ax.set_title(extr, fontsize=14)
    return fig, axes
fig, axes=map(erds1)
##### SECOND REC FAST ANAL
stop
rec2 = filedialog.askopenfilename() #запросить файл
print('File_2 is opened')
raweeg2 = dat2mne(rec2)
mne.set_eeg_reference(raweeg2);
raweeg2.filter(0.1, 30, fir_design='firwin', skip_by_annotation='edge')
events2 = mne.find_events(raweeg2, initial_event = True);
epochs2 = mne.Epochs(raweeg2, events, event_id, tmin=0.0, tmax=3.0, baseline=(0, 0), preload=True)      
erds2 = erdmaker(epochs2,11,11)
fig, axes=map(erds2)
######
fig.suptitle('subj^py, n=20', va='bottom', fontsize=16)
erds = (erds1+erds2)/2
fig, axes = map(erds)
#####
eegch = ['F3','F4','FC5', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4','FC6','C5','C3','C1','Cz', 'C2', 'C4', 'C6', 'CP5', 'CP3','CP1', 'CPz','CP2','CP4','CP6', 'P5', 'P3', 'P1', 'Pz', 'P2','P4', 'P6']
conds = ['mi_before', 'mi_fes', 'mi_after']
erds = pd.DataFrame(erds, index=eegch, columns=conds)
erds['subj'] = pd.Series(30*['nt'], index=eegch)
erds["ch"] = erds.index        
erds.to_excel('C:/data/tms_fes_erd/nt/nt_mi.xlsx', engine='xlsxwriter')
print('SAVED')
#long = pd.wide_to_long(erds, stubnames='mi', i='ch', j='cond', sep='_', suffix='\w+')
#long = long.reset_index()
#sns.barplot(x="ch", y="mi", hue="cond", data=long)

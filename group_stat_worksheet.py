# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 16:17:38 2020

@author: leoja
"""
from tkinter import filedialog
import pandas as pd
import seaborn as sns
rec1 = filedialog.askopenfilename() #запросить файл
#for in range(4):

fp = pd.read_excel('C:/data/gamesystems/RES/lateralization.xlsx', sheet_name=0)
af = pd.read_excel('C:/data/gamesystems/RES/lateralization.xlsx', sheet_name=1)
f34 = pd.read_excel('C:/data/gamesystems/RES/lateralization.xlsx', sheet_name=2)
f78 = pd.read_excel('C:/data/gamesystems/RES/lateralization.xlsx', sheet_name=3)
f910 = pd.read_excel('C:/data/gamesystems/RES/lateralization.xlsx', sheet_name=4)
data = pd.read_excel('C:/data/gamesystems/RES/lateralization.xlsx', sheet_name=5)
scores = pd.read_excel('C:/data/gamesystems/RES/lateralization.xlsx', sheet_name=6)


sns.barplot(x='cond', y='lat', hue='subj', data=scores)



def statistics():
    from scipy import stats
    afriedman = []
    tfriedman = []
    for i in [fp, af, f34, f78, f910]:
        print(i)
        stat, alpha_p = stats.friedmanchisquare(i['alpha_like'], i['alpha_dislike'], i['alpha_n'])
        stat, theta_p = stats.friedmanchisquare(i['theta_like'], i['theta_dislike'], i['theta_n'])
        afriedman.append(alpha_p)
        tfriedman.append(theta_p)
    friedman = pd.DataFrame(data=(afriedman, tfriedman), index=None).T
    return friedman

d = statistics()

af2 = pd.DataFrame([af['alpha_like'],af['alpha_dislike'],af['alpha_n']]).T
f78a = pd.DataFrame([f78['alpha_like'],f78['alpha_dislike'],f78['alpha_n']]).T
f78t = pd.DataFrame([f78['theta_like'],f78['theta_dislike'],f78['theta_n']]).T
f910t = pd.DataFrame([f910['theta_like'],f910['theta_dislike'],f910['theta_n']]).T
long = pd.read_excel('C:/data/gamesystems/RES/lateralization.xlsx', sheet_name=6).dropna


w = f78a.mean(axis=1)

sns.set_style("darkgrid")
sns.set_context("notebook", font_scale=1.5)
clr = ['#ff69b4','#f1a340','#f7f7f7','#998ec3']
sns.set_palette(clr)
img = [af2, f78a, f78t, f910t]
names = ['af2','f78a', 'f78t', 'f910t']
import matplotlib.pyplot as plt
for i,j in zip(img, names):
    plt.figure()
    sns.set_style("darkgrid")
    sns.set_palette(clr)
    g = sns.boxplot(data=i)
    filename='C:/data/gamesystems/RES/'+j+'.png'
    print(filename)
    plt.savefig(filename, dpi=300, format='png', transparent=True)

sns.boxplot(data=af2)
sns.boxplot(data=f78a) 
sns.boxplot(data=f78t) 
sns.boxplot(data=f910t) 


stats.wilcoxon(af['alpha_like'],af['alpha_dislike']) #p = 0.075
stats.wilcoxon(af['alpha_n'],af['alpha_dislike'])    #p = 0.53
stats.wilcoxon(af['alpha_like'],af['alpha_n'])       #p = 0.075   

stats.wilcoxon(f78['alpha_like'],f78['alpha_dislike'])  #p = 0.33
stats.wilcoxon(f78['alpha_n'],f78['alpha_dislike'])     #p = 0.007  
stats.wilcoxon(f78['alpha_like'],f78['alpha_n'])        #p = 0.33

stats.wilcoxon(f78['theta_like'],f78['theta_dislike'])  #p = 0.93
stats.wilcoxon(f78['theta_n'],f78['theta_dislike'])     #p = 0.02  
stats.wilcoxon(f78['theta_like'],f78['theta_n'])        #p = 0.06

stats.wilcoxon(f910['theta_like'],f910['theta_dislike'])  #p = 0.09
stats.wilcoxon(f910['theta_n'],f910['theta_dislike'])     #p = 0.1  
stats.wilcoxon(f910['theta_like'],f910['theta_n'])        #p = 0.53





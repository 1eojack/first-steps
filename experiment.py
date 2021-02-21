# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 14:15:46 2020

@author: leoja
"""

#coding:utf-8

import tkinter as tk
from psychopy import visual, core, event, clock
import random
#### GET SCREEN RESOLUTION
root = tk.Tk()
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
#### STIMULUS PREPARATION
stims = ['r1.mp4', 'l1.mp4', 'both1.mp4', 'r4_distr.mp4']
stims2 = ['right01.mp4','left01.mp4','both_1.mp4','right04_distr.mp4']
random.shuffle(stims2)
#a=random.sample(stims2, 40)

txt_1=u'Сейчас вам потребуется ознакомиться с видео-роликами. Как будете готовы - нажмите "пробел".'
txt_2=u'Отлично! теперь ваша задача - сыграть эти мелодии самостоятельно. Как будете готовы - нажмите "пробел".'

win = visual.Window([w, h], color=('#54C7FC'))
ISI = clock.StaticPeriod(win=win, screenHz=59, name='ISI')
                                                                    
####OPENING
txt = visual.TextStim(win, text=u'Приготовьтесь. Как будете готовы - нажмите "пробел".',font='Helvetica', pos=[0.5, 0])
txt.draw()
win.flip()
event.waitKeys(keyList=['space'])
####OBSERVATION BEFORE
movs = [visual.MovieStim3(win, i, size=[w,h]) for i in stims]



txt = visual.TextStim(win, text=txt_1,font='Helvetica', pos=[0.5, 0])
txt.draw()
win.flip()
event.waitKeys(keyList=['space'])


for mov in movs:
    
    while mov.status != visual.FINISHED:
        mov.draw()
        win.flip()

    win.flip()
    ISI.start(3)
    ISI.complete()
    
    
txt = visual.TextStim(win, text=txt_1, font='Helvetica', pos=[0.5, 0], height=0.5)
txt.draw()
win.flip()
event.waitKeys(keyList=['space'])


####MAIN EXPERIMENT SEQUENCE

#movs = [visual.MovieStim3(win, i, size=[w,h]) for i in stims2]
#for mov in movs:
#    while mov.status != visual.FINISHED:
#        mov.draw()
#        win.flip()
#
#    win.flip()
##    event.waitKeys()


win.close()
core.quit()



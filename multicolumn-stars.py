# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 08:30:39 2024

@author: JMCasado
"""

#General import
import os
import argparse
import glob
import numpy as np
import datetime
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import math
import pandas as pd

#Local import
from data_transform import smooth
from data_import.data_import import DataImport
from sound_module.simple_sound import simpleSound
from data_transform.predef_math_functions import PredefMathFunctions

# Instanciate the sonoUno clases needed
_dataimport = DataImport()
_simplesound = simpleSound()
_math = PredefMathFunctions()
# Sound configurations, predefined at the moment
_simplesound.reproductor.set_continuous()
_simplesound.reproductor.set_waveform('sine') # piano; sine
_simplesound.reproductor.set_time_base(0.03)
_simplesound.reproductor.set_min_freq(380)
_simplesound.reproductor.set_max_freq(800)
# The argparse library is used to pass the path and extension where the data
# files are located
parser = argparse.ArgumentParser()
# Receive the extension from the arguments
parser.add_argument("-t", "--file-type", type=str,
                    help="Select file type.",
                    choices=['csv', 'txt'])
# Receive the directory path from the arguments
parser.add_argument("-d1", "--directory1", type=str,
                    help="Indicate a directory to process as batch.")
#parser.add_argument("-d2", "--directory2", type=str,
#                    help="Indicate a directory to process as batch.")
#parser.add_argument("-d3", "--directory3", type=str,
#                    help="Indicate a directory to process as batch.")
#parser.add_argument("-d4", "--directory4", type=str,
#                    help="Indicate a directory to process as batch.")
# Indicate to save or not the plot
parser.add_argument("-p", "--save-plot", type=bool,
                    help="Indicate if you want to save the plot (False as default)",
                    choices=[False,True])
# Indicate if the user want to reproduce the data
parser.add_argument("-rep", "--play-dataset", type=bool,
                    help="Indicate if you want to reproduce the multimodal display (False as default)",
                    choices=[False,True])
# Alocate the arguments in variables, if extension is empty, select txt as
# default
args = parser.parse_args()
ext = args.file_type or 'txt'
#path = args.directory
path1 = args.directory1
#path2 = args.directory2
#path3 = args.directory3
#path4 = args.directory4
plot_flag = args.save_plot or True
play_flag = args.play_dataset or True
# Print a messege if path is not indicated by the user
if not path1:
    print('1At least on intput must be stated.\nUse -h if you need help.')
    exit()
#if not path2:
#    print('2At least on intput must be stated.\nUse -h if you need help.')
#    exit()
#if not path3:
#    print('3At least on intput must be stated.\nUse -h if you need help.')
#    exit()
#if not path4:
#    print('4At least on intput must be stated.\nUse -h if you need help.')
#    exit()
# Format the extension to use it with glob
extension = '*.' + ext

# Initialize a counter to show a message during each loop
i = 1
if plot_flag:
    # Create an empty figure or plot to save it
    cm = 1/2.54  # centimeters in inches
    #fig = plt.figure(figsize=(15*cm, 10*cm), dpi=300)
    fig = plt.figure()
    # Defining the axes so that we can plot data into it.
    #ax = plt.axes()
#Inits to generalize

# Loop to walk the directory and sonify each data file
now = datetime.datetime.now()
print(now.strftime('%Y-%m-%d_%H-%M-%S'))

# Open each file
dataO5, status, msg = _dataimport.set_arrayfromfile('data/O5.txt', ext)
dataA5, status, msg = _dataimport.set_arrayfromfile('data/A5.txt', ext)
dataG0, status, msg = _dataimport.set_arrayfromfile('data/G0.txt', ext)
data1, status, msg = _dataimport.set_arrayfromfile(path1, ext)
# Convert into numpy, split in x and y and normalyze
if dataO5.shape[1]<2:
    print("Error reading file 2, only detect one column.")
    exit()
if dataA5.shape[1]<2:
    print("Error reading file 3, only detect one column.")
    exit()
if dataG0.shape[1]<2:
    print("Error reading file 4, only detect one column.")
    exit()
if data1.shape[1]<2:
    print("Error reading file 1, only detect one column.")
    exit()
# Extract the names and turn to float
data_floatO5 = dataO5.iloc[1:, 1:].astype(float)
data_floatA5 = dataA5.iloc[1:, 1:].astype(float)
data_floatG0 = dataG0.iloc[1:, 1:].astype(float)
data_float1 = data1.iloc[1:, 1:].astype(float)

#Inicializamos la posición para no tener error cuando no haya recortes
x_pos_min = 0

# Select wavelengh to cut
abs_val_array = np.abs(data_floatO5.loc[:,1] - 3700)
x_pos_min = abs_val_array.idxmin()
abs_val_array = np.abs(data_floatO5.loc[:,1] - 4700)
x_pos_max = abs_val_array.idxmin()
# Cut first data set
data_floatO5 = dataO5.iloc[x_pos_min:x_pos_max, :].astype(float)
# Cut second data set
data_floatA5 = dataA5.iloc[x_pos_min:x_pos_max, :].astype(float)
# Cut third data set
data_floatG0 = dataG0.iloc[x_pos_min:x_pos_max, :].astype(float)
# Cut fourth data set
data_float1 = data1.iloc[x_pos_min:x_pos_max, :].astype(float)

# Generate the plot if needed
if plot_flag:
    # Configure axis, plot the data and save it
    # Erase the plot
    #ax.cla()
    
    #First plot
    ax1 = plt.subplot(311)
    ax1.plot(data_floatO5.loc[:,1], data_floatO5.loc[:,2], label='O5 V')
    ax1.plot(data_float1.loc[:,1], data_float1.loc[:,2], label='Unknown')
    # make these tick labels invisible
    ax1.tick_params('x', labelbottom=False)

    # Second plot
    ax2 = plt.subplot(312, sharex=ax1)
    ax2.plot(data_floatA5.loc[:,1], data_floatA5.loc[:,2], label='A5 V')
    ax2.plot(data_float1.loc[:,1], data_float1.loc[:,2], label='Unknown')
    # make these tick labels invisible
    ax2.tick_params('x', labelbottom=False)

    # Third plot
    ax3 = plt.subplot(313, sharex=ax1, sharey=ax1)
    ax3.plot(data_floatG0.loc[:,1], data_floatG0.loc[:,2], label='G0 V')
    ax3.plot(data_float1.loc[:,1], data_float1.loc[:,2], label='Unknown')
    
    ax1.legend()
    ax2.legend()
    ax3.legend()
    plt.pause(0.05)
    # Set the path to save the plot and save it
    plot_path = path1[:-6] + 'plot.png'
    fig.savefig(plot_path)
    
# Reproduction
# Normalize the data to sonify
xO5, yO5, status = _math.normalize(data_floatO5.loc[:,1], data_floatO5.loc[:,2], init=x_pos_min)
xA5, yA5, status = _math.normalize(data_floatA5.loc[:,1], data_floatA5.loc[:,2], init=x_pos_min)
xG0, yG0, status = _math.normalize(data_floatG0.loc[:,1], data_floatG0.loc[:,2], init=x_pos_min)
x1, y1, status = _math.normalize(data_float1.loc[:,1], data_float1.loc[:,2], init=x_pos_min)

if play_flag:
    """From here to save sound could be comented if the reproduction is not needed"""
    # Reproduction
    minvalO5 = float(data_floatO5.loc[:,2].min())
    maxvalO5 = float(data_floatO5.loc[:,2].max())
    minvalA5 = float(data_floatA5.loc[:,2].min())
    maxvalA5 = float(data_floatA5.loc[:,2].max())
    minvalG0 = float(data_floatG0.loc[:,2].min())
    maxvalG0 = float(data_floatG0.loc[:,2].max())
    minval1 = float(data_float1.loc[:,2].min())
    maxval1 = float(data_float1.loc[:,2].max())

    # To make reproduction on real time
    ordenadaO5 = np.array([min(minvalO5,minval1), max(maxvalO5,maxval1)])
    ordenadaA5 = np.array([min(minvalA5,minval1), max(maxvalA5,maxval1)])
    ordenadaG0 = np.array([min(minvalG0,minval1), max(maxvalG0,maxval1)])

    input("Press Enter to continue...")

    for i in range (1, 4):
        print(i)
        for x in range (x_pos_min, x_pos_max):
            if i==1:
                # Plot the position line
                if not x == x_pos_min:
                    line = red_line.pop(0)
                    line.remove()
                abscisa = np.array([float(data_floatO5.loc[x,1]), float(data_floatO5.loc[x,1])])
                red_line = ax1.plot(abscisa, ordenadaO5, 'r')
                plt.pause(0.05)
                # Make the sound
                _simplesound.reproductor.set_waveform('sine')
                _simplesound.make_sound(yO5[x], 1)
                _simplesound.reproductor.set_waveform('flute')
                _simplesound.make_sound(y1[x], 1)
                if x == (x_pos_max-1):
                    line = red_line.pop(0)
                    line.remove()
            if i==2:
                # Plot the position line
                if not x == x_pos_min:
                    line = red_line.pop(0)
                    line.remove()
                abscisa = np.array([float(data_floatA5.loc[x,1]), float(data_floatA5.loc[x,1])])
                red_line = ax2.plot(abscisa, ordenadaA5, 'r')
                plt.pause(0.05)
                # Make the sound
                _simplesound.reproductor.set_waveform('sine')
                _simplesound.make_sound(yA5[x], 1)
                _simplesound.reproductor.set_waveform('flute')
                _simplesound.make_sound(y1[x], 1)
                if x == (x_pos_max-1):
                    line = red_line.pop(0)
                    line.remove()
            if i==3:
                # Plot the position line
                if not x == x_pos_min:
                    line = red_line.pop(0)
                    line.remove()
                abscisa = np.array([float(data_floatG0.loc[x,1]), float(data_floatG0.loc[x,1])])
                red_line = ax3.plot(abscisa, ordenadaG0, 'r')
                plt.pause(0.05)
                # Make the sound
                _simplesound.reproductor.set_waveform('sine')
                _simplesound.make_sound(yG0[x], 1)
                _simplesound.reproductor.set_waveform('flute')
                _simplesound.make_sound(y1[x], 1)
                if x == (x_pos_max-1):
                    line = red_line.pop(0)
                    line.remove()
# Save sound
wav_nameO5 = path1[:-6] + 'O5.wav'
wav_nameA5 = path1[:-6] + 'A5.wav'
wav_nameG0 = path1[:-6] + 'G0.wav'
_simplesound.save_sound(wav_nameO5, data_floatO5.loc[:,1], yO5, init=x_pos_min) 
_simplesound.save_sound(wav_nameA5, data_floatA5.loc[:,1], yA5, init=x_pos_min)
_simplesound.save_sound(wav_nameG0, data_floatG0.loc[:,1], yG0, init=x_pos_min)
wav_nameO5Unk = path1[:-6] + 'O5-unknown.wav'
wav_nameA5Unk = path1[:-6] + 'A5-unknown.wav'
wav_nameG0Unk = path1[:-6] + 'G0-unknown.wav'
_simplesound.save_sound_multicol_stars(wav_nameO5Unk, data_floatO5.loc[:,1], yO5, y1, init=x_pos_min) 
_simplesound.save_sound_multicol_stars(wav_nameA5Unk, data_floatA5.loc[:,1], yA5, y1, init=x_pos_min)
_simplesound.save_sound_multicol_stars(wav_nameG0Unk, data_floatG0.loc[:,1], yG0, y1, init=x_pos_min)
# Print time
now = datetime.datetime.now()
print(now.strftime('%Y-%m-%d_%H-%M-%S'))
if plot_flag or play_flag:
    plt.pause(0.5)
    # Showing the above plot
    plt.show()
    plt.close()

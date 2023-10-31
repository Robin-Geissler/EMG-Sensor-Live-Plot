# This is a sample Python script.
import sys

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import serial
import numpy as np
import matplotlib.pyplot as plt
import threading
import atexit
import csv
import time
from statistics import mean
import os

from pynput.keyboard import Key, Listener



window_size = 50
window_size_SLOW = 10000
data_points = 1000
SLOW_count = 0
"""" Sampling Frequeny in Hz"""
fs = 1000
THREAD_CLOSE = False
LOCK_MEAN_FREQ = False

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.

def exit_csv_close():
    global csv_file, THREAD_CLOSE
    THREAD_CLOSE = True
    time.sleep(1)
    csv_file.close()

# def on_release(key):
#     if key == Key.esc:
#         print('Exiting...')
#         sys.exit()

 # with Listener(on_release=on_release) as listener:
    #     listener.join()

def calc_mean_freq(y,fs):
    global mean_freq
    spec = np.abs(np.fft.rfft(y))
    freq = np.fft.rfftfreq(len(y), d=1 / fs)
    amp = spec / spec.sum()
    mean_freq = (freq * amp).sum()
    print(str(mean_freq))

def calc_avg(y,window_size):
    global avg
    avg = round(np.sum(y[0: window_size]) / window_size, 2)

def calc_rms(y, window_size):
    global rms
    rms = round(np.sqrt(np.sum(np.square(y[0: window_size])) / window_size), 2)


def calc_rms_slow(y, window_size):
    global rms_slow
    rms_slow = round(np.sqrt(np.sum(np.square(y[0: window_size])) / window_size), 2)

def calc_mav(y, window_size):
    global mav
    mav = round(np.sum(abs(y[0: window_size])) / window_size, 2)


def read_data():
    global y, y_filtered, y_RMS, y_MAV
    global y_filtered_SLOW, y_RMS_SLOW_LARGE_FILTER, y_RMS_SLOW, y_MAV_SLOW
    global avg_thread,rms_thread,rms_slow_thread, mav_thread, mean_freq_thread
    global avg, rms, rms_slow, mav, mean_freq
    global SLOW_count
    global start_time

    while True:
        new_data = int.from_bytes(ser.read(4), byteorder='little', signed=True)

        with data_lock:
            y = np.roll(y,1)
            y[0] = new_data
            writer.writerow([str(time.time() - start_time), str(new_data)])

        """ time and frquency domain threads will be used by data_thread """
        """ time domain calculations"""
        avg_thread = threading.Thread(target=calc_avg, daemon=True, args=(y, window_size))
        avg_thread.start()
        rms_thread = threading.Thread(target=calc_rms, daemon=True, args=(y, window_size))
        rms_thread.start()
        rms_slow_thread = threading.Thread(target=calc_rms_slow, daemon=True, args=(y, window_size_SLOW))
        rms_slow_thread.start()
        mav_thread = threading.Thread(target=calc_mav, daemon=True, args=(y, window_size))
        mav_thread.start()
        """ frequency domain calculations """
        mean_freq_thread = threading.Thread(target=calc_mean_freq, daemon=True, args=(y, fs))
        mean_freq_thread.start()


        #print(new_average)



        with data_lock:
            y_filtered = np.roll(y_filtered,1)
            avg_thread.join()
            y_filtered[0] = avg

            y_RMS = np.roll(y_RMS,1)
            rms_thread.join()
            y_RMS[0] = rms

            y_MAV = np.roll(y_MAV,1)
            mav_thread.join()
            y_MAV[0] = mav



        if(SLOW_count > 200):
            SLOW_count = 0
            with data_lock:
                y_filtered_SLOW = np.roll(y_filtered_SLOW,1)
                y_filtered_SLOW[0] = avg

                y_RMS_SLOW = np.roll(y_RMS_SLOW,1)
                y_RMS_SLOW[0] = rms

                y_MAV_SLOW = np.roll(y_MAV_SLOW,1)
                y_MAV_SLOW[0] = mav

                y_RMS_SLOW_LARGE_FILTER = np.roll(y_RMS_SLOW_LARGE_FILTER, 1)
                rms_slow_thread.join()
                y_RMS_SLOW_LARGE_FILTER[0] = rms_slow
        else:
            SLOW_count = SLOW_count + 1
        if THREAD_CLOSE:
            return



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


    ser = serial.Serial(port='COM3', baudrate=115200)
    print('configured')

    #######################################################################################################################
        # Fast plot preparation
    #######################################################################################################################


    x = np.linspace(0, data_points - 1, data_points)

    y = np.zeros(data_points, dtype=np.int32)
    y_filtered = np.zeros(data_points, dtype=np.int32)
    y_RMS = np.zeros(data_points, dtype=np.int64)
    y_MAV = np.zeros(data_points, dtype=np.int32)


    fig = plt.figure(figsize=(20, 12))
    ax = fig.add_subplot(1, 1, 1)  # hier größe festlegen

    (ln,) = ax.plot(x, y, animated=True)
    (ln_filtered,) = ax.plot(x, y_filtered, label='Filtered Data', animated=True)
    (ln_RMS,) = ax.plot(x, y_RMS, label='RMS Data', animated=True)
    (ln_MAV,) = ax.plot(x, y_MAV, label='MAV Data', animated=True)
    ax.set_ylim(-500, 750)

#######################################################################################################################
# Slow plot preparation
#######################################################################################################################
    x_SLOW = np.linspace(0, data_points - 1, data_points)
    y_filtered_SLOW = np.zeros(data_points, dtype=np.int32)
    y_RMS_SLOW = np.zeros(data_points, dtype=np.int64)
    y_RMS_SLOW_LARGE_FILTER = np.zeros(data_points, dtype=np.int64)
    y_MAV_SLOW = np.zeros(data_points, dtype=np.int32)

    y_mean_freq_slow = np.zeros(data_points, dtype=np.int32)

    fig_SLOW = plt.figure(figsize=(20, 12))
    ax_SLOW = fig_SLOW.add_subplot(1, 1, 1)  # hier größe festlegen
    (ln_filtered_SLOW,) = ax_SLOW.plot(x_SLOW, y_filtered_SLOW, label='Filtered Data', animated=True)
    (ln_RMS_SLOW,) = ax_SLOW.plot(x_SLOW, y_RMS_SLOW, label='RMS Data', animated=True)
    (ln_RMS_SLOW_LARGE_FILTER,) = ax_SLOW.plot(x_SLOW, y_RMS_SLOW_LARGE_FILTER, label='RMS Data Filtered', animated=True)
    (ln_MAV_SLOW,) = ax_SLOW.plot(x_SLOW, y_MAV_SLOW, label='MAV Data', animated=True)
    (ln_mean_freq_slow,) = ax_SLOW.plot(x_SLOW, y_mean_freq_slow, label='Mean Freq', animated=True)

    ax_SLOW.set_ylim(-20, 250)

#######################################################################################################################
# Draw plots
#######################################################################################################################
    plt.legend()

    plt.show(block=False)
    plt.pause(0.1)
    bg = fig.canvas.copy_from_bbox(fig.bbox)
    bg_SLOW = fig_SLOW.canvas.copy_from_bbox(fig_SLOW.bbox)

    ax.draw_artist(ln)
    ax.draw_artist(ln_filtered)
    ax.draw_artist(ln_RMS)
    ax.draw_artist(ln_MAV)

    ax_SLOW.draw_artist(ln_filtered_SLOW)
    ax_SLOW.draw_artist(ln_RMS_SLOW)
    ax_SLOW.draw_artist(ln_MAV_SLOW)
    ax_SLOW.draw_artist(ln_RMS_SLOW_LARGE_FILTER)
    ax_SLOW.draw_artist(ln_mean_freq_slow)

    fig.canvas.blit(fig.bbox)
    fig_SLOW.canvas.blit(fig_SLOW.bbox)

#######################################################################################################################
# Prepare CSV File
#######################################################################################################################
    csv_file = open('readings.csv', 'w')
    writer = csv.writer(csv_file)
    atexit.register(exit_csv_close)


    writer.writerow(['time', 'y'])
    start_time = time.time()

#######################################################################################################################
# Thread setup
#######################################################################################################################
    avg = 0
    rms = 0
    rms_slow = 0
    mav = 0
    mean_freq = 0



    # Define a lock for synchronization
    data_lock = threading.Lock()

    data_thread = threading.Thread(target=read_data, daemon=True)
    data_thread.start()





    while True:
        fig.canvas.restore_region(bg)
        fig_SLOW.canvas.restore_region(bg_SLOW)

        ln.set_ydata(y)
        ln_filtered.set_ydata(y_filtered)
        ln_RMS.set_ydata(y_RMS)
        ln_MAV.set_ydata(y_MAV)
        ax.draw_artist(ln)
        ax.draw_artist(ln_filtered)
        ax.draw_artist(ln_RMS)
        ax.draw_artist(ln_MAV)

        ln_filtered_SLOW.set_ydata(y_filtered_SLOW)
        ln_RMS_SLOW.set_ydata(y_RMS_SLOW)
        ln_RMS_SLOW_LARGE_FILTER.set_ydata(y_RMS_SLOW_LARGE_FILTER)
        ln_MAV_SLOW.set_ydata(y_MAV_SLOW)
        ax_SLOW.draw_artist(ln_filtered_SLOW)
        ax_SLOW.draw_artist(ln_RMS_SLOW)
        ax_SLOW.draw_artist(ln_RMS_SLOW_LARGE_FILTER)
        ax_SLOW.draw_artist(ln_MAV_SLOW)
        ax_SLOW.draw_artist(ln_mean_freq_slow)



        fig.canvas.blit(fig.bbox)
        fig.canvas.flush_events()

        fig_SLOW.canvas.blit(fig_SLOW.bbox)
        fig_SLOW.canvas.flush_events()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import serial
import numpy as np
import matplotlib.pyplot as plt
import threading
import atexit
import csv
import time


# number of points to be plotted for each channel
data_points = 1000
# number of channels
CHANNELS = 8
# Flag to show if the writing thread still needs to be closed
THREAD_CLOSE = False


# x axis
x = np.linspace(0, data_points - 1, data_points)
# y original value
y_original = [np.zeros(data_points, dtype=np.float32) for _ in range(8)]
# y processed value
y_processed = [np.zeros(data_points, dtype=np.float32) for _ in range(8)]
# offsets
offset = np.zeros(8, dtype=np.float32)



def exit_csv_close():
    global csv_file, THREAD_CLOSE
    THREAD_CLOSE = True
    time.sleep(1)
    csv_file.close()



def read_data():
    global x, y_original, y_processed
    global start_time
    global offset

    while True:
        databuff = np.frombuffer(ser.read(32), dtype= np.int32)

        new_data = databuff[0]
        writer.writerow([str(time.time() - start_time), str(new_data)])

        with data_lock:
            #for i, value_i in enumerate(data_i, start=1):

            # Shift original measurement vales one to the right
            y_original = np.roll(y_original, shift=1, axis=1)
            # Fill the new first value with measurement data
            # Scaling factor = (V_ADC in mV / ADC_RES 2^24 / AMPLIFICATIO_FACTOR)
            y_original[:, 0] = databuff * (9000 / 16777216 / 24)
            # Shift processed measurement vales one to the right
            y_processed = np.roll(y_processed, shift=1, axis=1)
            # Calculate dynamic offset over average of all currently saved data points
            offset = np.round(np.mean(y_original[:, :data_points], axis=1) , 2)

            # Offset measurement data
            y_processed[:,0] = y_original[:,0] - offset


            #print(str(y[0]) + " --- " + str(y1[0]) + " --- " + str(y2[0]) + " --- " + str(y3[0]) + " --- " + str(y4[0]) + " --- " + str(y5[0]) + " --- " + str(y6[0]) + " --- " + str(y7[0]))





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Starting Visualization')


    ser = serial.Serial(port='COM5', baudrate=115200)
    print('Serial Interface Configured')

    #######################################################################################################################
        # Plot preparation
    #######################################################################################################################




    # Create Figure
    fig = plt.figure(figsize=(20, 12))

    # Create Plots for all channels
    ax = [fig.add_subplot(2, 4, i) for i in range(1, CHANNELS + 1)]

    # Create Lines for all Plots
    ln = [axi.plot(x, y_p, label = 'Channel ' + str(i), animated=True)[0] for i, (axi,y_p) in enumerate(zip(ax, y_processed),start=1)]

    # Set y axis and legend for all plots
    for axi in ax:
        axi.set_ylim(-10, 10)
        axi.legend()

    # Show the figure
    fig.show()



#######################################################################################################################
# Draw plots
#######################################################################################################################

    # Pause to update the plot display
    plt.pause(0.1)

    # Save the figure's background to optimize redrawing time for plot update
    bg = fig.canvas.copy_from_bbox(fig.bbox)

    # Draw each line on its respective axis
    for axi, lin in zip(ax, ln):
        axi.draw_artist(lin)

    # Update the figure canvas with the new drawings
    fig.canvas.blit(fig.bbox)

#######################################################################################################################
# Prepare CSV File
#######################################################################################################################
    # Open the CSV file for writing
    csv_file = open('readings.csv', 'w')

    # Create a CSV writer object
    writer = csv.writer(csv_file)

    # Register a function to close the CSV file on exit
    atexit.register(lambda: exit_csv_close())

    # Write the header row to the CSV file
    writer.writerow(['time', 'y'])

    # Record the start time for later use
    start_time = time.time()

#######################################################################################################################
# Thread setup
#######################################################################################################################

    # Define a lock to synchronize access to shared resources
    data_lock = threading.Lock()

    # Create and start a background thread to read data
    data_thread = threading.Thread(target=read_data, daemon=True)
    data_thread.start()

#######################################################################################################################
# Live plot update
#######################################################################################################################


    while True:
        # Restore the figure's background to prepare for redrawing
        fig.canvas.restore_region(bg)

        # Update each line artist with new data and draw on its axis
        for lin, y, axi in zip(ln, y_processed, ax):
            lin.set_ydata(y)
            axi.draw_artist(lin)

        # Refresh the canvas to show updated drawing
        fig.canvas.blit(fig.bbox)
        fig.canvas.flush_events()



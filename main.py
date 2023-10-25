# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import serial
import numpy as np
import matplotlib.pyplot as plt
import threading



window_size = 50
data_points = 1000





def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


    # #ser = serial.Serial( port = 'COM3', baudrate = 115200, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout=2)
    # ser = serial.Serial(port='COM3', baudrate=115200)
    # print('configured')
    #
    #
    # x = np.linspace(0,10, 500)
    # y = np.zeros(500, dtype=np.int64)
    #
    # fig, ax = plt.subplots()
    #
    # # animated=True tells matplotlib to only draw the artist when we
    # # explicitly request it
    # (ln,) = ax.plot(x, y, animated=True)
    #
    # ax.set_ylim(-20000, 20000)
    # # make sure the window is raised, but the script keeps going
    # plt.show(block=False)
    #
    # # stop to admire our empty window axes and ensure it is rendered at
    # # least once.
    # #
    # # We need to fully draw the figure at its final size on the screen
    # # before we continue on so that :
    # #  a) we have the correctly sized and drawn background to grab
    # #  b) we have a cached renderer so that ``ax.draw_artist`` works
    # # so we spin the event loop to let the backend process any pending operations
    # plt.pause(0.1)
    #
    # # get copy of entire figure (everything inside fig.bbox) sans animated artist
    # bg = fig.canvas.copy_from_bbox(fig.bbox)
    # # draw the animated artist, this uses a cached renderer
    # ax.draw_artist(ln)
    # # show the result to the screen, this pushes the updated RGBA buffer from the
    # # renderer to the GUI framework so you can see it
    # fig.canvas.blit(fig.bbox)
    #
    # while True:
    #     # reset the background back in the canvas state, screen unchanged
    #     fig.canvas.restore_region(bg)
    #     # update the artist, neither the canvas state nor the screen have changed
    #    # ln.set_ydata(int.from_bytes(ser.read(4), byteorder='little'))
    #     #ln.set_ydata(np.sin(x + int.from_bytes(ser.read(4), byteorder='little'), ))
    #     # set new y data
    #     y = np.roll(y, 1)
    #     y[0] = int.from_bytes(ser.read(4), byteorder='little', signed = True)
    #     #print(y[0])
    #     ln.set_ydata(y)
    #
    #     # re-render the artist, updating the canvas state, but not the screen
    #     ax.draw_artist(ln)
    #     # copy the image to the GUI state, but screen might not be changed yet
    #     fig.canvas.blit(fig.bbox)
    #     # flush any pending GUI events, re-painting the screen if needed
    #     fig.canvas.flush_events()
    #     # you can put a pause in if you want to slow things down
    #     # plt.pause(.1)



    ser = serial.Serial(port='COM3', baudrate=115200)
    print('configured')


    x = np.linspace(0, data_points - 1, data_points)
    y = np.zeros(data_points, dtype=np.int32)
    y_filtered = np.zeros(data_points, dtype=np.int32)
    y_RMS =  np.zeros(data_points, dtype=np.int64)
    y_MAV = np.zeros(data_points, dtype=np.int32)
    y_index = 0

    fig = plt.figure(figsize=(20,12))
    ax = fig.add_subplot(1,1,1) # hier größe festlegen
    (ln,) = ax.plot(x, y, animated=True)
    (ln_filtered,) = ax.plot(x, y_filtered, label='Filtered Data', animated=True)
    (ln_RMS,) = ax.plot(x, y_RMS, label='RMS Data', animated=True)
    (ln_MAV,) = ax.plot(x, y_MAV, label='MAV Data', animated=True)
    ax.set_ylim(-1000, 1750)

    plt.legend()
    # fig, axs = plt.subplots(2, 1, figsize=(16, 9), gridspec_kw={'height_ratios': [1, 2]})
    # axs[0].plot(y)
    # axs[1].scatter(x['level_1'], x['level_0'], c=x[0])

    plt.show(block=False)
    plt.pause(0.1)
    bg = fig.canvas.copy_from_bbox(fig.bbox)
    ax.draw_artist(ln)
    ax.draw_artist(ln_filtered)
    ax.draw_artist(ln_RMS)
    ax.draw_artist(ln_MAV)
    fig.canvas.blit(fig.bbox)

    # Define a lock for synchronization
    data_lock = threading.Lock()


    def read_data():
        global y, y_filtered, y_index, y_RMS, y_MAV
        while True:
            new_data = int.from_bytes(ser.read(4), byteorder='little', signed=True)
            new_average = round(np.sum(y[0: window_size]) / window_size, 2)
            new_RMS = round(np.sqrt(np.sum(np.square(y[0: window_size])) / window_size), 2)
            new_MAV = round(np.sum(abs(y[0: window_size])) / window_size, 2)


            print(new_average)


            with data_lock:
                y = np.roll(y,1)
                y[0] = new_data

                y_filtered = np.roll(y_filtered,1)
                y_filtered[0] = new_average

                y_RMS = np.roll(y_RMS,1)
                y_RMS[0] = new_RMS

                y_MAV = np.roll(y_MAV,1)
                y_MAV[0] = new_MAV
                #y[y_index] = new_data
                #y_index = (y_index + 1) % data_points


    data_thread = threading.Thread(target=read_data)
    data_thread.daemon = True
    data_thread.start()

    while True:
        fig.canvas.restore_region(bg)
        ln.set_ydata(y)
        ln_filtered.set_ydata(y_filtered)
        ln_RMS.set_ydata(y_RMS)
        ln_MAV.set_ydata(y_MAV)
        ax.draw_artist(ln)
        ax.draw_artist(ln_filtered)
        ax.draw_artist(ln_RMS)
        ax.draw_artist(ln_MAV)
        fig.canvas.blit(fig.bbox)
        fig.canvas.flush_events()



###############################################################
    # Create figure for plotting
#    fig = plt.figure()
#    ax = fig.add_subplot(1, 1, 1)
#    xs = []
#    ys = []




    # Set up plot to call animate() function periodically
#    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1, save_count=10000)
#    plt.show()
###############################################################



###############################################################
#    while True:
#        i = int.from_bytes(ser.read(4), byteorder='little')
#        print(i)
###############################################################



# See PyCharm help at https://www.jetbrains.com/help/pycharm/

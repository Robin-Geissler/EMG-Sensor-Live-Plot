# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import serial
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read potentials from EMG sensor
    potential = int.from_bytes(ser.read(4), byteorder='little', signed=True)
    print(potential)
    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%S.%f'))
    ys.append(potential)
    #'%H:%M:%S.%f'

    # Limit x and y lists to 20 items
    xs = xs[-200:]
    ys = ys[-200:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    #plt.xticks(rotation=90, ha='right')
    #plt.subplots_adjust(bottom=0.30)
    plt.title('EMG Measurement')
    plt.ylabel('Voltage')








def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')



    #ser = serial.Serial( port = 'COM3', baudrate = 115200, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout=2)
    ser = serial.Serial(port='COM3', baudrate=115200)
    print('configured')

    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []




    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=100, save_count=200)
    plt.show()

#    while True:
#        i = int.from_bytes(ser.read(4), byteorder='little')
#        print(i)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/

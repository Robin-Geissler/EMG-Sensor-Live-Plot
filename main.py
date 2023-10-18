# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import serial

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')



    #ser = serial.Serial( port = 'COM3', baudrate = 115200, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout=2)
    ser = serial.Serial(port='COM3', baudrate=115200)

    print('configured')
    while True:
        i = int.from_bytes(ser.read(4), byteorder='little')
        print(i)
    ser.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

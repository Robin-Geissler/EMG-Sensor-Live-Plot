# EMG Live Plotting
This is a script for live visualization of EMG data in Python. It is to be used together with this multichannel EMG sensor: [Multichannel EMG Sensor](https://github.com/Robin-Geissler/EMG-Sensor-Board)  

This script visualizes 8 channels simultaneously, and can easily be extended to more channels.
![Multichannel EMG Adapter](Figures/live_vis_signal.png "Live Visualisatioin Signal")
## Getting Started
To run a live visualization, perform the following steps:
1. Connect the Multichannel EMG over USB to the PC
2. Start the live script

## Trouble Shooting
These are known issues and solutions:
1. The script worked, but stopt operating: This happens if the EMG sensor was reset. Restart the script.
2. The USB port is incorrect: Every once in a while the USB port under which the system operates changes. Find the correct port using the device manager and update it in the source code of the script.


## License
Copyright (c) 2024 Fraunhofer EMFT

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


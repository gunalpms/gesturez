# gesturez
### Windows webcam gesture control. Tested on Windows 10 22H2.
##### ============================
#### Use your webcam to:
* Adjust volume
* Adjust brightness
* Switch apps using alt+tab 

### Usage:

Make sure python is installed and you have downloaded the source code.

Open cmd and navigate to the src direcory. Run main.py within the cmd to execute the program.

To close the camera window, open main.py and comment out lines 101 and 102 before executing.

If the brightness gesture crashes the program or doesn't work, chances are the brightness of your monitor
can't be controlled from within Windows settings. To prevent crashing, modify the contents of the brightness functions
such that the function content is only the keyword pass. The brightness functions are located in actions.py

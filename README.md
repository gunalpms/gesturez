# gesturez
### Windows webcam gesture control. Tested on Windows 10 22H2.
##### ============================
#### Use your webcam to:
* Adjust volume
* Adjust brightness
* Switch apps using alt+tab 

### Setup:

Make sure python is installed and you have downloaded the source code.

After installing python, use pip to install the dependencies. The dependencies are:

* opencv-python
* mediapipe
* pyautogui

Open cmd and navigate to the src direcory. Run main.py within the cmd to execute the program.

To close the camera window, open main.py and comment out lines 101 and 102 before executing.

If the brightness gesture crashes the program or doesn't work, chances are the brightness of your monitor
can't be controlled from within Windows settings. To prevent crashing, modify the contents of the brightness functions
such that the function content is only the keyword pass. The brightness functions are located in actions.py

### Gestures:
Hold your hand approximately 30cm from the camera for best results. 

#### 1) Adjusting volume (thumb and index finger):
_Hold close for decreasing, hold far apart for increasing. Fingers must be relatively horizontal._

![image](https://github.com/gunalpms/gesturez/assets/80674364/773fbe89-446d-49d3-a958-411cb34ea318)

#### 2) Adjusting brightness (thumb and middle finger): 
_Hold close for decreasing, hold far apart for increasing. Fingers must be relatively horizontal._

![image](https://github.com/gunalpms/gesturez/assets/80674364/95f8f5b5-62c9-4b94-9c08-dd0e9a816b7d)

#### 3) Application switch / alt+tsb (index, middle and ring fingers):
_Show the fingers to the camera and remove them from frame shortly afterwards._

![image](https://github.com/gunalpms/gesturez/assets/80674364/4be3ba7d-bee5-4d75-a14c-bb04bab2e1e5)

##### ============================

### TODO

* More functionality
* More robust gesture detection model
* Improved performance
* Less janky volume controls
* Fix lag when calling brightness adjust (if possible)

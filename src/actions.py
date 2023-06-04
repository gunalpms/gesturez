import subprocess
import pyautogui
import asyncio
# montior brightness levels
levels = []

# action functions

# using powershell commands to adjust volume
# source: https://www.byteinthesky.com/powershell/how-to-run-powershell-from-python/

async def volumeDown():
    subprocess.Popen(["powershell","(new-object -com wscript.shell).SendKeys([char]174)"],stdout=subprocess.PIPE)

async def volumeUp():
    subprocess.Popen(["powershell","(new-object -com wscript.shell).SendKeys([char]175)"],stdout=subprocess.PIPE)

# helper function to get brightness levels of the monitor. returns nothing, instead modifies the global variable
def getLevels():
    current_number = ""
    proc = subprocess.Popen(
    ["powershell","Get-Ciminstance -Namespace root/WMI -ClassName WmiMonitorBrightness | select -ExpandProperty level"]
    ,stdout=subprocess.PIPE)
    res = proc.communicate()[0]
    res = res.decode("utf-8")
    for i in res:
        if i == '\r':
            continue
        elif i == '\n':
            if current_number != "":
                levels.append(int(current_number))
                current_number = ""
        else:
            current_number += i
# helper function to get current brightness
def getCurrentBrightness():
    currentBrightnessProcedure = subprocess.Popen(
    ["powershell","Get-Ciminstance -Namespace root/WMI -ClassName WmiMonitorBrightness | select -ExpandProperty CurrentBrightness"]
    ,stdout=subprocess.PIPE)
    currentBrightness = int(currentBrightnessProcedure.communicate()[0].decode("utf-8"))
    return currentBrightness


async def brightnessUp():
    currentBrightness = getCurrentBrightness() 
    
    # getting brightness levels of the monitor. doing this repeatedly could cost computing power, so doing it
    # once per instance is fine. 
    if len(levels) == 0:
        getLevels()
    
    currentBrightnessIndex = levels.index(currentBrightness)

    # handling edge cases in order to not pass an invalid value to the brightnes adjustment shell script
    if currentBrightnessIndex == 0:
        currentBrightnessIndex += 1
    elif currentBrightnessIndex == len(levels)-1:
        currentBrightnessIndex -= 1

    # the brightness level to be set in the powershell script
    brightnessLevel = levels[currentBrightnessIndex+1]

    setBrightness = subprocess.Popen(
    ["powershell", f"$monitor = Get-WmiObject -ns root/wmi -class wmiMonitorBrightNessMethods\n$monitor.WmiSetBrightness(0, {brightnessLevel})"]
    ,stdout=subprocess.PIPE)

async def brightnessDown():
    currentBrightness = getCurrentBrightness() 
    
    # getting brightness levels of the monitor. doing this repeatedly could cost computing power, so doing it
    # once per instance is fine. 
    if len(levels) == 0:
        getLevels()
    
    currentBrightnessIndex = levels.index(currentBrightness)

    # handling edge cases in order to not pass an invalid value to the brightnes adjustment shell script
    if currentBrightnessIndex == 0:
        currentBrightnessIndex += 1
    elif currentBrightnessIndex == len(levels)-1:
        currentBrightnessIndex -= 1

    # the brightness level to be set in the powershell script
    brightnessLevel = levels[currentBrightnessIndex-1]

    setBrightness = subprocess.Popen(
    ["powershell", f"$monitor = Get-WmiObject -ns root/wmi -class wmiMonitorBrightNessMethods\n$monitor.WmiSetBrightness(0, {brightnessLevel})"]
    ,stdout=subprocess.PIPE)

async def altTab():
    pyautogui.keyDown('alt')
    await asyncio.sleep(0.01)
    pyautogui.press('tab')
    await asyncio.sleep(0.01)
    pyautogui.keyUp('alt')

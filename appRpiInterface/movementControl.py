import serial
from time import sleep

joystickLeft = 0.0
joystickRight = 0.0
directionLeft = 0
directionRight = 0
turretMode = "false"

serialPort = serial.Serial("/dev/ttyS0", 115200)

def uartSendJoystickData():
    output = "{0:.4f},{1:.4f},{2},{3}".format(joystickLeft, joystickRight, directionLeft, directionRight)
    
    serialPort.write(bytes(output))

    return

def decodeHTTPData(data):
    global joystickLeft
    global joystickRight
    global directionLeft
    global directionRight
    global turretMode

    data = data.decode("utf-8")
    
    if turretMode == "false":
        joystickLeft, joystickRight, turretMode = data.split(":")
        joystickLeft = float(joystickLeft)
        joystickRight = float(joystickRight)

        if(joystickLeft < 0):
            directionLeft = 1
            joystickLeft = abs(joystickLeft)
        else:
            directionLeft = 0
        
        if (joystickRight < 0):
            directionRight = 1
            joystickRight = abs(joystickRight)
        else:
            directionRight = 0
    else:
        _, _, turretMode = data.split(":")

    uartSendJoystickData()
    return

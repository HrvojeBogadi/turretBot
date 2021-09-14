import serial
from time import sleep

joystickLeft = 0.0
joystickRight = 0.0
turretMode = "false"

serialPort = serial.Serial("/dev/ttyS0", 115200)

def uartSendData(speedLeft, speedRight, directionLeft, directionRight):
    output = "{0:.4f},{1:.4f},{2},{3}\0".format(speedLeft, speedRight, directionLeft, directionRight)
    serialPort.write(bytes(output, "utf-8"))
    #sleep(0.1)


#Hardcoded speed and direction values to enable spining in turret mode
def spinMode():
    directionRight = 0
    directionLeft = 1
    speedRight = 0.6
    speedLeft = 0.6

    uartSendData(speedLeft, speedRight, directionLeft, directionRight)
    
    sleep(0.5)
    speedRight = 0.0
    speedLeft = 0.0

    uartSendData(speedLeft, speedRight, directionLeft, directionRight)
    

#Calculate and set the motors directions and speeds according to joystick
#   positions 
def setMotorSpeed(joyLeft, joyRight):
    speedLeft = abs(joystickRight)
    speedRight = abs(joystickRight)

    if(joystickRight < 0):
        directionLeft = 1
        directionRight = 1
    else:
        directionLeft = 0
        directionRight = 0
    
    if (joystickLeft < 0):
        speedLeft = speedLeft * (1 - abs(joystickLeft))
    elif (joystickLeft > 0):
        speedRight = speedRight * (1 - abs(joystickLeft))
    
    uartSendData(speedLeft, speedRight, directionLeft, directionRight)

#Read the data from the phone app joysticks and store it in global variables
def decodeHTTPData(data):
    global joystickLeft
    global joystickRight
    global turretMode

    data = data.decode("utf-8")

    joystickLeft, joystickRight, turretMode = data.split(":")
    joystickLeft = float(joystickLeft)
    joystickRight = float(joystickRight)
    '''
    if(turretMode == "true"):
        spinMode()
    else:
        setMotorSpeeds()
    '''
        
    return joystickLeft, joystickRight, turretMode





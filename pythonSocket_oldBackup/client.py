import os.path
import serial
import time
from easygui import *
import RPi.GPIO as GPIO
from wifi import Cell, Scheme
import configManager
import escapeRFID
import messageManager
    
configFile = "config";

moduleTypes = ["ButtonTrigger", "RfidSingle", "Button4Simultaneous", "Button4Ordered", "Button4OnOff"]
        
def buttonTrigger(data):
    
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    try:
        while True:
            if GPIO.input(11) == 1:
                print data[2]
                messageManager.sendMessage(data[2])
                time.sleep(1.0)
    except KeyboardInterrupt:
        GPIO.cleanup()
        configuration()
        
def configuration():
    data = configManager.readConfig(configFile)
    
    configOptions = ["Set Name", "Set IP", "Set Module Type", "Set Wifi", data[1].strip() + " Configuration", "Exit"]
    mode = buttonbox("What would you like to configure?", choices = configOptions)
    
    if mode == configOptions[0]:
		print "Set Name"
		newName = multenterbox("Set name for this module", "Name Config", ["Name"], [data[2].strip()])
		data[2] = newName[0] + "\n"
		configManager.writeConfig(configFile, data)
    if mode == configOptions[1]:
        print "Set IP"
        newIP = multenterbox("Set IP Address for Server", "IP Config", ["Local IP"], [data[0].strip()])
        data[0] = newIP[0] + "\n"
        configManager.writeConfig(configFile, data)
    elif mode == configOptions[2]:
        print "Set Module Type"
        newModuleMode = choicebox("Choose a mode for this module", "Module Mode", moduleTypes)
        data[1] = newModuleMode + "\n"
        configManager.writeConfig(configFile, data)
    elif mode == configOptions[3]:
        print "Set Wifi"
        connectToWifi()
    elif mode == configOptions[4]:
        print "Configure Module"
        configManager.configureModule(data[1].strip())
    elif mode == configOptions[5]:
        print "Exit"
        
    exit()
    
def connectToWifi():
    ssids = [cell.ssid for cell in Cell.all('wlan0')]
    
    newWifiName = choicebox("Choose a Wifi name", "Connect to Wifi", ssids)
    
    newWifiPassword = multenterbox("Set Wifi Password for " + newWifiName, "Wifi Password", ["Password"])
    print "newWifiPassword: " + str(newWifiPassword) + " , newWifiPassword.strip(): " + newWifiPassword[0]
    print "ssid index: " + str(ssids.index(newWifiName))
    cell = Cell.all('wlan0')[ssids.index(newWifiName)]
    
    scheme = Scheme.find('wlan0', 'escape')
    if scheme != None:
        scheme.delete()
    scheme = Scheme.for_cell('wlan0', 'escape', cell, newWifiPassword[0])
    scheme.save()
    scheme.activate()
    
def connectToScheme():
    scheme = Scheme.find('wlan0', 'escape')
    if scheme != None:
        print "Wifi data found - attempting to establish connection..."
        try:
            scheme.activate()
            print "Connection established"
            return
        except:
            print "Could not connect."
    else:
        print "No wifi settings stored."
        
    configuration()

def __main__():
    
    print "Client begins"
    
    data = configManager.readConfig(configFile)
    
    print "data: " + str(data)
    
    messageManager.setIP(data[0].strip())
    moduleMode = data[1].strip()
    
    connectToScheme()
    
    try:

        if moduleMode == "ButtonTrigger":
            buttonTrigger(data)
        elif moduleMode == "RfidSingle":
            rfid = escapeRFID.EscapeRFID(data)
            rfid.readRFID()
        elif moduleMode == "Button4Ordered":
            print "Button4Ordered not yet implemented"
        elif moduleMode == "Button4Simultaneous":
            print "Button4Simultaneous not yet implemented"
        elif moduleMode == "ButtonOnOff":
            print "buttonOnOff not yet implemented"
        else:
            print "No functionality for: " + moduleMode
            configuration()
            
    except KeyboardInterrupt:
        
        configuration()
    
    
__main__()
    

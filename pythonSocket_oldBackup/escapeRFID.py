import serial
import time
import configManager
import messageManager
from easygui import *

# base config format: [updateMethod: continuous/single,
#                      updateFrequency: # seconds between updates,
#                      tagID,tagID, tagID, etc]

class EscapeRFID():

    def __init__(self, aModuleData):
        self.moduleData = aModuleData
        self.RFIDData = configManager.readConfig(self.moduleData[1].strip())
        self.triggerTags = self.RFIDData[2].strip().split(',')
        print "Initialized. triggerTags: " + str(self.triggerTags)
        #self.readRFID(self.moduleData[0])

    def getTags(self):
        tags = []
        
        try:
            rfidPort = serial.Serial('/dev/ttyUSB0', 2400, timeout = 1)
        except:
            msgbox("Could not detect rfid device", "Rfid Error")
            return tags
            
        try:
            while True:
                tagID = rfidPort.read(12)
                
                if len(tagID) != 0:
                    rfidPort.close()
                    
                    tagID = tagID.strip()
                    
                    if tagID not in tags:
                        print "recorded: " + str(tagID)
                        tags.append(tagID.strip())
                    
                    time.sleep(0.5)
                    
                    rfidPort.open()
                    
        except KeyboardInterrupt:
            rfidPort.close()
            
        return tags
        
    def readRFID(self):
        try:
            rfidPort = serial.Serial('/dev/ttyUSB0', 2400, timeout = 1)
        except:
            msgbox("Could not detect rfid device", "Rfid Error")
            return
        
        try:
            while True:
                tagID = rfidPort.read(12)
                
                if len(tagID) != 0:
                    rfidPort.close()
                    
                    print "tagID pre-strip: " + tagID.strip()
                    tagID = tagID.strip()
                    
                    print "triggerTags: " + str(self.triggerTags)
                    
                    if tagID in self.triggerTags:
                        print "Sending trigger to " + self.moduleData[0] 
        
                        messageManager.sendMessage(tagID)
                    
                        time.sleep(0.5)
                    
                    rfidPort.open()
                    
        except KeyboardInterrupt:
            rfidPort.close()
            print "Program interrupted"

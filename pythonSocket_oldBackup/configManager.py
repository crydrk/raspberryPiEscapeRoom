from easygui import *
import escapeRFID

configDefault = ["128.0.0.1\n", "Unassigned\n", "NoName\n"]

# base config format: [updateMethod: continuous/single,
#                      updateFrequency: # seconds between updates,
#                      custom data per module type]
rfidSingleConfigDefault = ["single\n", "0.5\n", "123456, 654321\n"]
buttonTriggerConfigDefault = ["single\n", "0.5\n"]

configFileDict = {"config" : configDefault, "RfidSingle" : rfidSingleConfigDefault, "ButtonTrigger" : buttonTriggerConfigDefault}

def readConfig(configFilename):
    data = []
    try:
        f = open(configFilename + ".txt", 'r')
        print "Config file exists!"
        data = f.readlines()
        f.close()
    except IOError:
        print "Config file not found. Creating."
        f = open(configFilename + ".txt", 'w')
        for line in configFileDict[configFilename]:
            f.write(line)
        f.close()
        data = configFileDict[configFilename]
        
    return data
    
def writeConfig(configFilename, data):
    with open(configFilename + ".txt", 'w') as f:
        f.writelines(data)
        
    print "Config written successfully"
    
def configureModule(moduleType):
    data = readConfig(moduleType)
    data = configureStandardModule(data)
    data = configureSpecialtyModule(data, moduleType)
    writeConfig(moduleType, data)
    
def configureStandardModule(data):
    print "Configuring standard module"
    updateMethod = buttonbox("Continuous or single update?", "Update method", ["continuous", "single"])
    data[0] = updateMethod + "\n"
    if updateMethod == "continuous":
        updateFrequency = enterbox("Update Frequency (Time to wait between sending trigger updates to the server)", "Update Frequency", data[1].strip(), True)
        if updateFrequency != None:
            data[1] = updateFrequency + "\n"
            print "updateFrequency: " + updateFrequency
            
    return data
    
def configureSpecialtyModule(data, moduleType):
    
    if moduleType == "RfidSingle":
        msgbox("After pressing OK, scan all rfid objects that can trigger this module, and then press ctrl+c to continue")
        tags = escapeRFID.getTags()
        if len(tags) > 0:
            msgbox("Registered " + str(tags) + " to this module.")
            tagStr = ""
            for tag in tags:
                tagStr += tag + ","
            tagStr += "\n"
            data[2] = tagStr
        else:
            msgbox("No tag information recorded.")
    return data
        
def fileWritingTestCase():
    data = readConfig("RfidSingleConfig")
    print "data: " + str(data)
    data[1] = "nope\n"
    writeConfig("RfidSingleConfig", data)
    exit()
    

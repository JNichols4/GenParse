import arrays as a
import tests
import debug as d
import time
import os
import files_dvt as fdvt
import datetime
import errno

def pause(time_int=1):
    time.sleep(time_int)

def split_data(string, delimiter=','):
    return string.split(delimiter)

def replace_string(string,primary_special_string = ' ',secondary_special_string = '',primary_default_str = ' ',secondary_default_string = ''):
    #replace special strings such as key words and other strings first, then replace spaces and other building block chars second
    string = string.replace(primary_special_string,secondary_special_string)
    string = string.replace(primary_default_str,secondary_default_string)
    return string

def parse_thermal_file(importFile,outputFile,searchWord='Converged',enclosureType='',driveType=''):

    now = datetime.datetime.now()
    thermalsDirectory = os.getcwd()+'\\Thermals\\{}'.format(now.strftime("%Y-%m-%d"))

    if not os.path.exists(thermalsDirectory):
        try:
            os.makedirs(thermalsDirectory)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    outputFile = thermalsDirectory + '\\{} Thermals {} {} Parsed {}'.format(driveType,enclosureType,searchWord,now.strftime("%H-%M")) + '.txt'
    d.debug_out('Thermal file: {}'.format(outputFile))
    pos = a.thermalSelectionArray.index(searchWord)

    for i in range(len(a.thermalMasterArray[pos])):
        a.thermalMasterArray[pos] = []

    searchWordArray = tests.thermalSearchWordDict[searchWord]

    d.debug_out(""
                "\n        Search word: {}"
                "\n        Format: {}".format(searchWord, searchWordArray))

    incomingFile = open(importFile, "r")

    d.debug_out(searchWord)
    pause(1)

    for line in incomingFile:
        for i in range(len(a.thermalMasterArray)): #length of the array
            if searchWordArray[i] in line:
                line = line[26:]
                if i==0:
                    #look for the first search word, which is "time" var
                    #example of 'time = ' line: 02/24/2018 00:45:35 (now)
                    if searchWord=='Converged':
                        newline = line[7:26]
                        newline = newline.replace(' ',',')
                        a.thermalMasterArray[i].append(split_data(newline))
                        #newline data format: [02/24/2018,02:41:34] -> [mm/dd/yyyy, 24hr format]
                    else:
                        line = incomingFile.next()
                        newline = line[:12].replace(',','')
                        newline = newline + ',' + line[14:22]
                        a.thermalMasterArray[i].append(split_data(newline))
                        #newline data format: [,16:28:00] -> [24 hour format]
                if i==1:
                    #look for the second search word, "CurDegreesC"
                    newline = line[25:48]
                    newline = newline.replace(' CurDegreesC ',',')
                    a.thermalMasterArray[i].append(split_data(newline))
                    #newline data format: [00010000,32] -> [device number, temp reported]
                if i==2:
                    #look for the third search word, "Reported:"
                    startPos = line.index(searchWordArray[i])+len(searchWordArray[i])+1
                    endPos = startPos + 15
                    newline = line[startPos:endPos]
                    newline = replace_string(newline,' Actual:','','  ',',')
                    a.thermalMasterArray[i].append(split_data(newline))
                    #newline data format: [65,65] -> [Reported, Actual]
                if i==3:
                    #look for the fourth search word, "Tachometer "
                    if searchWord=='Converged':
                        fanString = line[:5]
                        startPos = line.index(searchWordArray[i])+len(searchWordArray[i])+22
                        endPos = startPos + 4
                        newline = fanString + ',' + line[startPos:endPos]
                        a.thermalMasterArray[i].append(split_data(newline))
                        #newline data format: [Fan 1, 3630] -> [Fan number, rpm]
                    else:
                        newline = line[2:7]
                        newline = newline + ',' + line[line.index(searchWordArray[i])+len(searchWordArray[i])+3
                                                        :line.index(searchWordArray[i])+len(searchWordArray[i])+7]
                        a.thermalMasterArray[i].append(split_data(newline))
                        #newline data format: [Fan 1, 3600] -> [Fan number, rpm]
                if i==4:
                    #look for the fifth search word, "Temperature: "
                    startPos = line.index(searchWordArray[i])+len(searchWordArray[i])+12
                    endPos = startPos+2
                    newline = line[startPos:endPos]
                    a.thermalMasterArray[i].append(newline)
                    #newline data format: [31] -> [Battery degrees C]
                if i==5:
                    #look for the sixth search word, "mfgCtlNeedsAttnSummaryShow"
                    newline = incomingFile.next()
                    newline = newline[26:]
                    newline = newline.replace('\n','')
                    a.thermalMasterArray[i].append(newline)
                    #newline data format: [NO NEEDS ATTENTION ENTRIES] -> [Test Status]
                if i==6:
                    endPos = line.index(searchWordArray[i])-1
                    startPos = endPos-2
                    newline = line[startPos:endPos]
                    a.thermalMasterArray[i].append(newline)
                    #newline data format: [24] -> [Number of devices]

    outgoingFile = open(outputFile,"w")

    #find the number of devices in the test array
    devices = int(a.thermalMasterArray[6][0])
    systemTemps = 6
    fanTachData = 4

    d.debug_out("Devices: {}".format(devices))
    pause(1)

    #write the header to the file: 'time = ','CurDegreesC','Reported: ','Tachometer ','Temperature: ','mfgCtlNeedsAttnSummaryShow'
    outgoingFile.write('Time,')

    # devices array -- make this smarter, what if the very first entry has a deprecated number of drives??
    for i in range(devices):
        outgoingFile.write('Device {}: '.format(i) + str(a.thermalMasterArray[1][i][0]) + ',')
    outgoingFile.write('Power Temp Sensor 1,Power Temp Sensor 2,Common Controller Sensor 1,Intel CPU Sensor 1,'
                       'Common Controller Temp Sensor 2,Intel CPU Sensor 2,Fan Tach. 1,Fan Tach. 2,Fan Tach. 1, Fan Tach. 2,Battery Temp,Status\n')

    #begin writing the correct output data in delimited format
    try:
        # number of times that we have collected time stamps becomes the number of rows
        for i in range(len(a.thermalMasterArray[0])-1):
            if (i%1)==0:
                outgoingFile.write(str(a.thermalMasterArray[0][i][1]) + ',')
                npos = i * devices
                mpos = i * systemTemps
                fpos = i * fanTachData
                for device_temp in range(devices): # number of devices thermal points
                    outgoingFile.write(str(a.thermalMasterArray[1][npos][1]) + ',')
                    npos+=1
                for system_temp in range(systemTemps):
                    outgoingFile.write(str(a.thermalMasterArray[2][mpos][0])+ ',')
                    mpos+=1
                for fan_tach in range(fanTachData):
                    outgoingFile.write(str(a.thermalMasterArray[3][fpos][1])+ ',')
                    fpos+=1
                outgoingFile.write(str(a.thermalMasterArray[4][i])+','+str(a.thermalMasterArray[5][i])+',\n')
        os.startfile(outputFile)
    except IndexError:
        print('Unable to suitably continue parsing. Might be at end of file. Clearing strings and opening log file.')
        os.startfile(outputFile)
        return None
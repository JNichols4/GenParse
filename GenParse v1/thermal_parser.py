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
    #d.debug_out('replace string special: {}'.format(string))
    string = string.replace(primary_default_str,secondary_default_string)
    #d.debug_out('replace string default: {}'.format(string))
    return string

def parse_thermal_file(importFile,outputFile,searchWord='Converged',enclosureType='',driveType=''):
    #
    #outputFile = fdvt.rename_file(outputFile,'Thermals',searchWord,importFile)
    #
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
    #
    #d.debug_out(importFile)
    #
    #d.debug_out("Length of array: {}".format(len(a.thermalMasterArray)))
    #
    for i in range(len(a.thermalMasterArray[pos])):
        a.thermalMasterArray[pos] = []
    #
    searchWordArray = tests.thermalSearchWordDict[searchWord]
    #Brings in the array of search words that we are interested in
    #
    d.debug_out(""
                "\n        Search word: {}"
                "\n        Format: {}".format(searchWord, searchWordArray))
    #pause(1)
    #
    incomingFile = open(importFile, "r")
    #
    #d.debug_out("Length of array: {}".format(len(a.thermalMasterArray)))
    #
    d.debug_out(searchWord)
    pause(1)
    #
    for line in incomingFile:
        for i in range(len(a.thermalMasterArray)): #length of the array
            if searchWordArray[i] in line:
                line = line[26:]
                #d.debug_out(line)
                if i==0: #look for the first search word, which is "time" var
                    #pause(1)
                    #example of 'time = ' line: 02/24/2018 00:45:35 (now)
                    if searchWord=='Converged':
                        newline = line[7:26]
                        newline = newline.replace(' ',',')
                        #d.debug_out(newline)
                        a.thermalMasterArray[i].append(split_data(newline))
                        #newline data format: [02/24/2018,02:41:34] -> [mm/dd/yyyy, 24hr format]
                    else:
                        line = incomingFile.next()
                        newline = line[:12].replace(',','')
                        #d.debug_out(line)
                        newline = newline + ',' + line[14:22]
                        #d.debug_out(newline)
                        a.thermalMasterArray[i].append(split_data(newline))
                        #newline data format: [,16:28:00] -> [24 hour format]
                if i==1: #look for the second search word, "CurDegreesC"
                    newline = line[25:48]
                    #d.debug_out(newline)
                    newline = newline.replace(' CurDegreesC ',',')
                    #d.debug_out(newline)
                    a.thermalMasterArray[i].append(split_data(newline))
                    #newline data format: [00010000,32] -> [device number, temp reported]
                if i==2: #look for the third search word, "Reported:"
                    startPos = line.index(searchWordArray[i])+len(searchWordArray[i])+1
                    endPos = startPos + 15
                    newline = line[startPos:endPos]
                    #d.debug_out(newline)
                    newline = replace_string(newline,' Actual:','','  ',',')
                    #d.debug_out(newline)
                    a.thermalMasterArray[i].append(split_data(newline))
                    #newline data format: [65,65] -> [Reported, Actual]
                if i==3: #look for the fourth search word, "Tachometer "
                    if searchWord=='Converged':
                        fanString = line[:5]
                        startPos = line.index(searchWordArray[i])+len(searchWordArray[i])+22
                        endPos = startPos + 4
                        newline = fanString + ',' + line[startPos:endPos]
                        #d.debug_out(newline)
                        a.thermalMasterArray[i].append(split_data(newline))
                        #newline data format: [Fan 1, 3630] -> [Fan number, rpm]
                    else:
                        newline = line[2:7]
                        newline = newline + ',' + line[line.index(searchWordArray[i])+len(searchWordArray[i])+3
                                                        :line.index(searchWordArray[i])+len(searchWordArray[i])+7]
                        #d.debug_out(newline)
                        a.thermalMasterArray[i].append(split_data(newline))
                        #newline data format: [Fan 1, 3600] -> [Fan number, rpm]
                if i==4: #look for the fifth search word, "Temperature: "
                    startPos = line.index(searchWordArray[i])+len(searchWordArray[i])+12
                    endPos = startPos+2
                    #d.debug_out('startPos={} endPos: {} i={}: '.format(startPos,endPos,i))
                    newline = line[startPos:endPos]
                    #d.debug_out(newline)
                    a.thermalMasterArray[i].append(newline)
                    #newline data format: [31] -> [Battery degrees C]
                if i==5: #look for the sixth search word, "mfgCtlNeedsAttnSummaryShow"
                    newline = incomingFile.next()
                    #d.debug_out(newline)
                    newline = newline[26:]
                    newline = newline.replace('\n','')
                    a.thermalMasterArray[i].append(newline)
                    #newline data format: [NO NEEDS ATTENTION ENTRIES] -> [Test Status]
                if i==6:
                    endPos = line.index(searchWordArray[i])-1
                    startPos = endPos-2
                    newline = line[startPos:endPos]
                    #d.debug_out(newline)
                    a.thermalMasterArray[i].append(newline)
                    #newline data format: [24] -> [Number of devices]

    outgoingFile = open(outputFile,"w")

    #find the number of devices in the test array
    devices = int(a.thermalMasterArray[6][0])
    systemTemps = 6
    fanTachData = 4

    d.debug_out("Devices: {}".format(devices))
    pause(1)

    '''
    #DEBUGGING ARRAY OUTPUT
    for i in range(len(a.thermalMasterArray)):
        outgoingFile.write("\nSearch:\n"+ '   ' + searchWordArray[i] + ':' + '\n')
        outgoingFile.write(str(a.thermalMasterArray[i]))
        d.debug_out(a.thermalMasterArray[i])
    for i in range(len(a.thermalMasterArray)):
        d.debug_out(len(a.thermalMasterArray[i]))
    '''

    #write the header to the file: 'time = ','CurDegreesC','Reported: ','Tachometer ','Temperature: ','mfgCtlNeedsAttnSummaryShow'
    outgoingFile.write('Time,')
    for i in range(devices): #devices array -- make this smarter, what if the very first entry has a deprecated number of drives??
        outgoingFile.write('Device {}: '.format(i) + str(a.thermalMasterArray[1][i][0]) + ',')
    outgoingFile.write('Power Temp Sensor 1,Power Temp Sensor 2,Common Controller Sensor 1,Intel CPU Sensor 1,'
                       'Common Controller Temp Sensor 2,Intel CPU Sensor 2,Fan Tach. 1,Fan Tach. 2,Fan Tach. 1, Fan Tach. 2,Battery Temp,Status\n')

    #begin writing the correct output data in delimited format
    #d.debug_out("length of array: {}".format(len(a.thermalMasterArray[0])-1))
    #pause(1)
    for i in range(len(a.thermalMasterArray[0])-1): # number of times that we have collected time stamps becomes the number of rows
        if (i%1)==0:
            # d.debug_out('Time array: {}'.format(a.thermalMasterArray[0]))
            # d.debug_out('Time data: {} counter'.format(i))
            outgoingFile.write(str(a.thermalMasterArray[0][i][1]) + ',')
            npos = i * devices
            mpos = i * systemTemps
            fpos = i * fanTachData
            #d.debug_out("Position: {}".format(npos))
            for device_temp in range(devices): # number of devices thermal points
                outgoingFile.write(str(a.thermalMasterArray[1][npos][1]) + ',')
                npos+=1
            #    if npos>80000:
            #        d.debug_out(npos)
            #        pause(.1)
            for system_temp in range(systemTemps):
                outgoingFile.write(str(a.thermalMasterArray[2][mpos][0])+ ',')
                mpos+=1
            for fan_tach in range(fanTachData):
                outgoingFile.write(str(a.thermalMasterArray[3][fpos][1])+ ',')
                fpos+=1
            outgoingFile.write(str(a.thermalMasterArray[4][i])+','+str(a.thermalMasterArray[5][i])+',\n')

        #ConvergedPowerTempSensor
        #ConvergedPowerTempSensor
        #CommonCtlrTempSensor
        #IntelCPUTempSensor
        #CommonCtlrTempSensor
        #IntelCPUTempSensor

    os.startfile(outputFile)
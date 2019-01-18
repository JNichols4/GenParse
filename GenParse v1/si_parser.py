import os
import arrays as a
import tests
import main as m
import debug as d
import enclosure_types as et
import time
import datetime
import errno

def generate_data_string(line,searchWordArray,i):
    lineIndex = line.index(searchWordArray[i]) + len(searchWordArray[i])
    newString = line[lineIndex:]
    newString = newString.replace('\n', '')
    return newString
def populate_file():
    return 0
def open_file():
    return 0
def populate_string(arrayLength,string=''):
    #add operations to this function
    return string
def c_header(array,importedFileName,outputFile):
    #begin header
    outputFile.write('{} {}{}'.format('/#S',importedFileName,'\n'))
    # /#S' + ' ' + importedFileName + '\n')
    for pos in range(len(array)):
        outputFile.write('Search Criteria: ' + array[pos] + '\n')
    outputFile.write('/#F' + '\n')
    #end header
def parse_file(fileName,outputFileName,searchWord='SAS HDD',controllerName = '',driveName = ''):
    pos = a.siSelectionArray.index(searchWord)
    now = datetime.datetime.now()
    siDirectory = os.getcwd()+'\\SI\\{}'.format(now.strftime("%Y-%m-%d"))

    if not os.path.exists(siDirectory):
        try:
            os.makedirs(siDirectory)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    outputFileName = '{}+{}'.format(driveName,controllerName) + now.strftime("%H-%M") + '.txt'
    fullOutputFileName = siDirectory + '\\' + outputFileName

    d.debug_out(fullOutputFileName)

    # make sure that the arrays are empty
    for i in range(len(a.siMasterArray[pos])):
        a.siMasterArray[pos][i] = []

    searchWordArray = tests.siSearchWordDict[searchWord] #brings in the array
    #example of searchWordArray = ['./smartctl','attached phy identifier = ','Invalid word count: ',
    #                              'Running disparity error count: ','Loss of dword synchronization count: ',
    #                              'Phy reset problem count: ']
    d.debug_out(searchWordArray)
    #
    incomingFile = open(fileName, "r")
    #
    for line in incomingFile:
        for i in range(len(a.siMasterArray[pos])):
            if searchWordArray[i] in line: #not defined in a.py! this is f'n specific
                if i==0:
                    newString = line[len(line)-11:len(line)-1]
                    newString = newString.replace('/','')
                    a.siMasterArray[pos][i].append(newString)
                else:
                    a.siMasterArray[pos][i].append(generate_data_string(line,searchWordArray,i))
    #
    #USED FOR DEBUGGING
    for i in range(5):
        print a.siMasterArray[pos][i]
    #
    outputFile = open(fullOutputFileName,"w+")
    #
    # file header
    c_header(searchWordArray,fileName,outputFile)
    #
    arraylen = len(a.siMasterArray[pos])
    testlen = (len(a.siMasterArray[pos][1]))
    #this is the length of the amount of data that is in the phy id array,
    #to match the length of the sas device array
    #come up with a better solution!
    #
    #d.debug_out(testlen)
    #
    for i in range(len(a.siMasterArray[pos])):
        d.debug_out(len(a.siMasterArray[pos][i]))
    #
    #time.sleep(5)
    #
    s = 0
    #
    for i in range(testlen):
        #
        if (i%2)==0 and i!=0: #0%2 will return 0
            s+=1
        #
        d.debug_out('iteration' + str(i))
        #
        outputString = '\n' + a.siMasterArray[pos][0][s] + ':phy:' + a.siMasterArray[pos][1][i]
        d.debug_out(outputString)
        #
        for x in range(2,arraylen):
            if len(outputString)<20:
                for space in range(20-len(outputString)):
                    outputString = outputString + ' '
                outputString = outputString + ' ['
            outputString = outputString + ' ' + a.siMasterArray[pos][x][i]
        outputString = outputString + ' ]'
        #
        #outputString = '\n' + a.siMasterArray[pos][0][i] + ':phy:' + a.dataArray[1][i] + ' [' + a.dataArray[2][i] + ' ' + \
        #                a.dataArray[3][i] + ' ' + a.dataArray[4][i] + ' ' + a.dataArray[5][i] +']'
        #
        #d.debug_out(outputString)
        #
        d.debug_out('Output String: ' + outputString)
        outputFile.write(outputString)
    os.startfile(fullOutputFileName)
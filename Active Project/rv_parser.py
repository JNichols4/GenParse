import os
import datetime
import errno

def parse_rv_file(parseType,drives, loopVar, exportFileName, importFileName,controllerName = '',driveName = ''):
    w, h = 5, (drives * loopVar)  # multiplied by two in order to account for both regular and high speed fan data
    print w, h
    dataStruct = [[0 for x in range(w)] for y in range(h)]
    dataStruct_row = 0
    dataStruct_col = 0

    now = datetime.datetime.now()
    rvDirectory = os.getcwd()+'\\RV\\{}'.format(now.strftime("%Y-%m-%d"))

    if not os.path.exists(rvDirectory):
        try:
            os.makedirs(rvDirectory)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    exportFileName = rvDirectory + '\\RV {} {} {}'.format(driveName,parseType,now.strftime("%H-%M")) + '.txt'

    importFile = open(importFileName, "r")
    exportFile = open(exportFileName, "w")

    csvFileName = exportFileName.replace('.txt', '.csv')
    csvFile = open(csvFileName, "w")

    for line in importFile:
        if 'complete, 180 seconds' in line:
            nameString = line[line.index('#0  device') + len('#0  device'):]
            if 'complete' in nameString:
                if dataStruct_row == 0:
                    indexVar = nameString.index('complete')
                    fnameString = nameString[:indexVar]
                    fnameString = fnameString.replace("  ", "")
                    fnameString = fnameString.replace(" ", "")
                    # print dataStruct_row, dataStruct_col
                    dataStruct[dataStruct_col][dataStruct_row] = 'Drive: {}'.format(fnameString)
                    dataStruct_row += 1
                newString = line[line.index('IOs,') + len('IOs,'):]
                indexVar = newString.index("IOs/s")
                finalString = newString[:indexVar]
                finalString = finalString.replace(" ", "")
                # print dataStruct_row, dataStruct_col
                dataStruct[dataStruct_col][dataStruct_row] = finalString
                # exportFile.write(finalString + '\n')
                dataStruct_row += 1
                if dataStruct_row == w:
                    dataStruct_col += 1
                    dataStruct_row = 0
                    if dataStruct_col == h:
                        break
    # print dataStruct
    # time.sleep(10)
    for x in range(w):
        for i in range(h):
            # print i
            data = dataStruct[i][x]
            # print data
            exportFile.write(str(data) + ",")
            csvFile.write(str(data) + ",")
        exportFile.write('\n')
        csvFile.write('\n')

    # os.startfile(fileName)
    # os.startfile(exportFileName)
    os.startfile(csvFileName)
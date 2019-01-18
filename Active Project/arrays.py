hddDeviceArray = []         #0 in array
hddPhyIDArray = []          #1 in array
hddInvWCArray = []          #2 in array
hddRunningDispArray = []    #3 in array
hddDwordLossArray = []      #4 in array
hddPhyResetArray = []       #5 in array
#
#'./smartctl','attached phy identifier = ','Invalid DWORD count = ','Running disparity error count = ','Loss of DWORD synchronization = ','Phy reset problem = '
ssdDeviceArray = []
ssdPhyIDArray = []
ssdInvWCArray = []
ssdRunningDispArray = []
ssdDwordLossArray = []
ssdPhyResetArray = []
#
ssdSpecDeviceArray = []
ssdSpecPhyIDArray = []
ssdSpecErrorArray = []
ssdSpecAddressFrameErrArray = []
ssdSpecAbandonClass_OPREJ_Array = []
ssdSpecRetryClass_OPREJ_Array = []
ssdSpecSSPFrameErrArray = []
#
hddDataArray = [hddDeviceArray,hddPhyIDArray,hddInvWCArray,hddRunningDispArray,hddDwordLossArray,hddPhyResetArray]
ssdDataArray = [ssdDeviceArray,ssdPhyIDArray,ssdInvWCArray,ssdRunningDispArray,ssdDwordLossArray,ssdPhyResetArray]
ssdSpecArray = [ssdSpecDeviceArray,ssdSpecPhyIDArray,ssdSpecErrorArray,ssdSpecAddressFrameErrArray,
                ssdSpecAbandonClass_OPREJ_Array,ssdSpecRetryClass_OPREJ_Array,ssdSpecSSPFrameErrArray]
#
siMasterArray = [hddDataArray,ssdDataArray,ssdSpecArray] #master,special,specialized
#
siSelectionArray = ['SAS HDD','SAS SSD','SAS SSD Spec.']
thermalSelectionArray = ['Converged','Legacy']
#
#'Converged':['time = ','CurDegreesC','Reported: ','Tachometer ','Temperature: ','mfgCtlNeedsAttnSummaryShow'
#'Legacy':['date','CurDegreesC','Reported: ','Speed: ','Temperature: ','mfgCtlNeedsAttnSummaryShow']
timeArray = []
deviceTempSensorArray = []
systemTempSensorArray = []
tachometerSensorArray = []
batteryTempSensorArray = []
mfgCtlAttnArray = []
devices = []

thermalMasterArray = [timeArray,deviceTempSensorArray,systemTempSensorArray,tachometerSensorArray,batteryTempSensorArray,mfgCtlAttnArray,devices]


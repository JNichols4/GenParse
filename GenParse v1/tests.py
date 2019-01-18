import enclosure_types
test_type = ['RV','SI']
test_dict = {'RV':['RV Baseline','UUT only','All (Non-HSF)','All (HSF)'],
             'SI':['Arapaho','Sandhawk','Razor-M','Otter'],
             'S&V':['SV Baseline','OpRandomVibe','OpShocks'],
             'Thermals':['Joshua','Ebbets','Alder','Camden','Wembley','Trafford','--NA--']}
enclosure_dict = {'RV':['Joshua','Ebbets','Alder','Camden','Wembley','Trafford'],
                  'SI':['SAS HDD','SAS SSD','SAS SSD Spec.'],
                  'S&V':['Joshua','Ebbets','Alder','Camden','Wembley','Trafford'],
                  'Thermals':['Converged','Legacy']}

siSearchWordDict = {'SAS HDD':['./smartctl','attached phy identifier = ','Invalid word count: ',
                               'Running disparity error count: ','Loss of dword synchronization count: ',
                               'Phy reset problem count: '],
                    'SAS SSD':['./smartctl','attached phy identifier = ','Invalid DWORD count = ',
                               'Running disparity error count = ','Loss of DWORD synchronization = ',
                               'Phy reset problem = '],
                    'SAS SSD Spec.':['./smartctl','attached phy identifier = ','Received ERROR  count: ',
                                     'Received address frame error count: ','Received abandon-class OPEN_REJECT count: ',
                                     'Received retry-class OPEN_REJECT count: ','Received SSP frame error count: ']}

thermalSearchWordDict = {'Converged':['time = ','CurDegreesC','Reported: ','Tachometer ','Temperature: ','mfgCtlNeedsAttnSummaryShow','devices,'],
               'Legacy':['date','CurDegreesC','Reported: ','Speed: ','Temperature: ','mfgCtlNeedsAttnSummaryShow','devices,']}
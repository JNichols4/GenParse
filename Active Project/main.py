import Tkinter as tk
import tkMessageBox
import time
import tkFileDialog
import os
import enclosure_types
import tests
import si_parser
import debug as d
import thermal_parser
import rv_parser
import errno

#ADD FUNCTIONALITIES FOR ALL SI TEST PARSING, SHOCK AND VIBRATION PARSING
class App(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)

        self.defaultsDirectory = os.getcwd() + '\\defaults\\'

        self.dict = tests.test_dict
        self.dict1 = tests.enclosure_dict
        self.driveArray = []
        self.ssdArray = []


        if not os.path.exists(self.defaultsDirectory):
            try:
                os.makedirs(self.defaultsDirectory)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        self.defaultDriveFile = 'availableDrives.txt'
        self.defaultSSDFile = 'availableSSDs.txt'

        #open the drive default configuration file
        try:
            driveFile = open(self.defaultsDirectory+self.defaultDriveFile,'r')
            ssdFile = open(self.defaultsDirectory+self.defaultSSDFile,'r')
            for line in driveFile:
                line = line.replace('\n','')
                self.driveArray.append(line)
            for line in ssdFile:
                line = line.replace('\n','')
                self.ssdArray.append(line)
        except IOError:
            tkMessageBox.showinfo('IMPORT ERROR',' Unable to import the default drive file: {}.'
                                                 '\n\nPlease recheck the default file in the directory: {}'.
                                                  format(self.defaultsDirectory+self.defaultDriveFile,self.defaultsDirectory))
            exit()

        print self.driveArray

        self.label1 = tk.Label(master,text="File Name")
        self.label1.grid(row=0, column=0)

        self.importEntry = tk.Entry(master,bd=2)
        self.importEntry.grid(row=0,column=1,columnspan=2,ipadx=175,pady=5,padx=15)

        self.browseButton1 = tk.Button(master, text="Browse for file", command=self.fileBrowser1)
        self.browseButton1.grid(row=0, column=3, columnspan=1, padx=5)

        self.appendButton = tk.Button(master, text="Parse", fg='black', bg='grey', command=self.onclick)
        self.appendButton.grid(row=1, column=5, ipadx=20, pady=5)

        self.quitButton = tk.Button(master, text="Quit", fg='black', bg='grey', command=master.quit)
        self.quitButton.grid(row=1, column=0, rowspan=1, ipadx=10)

        #LIST BUTTONS AND MENUS
        self.enclosureListInput = tk.StringVar(master)
        self.typeListInput = tk.StringVar(master)
        self.testListInput = tk.StringVar(master)
        self.driveListInput = tk.StringVar(master)

        self.testListInput.set(tests.test_type[0])  # sets the default to RV
        self.typeListInput.set(self.dict[tests.test_type[0]][0])
        self.driveListInput.set(self.driveArray[0])

        self.testMenu = tk.OptionMenu(master, self.testListInput, *self.dict.keys())

        d.debug_out(self.dict[self.testListInput.get()])

        self.typeMenu = tk.OptionMenu(master,self.typeListInput,*self.dict[self.testListInput.get()])
        #                                                               dict['RV'] -> 'Baseline'....

        self.driveListMenu = tk.OptionMenu(master,self.driveListInput,*self.driveArray)


        d.debug_out(self.dict[self.testListInput.get()])

        self.testListInput.trace('w', self.update_options)

        self.enclosureListInput.set(enclosure_types.enclosure_list[0])  # sets the default to Joshua
        self.enclosureMenu = tk.OptionMenu(master, self.enclosureListInput,*self.dict1[self.testListInput.get()])
        #                                                                dict1['RV'] -> 'Joshua...'
        self.testMenu.grid(row=1, column=1, ipadx=40)
        self.typeMenu.grid(row=1, column=2, ipadx=40)
        self.enclosureMenu.grid(row=1, column=3, ipadx=5)
        self.driveListMenu.grid(row=1,column=4,ipadx=5)

    def update_options(self,*args):
        self.typeListInput.set(self.dict[self.testListInput.get()][0])
        self.enclosureListInput.set(self.dict1[self.testListInput.get()][0])
        #                           self.dict#['NEW STRING'] -> default param in menu
        change_menu = self.typeMenu["menu"]
        change_menu1 = self.enclosureMenu["menu"]
        #
        change_menu.delete(0,"end")
        change_menu1.delete(0, "end")
        #
        for string in self.dict[self.testListInput.get()]:
            change_menu.add_command(label=string, command=lambda value=string: self.typeListInput.set(value))
        for string in self.dict1[self.testListInput.get()]:
            change_menu1.add_command(label=string, command=lambda value=string: self.enclosureListInput.set(value))
        #
        d.debug_out("update output {}".format(self.dict[self.testListInput.get()]))
        d.debug_out("update output {}".format(self.dict1[self.testListInput.get()]))
        #

    def fileBrowser1(self):
        filename = tkFileDialog.askopenfilename(parent=rootWindow,title="Browse for import file")
        if filename is '':
            return 0
        elif filename is not '':
            self.importEntry.delete(0, 'end')
            self.importEntry.insert(0,filename)

    def onclick(self):
        fileName = self.importEntry.get()
        exportFileName = os.getcwd() + "//appendedData.txt"
        if self.testListInput.get()=='Thermals':
            thermal_parser.parse_thermal_file(fileName,exportFileName,self.enclosureListInput.get(),
                                              enclosureType=self.typeListInput.get(),driveType=self.driveListInput.get())

        if self.testListInput.get()=='SI':
            enclosureName = self.enclosureListInput.get()
            controllerName = self.typeListInput.get()
            driveName = self.driveListInput.get()
            si_parser.parse_file(fileName,exportFileName,self.enclosureListInput.get(),
                                 controllerName=controllerName,driveName=driveName)

        if self.testListInput.get()=='RV':
            drives,indexVar,loopVar = 0,0,0
            if self.enclosureListInput.get() in enclosure_types.enclosure_list[:]:
                indexVar = enclosure_types.enclosure_list.index(self.enclosureListInput.get())
                drives = enclosure_types.enclosure_drives[indexVar]
            if self.typeListInput.get() in enclosure_types.run_type[:]:
                indexVar = enclosure_types.run_type.index(self.typeListInput.get())
                loopVar = enclosure_types.run_type_loop[indexVar]
                #print loopVar
            parseTypeString = 'in ' + self.enclosureListInput.get() + ' -' + self.typeListInput.get() + '- '
            rv_parser.parse_rv_file(parseTypeString,drives,loopVar,exportFileName,fileName,driveName=self.driveListInput.get())

if __name__ == "__main__":
    rootWindow = tk.Tk()
    rootWindow.title('DATA PARSER')
    app = App(rootWindow)
    app.mainloop()
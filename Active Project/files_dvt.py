import debug as d

def punctuate(string,addstring,punctuation=' '):
    return string + punctuation + addstring

def rename_file(appendedFileName,test_name,datatype,importFileName,fileExtensionDEFAULT='.txt'):
    newFileName = appendedFileName.replace(fileExtensionDEFAULT,'') #remove the .txt extension
    d.debug_out(newFileName)
    newFileName = punctuate(punctuate(newFileName.replace(newFileName,test_name),importFileName.replace(fileExtensionDEFAULT,'')),datatype)
    d.debug_out(newFileName)
    #this becomes {Thermals} {name string} {Legacy/Converged} for example
    newFileName = punctuate(newFileName,'.txt','')
    d.debug_out(newFileName)
    return newFileName
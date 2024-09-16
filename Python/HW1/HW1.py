def Main():
    #get file handle and open the file that is named in command line
    filehandle = open(sys.argv[1])
    LoadDiagnostics(filehandle)
    #CheckPower()
    
def LoadDiagnostics(filehandle):
    #loop through the file and ...
    for line in filehandle.readlines():
        print(line)
    filehandle.close() 

#def CheckPower():
    
    
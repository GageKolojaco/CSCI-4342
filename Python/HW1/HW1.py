def Main():
    #get file handle and open the file that is named in command line
    binaryVal = LoadDiagnostics(open(sys.argv[1]))
    power = CheckPower(binaryVal)
    return power
    
def LoadDiagnostics(filehandle):
    #loop through the file and ...
    for line in filehandle.readlines():
        print(line)
    filehandle.close() 

if __name__ == '__main__':
    Main()
#def CheckPower():
    
    
import sys

def Main():
    #get file handle and open the file that is named in command line
    gamma_rate = LoadDiagnostics(open(sys.argv[1]))
    power = CheckPower(gamma_rate)
    return power
    
def LoadDiagnostics(filehandle):
    #find the maximum length of the strings
    max_length = max(len(binary) for binary in filehandle.readlines())
    #create string for gamma rate
    gamma_rate = ''
    #create a list of lists for each index position
    list_of_binary_str = [[] for _ in range(max_length)]
    
    #loop through the each string in the file
    for line in filehandle.readlines():
        #loop through each character in each string
        for index, char in enumerate(line):
            #append the element to its respective list
            list_of_binary_str[index].append(char)
    filehandle.close()
    
    #loop through list of respective values
    for list_of_indexes in list_of_binary_str:
        for binary_str in list_of_indexes:
            count_0 = string.count('0')
            count_1 = string.count('1')
            if count_0 > count_1:
                gamma_rate + 0
            else:
                gamma_rate + 1
    return gamma_rate

            

if __name__ == '__main__':
    Main()
#def CheckPower():
    
    
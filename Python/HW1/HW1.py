import sys

def Main():
    power = CheckPower(
        LoadDiagnostics(
            open(sys.argv[1]) #get file handle and open the file that is named in command line
            )
        )
    print('Power Consumption rate: 'str(power))
    
def LoadDiagnostics(filehandle):
    print('Loading diagnostics...')
    #find the maximum length of the strings contained within the file
    max_length = max(len(binary) for binary in filehandle.readlines())
    #move the pointer back to the appropriate position to read the file again
    filehandle.seek(0)
    #create a list of lists for each index position
    list_of_binary_str = [[] for _ in range(max_length)]
    #loop through the each string in the file
    for line in filehandle.readlines():
        #loop through each character in each string
        for index, char in enumerate(line):
            #append the element to its respective list
            list_of_binary_str[index].append(char)
    #close filehandler
    return list_of_binary_str
    
def CheckPower(list_of_binary_str):
    #create string for gamma rate
    gamma_rate = ''
    #create string for epislon rate
    epsilon_rate = ''
    #loop through list of respective values
    for list_of_indexes in list_of_binary_str:
        count_0 = list_of_indexes.count('0')  #count how many 0's
        count_1 = list_of_indexes.count('1')  #count how many 1's
        if count_0 > count_1:
            gamma_rate += '0'  #append '0' to the gamma rate
        else:
            gamma_rate += '1'  #append '1' to the gamma rate
        print (gamma_rate)
    print('Gamma rate computed...')
    #we flip the gamma rate using slicing to deducte the epsilon rate
    epsilon_rate = gamma_rate[::-1]
    print('Epsilon rate computed...')
    #we use the int function at base 2 to deducte the base 10 values
    #of the gamma & epsilon rate
    gamma_value = int(gamma_rate, 2)
    epsilon_value = int(epsilon_rate, 2)
    return gamma_value * epsilon_value
#not sure why it wouldn't run the main function unless
#I put this, but the internet told me to
if __name__ == '__main__':
    Main()
    
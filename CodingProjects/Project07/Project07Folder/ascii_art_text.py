'''
ascii_art_text.py
Roman Schiffino 151B Fall Semester
This turns text into matrix art using more handy matrices.
'''
import sys as s
from matrix import *


def loadSymbols():
    '''
    This function opens the alphabet file and makes a list of all the symbols.
    This list is returned.
    '''
    symbols = []
    symbolKeyFile = open("Project07\Project07Folder\colossalFontAlphabet.txt","r")
    symbolLine = symbolKeyFile.readline()
    # Makes symbol list.
    for symbol in range(len(symbolLine)):
        symbols.append(symbolLine[symbol])
    symbolKeyFile.close()
    return symbols


def loadFont(symbolList):
    '''
    This function creates a symbol dictionary. We first open the the font symbols file and go through
    all the lines. this is stored as a list. Then 64 times,once per symbol, a 11 entry section of the 
    is taken as a symbol, A matrix is created with 11 rows and 14 columns, corresponds to symbol size.
    The new line indicator is stripped from each line and then the 14 characters of the line string 
    are iterated through and each spot in the matrix is set to the corresponding character. The dict 
    entry for each symbol in the list is then set as the corresponding matrix. This dictionary is 
    returned.
    '''
    symDic = {}
    symbolFontFile = open("Project07\Project07Folder\colossalFontSymbols.txt","r")
    fontLines = symbolFontFile.readlines()
    symbolFontFile.close()
    # Loops through every character.
    for symbol in range(64):
        # Rips an 11 entry list corresponding to each character.
        symbolLines = fontLines[(symbol*11):(symbol+1)*11]
        # Creates matrix.
        symbolMatrix = matData(11,14)
        # Loops through lines for each symbol.
        for line in range(11):
            # Sets each matrix entry to the corresponding character.
            for entry in range(14):
                symbolMatrix.set(line,entry,symbolLines[line].rstrip("\n")[entry])
        # Defines dictionary entry.
        symDic[symbolList[symbol]] = symbolMatrix
    return symDic


def stringInterpreter(string,symbolDic):
    '''
    Takes each character in the string and determines the corresponding matrix in the dictionary.
    First character becomes stringMatrix and then each follwing character is appended to the right
    of it.
    '''
    for i in range(len(string)):
        # First symbolMatrix.
        if i == 0:
            stringMatrix = symbolDic[string[i]]
        # Further character matrix appending.
        else:
            stringMatrix = stringMatrix.rAppend(symbolDic[string[i]])
    return stringMatrix


def outputGenerator(strMat):
    '''
    Saves stringMatrix to string in text file.
    '''
    with open(file="Project07\Project07Folder\TextToAscii.txt", mode="w") as outFile:
        outFile.write(str(strMat))
    outFile.close()


def main(length,text="sample"):
    '''
    Main function gives usage information and runs all other functions.
    '''
    if length == 1:
        print("Usage Example: python3 Project07/Project07Folder/ascii_art_text.py <text>")
    else:
        symbolKeys = loadSymbols()
        symbols = loadFont(symbolKeys)
        stringMat = stringInterpreter(text,symbols)
        print(stringMat)
        outputGenerator(stringMat)



if __name__ == '__main__':
    lengthOf = len(s.argv[0:])
    if lengthOf == 1:
        main(lengthOf)
    elif lengthOf == 2:
        text = s.argv[1]
        main(lengthOf,text)
    else:
        print("Please check for any typos, or refer to documentation.")
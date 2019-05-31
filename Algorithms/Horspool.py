import math
shiftTab = {}
charList = "?!:()[].,abcdefghijklmnopqrstuv1234567890"
hComps = 0
bfComps = 0

def ShiftTable(P, charList):
    """
    Takes a pattern string and a list of possible characters and builds a shift
    table (as a dictionary) for all possible characters
    """
    Table = {}
    for c in charList:
        Table[c] = len(P)

    for j in range (0, len(P)-1):
        nextChar = P[j]
        Table[nextChar] = len(P) - 1 - j
    return Table


def PrintShiftTab(pattern):
    """
    Takes the pattern as a string and prints the characters and shift values for the
    characters in the pattern
    """
    print("Shift Table:")
    for k, v in shiftTab.items():
        if k in pattern:
            print("|\'"+k+"\':", v, end="|\t")
    print('|other:', str(len(pattern)) + '|')



def Horspool(pattern, string):
    """
    Takes in two strings, a pattern and a text, and compares values by shifting according to the shift table
     returns the index of the pattern within the text or -1 if no pattern is found.
    """
    m = len(pattern)
    n = len(string)
    i = m - 1
    global hComps
    hComps = 0
    while i <= n - 1:
        k = 0
        if k <= m - 1:
            hComps +=1
        while k <= m -1 and pattern[m-1-k] == string[i-k]:
            k += 1
            hComps += 1
        if k == m:
            return i - m +1
        else:
            rightChar = string[i]
            i = i + shiftTab[rightChar] # do shift
    return -1


def BruteForce(pattern, string):
    """
    Takes in two strings, a pattern and a text, and compares every character in the text with the pattern,
    returning the index of the pattern within the string or -1 if no pattern exists within the string
    """
    m = len(pattern)
    n = len(string)
    global bfComps
    bfComps = 0
    for i in range(n-m+1):
        j = 0
        if j<m:
            bfComps += 1
        while j < m and pattern[j] == string[i + j]:
            j += 1
            bfComps += 1
        if j == m:
            return i
    return -1



if __name__ == '__main__':
    testcases = [
        ("gold", "goldfish"), ("fish","goldfish"), ("",""), ("B", "AAAABAAAA"), ("BA","AAAAAAAAAAAAAAAAA"), ("cat", "a bad bat and a fat cat sat in a hat")
    ]

    testIndex = 1
    for pattern, string in testcases:
        pattern = str(pattern).lower()
        string = str(string).lower()


        print("\n******* Test"+str(testIndex)+" *******\nPattern:", pattern, "\t|\tString:", string)
        shiftTab = ShiftTable(pattern, charList)
        PrintShiftTab(pattern)
        print("Horspool index:", Horspool(pattern, string))
        print("Horspool Comparisons:", hComps-1)
        print("Brute Force index:", BruteForce(pattern, string))
        print("Brute Force Comparisons:", bfComps-1)
        print("*********************\n")

        testIndex +=1


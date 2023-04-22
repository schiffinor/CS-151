from dataclasses import replace


class Lsystem:

    def __init__(self, filename=None):
        '''L-system class constructor

        Parameters:
        -----------
        filename: str. Filename of the L-system text file with the base string and 1+ replacement rules
        '''
        self.base = ""
        self.rules = []
        if filename != None:
            self.read(filename)

    def getBase(self):
        return self.base

    def setBase(self,newBase):
        self.base = newBase

    def getRule(self,ruleIdx):
        return self.rules[ruleIdx]

    def addRule(self,newRule):
        self.rules.append(newRule)
    
    def numRules(self):
        return len(self.rules)

    def read(self, filename):
        '''Reads the L-system base string and 1+ rules from a text file. Stores the data in the
        instance variables in the constructor in the format:

        base string: str.
            e.g. `'F-F-F-F'`
        replacement rules: list of 2 element sublists.
            e.g. `[['F', 'FF-F+F-F-FF']]` for one rule

        Parameters:
        -----------
        filename: str. Filename of the L-system text file with the base string and 1+ replacement
            rules
        '''
        ruleFile = open(filename,"r")
        lines = ruleFile.readlines()
        ruleFile.close()
        for line in lines:
            wordList = line.split()
            if wordList[0] == "base":
                self.setBase(wordList[1])
            elif wordList[0] == "rule":
                self.addRule([wordList[1],wordList[2]])
    
    def replace(self, currString):
        '''Applies the full set of replacement rules to current 'base' L-system string `currString`.

        Overall strategy:
        - Scan the L-system string left to right, char by char
        - Apply AT MOST ONE replacement rule to a matching character.
            Example: If the current char is 'F' and that matches a rule's find string 'F', apply
            that rule then move onto the next character in the L-system string (don't try to match
            more rules to the current char).
        - If no rule matches a rule find string, we just add the char as-is to the new string.

        Parameters:
        -----------
        currString: str. The current L-system base string.

        Returns:
        -----------
        newString: str. The base string `currString` with replacement rules applied to it.
        '''
        newString = ""
        for character in currString:
            ruleApplied = False
            for rule in self.rules:
                if rule[0] == character:
                    newString += rule[1]
                    ruleApplied = True
                    break
            if ruleApplied == False:
                newString += character
        return newString
    
    def buildString(self, n):
        '''Starting with the base string, apply the L-system replacement rules for `n` iterations.

        You should NOT change your base string instance variable here!

        Parameters:
        -----------
        n: int. Number of times you go through the L-system string to apply the replacement rules.

        Returns:
        -----------
        str. The L-system string after apply the replacement rules `n` times.
        '''
        newString = self.getBase()
        for i in range(n):
            newString = self.replace(newString)
        return newString
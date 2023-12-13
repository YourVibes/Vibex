from Section import *




# Emitter object keeps track of the generated code and outputs it.
class Emitter:
    def __init__(self, fullPath):
        self.fullPath = fullPath
        self.header = ""
        self.functions = ""
        self.code = ""


    def emit(self, text, section=Section.CODE, wrap=False):
        endline = ''
        if wrap:
            endline = '\n'
        if section == Section.CODE:
            self.code += text + endline
        elif section == Section.FUNCTIONS:
            self.functions += text + endline
        elif section == Section.HEADER:
            self.header += text + endline

    def deleteLastChars(self, section=Section.CODE, num=1):
        if section == Section.CODE:
            self.code = self.code[:len(self.code)-num]
        elif section == Section.FUNCTIONS:
            self.functions = self.functions[:len(self.functions)-num]
        elif section == Section.HEADER:
            self.header = self.header[:len(self.header)-num]


    def writeFile(self):
        with open(self.fullPath, 'w') as outputFile:
            outputFile.write(self.header + self.functions + self.code)

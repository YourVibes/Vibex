#################
### LIBRARIES ###
#################
from Token import *
from TokenType import *
from Lexer import *
from Section import *
from TerminalUtilities import *


import sys




##############
### PARSER ###
##############
class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.GLOBAL_SCOPE = 0           # Global scope
        self.scope = 1                  # Scope
        self.scopeMultiplier = 1        # -1 = True, 1 = False | Due to this all variables initialized in the function will have a negative value and will not be able to see the external except global
        self.section = Section.HEADER

        # Key : (Type, Scope)
        self.functions = dict()         # Declared functions
        self.variables = dict()         # Declared variables
        self.arrays = dict()            # Declared arrays

        self.labelsDeclared = set()     # Declared labels
        self.labelsGotoed = set()       # Labels recalled by goto

        self.curLine = 1                # Current line
        self.whereIsIt = ''             # Check if the program is in a switch-case

        self.prevToken = None           # Previous token
        self.curToken = None            # Current token
        self.peekToken = None           # Next token

        # Init of prevToken, curToken, peekToken
        self.nextToken()
        self.nextToken()




    ########################
    ### TOKEN OPERATIONS ###
    ########################
    # Check if previous token is equal to a kind of token
    def checkPrev(self, kind):
        return kind == self.prevToken.kind

    # Check if current token is equal to a kind of token
    def checkToken(self, kind):
        return kind == self.curToken.kind

    def checkMyToken(self, tok, kind):
        return kind == tok.kind

    # Check if the next token is equal to a kind of token
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    # Check if current token is equal to a kind of token and go to the next, otherwise returns error
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort('Expected ' + kind.name + ', got ' + self.curToken.kind.name + ' -> \'' + self.curToken.text + '\'')
        self.nextToken()

    # Goes to the next token
    def nextToken(self):
        self.prevToken = self.curToken
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    # Goes to the prev token
    def backToken(self, tempTok):
        self.peekToken = self.curToken
        self.curToken = self.prevToken
        self.prevToken = tempTok




    ########################
    ### SCOPE MANAGEMENT ###
    ########################
    # Update scope
    def updateScope(self, op):
        if op == '+':
            self.scope = (abs(self.scope)+1)*self.scopeMultiplier
        elif op == '-':
            self.scope = (abs(self.scope)-1)*self.scopeMultiplier
        else:
            self.abort('Internal error in updating scope')

    def checkIfItExistsInScope(self, name, value):
        if self.checkIfItExistsInScopeHelper(name, value, self.variables):
            return True
        elif self.checkIfItExistsInScopeHelper(name, value, self.arrays):
            return True
        elif self.checkIfItExistsInScopeHelper(name, value, self.functions):
            return True
        else:
            return False

    def checkIfItExistsInScopeHelper(self, name, value, dict):
        if name in dict:
            dictValue = dict[name]
            if (value < 0 and dictValue[1] >= 0) or (value >= 0 and dictValue[1] < 0):
                return False
            else:
                return True
        else:
            return False

    def checkIfIdentAlredyExists(self, name):
        self.checkIfIdentAlredyExistsHelper(name, self.variables)
        self.checkIfIdentAlredyExistsHelper(name, self.arrays)
        self.checkIfIdentAlredyExistsHelper(name, self.functions)

    def checkIfIdentAlredyExistsHelper(self, name, dict):
        if name in dict:
            self.abort(name + " is already declared")




    ############
    ### MAIN ###
    ############
    def program(self):
        self.emitter.emit('// Automatically created by Vibex Compiler\n', self.section, True)
        self.emitter.emit('#include <iostream>', self.section, True)
        self.emitter.emit('#include <io.h>', self.section, True)
        self.emitter.emit('#include <fcntl.h>', self.section, True)
        self.emitter.emit('#include <string>', self.section, True)
        self.emitter.emit('#include <cmath>', self.section, True)
        self.emitter.emit('\nusing namespace std;\n', self.section, True)
        self.section = Section.CODE
        self.emitter.emit('\nint main()\n{', self.section, True)
        self.emitter.emit('_setmode(_fileno(stdout), _O_U16TEXT);\n', self.section, True)

        # Skip \n
        while self.checkToken(TokenType.NEWLINE):
            self.nl()

        # It goes on until the end of the file
        while not self.checkToken(TokenType.EOF):
            self.statement()

        self.section = Section.CODE
        self.emitter.emit('\nreturn 0;\n}', self.section, True)

        # Check if all go to's have a reference label
        for label in self.labelsGotoed:
            if label not in self.labelsDeclared:
                self.abort('Attempting to GOTO to undeclared label: ' + label)




    ##############
    ### ERRORS ###
    ##############
    def abort(self, message):
        sys.exit(error('Error! ' + message + '\n\t\bat line: ' + str(self.lexer.getCurLine())))




    # Check what is the next token
    def statement(self):
        ###########
        ### FUN ###
        ###########
        if self.checkToken(TokenType.FUN):
            if self.section == Section.FUNCTIONS:
                self.abort("You cannot create nested functions")
            self.nextToken()
            self.match(TokenType.COLON)
            if Token.checkIfType(self.curToken.text) != None:
                funType = self.convertVbxToCppType(self.curToken.text)

                self.nextToken()
                if self.checkToken(TokenType.IDENT):
                    funName = self.curToken.text
                    self.checkIfIdentAlredyExists(funName)
                    self.functions.update({funName : (funType, self.scope)})

                    # Formal parameters
                    self.section = Section.FUNCTIONS
                    self.scopeMultiplier = -1
                    self.updateScope('+')
                    self.nextToken()
                    self.match(TokenType.LPAREN)
                    self.emitter.emit(funType + " " + funName + "(", self.section, False)
                    if self.checkToken(TokenType.RPAREN):
                        self.nextToken()
                    else:
                        stCycle = True
                        while self.checkToken(TokenType.COMMA) or stCycle:
                            if stCycle:
                                stCycle = False
                            self.emitter.emit(self.getFormalParametersExpression(), self.section, False)
                        self.emitter.deleteLastChars(self.section, 1)
                        self.match(TokenType.RPAREN)

                    # Body of the function
                    self.match(TokenType.LBRACE)
                    self.emitter.emit(")\n{", self.section, True)
                    while not self.checkToken(TokenType.RBRACE):
                        self.statement()
                    self.match(TokenType.RBRACE)
                    self.emitter.emit("}", self.section, True)
                    self.section = Section.CODE
                    self.scopeMultiplier = 1
                    self.updateScope('-')
                    self.garbageCollector()
                else:
                    self.abort("Expected IDENT, got " + self.curToken.kind.name)
            else:
                self.abort(self.curToken.text + " is not a type")
            self.nextToken()


        ##############
        ### RETURN ###
        ##############
        elif self.checkToken(TokenType.RETURN):
            self.nextToken()
            self.emitter.emit("return " + self.postfixExpression(self.infixToPostfixExpression(self.getExpression())) + ";", self.section, True)
            self.checkEndInstruction()




        ##############
        ### GLOBAL ###
        ##############
        elif self.checkToken(TokenType.GLOBAL):
            self.nextToken()
            if self.checkToken(TokenType.VAR):
                self.nextToken()
                self.match(TokenType.COLON)

                if Token.checkIfType(self.curToken.text) != None:
                    if self.checkToken(TokenType.VOID):
                        self.abort("You cannot use type void to define variables")
                    varType = self.convertVbxToCppType(self.curToken.text)

                    self.nextToken()
                    if self.checkToken(TokenType.IDENT):
                        varName = self.curToken.text
                        self.checkIfIdentAlredyExists(varName)
                        self.variables.update({varName : (varType, self.GLOBAL_SCOPE)})

                        self.nextToken()
                        if self.checkToken(TokenType.SEMICOLON):
                            self.emitter.emit(varType + " " + varName + ";", self.section, True)
                            self.nextToken()
                        elif self.checkToken(TokenType.NEWLINE):
                            self.emitter.emit(varType + " " + varName + ";", self.section, True)
                            self.nl()
                        else:
                            self.match(TokenType.EQ)
                            self.emitter.emit(varType + " " + varName + " = ", self.section, False)
                            self.emitter.emit(self.postfixExpression(self.infixToPostfixExpression(self.getExpression()), varType) + ";", self.section, True)
                            self.checkEndInstruction()
                    else:
                        self.abort("Expected IDENT, got " + self.curToken.kind.name)
                else:
                    self.abort(self.curToken.text + " is not a type")
            elif self.checkToken(TokenType.ARR):
                self.nextToken()
                self.match(TokenType.LBRACKET)
                arrDim = self.postfixExpression(self.infixToPostfixExpression(self.getArrayExpression()))
                self.match(TokenType.RBRACKET)
                self.match(TokenType.COLON)

                if Token.checkIfType(self.curToken.text) != None:
                    if self.checkToken(TokenType.VOID):
                        self.abort("You cannot use type void to define arrays")
                    arrType = self.convertVbxToCppType(self.curToken.text)

                    self.nextToken()
                    if self.checkToken(TokenType.IDENT):
                        arrName = self.curToken.text
                        self.checkIfIdentAlredyExists(arrName)
                        self.arrays.update({arrName : (arrType, self.GLOBAL_SCOPE)})

                        self.nextToken()
                        if self.checkToken(TokenType.SEMICOLON):
                            self.emitter.emit(arrType + " " + arrName + "[" + arrDim +"];", self.section, True)
                            self.nextToken()
                        elif self.checkToken(TokenType.NEWLINE):
                            self.emitter.emit(arrType + " " + arrName + "[" + arrDim +"];", self.section, True)
                            self.nl()
                        else:
                            self.match(TokenType.EQ)
                            self.emitter.emit(arrType + " " + arrName + "[" + arrDim +"]" + " = {", self.section, False)
                            self.match(TokenType.LBRACE)

                            stCycle = True
                            while self.checkToken(TokenType.COMMA) or stCycle:
                                if stCycle:
                                    stCycle = False
                                else:
                                    self.nextToken()
                                self.emitter.emit(self.postfixExpression(self.infixToPostfixExpression(self.getArrayExpression())) + ",", self.section, False)
                            self.emitter.deleteLastCharsHeader(1)
                            self.emitter.emit("};", True)
                            self.match(TokenType.RBRACE)
                            self.checkEndInstruction()
                    else:
                        self.abort("Expected IDENT, got " + self.curToken.kind.name)
                else:
                    self.abort(self.curToken.text + " is not a type")
            else:
                self.abort("Expected VAR or ARR, got " + self.curToken.kind.name)




        ###########
        ### VAR ###
        ###########
        elif self.checkToken(TokenType.VAR):
            self.nextToken()
            self.match(TokenType.COLON)

            if Token.checkIfType(self.curToken.text) != None:
                if self.checkToken(TokenType.VOID):
                    self.abort("You cannot use type void to define variables")
                varType = self.convertVbxToCppType(self.curToken.text)

                self.nextToken()
                if self.checkToken(TokenType.IDENT):
                    varName = self.curToken.text
                    if varName in self.arrays:
                        self.abort(varName + " is already an array")
                    elif varName in self.functions:
                        self.abort(varName + " is already a function")

                    if varName not in self.variables:
                        self.variables.update({varName : (varType, self.scope)})

                    self.nextToken()
                    if self.checkToken(TokenType.SEMICOLON):
                        self.emitter.emit(varType + " " + varName + ";", self.section, True)
                        self.nextToken()
                    elif self.checkToken(TokenType.NEWLINE):
                        self.emitter.emit(varType + " " + varName + ";", self.section, True)
                        self.nl()
                    else:
                        self.match(TokenType.EQ)
                        self.emitter.emit(varType + " " + varName + " = ", self.section, False)
                        self.emitter.emit(self.postfixExpression(self.infixToPostfixExpression(self.getExpression()), varType) + ';', self.section, True)
                        self.checkEndInstruction()
                else:
                    self.abort("Expected IDENT, got " + self.curToken.kind.name)
            else:
                self.abort(self.curToken.text + " is not a type")


        #############
        ### ARRAY ###
        #############
        elif self.checkToken(TokenType.ARR):
            self.nextToken()
            self.match(TokenType.LBRACKET)
            arrDim = self.postfixExpression(self.infixToPostfixExpression(self.getArrayExpression()))
            self.match(TokenType.RBRACKET)
            self.match(TokenType.COLON)

            if Token.checkIfType(self.curToken.text) != None:
                if self.checkToken(TokenType.VOID):
                    self.abort("You cannot use type void to define arrays")
                arrType = self.convertVbxToCppType(self.curToken.text)

                self.nextToken()
                if self.checkToken(TokenType.IDENT):
                    arrName = self.curToken.text
                    if arrName in self.variables:
                        self.abort(arrName + " is already a variable")
                    elif arrName in self.functions:
                        self.abort(arrName + " is already a function")

                    if arrName not in self.arrays:
                        self.arrays.update({arrName : (arrType, self.scope)})

                    self.nextToken()
                    if self.checkToken(TokenType.SEMICOLON):
                        self.emitter.emit(arrType + " " + arrName + "[" + arrDim +"];", self.section, True)
                        self.nextToken()
                    elif self.checkToken(TokenType.NEWLINE):
                        self.emitter.emit(arrType + " " + arrName + "[" + arrDim +"];", self.section, True)
                        self.nl()
                    else:
                        self.match(TokenType.EQ)
                        self.emitter.emit(arrType + " " + arrName + "[" + arrDim +"]" + " = {", self.section, False)
                        self.match(TokenType.LBRACE)

                        stCycle = True
                        while self.checkToken(TokenType.COMMA) or stCycle:
                            if stCycle:
                                stCycle = False
                            else:
                                self.nextToken()
                            self.emitter.emit(self.postfixExpression(self.infixToPostfixExpression(self.getArrayExpression())) + ",", self.section, False)
                        self.emitter.deleteLastChars(self.section, 1)
                        self.emitter.emit("};", self.section, True)
                        self.match(TokenType.RBRACE)
                        self.checkEndInstruction()
                else:
                    self.abort("Expected IDENT, got " + self.curToken.kind.name)
            else:
                self.abort(self.curToken.text + " is not a type")


        #############
        ### IDENT ###
        #############
        elif self.checkToken(TokenType.IDENT):
            identName = self.curToken.text
            identType = ''
            if identName in self.variables:
                identType = 'var'
            elif identName in self.arrays:
                identType = 'arr'
            elif identName in self.functions:
                identType = 'fun'
            else:
                self.abort(identName + " is not initialised")

            if identType == 'fun':
                self.nextToken()
                self.emitter.emit(self.getFunctionExpression(identName) + ";", self.section, True)
            else:
                if identType == 'arr':
                    self.nextToken()
                    self.match(TokenType.LBRACKET)
                    arrIndex = self.postfixExpression(self.infixToPostfixExpression(self.getExpression()), self.isChar(identName))
                    self.match(TokenType.RBRACKET)
                    self.emitter.emit(identName + "[" + arrIndex + "]", self.section, False)
                else:
                    self.emitter.emit(identName, self.section, False)
                    self.nextToken()

                if Token.checkIfAssignmentOperator(self.curToken.kind):
                    self.emitter.emit(' ' + self.curToken.text + ' ', self.section, False)
                    self.nextToken()
                else:
                    if Token.checkIfIncrementDecrementOperator(self.curToken.kind):
                        self.emitter.emit(self.curToken.text, self.section, False)
                        self.nextToken()
                    else:
                        self.abort("Expected ASSIGNMENT OPERATOR, got " + self.curToken.kind.name)
                self.emitter.emit(self.postfixExpression(self.infixToPostfixExpression(self.getExpression()), identType) + ";", self.section, True)

            self.checkEndInstruction()




        #############
        ### INPUT ###
        #############
        elif self.checkToken(TokenType.INPUT):
            self.nextToken()
            paren = False
            if self.checkToken(TokenType.LPAREN):
                self.nextToken()
                paren = True

            if self.checkToken(TokenType.IDENT):
                identName = self.curToken.text
                self.nextToken()
                if identName in self.variables:
                    self.emitter.emit("std::cin >> " + identName +";", self.section, True)
                elif identName in self.arrays:
                    self.match(TokenType.LBRACKET)
                    arrIndex = self.postfixExpression(self.infixToPostfixExpression(self.getArrayExpression()))
                    self.match(TokenType.RBRACKET)
                    self.emitter.emit("std::cin >> " + identName + "[" + arrIndex +"];", self.section, True)
                else:
                    self.abort(identName + " is not initialised")
            else:
                self.abort("Expected IDENT, got " + self.curToken.kind.name)

            if(paren):
                self.match(TokenType.RPAREN)

            self.checkEndInstruction()


        #############
        ### PRINT ###
        #############
        elif self.checkToken(TokenType.PRINT) or self.checkToken(TokenType.PRINTLN) or self.checkToken(TokenType.WPRINT) or self.checkToken(TokenType.WPRINTLN):
            startExpression = ''
            endExpression = ''
            if self.checkToken(TokenType.WPRINT) or self.checkToken(TokenType.WPRINTLN):
                startExpression = 'std::wcout'
            else:
                startExpression = 'std::cout'

            if self.checkToken(TokenType.PRINTLN) or self.checkToken(TokenType.WPRINTLN):
                endExpression = ' << std::endl'
            self.nextToken()

            if self.checkToken(TokenType.STRING_IDENT):
                self.emitter.emit(startExpression + " << \"" + self.curToken.text + "\"" + endExpression + ";", self.section, True)
                self.nextToken()
            else:
                self.emitter.emit(startExpression + " << " + self.postfixExpression(self.infixToPostfixExpression(self.getExpression())) + endExpression + ";", self.section, True)

            self.checkEndInstruction()




        ##########
        ### IF ###
        ##########
        elif self.checkToken(TokenType.IF):
            self.nextToken()
            self.emitter.emit("if(", self.section, False)

            self.condition()

            self.skipNl()
            self.match(TokenType.LBRACE)
            self.emitter.emit(")\n{", self.section, True)

            self.updateScope('+')
            while not self.checkToken(TokenType.RBRACE):
                self.statement()

            self.match(TokenType.RBRACE)
            self.emitter.emit("}", self.section, True)


            ###############
            ### ELSE IF ###
            ###############
            while self.checkToken(TokenType.ELIF) or (self.checkToken(TokenType.ELSE) and self.checkPeek(TokenType.IF)):
                if self.checkToken(TokenType.ELSE) and self.checkPeek(TokenType.IF):
                    self.nextToken()

                self.nextToken()
                self.emitter.emit("else if(", self.section, False)

                self.condition()

                self.skipNl()
                self.match(TokenType.LBRACE)
                self.emitter.emit(")\n{", self.section, True)

                while not self.checkToken(TokenType.RBRACE):
                    self.statement()

                self.match(TokenType.RBRACE)
                self.emitter.emit("}", self.section, True)

            ############
            ### ELSE ###
            ############
            if self.checkToken(TokenType.ELSE):
                self.nextToken()
                self.skipNl()
                self.match(TokenType.LBRACE)
                self.emitter.emit("else\n{", self.section, True)

                while not self.checkToken(TokenType.RBRACE):
                    self.statement()

                self.match(TokenType.RBRACE)

                self.emitter.emit("}", self.section, True)

            self.updateScope('-')
            self.garbageCollector()




        ##############
        ### SWITCH ###
        ##############
        elif self.checkToken(TokenType.SWITCH):
            self.nextToken()
            self.emitter.emit("switch(", self.section, False)

            self.emitter.emit(self.postfixExpression(self.infixToPostfixExpression(self.getExpression())) + ")", self.section, True)
            self.skipNl()
            self.match(TokenType.LBRACE)
            self.emitter.emit("{", self.section, True)

            self.whereIsIt = 'switch'
            self.updateScope('+')
            while not self.checkToken(TokenType.RBRACE):
                self.statement()
            self.updateScope('-')
            self.whereIsIt = ''
            self.match(TokenType.RBRACE)
            self.emitter.emit("}", self.section, True)
            self.garbageCollector()


        ############
        ### CASE ###
        ############
        elif self.checkToken(TokenType.CASE):
            if(self.whereIsIt != 'switch'):
                self.abort("You cannot use CASE keyword in this context")
            self.nextToken()
            self.emitter.emit("case ", self.section, False)
            self.emitter.emit(self.postfixExpression(self.infixToPostfixExpression(self.getExpression())) + ":", self.section, True)
            self.match(TokenType.COLON)


        ###############
        ### DEFAULT ###
        ###############
        elif self.checkToken(TokenType.DEFAULT):
            if(self.whereIsIt != 'switch'):
                self.abort("You cannot use DEFAULT keyword in this context")
            self.nextToken()
            self.match(TokenType.COLON)
            self.emitter.emit("default:", self.section, True)




        #############
        ### WHILE ###
        #############
        elif self.checkToken(TokenType.WHILE):
            self.nextToken()
            self.emitter.emit("while(", self.section, False)

            self.condition()

            self.skipNl()
            self.match(TokenType.LBRACE)
            self.emitter.emit(")\n{", self.section, True)

            self.updateScope('+')
            while not self.checkToken(TokenType.RBRACE):
                self.statement()

            self.match(TokenType.RBRACE)
            self.emitter.emit("}", self.section, True)

            self.updateScope('-')
            self.garbageCollector()


        ################
        ### DO-WHILE ###
        ################
        elif self.checkToken(TokenType.DO):
            self.nextToken()
            self.skipNl()
            self.match(TokenType.LBRACE)
            self.emitter.emit("do\n{", self.section, True)

            self.updateScope('+')
            while not self.checkToken(TokenType.RBRACE):
                self.statement()

            self.match(TokenType.RBRACE)
            self.match(TokenType.WHILE)
            self.emitter.emit("} while(", self.section, False)
            self.condition()
            self.emitter.emit(");", self.section, True)

            if self.checkToken(TokenType.SEMICOLON):
                self.nextToken()

            self.updateScope('-')
            self.garbageCollector()


        ###########
        ### FOR ###
        ###########
        elif self.checkToken(TokenType.FOR):
            self.parentheses = False

            self.nextToken()
            self.emitter.emit("for(", self.section, False)

            self.updateScope('+')
            if self.checkToken(TokenType.LPAREN):
                self.nextToken()
                self.parentheses = True

            self.varInit()
            self.match(TokenType.SEMICOLON)
            self.emitter.emit("; ", self.section, False)
            self.condition()
            self.match(TokenType.SEMICOLON)
            self.emitter.emit("; ", self.section, False)
            self.iterationStep()

            if(self.parentheses):
                self.match(TokenType.RPAREN)

            self.skipNl()
            self.match(TokenType.LBRACE)
            self.emitter.emit(")\n{", self.section, True)

            while not self.checkToken(TokenType.RBRACE):
                self.statement()

            self.match(TokenType.RBRACE)
            self.emitter.emit("}", self.section, True)

            self.updateScope('-')
            self.garbageCollector()




        #############
        ### LABEL ###
        #############
        elif self.checkToken(TokenType.LABEL):
            self.nextToken()

            if self.curToken.text in self.labelsDeclared:
                self.abort("Label already exists: " + self.curToken.text)
            self.labelsDeclared.add(self.curToken.text)

            self.emitter.emit(self.curToken.text + ":", self.section, True)
            self.match(TokenType.IDENT)

            if self.checkToken(TokenType.COLON):
                self.nextToken()


        ############
        ### GOTO ###
        ############
        elif self.checkToken(TokenType.GOTO):
            self.nextToken()
            self.labelsGotoed.add(self.curToken.text)
            self.emitter.emit("goto " + self.curToken.text + ";", self.section, True)
            self.match(TokenType.IDENT)

            if self.checkToken(TokenType.SEMICOLON):
                self.nextToken()




        ###########
        ### CPP ###
        ###########
        elif self.checkToken(TokenType.CPP_CODE):
            self.emitter.emit(self.curToken.text, self.section, True)
            self.nextToken()


        ###########
        ### ASM ###
        ###########
        elif self.checkToken(TokenType.ASM_CODE):
            self.emitter.emit("asm (" + self.curToken.text + ");", self.section, True)
            self.nextToken()




        #############
        ### BREAK ###
        #############
        elif self.checkToken(TokenType.BREAK):
            self.emitter.emit("break;", self.section, True)
            self.nextToken()
            self.checkEndInstruction()


        ################
        ### CONTINUE ###
        ################
        elif self.checkToken(TokenType.CONTINUE):
            self.emitter.emit("continue;", self.section, True)
            self.nextToken()
            self.checkEndInstruction()




        ###############
        ### NEWLINE ###
        ###############
        elif self.checkToken(TokenType.NEWLINE):
            self.nl()


        #############
        ### ERROR ###
        #############
        else:
            self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")




    #################################
    ### OPERATIONS FOR FOR LOOPS  ###
    #################################
    # Var initialization
    def varInit(self):
        self.match(TokenType.VAR)
        self.match(TokenType.COLON)

        if Token.checkIfType(self.curToken.text) != None:
            varType = self.curToken.text
            varType = varType.lower()
            if varType == 'int':
                varType = 'int'
            elif varType == 's_int':
                varType = 'short int'
            elif varType == 'l_int':
                varType = 'long int'
            elif varType == 'u_int':
                varType = "unsigned int"
            elif varType == 'us_int':
                varType = "unsigned short int"
            elif varType == 'ul_int':
                varType = "unsigned long int"
            else:
                self.abort("You cannot use this type to define index variable in a for loop")

            self.nextToken()
            if self.checkToken(TokenType.IDENT):
                if self.curToken.text in self.variables:
                    self.abort("The variable has already been declared outside the for loop")
                self.variables.update({self.curToken.text : (varType, self.scope)})
            else:
                self.abort("Expected IDENT, got " + self.curToken.kind.name)
        else:
            self.abort(self.curToken.text + " is not a type")

        varName = self.curToken.text
        self.nextToken()

        self.match(TokenType.EQ)
        self.emitter.emit(varType + " " + varName + "=", self.section, False)
        if self.checkToken(TokenType.TRUE) or self.checkToken(TokenType.FALSE):
            self.emitter.emit(self.curToken.text, self.section, False)
            self.nextToken()
        else:
            self.emitter.emit(self.postfixExpression(self.infixToPostfixExpression(self.getExpression()), varType), self.section, False)

    # Iteration step
    def iterationStep(self):
        prevIncDec = False
        if Token.checkIfIncrementDecrementOperator(self.curToken.kind):
            prevIncDec = True
            self.emitter.emit(self.curToken.text, self.section, False)
            self.nextToken()

        identName = self.curToken.text
        identType = ''
        if identName in self.variables:
            identType = 'var'
        elif identName in self.arrays:
            self.abort("You cannot use an array to define the iteration step of a for loop")
        elif identName in self.functions:
            self.abort("You cannot use a function to define the iteration step of a for loop")
        else:
            self.abort(identName + " is not initialised")

        self.emitter.emit(identName, self.section, False)
        self.nextToken()

        if Token.checkIfAssignmentOperator(self.curToken.kind):
            self.emitter.emit(' ' + self.curToken.text + ' ', self.section, False)
            self.nextToken()
            self.emitter.emit(self.postfixExpression(self.infixToPostfixExpression(self.getExpression()), identType), self.section, False)
        else:
            if Token.checkIfIncrementDecrementOperator(self.curToken.kind):
                self.emitter.emit(self.curToken.text, self.section, False)
                self.nextToken()
            elif not prevIncDec:
                self.abort("Expected ASSIGNMENT OPERATOR, got " + self.curToken.kind.name)




    #######################
    ### SKIP MANAGEMENT ###
    #######################
    # Checks whether the instruction was closed correctly
    def checkEndInstruction(self):
        if self.checkToken(TokenType.SEMICOLON):
            self.semicolon()
        elif self.checkToken(TokenType.NEWLINE):
            self.nl()
        else:
            self.abort("SEMICOLON or NEWLINE expected")

    # Go to the newline
    def nl(self):
        self.match(TokenType.NEWLINE)
        self.curLine += 1
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
            self.curLine += 1

    # Skip all the newline
    def skipNl(self):
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
            self.curLine += 1

    # Skip semicolons
    def semicolon(self):
        self.match(TokenType.SEMICOLON)
        while self.checkToken(TokenType.SEMICOLON):
            self.nextToken()




    #############################
    ### EXPRESSION MANAGEMENT ###
    #############################
    # Condition
    def condition(self):
        while not self.checkToken(TokenType.NEWLINE) and not self.checkToken(TokenType.LBRACE) and not self.checkToken(TokenType.SEMICOLON):
            expr = []
            kind = self.curToken.kind
            while not Token.checkIfComparisonOperator(kind) and not Token.checkIfLogicalOperator(kind) and not self.checkToken(TokenType.NEWLINE) and not self.checkToken(TokenType.LBRACE) and not self.checkToken(TokenType.SEMICOLON):
                expr.append(self.curToken)
                self.nextToken()
            if(len(expr) > 0):
                if(len(expr) == 1):
                    self.emitter.emit(expr[0].text, self.section, False)
                else:
                    self.emitter.emit(self.postfixExpression(self.infixToPostfixExpression(expr)), self.section, False)
            if not self.checkToken(TokenType.NEWLINE) and not self.checkToken(TokenType.LBRACE) and not self.checkToken(TokenType.SEMICOLON):
                self.emitter.emit(self.curToken.text, self.section, False)
                self.nextToken()


    # Check if the prev token is an expression stop word
    def prevTokenIsAnExpressionStopWord(self):
        if (self.checkPrev(TokenType.NEWLINE) or self.checkPrev(TokenType.COMMA) or self.checkPrev(TokenType.COLON) or self.checkPrev(TokenType.SEMICOLON) or self.checkPrev(TokenType.LBRACKET) or self.checkPrev(TokenType.RBRACKET) or self.checkPrev(TokenType.LBRACE) or self.checkPrev(TokenType.RBRACE)):
            return True
        else:
            return False

    # Check if the current token is an expression stop word
    def curTokenIsAnExpressionStopWord(self):
        if (self.checkToken(TokenType.NEWLINE) or self.checkToken(TokenType.COMMA) or self.checkToken(TokenType.COLON) or self.checkToken(TokenType.SEMICOLON) or self.checkToken(TokenType.LBRACKET) or self.checkToken(TokenType.RBRACKET) or self.checkToken(TokenType.LBRACE) or self.checkToken(TokenType.RBRACE)):
            return True
        else:
            return False

    # Check if the current token is an expression stop word
    def peekTokenIsAnExpressionStopWord(self):
        if (self.checkPeek(TokenType.NEWLINE) or self.checkPeek(TokenType.COMMA) or self.checkPeek(TokenType.COLON) or self.checkPeek(TokenType.SEMICOLON) or self.checkPeek(TokenType.LBRACKET) or self.checkPeek(TokenType.RBRACKET) or self.checkPeek(TokenType.LBRACE) or self.checkPeek(TokenType.RBRACE)):
            return True
        else:
            return False


    # Formal parameters expression
    def getFormalParametersExpression(self):
        expr = ""
        if self.checkToken(TokenType.VAR): 
            self.nextToken()
            self.match(TokenType.COLON)

            if Token.checkIfType(self.curToken.text) != None:
                if self.checkToken(TokenType.VOID):
                    self.abort("You cannot use type void to define variables")
                parType = self.convertVbxToCppType(self.curToken.text)

                self.nextToken()
                parName = self.curToken.text
                self.match(TokenType.IDENT)
                if self.checkIfItExistsInScope(parName, self.scope):
                    self.abort("The following parameter has already been declared: " + parName)
                else:
                    self.variables.update({parName : (parType, self.scope)})
                    
                expr += parType + " " + parName + ","
            else:
                self.abort(self.curToken.text + " is not a type")
        elif self.checkToken(TokenType.ARR):
            self.nextToken()
            self.match(TokenType.LBRACKET)
            arrDim = self.postfixExpression(self.infixToPostfixExpression(self.getArrayExpression()))
            self.match(TokenType.RBRACKET)
            self.match(TokenType.COLON)
            if Token.checkIfType(self.curToken.text) != None:
                if self.checkToken(TokenType.VOID):
                    self.abort("You cannot use type void to define variables")
                parType = self.convertVbxToCppType(self.curToken.text)

                self.nextToken()
                parName = self.curToken.text
                self.match(TokenType.IDENT)
                if self.checkIfItExistsInScope(parName, self.scope):
                    self.abort("The following parameter has already been declared: " + parName)
                else:
                    self.arrays.update({parName : (parType, self.scope)})
                expr += parType + " " + parName + "[" + arrDim + "],"
            else:
                self.abort(self.curToken.text + " is not a type")
        return expr


    # Actual parameters expression
    def getActualParametersExpression(self):
        expr = ""
        stCycle = True
        while self.checkToken(TokenType.COMMA) or stCycle:
            if stCycle:
                stCycle = False
            expr += self.postfixExpression(self.infixToPostfixExpression(self.getExpression())) + ","
            if self.checkPeek(TokenType.COMMA):
                self.nextToken()
        expr = expr[:len(expr)-1]
        return expr


    # Function expression
    def getFunctionExpression(self, funName):
        expr = ""
        self.match(TokenType.LPAREN)
        expr += funName + "("
        if self.checkToken(TokenType.RPAREN):
            self.nextToken()
        else:
            expr += self.getActualParametersExpression()
            if not self.checkPrev(TokenType.RPAREN):
                self.abort("Expected IDENT, got " + self.curToken.kind.name)
        expr += ")"
        return expr


    # Get infix expression
    def getExpression(self):
        expr = []
        lastAnalysisInAFunction = False
        parenCount = 0
        while not self.curTokenIsAnExpressionStopWord() and parenCount >= 0:
            if lastAnalysisInAFunction and self.prevTokenIsAnExpressionStopWord():
                break

            if self.checkPeek(TokenType.LBRACKET): # If it is an array
                arrName = self.curToken.text
                self.nextToken()
                self.nextToken()
                expr.append(Token(arrName + "[" + self.postfixExpression(self.infixToPostfixExpression(self.getArrayExpression())) + "]", TokenType.ARRAY))
                lastAnalysisInAFunction = False
                self.nextToken()
            elif self.checkPeek(TokenType.LPAREN) and self.checkToken(TokenType.IDENT): # If it is a function
                funName = self.curToken.text
                self.nextToken()
                expr.append(Token(funName + "(" + self.getActualParametersExpression() + ")", TokenType.FUNCTION))
                lastAnalysisInAFunction = True
            else:
                if self.checkToken(TokenType.IDENT):
                    if(not self.checkIfItExistsInScope(self.curToken.text, self.scope)):
                        self.abort(self.curToken.text + " is not initialised")
                elif self.checkToken(TokenType.LPAREN):
                    parenCount += 1
                elif self.checkToken(TokenType.RPAREN):
                    parenCount -= 1

                expr.append(self.curToken)
                lastAnalysisInAFunction = False
                self.nextToken()

        return expr


    # Get infix expression for array dimension and index
    def getArrayExpression(self):
        expr = []
        while(not self.isAnExpressionStopWord() and not self.checkToken(TokenType.LBRACE) and not self.checkToken(TokenType.RBRACE)):
            expr.append(self.curToken)
            self.nextToken()
        return expr


    # Convert an infix expression to postfix
    def infixToPostfixExpression(self, expr):
        res = []
        stack = []

        def getPrecedence(operator):
            precedences = {
                TokenType.PLUS:             1,
                TokenType.MINUS:            1,
                TokenType.ASTERISK:         2,
                TokenType.SLASH:            2,
                TokenType.PERCENT:          2,
                TokenType.ASTERISKASTERISK: 2,
                TokenType.BW_AND:           100,
                TokenType.BW_OR:            100,
                TokenType.BW_XOR:           100,
                TokenType.BW_LSHIFT:        100,
                TokenType.BW_RSHIFT:        100,
                TokenType.BW_NOT:           100,
            }
            return precedences.get(operator, 0)
        
        def checkUnary():
            nonlocal i, unary

            if self.checkMyToken(expr[i], TokenType.PLUS):
                unary = '+'
                i+=1
            elif self.checkMyToken(expr[i], TokenType.MINUS):
                unary = '-'
                i+=1
            elif self.checkMyToken(expr[i], TokenType.INCREMENT):
                unary = '++'
                i+=1
            elif self.checkMyToken(expr[i], TokenType.DECREMENT):
                unary = '--'
                i+=1
            elif self.checkMyToken(expr[i], TokenType.BW_NOT):
                unary = '~'
                i+=1

        def checkNumSys():
            nonlocal i, numSys

            if self.checkMyToken(expr[i], TokenType.BIN):
                numSys = '0b'
                i+=1
            elif self.checkMyToken(expr[i], TokenType.OCT):
                numSys = '0'
                i+=1
            elif self.checkMyToken(expr[i], TokenType.DEC):
                numSys = ''
                i+=1
            elif self.checkMyToken(expr[i], TokenType.HEX):
                numSys = '0x'
                i+=1

        i = 0
        while i < len(expr):
            unary = ''
            numSys = ''

            if self.checkMyToken(expr[i], TokenType.LPAREN):
                stack.append(Token('(', TokenType.LPAREN))
                i+=1

            if i>0:
                if not self.checkMyToken(expr[i-1], TokenType.IDENT) and not self.checkMyToken(expr[i-1], TokenType.STRING_IDENT) and not self.checkMyToken(expr[i-1], TokenType.NUMBER) and not self.checkMyToken(expr[i-1], TokenType.RPAREN):
                    checkUnary()
            else:
                checkUnary()

            checkNumSys()

            if self.checkMyToken(expr[i], TokenType.NUMBER):
                res.append(Token('(' + unary + numSys + expr[i].text + ')', expr[i].kind))
            elif self.checkMyToken(expr[i], TokenType.LABS):
                res.append(expr[i])
            elif self.checkMyToken(expr[i], TokenType.RABS):
                while stack and not self.checkMyToken(stack[-1], TokenType.LABS):
                    res.append(stack.pop())
                res.append(expr[i])
            elif self.checkMyToken(expr[i], TokenType.IDENT):
                ndUnary = ''
                if(i < len(expr)-1):
                    if Token.checkIfIncrementDecrementOperator(expr[i+1].kind):
                        ndUnary = expr[i+1].text
                text = '(' + unary + expr[i].text + ndUnary + ')'
                res.append(Token(text, expr[i].kind))
                if ndUnary != '': i+=1
            elif self.checkMyToken(expr[i], TokenType.STRING_IDENT) or self.checkMyToken(expr[i], TokenType.ARRAY) or self.checkMyToken(expr[i], TokenType.FUNCTION) or self.checkMyToken(expr[i], TokenType.TRUE) or self.checkMyToken(expr[i], TokenType.FALSE):
                res.append(expr[i])
            elif Token.checkIfType(expr[i].text) is not None:
                while stack and getPrecedence(stack[-1]) >= getPrecedence(expr[i]):
                    res.append(stack.pop())
                stack.append(expr[i])
            elif self.checkMyToken(expr[i], TokenType.RPAREN):
                while stack and not self.checkMyToken(stack[-1], TokenType.LPAREN):
                    res.append(stack.pop())
            else:
                stack.append(expr[i])

            i+=1

        while stack:
            res.append(stack.pop())

        filteredRes = [token for token in res if token.kind != TokenType.LPAREN]
        return filteredRes


    # Analyze a postfix expression
    def postfixExpression(self, expr, type=''):
        stack = []
        subStack = []
        mode = ''

        for token in expr:
            if mode == 'abs':
                if not self.checkMyToken(token, TokenType.RABS):
                    subStack.append(token)
                else:
                    mode = ''
                    absExpr = self.postfixExpression(subStack)
                    stack.append('(' + absExpr + ' >= 0 ? ' + absExpr + ' : -(' + absExpr + '))')
            elif self.checkMyToken(token, TokenType.NUMBER) or self.checkMyToken(token, TokenType.IDENT) or self.checkMyToken(token, TokenType.FUNCTION) or self.checkMyToken(token, TokenType.ARRAY) or self.checkMyToken(token, TokenType.TRUE) or self.checkMyToken(token, TokenType.FALSE):
                stack.append(token.text)
            elif self.checkMyToken(token, TokenType.STRING_IDENT):
                if Token.checkIfCharType(type) != None:
                    stack.append("'" + token.text + "'")
                elif type == 'wstring':
                    stack.append('L"' + token.text + '"')
                else:
                    stack.append('"' + token.text + '"')
            elif self.checkMyToken(token, TokenType.ASTERISKASTERISK):
                exp = stack.pop()
                base = stack.pop()
                stack.append('pow(' + str(base) + ', ' + str(exp) + ')')
            elif self.checkMyToken(token, TokenType.LABS):
                if mode == 'abs':
                    self.abort('You cannot create nested absolute values')
                else:
                    mode = 'abs'
            else:
                operand2 = stack.pop()
                operand1 = stack.pop()
                stack.append('(' + str(operand1) + str(token.text) + str(operand2) + ')')

        return stack[0] if len(stack)>0 else ''




    #####################
    ### TYPE CONTROLS ###
    #####################
    # Convert Vibex type to C++ type
    def convertVbxToCppType(self, type):
        type = type.lower()
        if type == 's_int':
            type = 'short int'
        elif type == 'l_int':
            type = 'long int'
        elif type == 'l_double':
            type = 'long double'
        elif type == 'u_int':
            type = 'unsigned int'
        elif type == 'us_int':
            type = 'unsigned short int'
        elif type == 'ul_int':
            type = 'unsigned long int'
        elif type == 'u_char':
            type = 'unsigned char'
        return type

    # Check if it is a char
    def isChar(self, name):
        if name in self.variables:
            value = self.variables[name]
            return Token.checkIfCharType(value[0])
        elif name in self.arrays:
            value = self.arrays[name]
            return Token.checkIfCharType(value[0])
        else:
            return False




    #########################
    ### GARBAGE COLLECTOR ###
    #########################
    def garbageCollector(self):
        targetValue = 0
        for value in self.variables.values():
            if abs(value[1]) > abs(targetValue):
                targetValue = value[1]
        for value in self.arrays.values():
            if abs(value[1]) > abs(targetValue):
                targetValue = value[1]
        self.deleteLastScope(targetValue)

    # Delete last scope
    def deleteLastScope(self, value):
        self.deleteKeysByValue(self.variables, value)
        self.deleteKeysByValue(self.arrays, value)

    # Delete all keys with a value in a dictionarys
    def deleteKeysByValue(self, dictionary, value):
        keys = []
        for key, val in dictionary.items():
            if val[1] == value:
                keys.append(key)
        for key in keys:
            del dictionary[key]
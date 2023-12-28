from Token import *
from TokenType import *
from TerminalUtilities import *

import sys




# Lexer keeps track of the current position in the source code and produces each token
class Lexer:
    def __init__(self, source):
        # Source code to be analysed as string
        self.source = source + '\n'     # Add a new line to simplify scanning/analysis of the last token/instruction
        self.curChar = ''               # Current character in the string
        self.curLine = 1                # Current line in the code
        self.curPos = -1                # Current position in the string
        self.nextChar()                 # Go to the pos 0

        self.numSysMode = 10            # Numerical systems


    # Get the current line
    def getCurLine(self):
        return self.curLine

    # Process the next character
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0' # EOF
        else:
            self.curChar = self.source[self.curPos]

    # Returns the lookahead character
    def peek(self, peekUnit=1):
        if self.curPos + peekUnit >= len(self.source):
            return '\0'
        return self.source[self.curPos + peekUnit]



    def checkBetween2Possibilities(self, ndChar, simpleTok, compoundTok):
        if self.peek() == ndChar:
            lastChar = self.curChar
            self.nextChar()
            return Token(lastChar + self.curChar, compoundTok)
        else:
            return Token(self.curChar, simpleTok)

    def checkBetween3Possibilities(self, ndChar, rdChar, simpleTok, compoundTok1, compoundTok2):
        if self.peek() == ndChar:
            lastChar = self.curChar
            self.nextChar()
            return Token(lastChar + self.curChar, compoundTok1)
        elif self.peek() == rdChar:
            lastChar = self.curChar
            self.nextChar()
            return Token(lastChar + self.curChar, compoundTok2)
        else:
            return Token(self.curChar, simpleTok)

    def checkBetween4Possibilities(self, ndChar, rdChar, thChar, simpleTok, compoundTok1, compoundTok2, compoundTok3):
        if self.peek() == ndChar:
            lastChar = self.curChar
            self.nextChar()
            return Token(lastChar + self.curChar, compoundTok1)
        elif self.peek() == rdChar:
            lastChar = self.curChar
            self.nextChar()
            return Token(lastChar + self.curChar, compoundTok2)
        elif self.peek() == thChar:
            lastChar = self.curChar
            self.nextChar()
            return Token(lastChar + self.curChar, compoundTok3)
        else:
            return Token(self.curChar, simpleTok)



    # Invalid token found, print an error message and exit
    def abort(self, message):
        sys.exit(error("Lexical analysis error! " + message + "\n\t\bat line: " + str(self.curLine)))


    @staticmethod
    def isBinDigit(char):
        return char == "0" or char == "1"

    @staticmethod
    def isOctDigit(char):
        return char == "0" or char == "1" or char == "2" or char == "3" or char == "4" or char == "5" or char == "6" or char == "7"

    @staticmethod
    def isHexDigit(char):
        return char == "0" or char == "1" or char == "2" or char == "3" or char == "4" or char == "5" or char == "6" or char == "7" or char == "8" or char == "9" or char == "a" or char == "A" or char == "b" or char == "B" or char == "c" or char == "C" or char == "d" or char == "D" or char == "e" or char == "E" or char == "f" or char == "F"




    # Returns the next token
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        # Check the first character of this token to see if we can decide what it is.
        # If it is a multi-character operator (e.g. !=), a number, an identifier or a keyword, then it will process the remainder
        if self.curChar == '+':
            token = self.checkBetween3Possibilities('+', '=', TokenType.PLUS, TokenType.INCREMENT, TokenType.PLUSEQ)
        elif self.curChar == '-':
            token = self.checkBetween3Possibilities('-', '=', TokenType.MINUS, TokenType.DECREMENT, TokenType.MINUSEQ)
        elif self.curChar == '*':
            token = self.checkBetween3Possibilities('*', '=', TokenType.ASTERISK, TokenType.ASTERISKASTERISK, TokenType.ASTERISKEQ)
        elif self.curChar == '/':
            token = self.checkBetween2Possibilities('=', TokenType.SLASH, TokenType.SLASHEQ)
        elif self.curChar == '%':
            token = self.checkBetween2Possibilities('=', TokenType.PERCENT, TokenType.PERCENTEQ)
        elif self.curChar == ',':
            token = Token(self.curChar, TokenType.COMMA)
        elif self.curChar == ';':
            token = Token(self.curChar, TokenType.SEMICOLON)
        elif self.curChar == '(':
            token = self.checkBetween2Possibilities('|', TokenType.LPAREN, TokenType.LABS)
        elif self.curChar == ')':
            token = Token(self.curChar, TokenType.RPAREN)
        elif self.curChar == '{':
            token = Token(self.curChar, TokenType.LBRACE)
        elif self.curChar == '}':
            token = Token(self.curChar, TokenType.RBRACE)
        elif self.curChar == '[':
            token = Token(self.curChar, TokenType.LBRACKET)
        elif self.curChar == ']':
            token = Token(self.curChar, TokenType.RBRACKET)
        elif self.curChar == ':':
            token = Token(self.curChar, TokenType.COLON)
        elif self.curChar == '.':
            token = Token(self.curChar, TokenType.DOT)
        elif self.curChar == '^':
            token = self.checkBetween2Possibilities('=', TokenType.BW_XOR, TokenType.BW_XOREQ)
        elif self.curChar == '~':
            token = Token(self.curChar, TokenType.BW_NOT)
        elif self.curChar == '=':
            # Check whether this token is = or ==
            token = self.checkBetween2Possibilities('=', TokenType.EQ, TokenType.EQEQ)
        elif self.curChar == '>':
            # Check if this is a > or >= or >> or >>=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            elif self.peek() == '>':
                self.nextChar()
                if self.peek() == '=':
                    self.nextChar()
                    token = Token('>>=', TokenType.BW_RSHIFTEQ)
                else:
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token(lastChar + self.curChar, TokenType.BW_RSHIFT)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
            # Check if this is a token < or <= or << or <<=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            elif self.peek() == '<':
                self.nextChar()
                if self.peek() == '=':
                    self.nextChar()
                    token = Token('<<=', TokenType.BW_LSHIFTEQ)
                else:
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token(lastChar + self.curChar, TokenType.BW_LSHIFT)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '&':
            token = self.checkBetween3Possibilities('&', '=', TokenType.BW_AND, TokenType.AND, TokenType.BW_ANDEQ)
        elif self.curChar == '|':
            token = self.checkBetween4Possibilities('|', '=', ')', TokenType.BW_OR, TokenType.OR, TokenType.BW_OREQ, TokenType.RABS)
        elif self.curChar == '!':
            token = self.checkBetween2Possibilities('=', TokenType.NOT, TokenType.NOTEQ)
        elif self.curChar == '\"':
            # Get characters in quotes
            self.nextChar()
            startPos = self.curPos
            while self.curChar != '\"':
                # Do not allow special characters in the string, no escape characters, carriage returns, tabulations or %
                if self.curChar in ('\0'):
                    self.abort("Character not allowed in string")
                self.nextChar()
            tokText = self.source[startPos: self.curPos]  # Get the substring
            token = Token(tokText, TokenType.STRING_IDENT)
        elif self.curChar == "'":
            # Get characters in quotes
            self.nextChar()
            startPos = self.curPos
            while self.curChar != "'":
                # Do not allow special characters in the string, no escape characters, carriage returns, tabulations or %
                if self.curChar in ('\0'):
                    self.abort("Character not allowed in string")
                self.nextChar()
            tokText = self.source[startPos: self.curPos]  # Get the substring
            tokText = self.stringCorrection(tokText)
            token = Token(tokText, TokenType.STRING_IDENT)
        elif self.numSysMode == 2 and self.isBinDigit(self.curChar):
            # The main character is a number, so it must be a number
            # Get all consecutive numbers and the decimal point if present
            startPos = self.curPos
            while self.isBinDigit(self.peek()):
                self.nextChar()
            # Get the substring
            tokText = self.source[startPos: self.curPos + 1]
            token = Token(tokText, TokenType.NUMBER)
        elif self.numSysMode == 8 and self.isOctDigit(self.curChar):
            # The main character is a number, so it must be a number
            # Get all consecutive numbers and the decimal point if present
            startPos = self.curPos
            while self.isOctDigit(self.peek()):
                self.nextChar()
            # Get the substring
            tokText = self.source[startPos: self.curPos + 1]
            token = Token(tokText, TokenType.NUMBER)
        elif self.numSysMode == 10 and self.curChar.isdigit():
            # The main character is a number, so it must be a number
            # Get all consecutive numbers and the decimal point if present
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.':  # Decimal!
                self.nextChar()
                # There must be at least one digit after the decimal point
                if not self.peek().isdigit():
                    # Error!
                    self.abort("Character not allowed in number.")
                while self.peek().isdigit():
                    self.nextChar()
            # Get the substring
            tokText = self.source[startPos: self.curPos + 1]
            token = Token(tokText, TokenType.NUMBER)
        elif self.numSysMode == 16 and self.isHexDigit(self.curChar):
            # The main character is a number, so it must be a number
            # Get all consecutive numbers and the decimal point if present
            startPos = self.curPos
            while self.isHexDigit(self.peek()):
                self.nextChar()
            # Get the substring
            tokText = self.source[startPos: self.curPos + 1]
            token = Token(tokText, TokenType.NUMBER)
        elif self.curChar.isalpha():
            self.numSysMode = 10 # Set default number system to decimal
            # The main character is a letter, so it must be an identifier or keyword
            # Get all consecutive alphanumeric characters
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()
            # Checks whether the token is a keyword (case-insensitive)
            tokText = self.source[startPos: self.curPos + 1]
            keyword = Token.checkIfKeyword(tokText)
            if keyword is not None:  # Keyword
                token = Token(self.source[startPos: self.curPos + 1], keyword)
                if token.text.upper() == "CPP":
                    self.nextChar()
                    startPos = self.curPos
                    while self.peek() != "#":
                        self.nextChar()
                    token = Token(self.source[startPos: self.curPos + 1], TokenType.CPP_CODE)
                    self.nextChar()
                elif token.text.upper() == "ASM":
                    self.nextChar()
                    startPos = self.curPos
                    while self.peek() != "#":
                        self.nextChar()
                    token = Token(self.source[startPos: self.curPos + 1], TokenType.ASM_CODE)
                    self.nextChar()
            else: 
                tokText = tokText.upper()
                if(tokText == 'IN'):
                    token = Token(self.source[startPos: self.curPos + 1], TokenType.INPUT)
                elif(tokText == 'RET'):
                    token = Token(self.source[startPos: self.curPos + 1], TokenType.RETURN)
                else: # Identifier
                    operator = Token.checkIfOperator(tokText)
                    numSys = Token.checkIfNumSys(tokText)
                    if operator is not None:
                        token = Token(self.source[startPos: self.curPos + 1], operator)
                    elif numSys is not None:
                        token = Token(self.source[startPos: self.curPos + 1], numSys)
                        if(numSys == TokenType.BIN):
                            self.numSysMode = 2
                        elif(numSys == TokenType.BIN):
                            self.numSysMode = 8
                        elif(numSys == TokenType.BIN):
                            self.numSysMode = 10
                        else:
                            self.numSysMode = 16
                    else:
                        token = Token(self.source[startPos: self.curPos + 1], TokenType.IDENT)
        elif self.curChar == '\n':
            # New line
            token = Token('\n', TokenType.NEWLINE)
            self.curLine += 1
        elif self.curChar == '\0':
            # EOF
            token = Token('', TokenType.EOF)
        else:
            # Unknown token
            self.abort("Unknown token: " + self.curChar)
        self.nextChar()
        return token


    # Skip blanks except new lines, which will be used to indicate the end of an instruction
    def skipWhitespace(self):
        while self.curChar in (' ', '\t', '\r'):
            self.nextChar()

    # Skip comments
    def skipComment(self):
        if self.curChar == '#':
            if self.peek() == '#': # Multiline comment
                self.nextChar()
                self.nextChar()
                while self.curChar != '#' and self.peek() != '#':
                    self.nextChar()
                    if self.curChar == '\n':
                        # New line
                        self.curLine += 1
                self.nextChar()
                self.nextChar()
                self.nextChar()
                self.skipWhitespace()
            else: # Inline comment
                while self.curChar != '\n':
                    self.nextChar()


    # String correction
    def stringCorrection(self, str):
        newStr = ""
        for char in str:
            if char == '"':
                newStr += '\\'
            newStr += char
        return newStr

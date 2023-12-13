from TokenType import *




# Token contains the original text and the token type
class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText  # The actual text of the token, used for identifiers, strings and numbers
        self.kind = tokenKind  # The TokenType to which this token is classified


    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            tokenText = tokenText.upper()
            if kind.name == tokenText and 100 <= kind.value <= 999:
                return kind
        return None


    @staticmethod
    def checkIfOperator(tokenText):
        for kind in TokenType:
            tokenText = tokenText.upper()
            if kind.name == tokenText and 1000 <= kind.value <= 1999:
                return kind
        return None

    @staticmethod
    def checkIfAssignmentOperator(kind):
        if 1020 <= kind.value < 1039:
            return True
        return False

    @staticmethod
    def checkIfComparisonOperator(kind):
        if 1040 <= kind.value < 1049:
            return True
        return False

    @staticmethod
    def checkIfLogicalOperator(kind):
        if 1050 <= kind.value < 1059:
            return True
        return False


    @staticmethod
    def checkIfType(tokenText):
        for kind in TokenType:
            tokenText = tokenText.upper()
            if kind.name == tokenText and 3000 <= kind.value < 3999:
                return kind
        return None

    @staticmethod
    def checkIfCharType(tokenText):
        for kind in TokenType:
            tokenText = tokenText.upper()
            if kind.name == tokenText and 3040 <= kind.value < 3049:
                return kind
        return None

    @staticmethod
    def checkIfStringType(tokenText):
        for kind in TokenType:
            tokenText = tokenText.upper()
            if kind.name == tokenText and 3050 <= kind.value < 3059:
                return kind
        return None


    @staticmethod
    def checkIfNumSys(tokenText):
        for kind in TokenType:
            tokenText = tokenText.upper()
            if kind.name == tokenText and 4000 <= kind.value < 4999:
                return kind
        return None
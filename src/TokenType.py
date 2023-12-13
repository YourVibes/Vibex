import enum




# TokenType is the enum for all token types
class TokenType(enum.Enum):
    ###################
    ### END OF FILE ###
    ###################
    EOF             = -1


    #############
    ### BASIC ###
    #############
    NEWLINE         = 0
    NUMBER          = 1
    IDENT           = 2
    STRING_IDENT    = 3
    CPP_CODE        = 4
    ASM_CODE        = 5


    ################
    ### KEYWORDS ###
    ################
    # Libraries
    IMPORT          = 100

    # Basic
    VAR             = 110 # Variable
    ARR             = 111 # Array
    GLOBAL          = 112

    # Boolean values
    TRUE            = 120
    FALSE           = 121

    # Other values
    NULL            = 130
    UNDEFINED       = 131

    # Conditions
    IF              = 140
    ELIF            = 141
    ELSE            = 142
    SWITCH          = 143
    CASE            = 144
    DEFAULT         = 145

    # Loops
    FOR             = 150
    WHILE           = 151
    DO              = 152

    # Functions
    FUN             = 160 # Function
    RETURN          = 161

    # Jumps
    LABEL           = 170
    GOTO            = 171
    BREAK           = 172
    CONTINUE        = 173

    # Exceptions
    TRY             = 180
    CATCH           = 181
    FINALLY         = 182
    THROW           = 183

    # I/O
    INPUT           = 190
    PRINT           = 191
    PRINTLN         = 192
    WPRINT          = 193
    WPRINTLN        = 194

    # OOP
    CLASS           = 200

    # Super powers
    CPP             = 210
    ASM             = 211


    #################
    ### OPERATORS ###
    #################
    # Arithmetic
    PLUS            = 1000
    MINUS           = 1001
    ASTERISK        = 1002
    SLASH           = 1003
    PERCENT         = 1004
    ASTERISKASTERISK= 1005
    LABS            = 1006 # Left absolute (|
    RABS            = 1007 # Right absolute |)

    # Bitwise
    BW_AND          = 1010 # Bitwise And
    BW_OR           = 1011 # Bitwise Or
    BW_XOR          = 1012 # Bitwise Xor
    BW_LSHIFT       = 1013 # Bitwise Left Shift
    BW_RSHIFT       = 1014 # Bitwise Right Shift
    BW_NOT          = 1015 # Bitwise Not

    # Assignment
    EQ              = 1020
    PLUSEQ          = 1021
    MINUSEQ         = 1022
    ASTERISKEQ      = 1023
    SLASHEQ         = 1024
    PERCENTEQ       = 1025
    BW_ANDEQ        = 1026
    BW_OREQ         = 1027
    BW_XOREQ        = 1028
    BW_LSHIFTEQ     = 1029
    BW_RSHIFTEQ     = 1030

    # Comparison
    EQEQ            = 1040
    NOTEQ           = 1041
    LT              = 1042
    LTEQ            = 1043
    GT              = 1044
    GTEQ            = 1045

    # Logical
    AND             = 1050
    OR              = 1051
    NOT             = 1052

    # Misc
    INCREMENT       = 1060
    DECREMENT       = 1061


    ####################
    ### PUNCTUATIONS ###
    ####################
    COMMA           = 2000 # ,
    SEMICOLON       = 2001 # ;
    COLON           = 2002 # :
    DOT             = 2003 # .
    LBRACE          = 2004 # {
    RBRACE          = 2005 # }
    LBRACKET        = 2006 # [
    RBRACKET        = 2007 # ]
    LPAREN          = 2008 # (
    RPAREN          = 2009 # )

    #############
    ### TYPES ###
    #############
    # Void
    VOID            = 3000

    # Integer
    S_INT           = 3010 # short int
    INT             = 3011 # int
    L_INT           = 3012 # long int
    US_INT          = 3013 # unsigned short int
    U_INT           = 3014 # unsigned int
    UL_INT          = 3015 # unsigned long int

    # Float
    FLOAT           = 3020 # float

    # Double
    DOUBLE          = 3030 # double
    L_DOUBLE        = 3031 # long double

    # Char
    CHAR            = 3040 # char
    U_CHAR          = 3041 # unsigned char

    # String
    STRING          = 3050 # string
    WSTRING         = 3051 # wstring

    # Boolean
    BOOL            = 3060 # boolean


    #########################
    ### NUMERICAL SYSTEMS ###
    #########################
    BIN             = 4000 # Binary
    OCT             = 4001 # Octal
    DEC             = 4002 # Decimal
    HEX             = 4003 # Hexadecimal


    #######################
    ### PARSING SUPPORT ###
    #######################
    FUNCTION        = 10000
    ARRAY           = 10001
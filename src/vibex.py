# Made with <3 by Christian Alessandri
# With the help of Davide Sciaulino




#################
### LIBRARIES ###
#################
from Lexer import *
from Parser import *
from Emitter import *
from TerminalUtilities import *


import os
import sys
import platform
import subprocess
import json




#################
### CONSTANTS ###
#################
WINDOWS = 'Windows'
LINUX = 'Linux'
MACOS = 'macOS'
CPP_FILE_EXTENSION = '.cpp'




#################
### FUNCTIONS ###
#################
def title():
    print('  _   ___ __             _____                _ __       ')
    print(' | | / (_) /  _____ __  / ___/__  __ _  ___  (_) /__ ____')
    print(" | |/ / / _ \/ -_) \ / / /__/ _ \/  ' \/ _ \/ / / -_) __/")
    print(' |___/_/_.__/\__/_\_\  \___/\___/_/_/_/ .__/_/_/\__/_/   ')
    print('                                      /_/                ')


def detectOS():
    sys = platform.system()
    
    if sys == WINDOWS:
        return WINDOWS
    elif sys == LINUX:
        return LINUX
    elif sys == 'Darwin':
        return MACOS
    else:
        return -1


def getTokens(lexer):
    tokens = []
    tokens.append(lexer.getToken())
    while tokens[-1].kind != TokenType.EOF:
        tokens.append(lexer.getToken())
    tokens.append(lexer.getToken())
    return tokens


def convertVbxToCpp(source, fn):
    # Initialize the lexer, emitter, and parser
    lexer = Lexer(source)
    tokens = getTokens(lexer)

    emitter = Emitter(fn)
    parser = Parser(tokens, emitter)

    parser.program()  # Start the parser
    emitter.writeFile()  # Write the output to file


def deleteFile(myOS, fn):
    os.remove(fn) if myOS==WINDOWS else subprocess.run(['rm', fn])




#######################
### OTHER CONSTANTS ###
#######################
MY_OS = detectOS()




############
### MAIN ###
############
def main():
    title()
    print()


    # Find data.json
    vbxData = -1
    try:
        with open('data.json', 'r') as file:
            vbxData = json.load(file)
    except:
        print(warning('Warning: Cannot find the file data.json'))


    CPP_COMPILER = 'g++' if vbxData == -1 else vbxData['cpp_compiler']


    # Check arguments
    if len(sys.argv) < 3:
        if len(sys.argv) == 2:
            if sys.argv[1].lower() == '-h' or sys.argv[1].lower() == '--help':
                print('Usage: python3 vibex.py [options] file...\nOptions:')
                print('  --help or -h\t\tDisplay this information.')
                print('  -c <file>\t\tCompile Vibex file and get .exe file.')
                print('  -s <arg> <file>\tCompile Vibex file and get <arg> file.')
                print('  \t\t\t<arg> can be:')
                print('  \t\t\t  --asm\tFor assembly file')
                print('  \t\t\t  --cpp\tFor C++ file')
                print('  --version or -v\tDisplay compiler version information.')
                print('  --credits\t\tDisplay compiler authors information.')
        else:
            sys.exit(error('Error: Compiler needs at least three arguments.'))
    else:
        ###############
        ### COMPILE ###
        ###############
        if sys.argv[1] == '-c':
            if len(sys.argv) != 3:
                sys.exit(error('Error: Expected 3 arguments, got ' + str(len(sys.argv))))
            elif sys.argv[2][-4:] != '.vbx':
                sys.exit(error('Error: Compiler can compile only .vbx file.'))
            try:
                with open(sys.argv[2], 'r') as inputFile:
                    source = inputFile.read()
                fileName = sys.argv[2][:-4] + CPP_FILE_EXTENSION
                convertVbxToCpp(source, fileName)
                subprocess.run([CPP_COMPILER, fileName, '-o', 'out'])
                try:
                    deleteFile(MY_OS, fileName)
                except:
                    print(warning('Warning: Unable to delete ' + fileName))
                print('Compiling completed.')
            except FileNotFoundError:
                sys.exit(error(f"Error: The file '{sys.argv[2]}' was not found."))
            except IOError:
                sys.exit(error(f"Error: Unable to open the file '{sys.argv[2]}'."))
            """
            except Exception as e:
                sys.exit(error(f"Unknown error: {e}"))
            """


        ###############
        ### GET ASM ###
        ###############
        elif sys.argv[1].lower() == '-s' and sys.argv[2].lower() == '--asm':
            if len(sys.argv) != 4:
                sys.exit(error("Error: Expected 4 arguments, got " + str(len(sys.argv))))
            elif sys.argv[3][-4:] != '.vbx':
                sys.exit(error("Error: Compiler can compile only .vbx file."))

            try:
                with open(sys.argv[3], 'r') as inputFile:
                    source = inputFile.read()

                fileName = sys.argv[3][:-4] + CPP_FILE_EXTENSION
                convertVbxToCpp(source, fileName)
                subprocess.run([CPP_COMPILER, fileName, "-S"])
                try:
                    deleteFile(MY_OS, fileName)
                except:
                    print(warning("Warning: Unable to delete " + fileName))
                print("Compiling completed.")
            except FileNotFoundError:
                sys.exit(error(f"Error: The file '{sys.argv[2]}' was not found."))
            except IOError:
                sys.exit(error(f"Error: Unable to open the file '{sys.argv[2]}'."))
            """
            except Exception as e:
                sys.exit((f"Unknown error: {e}"))
            """


        ###############
        ### GET C++ ###
        ###############
        elif sys.argv[1].lower() == '-s':
            if len(sys.argv) != 3 and len(sys.argv) != 4:
                sys.exit(error("Error: Expected 3 or 4 arguments, got " + str(len(sys.argv))))
            argvIndex = 2
            if sys.argv[2].lower() == '--cpp':
                argvIndex = 3
            try:
                with open(sys.argv[argvIndex], 'r') as inputFile:
                    source = inputFile.read()

                fileName = sys.argv[argvIndex][:-4] + CPP_FILE_EXTENSION
                convertVbxToCpp(source, fileName)
                print("Compiling completed.")
            except FileNotFoundError:
                print(error(f"Error: The file '{sys.argv[2]}' was not found."))
            except IOError:
                print(error(f"Error: Unable to open the file '{sys.argv[2]}'."))
            """
            except Exception as e:
                print(error(f"Unknown error: {e}"))
            """


        ###############
        ### VERSION ###
        ###############
        elif sys.argv[1].lower() == '-v' or sys.argv[1].lower() == '--version':
            print(error("Error: Cannot find the file data.json")) if vbxData==-1 else print(f"Vibex version: {vbxData['version']}")


        ###############
        ### CREDITS ###
        ###############
        elif sys.argv[1] == '--credits':
            print(error("Error: Cannot find the file data.json")) if vbxData==-1 else print(f"Authors: {vbxData['authors']}")




if __name__ == "__main__":
    main()

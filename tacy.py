#-------------------------------------------------------------------------------
# Name:        tacy
# Purpose:     IPPe final project - Three code address interpreter
#
# Author:      Guillermo Montes Martos (xmonte03)
# Created:     April 18
#-------------------------------------------------------------------------------


import sys
from interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print('Error: wrong number of arguments. Ex: "python tacy.py <file.xml>"', file=sys.stderr)
        exit(20)
    app = Interpreter(sys.argv[1])
    app.run()

if __name__ == '__main__':
    main()
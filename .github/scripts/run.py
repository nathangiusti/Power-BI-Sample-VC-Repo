import requests
import sys


def main():
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

    for file in sys.argv:
        if file.endswith(".pbix"):
            print(file)
            
    print("Done")
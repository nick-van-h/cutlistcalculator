from cutlist import getCutLists
import sys
import argparse

if __name__ == '__main__':
    #Argument parser
    text = "This program calculates the most optimal cutlist for beams and planks."
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument("-i", "--input", help="custom location of input json file (e.g. 'localhost:8080/foo/bar.json'", default="")
    parser.add_argument("-o", "--output", help="custom location of output folder (e.g. 'localhost:8080/foo' -> 'localhost:8080/foo/cutlist_result.json'", default="")
    args = parser.parse_args()

    #Kick-off
    result = getCutLists(args.input, args.output)

    #Exit function with VS Code workaround
    try:
        sys.exit(result)
    except:
        print(result)
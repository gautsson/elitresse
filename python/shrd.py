import shrdlite

def getInput():	
    input = raw_input("\nEnter a command for SHRDLITE:\n\n")
    return input.split()

if __name__ == '__main__':
    x = getInput()
    y = shrdlite.parse(x)
    print y
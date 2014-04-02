import shrdlite

def getInput():	
    input = raw_input("\nEnter a command for SHRDLITE:\n\n")
    return input.split()
	
def searchBasicEntity(usrInput, world):
    objlist = []
    for worldObj in world:
        ok = True
        if usrInput[0] != "anyform" and usrInput[0] != world[worldObj]['form']:
            ok = False
        if usrInput[1] and usrInput[1] != world[worldObj]['size']:
            ok = False
        if usrInput[2] and usrInput[2] != world[worldObj]['color']:
            ok = False
        if ok:
            objlist.append(worldObj)
    return objlist

def interpret():
    world = {
        "a": { "form":"brick",   "size":"large",  "color":"green" },
        "b": { "form":"brick",   "size":"small",  "color":"white" },
        "c": { "form":"plank",   "size":"large",  "color":"red"   },
        "d": { "form":"plank",   "size":"small",  "color":"green" },
        "e": { "form":"ball",    "size":"large",  "color":"white" },
        "f": { "form":"ball",    "size":"small",  "color":"black" },
        "g": { "form":"table",   "size":"large",  "color":"blue"  },
        "h": { "form":"table",   "size":"small",  "color":"red"   },
        "i": { "form":"pyramid", "size":"large",  "color":"yellow"},
        "j": { "form":"pyramid", "size":"small",  "color":"red"   },
        "k": { "form":"box",     "size":"large",  "color":"yellow"},
        "l": { "form":"box",     "size":"large",  "color":"red"   },
        "m": { "form":"box",     "size":"small",  "color":"yellow"  }
    }
    objlist = searchBasicEntity(["box","small","yellow"], world)
    for obj in objlist:
        print obj

    

if __name__ == '__main__':
    x = getInput()
    y = shrdlite.parse(x)
    print y
    interpret()
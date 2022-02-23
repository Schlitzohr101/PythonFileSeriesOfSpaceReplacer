import os
import enum

import sys

class OperatingSystems(enum.Enum):
    MAC = 0
    WIN = 1
    LINUX =  2

os_dict = {
    "w": OperatingSystems.WIN,
    "m": OperatingSystems.MAC,
    "l": OperatingSystems.LINUX
}

slash_dict = {
    OperatingSystems.WIN: "\\",
    OperatingSystems.LINUX: "/",
    OperatingSystems.MAC: "/"
}



def fileloader(filepath, parameter = None):
    file = None
    try:
        if parameter == None:
            print("trying to open file: "+filepath)
            file = open(filepath)
        else:
            print("trying to open file: "+filepath+" w/ parameter",parameter)
            file = open(filepath,parameter)
    except Exception as e:
        print("failed to load file!!!")
        print(e)
        return None

    return file

def findNextNonSpace(somestr, str_pos):
    pos = -1
    for i in range(str_pos, len(somestr)):
        # print("i)",i, end="    ")
        # print("str[i]:",somestr[i])
        if somestr[i] != ' ':
            #print(somestr[str_pos: i], end="  ")
            #print("end of space series")
            pos = i
            break
    return pos

def parseSeriesOfSpacesToNewLine(somestring):
    new_data = ""
    space_pos = somestring.find(" ")
    nxt_nonspace = findNextNonSpace(somestring,space_pos)
    new_data = somestring[0:space_pos]

    while nxt_nonspace != -1:
        if nxt_nonspace - space_pos <= 100:
           # print("skipping! spaces were not a series going 100 spaces ahead")
            space_pos = somestring.find(" ", nxt_nonspace)
            new_data += somestring[nxt_nonspace:space_pos]
            nxt_nonspace = findNextNonSpace(somestring, space_pos)
        else:
            new_data+="\n"
            print("found series at")
            print("spacePos:", space_pos)
            print("next non space:",nxt_nonspace)

            print("next...")
            space_pos = somestring.find(" ", nxt_nonspace)
            new_data += somestring[nxt_nonspace:space_pos]
            nxt_nonspace = findNextNonSpace(somestring, space_pos)
    print("out of series to parse!!! ending ")
    return new_data






    return somestring




folderpath = os.path.dirname(__file__)
filename = ""
output_file_name = ""
opt_sys = None
fileGiven = False
osGiven = False
outputGiven = False

for arg in sys.argv:
    print(arg)
    if arg.find("-f") != -1 and not fileGiven:
        fileGiven = True
    elif fileGiven:
        fileGiven = False
        filename = arg
    elif arg.find("-os") != -1 and not osGiven:
        osGiven = True
    elif osGiven:
        if arg.lower().find("w") != -1:
            opt_sys = os_dict.get("w")
        elif arg.lower().find("m") != -1:
            opt_sys = os_dict.get("m")
        elif arg.lower().find("l") != -1:
            opt_sys = os_dict.get("l")
    elif arg.find("-o") != -1 and not outputGiven:
        outputGiven = True
    elif outputGiven:
        output_file_name = arg
        outputGiven = False

if filename == "":
    print("failed to give a file, please use -f flag followed by name of file in the same directory as this program...")
else:
    if opt_sys == None:
        print("no os given assuming windows, please use -os flag and specify what os win, mac, or linux")
        opt_sys = os_dict.get("w")
    
    slash_char = slash_dict.get(opt_sys)

    file_to_use = fileloader(folderpath+slash_char+filename)
    if file_to_use != None:
        print(file_to_use)
        print("file successfully loaded")

        data = file_to_use.read()

        data = parseSeriesOfSpacesToNewLine(data)

        print("\n\nRESULT:\n\n"+data)

        if output_file_name == "":
            print("no output file given using hw.txt as default")
            output_file_name = "hw.txt"

        file_to_write = fileloader(folderpath+slash_char+output_file_name, "w")
        if file_to_write != None:
            print("successfully opened file")
            file_to_write.close()
            file_to_write = fileloader(folderpath+slash_char+output_file_name,"w")
            file_to_write.write(data)
        else:
            print("failed to load...")

    else:
        print("failed to load file... ending program")
    
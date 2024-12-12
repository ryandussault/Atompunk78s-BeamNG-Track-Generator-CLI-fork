#Atompunk78's BeamNG Track Generator
#Licenced under the CC BY-NC-SA 4.0 (see licence.txt for more info)
version = "1.9"

from random import randint, choice
import json
import sys
import os
import math
from sys import argv

fileStart = """
{
  "author": "Atompunk78's Track Generator ?5",
  "connected": false,
  "date": "0",
  "defaultLaps": 1,
  "difficulty": 0,
  "environment": {
    "fog": 0.0005,
    "tod": {
      "azimuthOverride": 1,
      "dayLength": 0,
      "dayScale": 0,
      "nightScale": 0,
      "startTime": 0,
      "time": 0
    }
  },
  "length": 0,
  "level": "smallgrid",
  "materials": [],
  "reversible": true,
  "subPieces": [
    [
      {
        "bank": {
          "interpolation": "smoothSlope",
          "value": 0
        },
        "height": {
          "interpolation": "smoothSlope",
          "value": 0
        },
        "piece": "init",
        "width": {
          "interpolation": "smoothSlope",
          "value": ?4
        }
      },
      {
        "centerMesh": "?1",
        "leftMesh": "?2",
        "rightMesh": "?3",
        "length": 2,
        "piece": "freeForward"
      },
"""

fileEnd = """
      {
        "centerMesh": "?1",
        "leftMesh": "?2",
        "rightMesh": "?3",
        "length": 2,
        "piece": "freeForward"
      }
    ]
  ],
  "subTrackPositions": [
    {
      "hdg": 0,
      "x": 0,
      "y": 0,
      "z": ?4
    }
  ],
  "version": "1.1"
}
""" #the version just above represents the track editor version, not that of this program

currentFileString = ""
currentHeight = 0
currentLength = 0

try:
    with open("config.json", "r") as file:
        parameters = json.load(file)
except:
    print("\nThe config file cannot be read. If this issue persists, redownload the file.\n")
    sys.exit(1)

def findBeamNGVersion():
    n = 10
    found = False
    while not found:
        parameters["savePath"] = parameters["savePath"].replace("0."+str(n-1), "0."+str(n))
        if parameters["showDebugMessages"]:
            print("Trying for BeamNG version 0."+str(n))
        if os.path.exists(parameters["savePath"]):
            found = True
        n += 1
        if n >= 100:
            print("The path to BeamNG could not be found, you will have to manually enter the path to the trackEditor folder into the config file.")
            sys.exit(1)

if parameters["savePath"] == "AUTODETECT":
    print("Automatically detecting file path to BeamNG...")
    parameters["savePath"] = os.path.expanduser("~").replace("\\", "/") #just in case the backslashes cause issues
    if os.path.exists(parameters["savePath"]):
        parameters["savePath"] += "/AppData/Local/BeamNG.drive/0.34/trackEditor"
        if not os.path.exists(parameters["savePath"]):
            print("Path could not be found, retrying for new BeamNG versions...")
            findBeamNGVersion()
    else:
        print("Home directory could not be found, you will have to manually enter the path to the trackEditor folder into the config file.")
        sys.exit(1)
    with open("config.json", "w") as file:
        json.dump(parameters, file, indent=4)
        print("Path found and updated")

#analyzes all passed arguments and applies the passed values to the track parameters
def argalyzer(args):
    #loops through all passed args
    for arg in range(len(args)):
        #excludes the file path/execution command, which is the first arg
        if arg != 0:
          #parses parameter args into argument and value, args withour a value are just assigned to the argument variable
          try:
            argument,value = argv[arg].split("=")
          except ValueError:
              argument = argv[arg]

              #throw away to avoid error 
              value = 0
          
          #attepts to convert the value to an int, if that fails, a bool. and if that fails it throws an error
          try:
            value = int(value)
          #triggers when the 'value' part of the arg is not a number
          except ValueError:
                  #prevents the error message form printing when passing in a track name
                  if argument == "-tn" or argument == "-p":
                      pass
                  else:  
                    print(f"invalid argument: {argv[arg]}")
                    print_valid_args()
                    exit()

          #track length param
          if argument == "-tl":
              parameters["totalLength"] = value

          #track width param
          elif argument == "-tw":
              parameters["trackWidth"] = value

          #short straight distro param
          elif argument == "-ssd":
              param_distrobution_edit("tileTypeDist", 1, value)
          
          #long straight distro param
          elif argument == "-lsd":
              param_distrobution_edit("tileTypeDist", 2, value)
          
          #short turn distro param
          elif argument == "-std":
              param_distrobution_edit("tileTypeDist", 3, value)
          
          #long turn distro param
          elif argument == "-ltd":
              param_distrobution_edit("tileTypeDist", 4, value)
          
          #start height param
          elif argument == "-sh":
              parameters["startHeight"] = value

          #overwrite track param
          elif argument == "-dot":
              parameters["overwriteTracks"] = True

          #track name param
          elif argument == "-tn":
              parameters["trackName"] = value+".json"

          #controls the values of the height dist for all pieces
          elif argument == "-hm":
              height_multiplier(value/100)

          #controls the chance of a height change for all pieces
          elif argument == "-hcc":
              height_change_chance(value)

          #help menu param
          elif argument == "-h":
              print_valid_args()
              exit()

          #preset param
          elif argument == "-p":
              parameters["trackType"] = value
          
          #verbose param
          elif argument == "-v":
              parameters["showDebugMessages"] = True

          #error catcher for invalid inputs that still follow the proper input format
          else:
              print(f"unrecognized argument: {argv[arg]}")
              print_valid_args()
              exit()

#removes the default number of parameter designators (such as '1' when refering to short straight tile pieces in the tile type list) in any paramter that is a list, then adds the passed in amount, 
# function takes the parameter to be edited, the designator for the distrobution parameter (such as '1' when refering to short straight tile pieces), and the number of designators to be added
#TODO clean up tyle type designators to be self explanatory strings, not numbers
def param_distrobution_edit(param, distro_designator, new_distro_amount):
    #transfers all params over except the designated one
    param_distrobution_list = []
    for i in range(len(parameters[param])):
        if parameters[param][i] != distro_designator:
            param_distrobution_list.append(parameters[param][i])
    #appends the specified number of param designators to the new list
    for j in range(new_distro_amount):
        param_distrobution_list.append(distro_designator)
    #sets the list in the specified parameter to the new list
    parameters[param] = param_distrobution_list

#controls the heights in the parameters
def height_multiplier(mult):
    for x in range(len(parameters["shortStraightHeightDist"])):
        parameters["shortStraightHeightDist"][x] *= mult
    for x in range(len(parameters["shortTurnHeightDist"])):
        parameters["shortTurnHeightDist"][x] *= mult
    for x in range(len(parameters["longTurnHeightDist"])):
        parameters["longTurnHeightDist"][x] *= mult
    for x in range(len(parameters["longStraightHeightDist"])):
        parameters["longStraightHeightDist"][x] *= mult

def height_change_chance(chance):
    parameters["shortStraightHeightChanceDist"].clear()
    parameters["shortTurnHeightChanceDist"].clear()
    parameters["longStraightHeightChanceDist"].clear()
    parameters["longTurnHeightChanceDist"].clear()

    no_chance = 100-chance

    for x in range(chance):
      parameters["shortStraightHeightChanceDist"].append(1)
      parameters["shortTurnHeightChanceDist"].append(1)
      parameters["longStraightHeightChanceDist"].append(1)
      parameters["longTurnHeightChanceDist"].append(1)
    for y in range(no_chance):
      parameters["shortStraightHeightChanceDist"].append(0)
      parameters["shortTurnHeightChanceDist"].append(0)
      parameters["longStraightHeightChanceDist"].append(0)
      parameters["longTurnHeightChanceDist"].append(0)
#prints the help message
def print_valid_args():
    print("")
    print(" valid argument structure follows '-param=value', ie '-tl=50', which sets the total track length to 50")
    print(" all arguments, unless otherwise specified, take a value\n")
    print(" valid commands include:")
    print(" -tl     sets the total track length")
    print(" -tw     sets the tracks width")
    print(" -ssd    changes the distribution of the short straight tile type, the default is 2")
    print(" -lsd    changes the distribution of the long straight tile type, the default is 2")
    print(" -std    changes the distribution of the short turn tile type, the default is 8")
    print(" -ltd    changes the distribution of the long turn tile type, the default is 2")
    print(" -dot   causes the program to not overwrite the same track file, takes no input")
    print(" -sh     sets the starts height of the track, values below 1 do not work")
    print(" -tn     changes the track name, takes a string, no spaces for now")
    print(" -p      changes the preset, if passed all other command line arguments will be ignored and the preset loaded, takes the name of the preset as a string")
    print(" -hm     height multiplier, takes am integer representing percent multipler (ie: input of 50=50% multiplier), changes the height change of the track pieces")
    print(" -hcc    height change chance, controls the chance of the height of a piece differing from the last, take a whole number representing a percent(ie: an input of 25=25% chance of height change)")
    print(" -v      verbose, shows debug messages, takes no value")
    print(" -h      prints this help message\n")

#pre check to see if any args have been passed
if len(argv) > 1:
    argalyzer(argv)

if parameters["trackType"] != "custom":
  try:
      with open(f"Presets/{parameters['trackType']}.json", "r") as file:
          parameters |= json.load(file)
  except FileNotFoundError:
      print(f"\nThe preset {parameters['trackType']}.json cannot be found.\n")
      sys.exit(1)
  except:
      print(f"\nThe preset cannot be read. Fix any syntax errors, and if this issue persists, redownload the file.\n")
      sys.exit(1)

fileName = parameters["savePath"] + "/" + parameters["trackName"]

fileStart = fileStart.replace("?1", parameters["centreMeshType"]).replace("?2", parameters["leftMeshType"]).replace("?3", parameters["rightMeshType"]).replace("?4", str(parameters["trackWidth"])).replace("?5", "v"+version)
fileEnd = fileEnd.replace("?1", parameters["centreMeshType"]).replace("?2", parameters["leftMeshType"]).replace("?3", parameters["rightMeshType"]).replace("?4", str(parameters["startHeight"]))

def addPiece():
    global currentHeight
    global currentLength
    randomNumber = choice(parameters["tileTypeDist"])

    if randomNumber == 1: #short straight
        length = randint(parameters["shortStraightLengthMin"], parameters["shortStraightLengthMax"])
        currentHeight += choice(parameters["shortStraightHeightDist"])
        currentHeight=height_check(currentHeight)
        newPiece = f"""
      [
        "centerMesh": \"{parameters['centreMeshType']}\",
        "leftMesh": \"{parameters['leftMeshType']}\",
        "rightMesh": \"{parameters['rightMeshType']}\",
        "length": {length},
        "piece": "freeForward"?
      ],"""
        if choice(parameters["shortStraightHeightChanceDist"]) == 1: #only sometimes update height
            newPiece = newPiece.replace("?",f""",
        "height": [
          "interpolation": "smoothSlope",
          "value": {currentHeight}
        ]""")
        currentLength += length * 4
        
    elif randomNumber == 2: #long straight
        length = randint(parameters["longStraightLengthMin"], parameters["longStraightLengthMax"])
        currentHeight += choice(parameters["longStraightHeightDist"])
        currentHeight=height_check(currentHeight)
        newPiece = f"""
      [
        "centerMesh": \"{parameters['centreMeshType']}\",
        "leftMesh": \"{parameters['leftMeshType']}\",
        "rightMesh": \"{parameters['rightMeshType']}\",
        "length": {length},
        "piece": "freeForward"?
      ],"""
        if choice(parameters["longStraightHeightChanceDist"]) == 1:
            newPiece = newPiece.replace("?",f""",
        "height": [
          "interpolation": "smoothSlope",
          "value": {currentHeight}
        ]""")
        currentLength += length * 4
        
    elif randomNumber == 3: #short turn
        direction = choice([-1,1])
        length = randint(parameters["shortTurnLengthMin1"], parameters["shortTurnLengthMax1"]) + randint(parameters["shortTurnLengthMin2"], parameters["shortTurnLengthMax2"])
        radius = randint(parameters["shortTurnRadiusMin1"], parameters["shortTurnRadiusMax1"]) + randint(parameters["shortTurnRadiusMin2"], parameters["shortTurnRadiusMax2"])
        currentHeight += choice(parameters["shortTurnHeightDist"])
        currentHeight=height_check(currentHeight)
        newPiece = f"""
      [
        "centerMesh": \"{parameters['centreMeshType']}\",
        "leftMesh": \"{parameters['leftMeshType']}\",
        "rightMesh": \"{parameters['rightMeshType']}\",
        "direction": {direction},
        "length": {length},
        "piece": "freeCurve",
        "radius": {radius}?
      ],"""
        if choice(parameters["shortTurnHeightChanceDist"]) == 1:
            newPiece = newPiece.replace("?",f""",
        "height": [
          "interpolation": "smoothSlope",
          "value": {currentHeight}
        ]""")
        currentLength += round(2 * math.pi * radius * (length / 360), 1)
        
    elif randomNumber == 4: #long turn
        direction = choice([-1,1])
        length = randint(parameters["longTurnLengthMin1"], parameters["longTurnLengthMax1"]) + randint(parameters["longTurnLengthMin2"], parameters["longTurnLengthMax2"])
        radius = randint(parameters["longTurnRadiusMin1"], parameters["longTurnRadiusMax1"]) + randint(parameters["longTurnRadiusMin2"], parameters["longTurnRadiusMax2"])
        if radius <= parameters["longTurnRadiusMax1"]: #stops too long and gentle corners somewhat
            length += randint(parameters["longTurnLengthMin2"], parameters["longTurnLengthMax2"])
        currentHeight += choice(parameters["longTurnHeightDist"])
        #prevents heights below 1
        currentHeight=height_check(currentHeight)
        newPiece = f"""
      [
        "centerMesh": \"{parameters['centreMeshType']}\",
        "leftMesh": \"{parameters['leftMeshType']}\",
        "rightMesh": \"{parameters['rightMeshType']}\",
        "direction": {direction},
        "length": {length},
        "piece": "freeCurve",
        "radius": {radius}?
      ],"""
        if choice(parameters["longTurnHeightChanceDist"]) == 1:
            newPiece = newPiece.replace("?",f""",
        "height": [
          "interpolation": "smoothSlope",
          "value": {currentHeight}
        ]""")
        currentLength += round(2 * math.pi * radius * (length / 360), 1)

    return newPiece.replace("[","{").replace("]","}").replace("?","")

def height_check(current_height):
    if parameters["startHeight"]+current_height<1:
        current_height=1
        return current_height
    else:
      return current_height

acceptableTrack = False
while not acceptableTrack: #makes sure track doesn't go below 0 height
    acceptableTrack = True
    while currentLength < parameters["totalLength"]:
      if acceptableTrack:
          if parameters["startHeight"] + currentHeight > 0:
              currentFileString += addPiece()
          else:
              acceptableTrack=False
    if not acceptableTrack and parameters["showDebugMessages"]:
      currentFileString = ""
      currentHeight = 0
      print("\nTrack layout invalid, regenerating track...",end="")

currentFileString = fileStart + currentFileString + fileEnd

if not parameters["overwriteTracks"]:
  with open("data.txt", "r+") as file:
      try:
        data = eval(file.read())
      except:
          data = []
      existingFile = False
      for name in data:
          if fileName == name[0]:
              existingFile = True
              dataLocation = data.index(name)
      if existingFile:
          data[dataLocation][1] += 1
          saveName = fileName.replace(".json","") + "_" + str(data[dataLocation][1])
      else:
          data.append([fileName, 1])
          saveName = fileName.replace(".json","") + "_1"
      saveName += ".json"
  
  with open("data.txt", "w") as file:
      file.write(str(data))
else:
    saveName = fileName

with open(saveName, "w") as file:
    file.write(currentFileString)

print(f"\nTrack successfully generated and saved to {saveName}\n")

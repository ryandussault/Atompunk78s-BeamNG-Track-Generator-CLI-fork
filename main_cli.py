#Atompunk78's BeamNG Track Generator
#Licenced under the CC BY-NC-SA 4.0 (see licence.txt for more info)
version = "1.10"

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
  "materialFields":{
    "A":{
      "baseTexture":"/core/art/trackBuilder/track_editor_?6_d.dds",
      "groundtype":"?7"
    },
    "B":{},
    "C":{},
    "D":{},
    "E":{},
    "F":{},
    "G":{},
    "H":{}
  },
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
currentPosition = [0, 0, 0]
currentHeading = 0 #degrees
step = 1.0
increment=5.0

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
    global step
    global increment
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
                  #prevents the error message form printing when passing in a string for certian arguments
                  if argument == "-p" or argument == "-tn" or argument == "-tt" or argument == "-tm":
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

          #disable overlap protection param
          elif argument == "-dod":
              parameters["checkForOverlap"] = False

          #track name param
          elif argument == "-tn":
              parameters["trackName"] = value+".json"

          #Track texture param
          elif argument == "-tt":
              parameters["trackTexture"] = value

          #track material param
          elif argument == "-tm":
              parameters["groundType"] = value

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
          #step param for long tracks  
          elif argument == "-step":
              step=value  
          #increment command for long tracks  
          elif argument == "-inc":
              increment = value

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
    print(" -dot    causes the program to not overwrite the same track file, takes no input")
    print(" -dod    disable overlap detection, takes no input, when passed it disables overlap protection")
    print(" -sh     sets the starts height of the track, values below 1 do not work")
    print(" -tn     changes the track name, takes a string, no spaces for now")
    print(" -p      changes the preset, if passed height and piece related arguments will be ignored, takes the name of the preset as a string")
    print(" -hm     height multiplier, takes am integer representing percent multipler (ie: input of 50=50% multiplier), changes the height change of the track pieces")
    print(" -hcc    height change chance, controls the chance of the height of a piece differing from the last, take a whole number representing a percent(ie: an input of 25=25% chance of height change)")
    print(" -tt     track texture, takes a string, lower case, possible options are: 'base', 'mud', 'ice', 'grass', 'sand' (no quotes)")
    print(" -tm     track material, takes a string, controls the type of surface, main choices are: 'SAND', 'MUD', 'GRASS', 'ASPHALT', 'CONCRETE', 'ICE', 'DIRT', 'ASPHALT_PREPPED' (no quotes)")
    print(" -v      verbose, shows debug messages, takes no value")
    print(" -h      prints this help message\n")
    print(" -step   default of 1, set to 4 for tracks greater than 10,000 in length, only applies when using overlap detection")
    print(" -inc    increment, similar to step, default value is 5, recommend a value of 10 for tracks >10,000 in length, only applies when usig overlap detection")
    print(" \nfor long tracks, >10,000 length, when using overlap detection, double both step and increment, (defaults: step=1, increment=5)\n  every doubling of step and increment decreases compute time by about 4x, however each increase sacrifices accuracy")

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

fileStart = fileStart.replace("?1", parameters["centreMeshType"]).replace("?2", parameters["leftMeshType"]).replace("?3", parameters["rightMeshType"]).replace("?4", str(parameters["trackWidth"])).replace("?5", "v"+version).replace("?6", parameters["trackTexture"]).replace("?7", parameters["groundType"])
fileEnd = fileEnd.replace("?1", parameters["centreMeshType"]).replace("?2", parameters["leftMeshType"]).replace("?3", parameters["rightMeshType"]).replace("?4", str(parameters["startHeight"]))

positions = [(0, 0, parameters["startHeight"])]
print()

def segments_intersect(p1, p2, p3, p4): #this function is primarily written by ChatGPT; comments have been removed, for documentation check under the fridge
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    x3, y3 = p3[0], p3[1]
    x4, y4 = p4[0], p4[1]

    def orientation(ax, ay, bx, by, cx, cy):
        val = (by - ay) * (cx - bx) - (bx - ax) * (cy - by)
        if val > 0:
            return 1
        elif val < 0:
            return 2
        return 0

    def on_segment(ax, ay, bx, by, cx, cy):
        return min(ax,bx) <= cx <= max(ax,bx) and min(ay,by) <= cy <= max(ay,by)
    
    o1 = orientation(x1, y1, x2, y2, x3, y3)
    o2 = orientation(x1, y1, x2, y2, x4, y4)
    o3 = orientation(x3, y3, x4, y4, x1, y1)
    o4 = orientation(x3, y3, x4, y4, x2, y2)

    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and on_segment(x1, y1, x2, y2, x3, y3):
        return True
    if o2 == 0 and on_segment(x1, y1, x2, y2, x4, y4):
        return True
    if o3 == 0 and on_segment(x3, y3, x4, y4, x1, y1):
        return True
    if o4 == 0 and on_segment(x3, y3, x4, y4, x2, y2):
        return True
    return False

def check_overlaps():
    for i in range(len(positions)-1):
        for j in range(i+3, len(positions)-1):
            p1 = positions[i]
            p2 = positions[i+1]
            p3 = positions[j]
            p4 = positions[j+1]

            if segments_intersect(p1, p2, p3, p4):
                z_avg_seg1 = (p1[2] + p2[2]) / 2.0
                z_avg_seg2 = (p3[2] + p4[2]) / 2.0
                if abs(z_avg_seg1 - z_avg_seg2) < 12:
                    return False
    return True

def UpdatePositions(height, length, radius=None, direction=None): #also primarily ChatGPT; o1 is so powerful
    global positions, currentHeading, increment, step
    x_start, y_start, _ = positions[-1]

    if radius is None:
        # Straight segment subdivision
        steps = int(math.ceil(length / step))
        for s in range(1, steps+1):
            dist = s * step
            if dist > length:
                dist = length
            nx = x_start + dist * math.sin(math.radians(currentHeading))
            ny = y_start + dist * math.cos(math.radians(currentHeading))
            nz = height
            positions.append((nx, ny, nz))
    else:
        # Curved segment subdivision
        angle_delta = -length * direction
        increment = increment if abs(angle_delta) >= 5 else angle_delta
        scaled_radius = radius * 4
        center_angle = currentHeading - 90 * direction
        cx = x_start + scaled_radius * math.sin(math.radians(center_angle))
        cy = y_start + scaled_radius * math.cos(math.radians(center_angle))
        dx = x_start - cx
        dy = y_start - cy
        theta_start = math.degrees(math.atan2(dx, dy))

        total_steps = int(abs(angle_delta) / increment)
        sign = 1 if angle_delta > 0 else -1

        current_angle = theta_start
        for s in range(1, total_steps+1):
            a = current_angle + increment * sign
            # check if we overshoot the final angle
            final_angle = theta_start + angle_delta
            if sign > 0 and a > final_angle:
                a = final_angle
            elif sign < 0 and a < final_angle:
                a = final_angle
            nx = cx + scaled_radius * math.sin(math.radians(a))
            ny = cy + scaled_radius * math.cos(math.radians(a))
            nz = height
            positions.append((nx, ny, nz))
            current_angle = a

        currentHeading = (currentHeading + angle_delta) % 360


def addPiece():
    global currentHeight
    global currentLength
    global positions
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
        UpdatePositions(currentHeight, length)
        
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
        UpdatePositions(currentHeight, length)
        
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
        currentLength += round(2 * math.pi * (radius * 4) * (length / 360), 1)
        UpdatePositions(currentHeight, length, radius, direction)
        
    elif randomNumber == 4: #long turn
        direction = choice([-1,1])
        length = randint(parameters["longTurnLengthMin1"], parameters["longTurnLengthMax1"]) + randint(parameters["longTurnLengthMin2"], parameters["longTurnLengthMax2"])
        radius = randint(parameters["longTurnRadiusMin1"], parameters["longTurnRadiusMax1"]) + randint(parameters["longTurnRadiusMin2"], parameters["longTurnRadiusMax2"])
        if radius <= parameters["longTurnRadiusMax1"]: #stops too long and gentle corners somewhat
            length += randint(parameters["longTurnLengthMin2"], parameters["longTurnLengthMax2"])
        currentHeight += choice(parameters["longTurnHeightDist"])
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
        currentLength += round(2 * math.pi * (radius * 4) * (length / 360), 1)
        UpdatePositions(currentHeight, length, radius, direction)

    return newPiece.replace("[","{").replace("]","}").replace("?","")

def height_check(current_height):
    if parameters["startHeight"]+current_height<1:
        current_height=1
        return current_height
    else:
      return current_height

acceptableTrack = False
count = 0
while not acceptableTrack: #makes sure track doesn't go below 0 height
    acceptableTrack = True
    currentFileString = ""
    currentHeight = 0
    currentLength = 0
    positions = [(0, 0, parameters["startHeight"])]
    currentHeading = 0

    while currentLength < parameters["totalLength"]:
      if acceptableTrack:
          if parameters["startHeight"] + currentHeight > 0:
              currentFileString += addPiece()
          else:
              acceptableTrack = False

    if acceptableTrack and parameters["checkForOverlap"]:
        acceptableTrack = check_overlaps()

    if not acceptableTrack and parameters["showDebugMessages"]:
      print("Track layout invalid, regenerating track, attempt: ", count)
    count += 1
    if count > 1000:
        print("\nMaximum retries reached, exiting program. If this keeps happening, lower the maximum length or disable checkForOverlap.\n")
        sys.exit(1)

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

print(f"Track successfully generated and saved to {saveName}\n")

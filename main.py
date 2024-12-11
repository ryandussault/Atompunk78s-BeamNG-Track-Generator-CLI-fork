#Atompunk78's BeamNG Track Generator
#Licenced under the CC BY-NC-ND 4.0 (see licence.txt for more info)
version = "1.6"

from random import randint, choice
import json
import sys

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

try:
    with open("config.json", "r") as file:
        parameters = json.load(file)
except:
    print("\nThe config file cannot be read. If this issue persists, redownload the file.\n")
    sys.exit(1)

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
    randomNumber = choice(parameters["tileTypeDist"])

    if randomNumber == 1: #short straight
        length = randint(parameters["shortStraightLengthMin"], parameters["shortStraightLengthMax"])
        currentHeight += choice(parameters["shortStraightHeightDist"])
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
        
    elif randomNumber == 2: #long straight
        length = randint(parameters["longStraightLengthMin"], parameters["longStraightLengthMax"])
        currentHeight += choice(parameters["longStraightHeightDist"])
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
        
    elif randomNumber == 3: #short turn
        direction = choice([-1,1])
        length = randint(parameters["shortTurnLengthMin1"], parameters["shortTurnLengthMax1"]) + randint(parameters["shortTurnLengthMin2"], parameters["shortTurnLengthMax2"])
        radius = randint(parameters["shortTurnRadiusMin1"], parameters["shortTurnRadiusMax1"]) + randint(parameters["shortTurnRadiusMin2"], parameters["shortTurnRadiusMax2"])
        currentHeight += choice(parameters["shortTurnHeightDist"])
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
        
    elif randomNumber == 4: #long turn
        direction = choice([-1,1])
        length = randint(parameters["longTurnLengthMin1"], parameters["longTurnLengthMax1"]) + randint(parameters["longTurnLengthMin2"], parameters["longTurnLengthMax2"])
        radius = randint(parameters["longTurnRadiusMin1"], parameters["longTurnRadiusMax1"]) + randint(parameters["longTurnRadiusMin2"], parameters["longTurnRadiusMax2"])
        if radius <= parameters["longTurnRadiusMax1"]: #stops too long and gentle corners somewhat
            length += randint(parameters["longTurnLengthMin2"], parameters["longTurnLengthMax2"])
        currentHeight += choice(parameters["longTurnHeightDist"])
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

    return newPiece.replace("[","{").replace("]","}").replace("?","")

acceptableTrack = False
while not acceptableTrack: #makes sure track doesn't go below 0 height
    acceptableTrack = True
    for i in range(parameters["totalLength"]):
      if acceptableTrack:
          if parameters["startHeight"] + currentHeight > 0:
              currentFileString += addPiece()
          else:
              acceptableTrack = False
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
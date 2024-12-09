#Atompunk78's BeamNG Track Generator
#Licenced under the CC BY-NC-ND 4.0 (see licence.txt for more info)
#v1.3

from random import randint, choice

fileStart = """
{
  "author": "Atompunk78's Track Generator v1.3",
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
      "z": 50
    }
  ],
  "version": "1.1"
}
""" #the version just above represents the track editor version, not that of this program

currentFileString = ""
currentHeight = 0

parameters = {
    "savePath": "C:/Users/User/AppData/Local/BeamNG.drive/0.33/trackEditor/Atompunk78's_autogen_track.json", #this path will break every time there's a major beamng update
    "overwriteTracks": True, #should the newly-generated track overwrite the old one?
    "totalLength": 100,
    "trackWidth": 8,
    "centreMeshType": "flat",
    "leftMeshType": "smallDiagonal",
    "rightMeshType": "smallDiagonal",
    "tileTypeDist": [1,2,3,3,3,4],
    "shortStraightLengthMin": 2,
    "shortStraightLengthMax": 4,
    "shortStraightHeightDist": [-1,0,1],
    "shortStraightHeightChanceDist": [0,0,1],
    "longStraightLengthMin": 4,
    "longStraightLengthMax": 10,
    "longStraightHeightDist": [-8,-5,-2,0,2,5,8],
    "longStraightHeightChanceDist": [0,0,1],
    "shortTurnLengthMin1": 10,
    "shortTurnLengthMax1": 20,
    "shortTurnLengthMin2": 5,
    "shortTurnLengthMax2": 20,
    "shortTurnRadiusMin1": 1,
    "shortTurnRadiusMax1": 8,
    "shortTurnRadiusMin2": 1,
    "shortTurnRadiusMax2": 8,
    "shortTurnHeightDist": [-1,0,1],
    "shortTurnHeightChanceDist": [0,0,1],
    "longTurnLengthMin1": 15,
    "longTurnLengthMax1": 60,
    "longTurnLengthMin2": 15,
    "longTurnLengthMax2": 60,
    "longTurnRadiusMin1": 3,
    "longTurnRadiusMax1": 16,
    "longTurnRadiusMin2": 3,
    "longTurnRadiusMax2": 16,
    "longTurnHeightDist": [-8,-3,0,0,3,8],
    "longTurnHeightChanceDist": [0,1],
}

fileStart = fileStart.replace("?1", parameters["centreMeshType"]).replace("?2", parameters["leftMeshType"]).replace("?3", parameters["rightMeshType"]).replace("?4", str(parameters["trackWidth"]))
fileEnd = fileEnd.replace("?1", parameters["centreMeshType"]).replace("?2", parameters["leftMeshType"]).replace("?3", parameters["rightMeshType"])

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


for i in range(parameters["totalLength"]):
    currentFileString += addPiece()

currentFileString = fileStart + currentFileString + fileEnd

if not parameters["overwriteTracks"]:
  with open("data.txt", "r+") as file:
      try:
        data = eval(file.read())
      except:
          data = []
      existingFile = False
      for name in data:
          if parameters["savePath"] == name[0]:
              existingFile = True
              dataLocation = data.index(name)
      if existingFile:
          data[dataLocation][1] += 1
          saveName = parameters["savePath"].replace(".json","") + "_" + str(data[dataLocation][1])
      else:
          data.append([parameters["savePath"], 1])
          saveName = parameters["savePath"].replace(".json","") + "_1"
      saveName += ".json"
  
  with open("data.txt", "w") as file:
      file.write(str(data))
else:
    saveName = parameters["savePath"]

with open(saveName, "w") as file:
    file.write(currentFileString)

print(f"\nTrack successfully generated and saved to {saveName}\n")
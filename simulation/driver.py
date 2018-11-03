import argparse
import json
import os

from simulation import viticulture_monte_carlo
from viticulture import WineOrderDeck, Field, FieldType


def GenerateResultsNameFromParameters(Parameters):

    Fields = Parameters["Fields"]
    return "S{0:d}{1:d}_M{2:d}{3:d}_L{4:d}{5:d}_OPT{6:d}results.json".format(
        Fields['0']["Capacity"],
        Fields['0']["Layout"],
        Fields['1']["Capacity"],
        Fields['1']["Layout"],
        Fields['2']["Capacity"],
        Fields['2']["Layout"],
        Parameters["Optimization"]
    )

def GenerateFieldsParameterFromFile(FieldFile):

    with open(FieldFile, 'r') as f:
        FileText = f.read()
        return json.loads(FileText)


def GenerateFieldMapFromParameters(FieldParams):


    SField = Field(5)
    MField = Field(6)
    LField = Field(7)

    MParams = FieldParams['1']
    LParams = FieldParams['2']

    MRedGrade = int((MParams["Capacity"] + MParams["Layout"])/2)
    MWhiteGrade = int(abs((MParams["Capacity"] - MParams["Layout"]) / 2))

    LRedGrade = int((LParams["Capacity"] + LParams["Layout"]) / 2)
    LWhiteGrade = int(abs((LParams["Capacity"] - LParams["Layout"]) / 2))

    MField.SetField(RedGrade=MRedGrade, WhiteGrade=MWhiteGrade)
    LField.SetField(RedGrade=LRedGrade, WhiteGrade=LWhiteGrade)

    return {
        FieldType.SMALL  : SField,
        FieldType.MEDIUM : MField,
        FieldType.LARGE  : LField
    }



def Simulate(WineDeckFile, FieldParamPath, ResultPath):

    # WineDeck = WineOrderDeck("wine_def.csv")
    WineDeck = WineOrderDeck(WineDeckFile)

    NumSim = 1500
    OptLevel = 1


    for filename in os.listdir(FieldParamPath):

        FieldParams = GenerateFieldsParameterFromFile(FieldParamPath + filename)
        FieldMap = GenerateFieldMapFromParameters(FieldParams)

        Parameters = {
            "Fields": FieldParams,
            "Optimization": OptLevel
        }

        OutName = GenerateResultsNameFromParameters(Parameters)

        ResultsDict = {}
        for i in range(NumSim):

            WineDeck.ReshuffleDeck()

            Results = viticulture_monte_carlo.Play(FieldMap, WineDeck, OptLevel)

            ResultsDict[i] = Results

        SimulationLog = {
            "Parameters": Parameters,
            "Results": ResultsDict
        }

        with open(ResultPath + OutName, 'w') as f:
            f.write(json.dumps(SimulationLog, indent=2))



def Simulate_SameDeck(WineDeckFile, FieldParamPath, ResultPath):

    # WineDeck = WineOrderDeck("wine_def.csv")
    WineDeck = WineOrderDeck(WineDeckFile)

    NumSim = 1500
    OptLevel = 1

    FileMap = {}

    for filename in os.listdir(FieldParamPath):

        FieldParams = GenerateFieldsParameterFromFile(FieldParamPath + filename)
        FieldMap = GenerateFieldMapFromParameters(FieldParams)

        Parameters = {
            "Fields": FieldParams,
            "Optimization": OptLevel
        }

        OutName = GenerateResultsNameFromParameters(Parameters)

        FileMap[filename] = {
            "FieldParams" : FieldParams,
            "FieldMap" : FieldMap,
            "Parameters" : Parameters,
            "OutName" : OutName
        }


    # [{
    #   Simulation : 1,
    #   Results :
    #     {
    #     File1 : Results,
    #     File2 : Results
    #     }
    #   }, ...

    for i in range(NumSim):

        WineDeck.ReshuffleDeck()

        ResultsDict = {}
        for filename in os.listdir(FieldParamPath):



            Results = viticulture_monte_carlo.Play(FileMap[filename]["FieldMap"], WineDeck, OptLevel)

            ResultsDict[i] = Results

        SimulationLog = {
            "Parameters": FileMap[filename]["Parameters"],
            "Results": ResultsDict
        }

        with open(ResultPath + FileMap["OutName"], 'w') as f:
            f.write(json.dumps(SimulationLog, indent=2))




if __name__ == '__main__':


    parser = argparse.ArgumentParser(description="Process simulation parameters", add_help=True)

    parser.add_argument('-w', dest='WineDeckFile', type=str, help="Wine deck csv file")
    parser.add_argument('-f', dest='FieldParamPath', type=str, help="Path to field parameters")
    parser.add_argument('-o', dest='ResultsPath', type=str, help="Path to store results")
    # parser.add_help()

    args = parser.parse_args()

    if not os.path.isdir(args.ResultsPath):
        os.makedirs(args.ResultsPath)

    Simulate(args.WineDeckFile, args.FieldParamPath, args.ResultsPath)












from ViticultureConstants import *
import Solver
from WineOrderDeck import WineOrderDeck
from Player import Player
from Field import  Field
import json
import time
from collections import defaultdict
import copy

def NaivePlay(FieldMap, WineDeck):


    Mondavi = Player()

    # For now, we'll hard code our initial conditions,
    # but eventually, we'll be setting these parametrically
    Mondavi.SetFieldMap(FieldMap)

    YearsPassed = 0

    CurrentObjective = None
    HarvestPath = []
    FieldsHarvested = []
    OrdersCompleted = []

    while Mondavi.GetVP() < 20:

        # If we do not have a current objective, pick one up.
        if CurrentObjective is None:
            CurrentObjective = WineDeck.DrawCard()


            # Get the path we need to take to meet the objective.
            Path = Solver.GetPathForObjective(
                CurrentObjective,
                Mondavi.GetCrushPad(),
                Mondavi.GetCellar(),
                Mondavi.GetFieldMap()
            )

            # Solver.DetermineWhenToTurnGrapesToWine(
            #     CurrentObjective,
            #     copy.deepcopy(Path),
            #     copy.deepcopy(Mondavi.GetCrushPad()),
            #     copy.deepcopy(Mondavi.GetCellar()),
            #     copy.deepcopy(Mondavi.GetFieldMap())
            # )


            # This can happen if we cannot fulfill the order. Just increment the year and move on.
            if not Path:
                CurrentObjective = None
                YearsPassed += 1
                continue


            HarvestPath = Path


        # Harvest the next field.
        (FieldToHarvest, IsCritical) = HarvestPath.pop(0)
        FieldsHarvested.append(FieldToHarvest)

        # Harvest and add to the Crush pad
        Mondavi.HarvestField(FieldToHarvest)

        # See if our need is fulfilled.
        UsedGrapes = defaultdict(list)
        if Solver.NeedIsFulfilled(CurrentObjective, Mondavi.GetCrushPad(), Mondavi.GetCellar(), UsedGrapes):
            # Remove the grapes that we are using from the crush pad.

            for GrapeList in UsedGrapes.values():
                Mondavi.RemoveGrapesFromCrushPad(GrapeList)

            # Increase our number of victory points
            Mondavi.AddVP(CurrentObjective.GetVP())

            OrdersCompleted.append(
                {
                    "Order" : CurrentObjective.PrintDictionary(),
                    "Year" : YearsPassed
                }
            )

            # Reset out objective
            CurrentObjective = None


        Mondavi.Age()
        YearsPassed += 1

    return \
        {
            "Years" : YearsPassed,
            "Fields" : FieldsHarvested,
            "Orders" : OrdersCompleted,
            "VP" : Mondavi.GetVP()
        }


def Play(FieldMap, WineDeck):

    Mondavi = Player()

    Mondavi.SetFieldMap(FieldMap)

    YearsPassed = 0

    CurrentObjective = None
    NextObjective = None
    HarvestPath = []
    FieldsHarvested = []
    OrdersCompleted = []

    while Mondavi.GetVP() < 20:

        # If we do not have a current objective, pick one up.
        if CurrentObjective is None:
            CurrentObjective = WineDeck.DrawCard()

            # Get the path we need to take to meet the objective.
            Path = Solver.GetPathForObjective(
                CurrentObjective,
                Mondavi.GetCrushPad(),
                Mondavi.GetCellar(),
                Mondavi.GetFieldMap()
            )

            # This can happen if we cannot fulfill the order. Just increment the year and move on.
            if not Path:
                YearsPassed += 1
                continue

            HarvestPath = Path

        # Harvest the next field.
        (FieldToHarvest, IsCritical) = HarvestPath.pop(0)
        FieldsHarvested.append(FieldToHarvest)

        # Harvest and add to the Crush pad
        Mondavi.HarvestField(FieldToHarvest)

        # See if our need is fulfilled.
        UsedGrapes = defaultdict(list)
        if Solver.NeedIsFulfilled(CurrentObjective, Mondavi.GetCrushPad(), Mondavi.GetCellar(), UsedGrapes):
            # Remove the grapes that we are using from the crush pad.

            for GrapeList in UsedGrapes.values():
                Mondavi.RemoveGrapesFromCrushPad(GrapeList)

            # Increase our number of victory points
            Mondavi.AddVP(CurrentObjective.GetVP())

            OrdersCompleted.append(
                {
                    "Order": CurrentObjective.PrintDictionary(),
                    "Year": YearsPassed
                }
            )

            # Reset out objective.
            # It's either None or something. In either case, it works for us.
            CurrentObjective = copy.deepcopy(NextObjective)
            NextObjective = None

        elif not IsCritical and NextObjective is None:

            NextObjective = WineDeck.DrawCard()

            HarvestPath = Solver.ResolveObjectives(
                CurrentObjective,
                NextObjective,
                HarvestPath,
                copy.deepcopy(Mondavi.GetCrushPad()),
                copy.deepcopy(Mondavi.GetCellar()),
                Mondavi.GetFieldMap()
            )


            pass

        Mondavi.Age()
        YearsPassed += 1

    return \
        {
            "Years": YearsPassed,
            "Fields": FieldsHarvested,
            "Orders": OrdersCompleted,
            "VP" : Mondavi.GetVP()
        }




def Simulate(Parameters, OptimizationLevel, NumSims=1000):
    pass

if __name__ == '__main__':


    WineDeck = WineOrderDeck("WineOrderDefPython.csv")
    # FieldMap = ParseFieldMap("FieldMap.txt")


    NumSim = 1500

    SField = Field(5)
    MField = Field(6)
    LField = Field(7)

    MField.SetField(RedGrade=3, WhiteGrade=3)
    LField.SetField(RedGrade=4, WhiteGrade=3)

    FieldMap = {
        FieldType.SMALL  : SField,
        FieldType.MEDIUM : MField,
        FieldType.LARGE  : LField
    }


    Parameters = {
        "Fields" : {
            FieldType.SMALL : SField.GetLayout(),
            FieldType.MEDIUM : MField.GetLayout(),
            FieldType.LARGE : LField.GetLayout(),
        },
        "Optimization" : 1
    }

    Optimization = 0

    print(json.dumps(Parameters, indent=2))

    ResultsDict = {}
    for i in range(NumSim):

        WineDeck.ReshuffleDeck()

        if Optimization == 1:
            Results = Play(FieldMap, WineDeck)
        else:
            Results = NaivePlay(FieldMap, WineDeck)

        ResultsDict[i] = Results


    SimulationLog = {
        "Parameters" : Parameters,
        "Results" : ResultsDict
    }


    # print(json.dumps(SimulationLog, indent=2))

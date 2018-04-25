from ViticultureConstants import *
import Solver
from WineOrderDeck import WineOrderDeck
from Player import Player
from Field import  Field
import cProfile
import time
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

            Solver.DetermineWhenToTurnGrapesToWine(
                CurrentObjective,
                copy.deepcopy(Path),
                copy.deepcopy(Mondavi.GetCrushPad()),
                copy.deepcopy(Mondavi.GetCellar()),
                copy.deepcopy(Mondavi.GetFieldMap())
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
        UsedGrapes = []
        if Solver.NeedIsFulfilled(CurrentObjective, Mondavi.GetCrushPad(), Mondavi.GetCellar(), UsedGrapes):

            # Remove the grapes that we are using from the crush pad.
            Mondavi.RemoveGrapesFromCrushPad(UsedGrapes)

            # Increase our number of victory points
            Mondavi.AddVP(CurrentObjective.GetVP())

            OrdersCompleted.append(
                {
                    "Order" : CurrentObjective,
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
            "Orders" : OrdersCompleted
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
        UsedGrapes = []
        if Solver.NeedIsFulfilled(CurrentObjective, Mondavi.GetCrushPad(), Mondavi.GetCellar(), UsedGrapes):
            # Remove the grapes that we are using from the crush pad.
            Mondavi.RemoveGrapesFromCrushPad(UsedGrapes)

            # Increase our number of victory points
            Mondavi.AddVP(CurrentObjective.GetVP())

            OrdersCompleted.append(
                {
                    "Order": CurrentObjective,
                    "Year": YearsPassed
                }
            )

            # Reset out objective.
            # It's either None or something. In either case, it works for us.
            CurrentObjective = NextObjective

        elif not IsCritical and NextObjective is None:

            NextObjective = WineDeck.DrawCard()

            # Solver.ResolveObjectives(CurrentObjective, NextObjective, Mondavi.GetCrushPad(), Mondavi.GetCellar(), Mondavi.GetFieldMap())

            pass

        Mondavi.Age()
        YearsPassed += 1

    return \
        {
            "Years": YearsPassed,
            "Fields": FieldsHarvested,
            "Orders": OrdersCompleted
        }


    # For now, we'll hard code our initial conditions,
    # but eventually, we'll be setting these parametrically
    # MField.SetField(RedGrade=3, WhiteGrade=3)
    # LField.SetField(RedGrade=4, WhiteGrade=3)
    #
    # WineDeck = WineOrderDeck("WineOrderDefPython.csv")
    #
    #
    # YearsPassed = 0
    #
    # ObjectiveSet = False
    # CurrentObjective = None
    # NextObjective = None
    # HarvestPath = []
    #
    # while MyPlayer.GetVP() < 20:
    #
    #     # If we do not have a current objective, pick one up.
    #     if not ObjectiveSet:
    #         CurrentObjective = WineDeck.DrawCard()
    #
    #
    #         # Get the path we need to take to meet the objective.
    #         Path = Solver.GetPathForObjective(CurrentObjective, CPad, Cellar, FieldMap)
    #
    #
    #         # This can happen if we cannot fulfill the order. Just increment the year and move on.
    #         if not Path:
    #             YearsPassed += 1
    #             continue
    #
    #         ObjectiveSet = True
    #         HarvestPath = Path
    #
    #
    #     # Harvest the next field.
    #     (FieldToHarvest, IsCritical) = HarvestPath.pop(0)
    #
    #     # Harvest and add to the Crush pad
    #     GrapesFromField = FieldMap[FieldToHarvest].HarvestField()
    #     CPad.AddGrapes(GrapesFromField)
    #
    #     # See if our need is fulfilled.
    #     UsedGrapes = []
    #     if Solver.NeedIsFulfilled(CurrentObjective, CPad, UsedGrapes):
    #
    #         # Remove the grapes that we are using from the crush pad.
    #         CPad.RemoveGrapes(UsedGrapes)
    #
    #         # Increase our number of victory points
    #         CurrentVP += CurrentObjective.GetVP()
    #
    #         # Reset out objective
    #         CurrentObjective = NextObjective if NextObjective is not None else None
    #         ObjectiveSet = CurrentObjective is not None
    #
    #     elif not IsCritical and NextObjective is None:
    #         print("got here")
    #
    #
    #
    #
    #     CPad.AgeCrushPad()
    #
    #     YearsPassed += 1



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

    start_time = time.time()

    for i in range(NumSim):

        WineDeck.ReshuffleDeck()

        Results = NaivePlay(FieldMap, WineDeck)





    print("\nExecution Time: {0:0.5f}s".format(time.time() - start_time))
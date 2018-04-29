import copy
from collections import defaultdict

from simulation import Solver
from viticulture import Wine, WineOrder, WineOrderDeck, FieldType, Field, \
    WineType, Player, VP_THRESHOLD


def DebugPlay(FieldMap, WineDeck, OptLevel):

    Mondavi = Player()

    Mondavi.SetFieldMap(FieldMap)

    YearsPassed = 0

    WineDeckl = [
        WineOrder([Wine(WineType.WHITE, 4), Wine(WineType.BLUSH, 4)], 3, 2),
        WineOrder([Wine(WineType.RED, 6), Wine(WineType.WHITE, 6)], 3, 2),
        WineOrder([Wine(WineType.RED, 3), Wine(WineType.WHITE, 1)], 3, 2),
    ]

    CurrentObjective = None
    NextObjective = None
    HarvestPath = []
    FieldsHarvested = []
    OrdersCompleted = []
    VPTime = []

    while Mondavi.GetVP() < 20 and YearsPassed < 25:

        print("Top of loop:")
        print(CurrentObjective)
        print(HarvestPath)
        print(Mondavi.GetCrushPad())
        print()

        # If we do not have a current objective, pick one up.
        if CurrentObjective is None:
            CurrentObjective = WineDeckl.pop(0)

            # Get the path we need to take to meet the objective.
            Path = Solver.GetPathForObjective(
                CurrentObjective,
                Mondavi.GetCrushPad(),
                Mondavi.GetCellar(),
                Mondavi.GetFieldMap()
            )

            if len(WineDeckl) == 2:
                Path = [(FieldType.MEDIUM, True), (FieldType.MEDIUM, True)]
            elif len(WineDeckl) == 1:
                Path = [(FieldType.MEDIUM, True), (FieldType.MEDIUM, False), (FieldType.LARGE, False)]

            # This can happen if we cannot fulfill the order. Just increment the year and move on.
            if not Path:
                CurrentObjective = None
                VPTime.append(Mondavi.GetVP())
                YearsPassed += 1
                continue

            HarvestPath = Path
            print("Set objective:")
            print(CurrentObjective)
            print(HarvestPath)
            print(Mondavi.GetCrushPad())
            print()

        # Harvest the next field.
        if not HarvestPath:
            HarvestPath.append(FieldType.LARGE)

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

            print("Complete objective:")
            print(CurrentObjective)
            print(HarvestPath)
            print(Mondavi.GetCrushPad())
            print()

            if CurrentObjective:
                print("Switched from next -> current")

        elif not IsCritical and NextObjective is None and OptLevel > 0:

            NextObjective = WineDeckl.pop(0)

            (HarvestPath, Resolved) = ([(FieldType.MEDIUM, True), (FieldType.MEDIUM, False)], True)

            if not Resolved:
                NextObjective = None
            else:
                print("Got next objective")
                print(NextObjective)
                print(HarvestPath)
                print(Mondavi.GetCrushPad())
                print()


        Mondavi.Age()
        VPTime.append(Mondavi.GetVP())
        YearsPassed += 1

    return \
        {
            "Years": YearsPassed,
            "Fields": FieldsHarvested,
            "Orders": OrdersCompleted,
            "VP" : Mondavi.GetVP(),
            "VPTime" : VPTime
        }






def Play(FieldMap, WineDeck, OptLevel):

    Mondavi = Player()

    Mondavi.SetFieldMap(FieldMap)

    YearsPassed = 0

    CurrentObjective = None
    NextObjective = None
    HarvestPath = []
    FieldsHarvested = []
    OrdersCompleted = []
    VPTime = []

    while Mondavi.GetVP() < VP_THRESHOLD and YearsPassed < 25:

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
                CurrentObjective = None
                VPTime.append(Mondavi.GetVP())
                YearsPassed += 1
                continue

            HarvestPath = Path

        # Harvest the next field.
        if not HarvestPath:
            HarvestPath.append((FieldType.LARGE, False))

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


        elif not IsCritical and NextObjective is None and OptLevel > 0:

            NextObjective = WineDeck.DrawCard()

            (HarvestPath, Resolved) = Solver.ResolveObjectives(
                CurrentObjective,
                NextObjective,
                HarvestPath,
                copy.deepcopy(Mondavi.GetCrushPad()),
                copy.deepcopy(Mondavi.GetCellar()),
                Mondavi.GetFieldMap()
            )

            if not Resolved:
                NextObjective = None


        Mondavi.Age()
        VPTime.append(Mondavi.GetVP())
        YearsPassed += 1

    return \
        {
            "Years": YearsPassed,
            "Fields": FieldsHarvested,
            "Orders": OrdersCompleted,
            "VP" : Mondavi.GetVP(),
            "VPTime" : VPTime
        }


if __name__ == '__main__':


    WineDeck = WineOrderDeck("wine_def.csv")
    # FieldMap = ParseFieldMap("FieldMap.txt")


    NumSim = 1500

    SField = Field(5)
    MField = Field(6)
    LField = Field(7)

    MField.SetField(RedGrade=2, WhiteGrade=4)
    LField.SetField(RedGrade=6, WhiteGrade=1)

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

    Results = DebugPlay(FieldMap, WineDeck, 1)

    ResultsDict = {}
    for i in range(NumSim):

        print(i)

        WineDeck.ReshuffleDeck()

        Results = DebugPlay(FieldMap, WineDeck, 1)

        ResultsDict[i] = Results


    SimulationLog = {
        "Parameters" : Parameters,
        "Results" : ResultsDict
    }

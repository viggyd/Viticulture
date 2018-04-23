from ViticultureConstants import *
from Cellar import WineCellar
from CrushPad import CrushPad
from WineOrder import WineOrder
from Grape import Grape
from Field import Field
from Wine import Wine
import copy
import collections
import pprint
import random
import csv

# Hello!
# You will note that there is a lot of list comprehension going on here.
# I am as of yet unsure of how this will affect the final simulations.
# But it's always better to optimize later as needed.







def NeedIsFulfilled(Order, Crush):

    # Check if the wine order can be filled based on the crush pad given
    CrushMap = Crush.GetCrushMap()
    NumNeeded = Order.GetNumRedWhiteGrapes()

    # Sanity check. If we don't have the right number of each type, we may as well give up now.
    for Key, Val in NumNeeded.items():

        if len(CrushMap[Key]) < Val:
            return False



    NumFulfilled = 0

    WinesInOrder = Order.GetWines()

    # Separate into different arrays based on type needed to fill
    RedWhiteWines = [x for x in WinesInOrder if x.GetType() == WineType.RED or x.GetType() == WineType.WHITE]
    BlushWines = [x for x in WinesInOrder if x.GetType() == WineType.BLUSH]
    SparklingWines = [x for x in WinesInOrder if x.GetType() == WineType.SPARKLING]

    for Bottle in RedWhiteWines:


        if Bottle.GetType() == WineType.RED \
            or Bottle.GetType() == WineType.WHITE:

            # See if it is in the crush map
            GrapeArray = CrushMap[Bottle.GetType()]

            # Get all grapes that satisfy the condition
            TestFill = [x for x in GrapeArray if x >= Bottle.GetGrade()]

            # If we have no grapes that meet the condition, the need is not yet met.
            if not TestFill:
                return False

            # Remove the grape from our crush pad and increment number of fulfilled wines in the order.
            CrushMap[Bottle.GetType()].remove(min(TestFill))
            NumFulfilled += 1


    # We're going to do something tricky here. We aren't actually going to 'solve' the
    # sparkling need. We know that a sparkling is 2R-1W. Which is just an additional
    # Red away from a blush. Well, what we can do is remove the minimum reds from the
    # red crush map and pretend that all the rest are actually blush. It takes a bit more
    # processing to do, but we'll see. I can't think of a better way to do this...
    #
    # NOTE: This may not be entirely accurate.
    for Bottle in SparklingWines:

        CurrentMinRed = min(CrushMap[GrapeType.RED])

        # Get the would-be blush wine grade and create the new wine based on that grade
        BlushGrade = Bottle.GetGrade() - CurrentMinRed
        BlushWine = Wine(WineType.BLUSH, BlushGrade)

        # Add the new blush wine to our list of blush wines
        BlushWines.append(BlushWine)

        # Remove the min red from our crush pad.
        CrushMap[GrapeType.RED].remove(CurrentMinRed)


    # Now, we just have to figure out how we're going to solve this part. :D
    # A brute force approach would be to do find all possible combinations for all bottles.
    # Here's the idea:
    # Take the smallest grape (including both red and white)
    # Find the smallest opposite grape that meets the bottle's condition.
    # If it is found, remove both from the crush pad
    # If it is not found, try the next min.
    # Repeat.
    #
    # I believe this is the best way to go about this.
    #
    for Bottle in BlushWines:

        RedCrush = CrushMap[GrapeType.RED]
        WhiteCrush = CrushMap[GrapeType.WHITE]

        # Trying to figure out how to solve this is tricky because there are so many combinations.
        # It almost feels like the sparkling and blush have to be solved at the same time. Hmm.

        pass






        # for j, Item in enumerate(Grapes):
        #
        #     if Item.MeetsGrade(Bottle.GetType(), Bottle.GetGrade()):
        #         GrapeFound = True
        #         GrapeRemove = j
        #         break
        #
        # if GrapeFound:
        #     NumFulfilled += 1
        #     del Grapes[GrapeRemove]
        #     GrapeFound = False
        #     GrapeRemove = -1
        # else:
        #     return False

    return NumFulfilled == len(Order.GetWines())

    # If we only have basic types and we're done, return now. Yay
    # if len(Order) == 0:
    #     return True



    # For blush/sparkling, it is easier to use a dictionary with lists of red/white.






    pass



def DetermineBestPath(Order, CPad, FieldMap, FullPath, CurrentBranch=0, Years=0, CurrentPath=list(), Initial=True):
    """
    Do a depth first search to exhaustively list all possible field harvestations until we can fulfill our order.
    """

    # Base condition:
    # Check if need is fulfilled based on crush pad
    if NeedIsFulfilled(Order, CPad):
        if CurrentPath not in FullPath: # Only append if not in paths we already know.
            FullPath.append(CurrentPath)
        return

    # Break condition
    # This is used to avoid stack overflows.
    if Years >= 10:
        print("ERROR: Unable to determine a path to complete objective. The program has failed.")
        return

    # Special case if initial entry
    if Initial:
        DetermineBestPath(Order, copy.deepcopy(CPad), FieldMap, FullPath, FieldType.MEDIUM, Years + 1, copy.deepcopy(CurrentPath), False)
        DetermineBestPath(Order, copy.deepcopy(CPad), FieldMap, FullPath, FieldType.LARGE, Years + 1, copy.deepcopy(CurrentPath), False)
        return

    # Harvest field and add to crush pad
    Grapes = FieldMap[CurrentBranch].HarvestField(True)
    CPad.AddGrapes(Grapes)
    CurrentPath.append(CurrentBranch)
    CPad.AgeCrushPad()

    # Recurse!
    DetermineBestPath(Order, copy.deepcopy(CPad), FieldMap, FullPath, FieldType.MEDIUM, Years + 1, copy.deepcopy(CurrentPath), False)
    DetermineBestPath(Order, copy.deepcopy(CPad), FieldMap, FullPath, FieldType.LARGE, Years + 1, copy.deepcopy(CurrentPath), False)



def RemoveSuboptimalPaths(HarvestPaths):

    # Find lengths of all items in harvest paths
    Lengths = [len(x) for x in HarvestPaths]
    MinPath = min(Lengths)
    return [x for x in HarvestPaths if len(x) == MinPath]



def DetermineCriticalHarvests(HarvestPaths, Order):

    CriticalHarvests = []

    for Path in HarvestPaths:


        # Create an array of copies of paths.
        CriticalHarvestsInYear = []
        for i in range(len(Path)):

            TestPath = copy.deepcopy(Path)
            TestPath[i] = -1

            CPad = CrushPad()

            for Year in TestPath:

                if Year == -1:
                    CPad.AgeCrushPad()
                    continue

                # Harvest field, add grapes to crush pad, then age.
                Grapes = FieldMap[Year].HarvestField(True)
                CPad.AddGrapes(Grapes)
                CPad.AgeCrushPad()

            # At the end, see if the need is still fulfilled.
            # Basically, if need is fulfilled, the harvest isn't critical, hence the not in front.
            CriticalHarvestsInYear.append(not NeedIsFulfilled(Order, CPad))

        Test = list(zip(copy.deepcopy(Path), CriticalHarvestsInYear))
        CriticalHarvests.append(Test)



    return CriticalHarvests



def ChoosePath(CriticalHarvests):


    # Count the number of critical harvests
    TotalCriticals = [[x[1] for x in y] for y in CriticalHarvests]

    # Add them all up
    TotalCriticals = [sum(x) for x in TotalCriticals]

    # Determine fewest number of critical harvest from all options
    MinCritical = min(TotalCriticals)

    # Get only indices where we meet the minimum critical
    TotalCriticals = [i for i, x in enumerate(TotalCriticals, 1) if x == MinCritical]
    # TotalCriticals = [x for x in TotalCriticals if x == MinCritical]

    # Okay, now we want to minimize the final critical harvest. That is, if we have two critical harvests,
    # We want them to be as early as possible. So [1 1 0 0] is preferable to [1 0 1 0].
    MinCriticalPaths = [x for i, x in enumerate(CriticalHarvests, 1) if i in TotalCriticals]

    # Determine indices with critical harvests
    CriticalIndices = [[i for i, x in enumerate(y, 1) if x[1]] for y in MinCriticalPaths]

    # Foreach of the paths, determine the maximum year the critical harvest occurs
    MaxCriticalHarvest = [max(x) for x in CriticalIndices]

    # Determine the least upper bound (min of all maxes, i.e. the least of all evils)
    SupremumCritical = min(MaxCriticalHarvest)

    # Now, take all those paths that meet the minimum
    FinalCandidateIndices = [i for i, x in enumerate(MaxCriticalHarvest) if x == SupremumCritical]

    # Determine final list of candidates by making sure the selected indices can be found in the pool
    FinalCandidates = [x for i, x in enumerate(MinCriticalPaths) if i in FinalCandidateIndices]

    # I've run out of heuristics at the moment. If we really don't have anything better, pick randomly.
    # At this point, they are equal.
    # Get a random one since it doesn't really matter at this point.
    Index = random.randint(1, len(FinalCandidates))


    return FinalCandidates[Index - 1]











def EstimateYears(Order, CPad, Cellar, FieldMap):

    # This is tricky.

    # First figure out what wines we need to create
    NeededWines = Order.GetWines()

    # Now, figure out the minimum grades needed to fulfill the order.
    # The difficulty is in determining the minima for filling multi grape orders.
    NeededReds = []
    NeededWhites = []
    NumRed = 0
    NumWhite = 0
    for Bottle in NeededWines:

        if Bottle.GetType() == WineType.RED:
            NeededReds.append(Bottle.GetGrade())
            NumRed += 1
        elif Bottle.GetType() == WineType.WHITE:
            NeededWhites.append(Bottle.GetGrade())
            NumWhite += 1
        elif Bottle.GetType() == WineType.BLUSH:
            NumRed += 1
            NumWhite += 1
        else:
            NumRed += 2
            NumWhite += 1

    # So now we have the numbers we need.
    print("Number of red grapes needed: {0:d}\nNumber of white grapes needed: {1:d}".format(NumRed, NumWhite))


    HarvestPaths = []
    DetermineBestPath(Order, CPad, FieldMap, HarvestPaths)
    HarvestPaths = RemoveSuboptimalPaths(HarvestPaths)
    CriticalHarvests = DetermineCriticalHarvests(HarvestPaths, Order)
    CurrentPath = ChoosePath(CriticalHarvests)

    return CurrentPath


def DetermineYearToDrawNewOrder(CurrentPath):
    pass



def ConstructWineDeck(FilePath):
    WineDeck = []

    with open(FilePath, 'r') as f:

        WineReader = csv.DictReader(f, delimiter=',')

        for row in WineReader:

            Wines = WineListFromTextFile(row['wines'])
            WineDeck.append(WineOrder(Wines, row['vp'], row['residual']))

    return WineDeck

def WineListFromTextFile(WineListStr):

    # Remove the []
    TempStr = WineListStr[1:-1]

    WineArray = TempStr.split()

    Wines = []
    for Item in WineArray:

        Grade = Item[0]
        Type = Item[1]
        WType = WineType.RED

        if Type.lower() == "r":
            WType = WineType.RED
        elif Type.lower() == "w":
            WType = WineType.WHITE
        elif Type.lower() == "b":
            WType = WineType.BLUSH
        elif Type.lower() == "s":
            WType = WineType.SPARKLING

        Wines.append(Wine(WType, Grade))

    return Wines



if __name__ == '__main__':

    pp = pprint.PrettyPrinter(indent=2)

    # Set up our game.
    # We will be starting with a full field...
    SField = Field(5)
    MField = Field(6)
    LField = Field(7)

    Cellar = WineCellar()
    CPad = CrushPad()

    # For now, we'll hard code our initial conditions,
    # but eventually, we'll be setting these parametrically
    MField.SetField(RedGrade=3, WhiteGrade=3)
    LField.SetField(RedGrade=4, WhiteGrade=3)


    WineDeck = ConstructWineDeck("WineOrderDefPython.csv")



    # WineList = [Wine(WineType.RED, 7), Wine(WineType.WHITE, 6)] # Expected 2 years from empty

    WineList = [Wine(WineType.BLUSH, 9), Wine(WineType.RED, 6), Wine(WineType.WHITE, 6)]

    CurrentWineOrder = WineOrder(WineList, 6, 2)


    FieldMap = {
        FieldType.SMALL : SField,
        FieldType.MEDIUM : MField,
        FieldType.LARGE : LField
    }

    # Okay, so we now have our objective. What now?
    # We play the game. Let's try to estimate how many years it'll take to fulfill this order
    CurrentPath = EstimateYears(CurrentWineOrder, CPad, Cellar, FieldMap)

    print("Number of years to complete objective: {0:d}".format(len(CurrentPath) + 1))
    pp.pprint(CurrentPath)


    # ChoosePath(
    #     [
    #     [(FieldType.LARGE, True), (FieldType.MEDIUM, False), (FieldType.LARGE, True), (FieldType.MEDIUM, False)],
    #     [(FieldType.LARGE, True), (FieldType.LARGE, True), (FieldType.MEDIUM, False), (FieldType.MEDIUM, False)]
    #     ]
    # )



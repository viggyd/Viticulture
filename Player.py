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

def GrapeMapFromGrapes(Grapes):

    GrapeMap = collections.defaultdict(list)

    for Grp in Grapes:
        GrapeMap[Grp.GetType()].append(Grp.GetGrade())

    return GrapeMap


def GetNumRedWhiteGrapeFromOrder(Order):

    NumFillNeeds = {
        GrapeType.RED : 0,
        GrapeType.WHITE : 0
    }

    for Bottle in Order.GetWines():

        if Bottle.GetType() == WineType.RED:
            NumFillNeeds[GrapeType.RED] += 1
        elif Bottle.GetType() == WineType.WHITE:
            NumFillNeeds[GrapeType.WHITE] += 1
        elif Bottle.GetType() == WineType.BLUSH:
            NumFillNeeds[GrapeType.RED] += 1
            NumFillNeeds[GrapeType.WHITE] += 1
        elif Bottle.GetType() == WineType.SPARKLING:
            NumFillNeeds[GrapeType.RED] += 2
            NumFillNeeds[GrapeType.WHITE] += 1

    return NumFillNeeds

def NeedIsFulfilled(Order, Crush):

    # Check if the wine order can be filled based on the crush pad given

    Grapes = Crush.GetGrapes()

    CrushMap = GrapeMapFromGrapes(Grapes)
    NumNeeded = GetNumRedWhiteGrapeFromOrder(Order)

    # Sanity check. If we don't have the right number of each type, we may as well give up now.
    for Key, Val in NumNeeded.items():

        if len(CrushMap[Key]) < Val:
            return False



    NumFulfilled = 0


    WinesInOrder = Order.GetWines()

    # Separate into different arrays based on type needed to fill
    RedWhiteWines = [x for x in WinesInOrder if x.GetType() == WineType.RED or x.GetType == WineType.WHITE]
    BlushWines = [x for x in WinesInOrder if x.GetType() == WineType.BLUSH]
    SparklingWines = [x for x in WinesInOrder if x.GetType() == WineType.SPARKLING]

    for Bottle in RedWhiteWines:


        if Bottle.GetType() == WineType.RED \
            or Bottle.GetType() == WineType.WHITE:

            # See if it is in the crush map
            GrapeArray = CrushMap[Bottle.GetType()]
            TestFill = [x for x in GrapeArray if x >= Bottle.GetGrade()]

            # We can't fill it if we can't fill this one.
            if not TestFill:
                return False

            # 'Remove' from our crush pad and increment number of wines filled
            CrushMap[Bottle.GetType()].remove(min(TestFill))
            NumFulfilled += 1


    for Bottle in BlushWines:
        pass


    for Bottle in SparklingWines:
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

    print("break")

    ImaginaryCrush = CrushPad()
    ImaginaryCellar = WineCellar()

    OrderFulfilled = False
    NumYears = 0

    HarvestPaths = []
    DetermineBestPath(Order, CPad, FieldMap, HarvestPaths)
    HarvestPaths = RemoveSuboptimalPaths(HarvestPaths)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(HarvestPaths)

    # Keep going until we can fill the order
    # while not OrderFulfilled:
    #
    #     # Harvest a field
    #
    #     # Make two wines (optional)
    #
    #     # Increment number of years it'll take
    #     NumYears += 1








if __name__ == '__main__':


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

    # TODO: Add a wine order deck to randomly draw wine orders.
    WineList = [Wine(WineType.RED, 7), Wine(WineType.WHITE, 6)] # Expected 2 years from empty
    CurrentWineOrder = WineOrder(WineList, 6, 2)


    FieldMap = {
        FieldType.SMALL : SField,
        FieldType.MEDIUM : MField,
        FieldType.LARGE : LField
    }

    # Okay, so we now have our objective. What now?
    # We play the game. Let's try to estimate how many years it'll take to fulfill this order
    EstimateYears(CurrentWineOrder, CPad, Cellar, FieldMap)









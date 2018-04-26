from ViticultureConstants import *
from CrushPad import CrushPad
from Grape import Grape
from Wine import Wine
import copy
import random
from collections import defaultdict




def ResolveObjectives(CurrentObjective, NextObjective, HarvestPath, Crush, Cellar, FieldMap):


    NumRedWhite = CurrentObjective.GetNumRedWhiteGrapes()


    for Type, Number in NumRedWhite.items():

        # Remove from the crush pad the number of red/white in the order.
        for i in range(Number):

            Crush.RemoveLargestGrape(Type)


    # If we have any excess, it is ours to do with as we please. Leave them.
    NewObjPath = GetPathForObjective(NextObjective, Crush, Cellar, FieldMap)

    Delta = len(HarvestPath) - len(NewObjPath)

    HarvestPath = NewObjPath
    for i in range(Delta + 1):
        HarvestPath.append((random.choice([FieldType.MEDIUM, FieldType.LARGE]), False))


    return HarvestPath






def DetermineWhenToTurnGrapesToWine(Order, Path, Crush, Cellar, FieldMap):

    # Harvest critical paths and age the rest.
    for (FieldHarvest, FieldIsCritical) in Path:

        Crush.AgeCrushPad()
        Cellar.AgeCellar()

        if FieldIsCritical:
            Crush.AddGrapes(FieldMap[FieldHarvest].HarvestField(True))




    # Get a map for which wines require which grapes.
    WineGrapeMap = defaultdict(list)
    NeedIsFulfilled(Order, Crush, Cellar, WineGrapeMap)


    for (FieldHarvest, FieldIsCritical) in reversed(Path):

        # If the field is critical, then the harvests we get from this field will match some entries in our dictionary.
        if FieldIsCritical:
            Grapes = FieldMap[FieldHarvest].HarvestField(True)

        # Unage our grapes
        for Key, Value in WineGrapeMap.items():
            for item in Value:
                pass
                # item.SetGrade(item.GetGrade() - 1)

    print("x")



def NeedIsFulfilled(Order, Crush, Cellar, UsedGrapes=defaultdict(list)):

    # Check if the wine order can be filled based on the crush pad given
    CrushMap = Crush.GetCrushMap()
    NumNeeded = Order.GetNumRedWhiteGrapes()


    if Cellar is not None: # Put code to check the cellar here.
        pass



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

            UsedGrapes[Bottle].append(Grape(Bottle.GetType(), min(TestFill)))

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
        UsedGrapes[Bottle].append(Grape(GrapeType.RED, CurrentMinRed))



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

    # First, generate all possible solutions for the bottles.
    BlushSolutions = []
    for Bottle in BlushWines:
        BlushSolutions.append([Bottle, GenerateBlushSolutions(Bottle, CrushMap)])

    SolveBlushWines(BlushSolutions)

    for Item in BlushSolutions:

        if not Item[1]:
            return False
        else:
            NumFulfilled += 1
            UsedGrapes[Bottle].append(Grape(GrapeType.RED, Item[1][0][GrapeType.RED]))
            UsedGrapes[Bottle].append(Grape(GrapeType.WHITE, Item[1][0][GrapeType.WHITE]))

    return NumFulfilled == len(Order.GetWines())

def GenerateBlushSolutions(WineBottle, CrushMap):

    AllSolutions = []

    for RedGrade in CrushMap[GrapeType.RED]:
        for WhiteGrade in CrushMap[GrapeType.WHITE]:

            if RedGrade + WhiteGrade >= WineBottle.GetGrade():
                AllSolutions.append(
                    {
                        GrapeType.RED: RedGrade,
                        GrapeType.WHITE: WhiteGrade
                    }
                )

    return AllSolutions

def SolveBlushWines(BlushSolutions):

    # Sort the solutions by the grade.
    # BlushKeys = sorted(BlushSolutions)
    BlushKeys = sorted([x[0] for x in BlushSolutions])
    FinishedBlush = []

    for i, Bottle in enumerate(BlushKeys):

        CurrentItem = BlushSolutions[i]
        CurrentSol = CurrentItem[1]

        # If we have no solution set, we're done.
        if not CurrentSol:
            return

        CopySol = copy.deepcopy(CurrentSol)
        Choice = random.choice(CurrentSol)

        for j, SecItem in enumerate(BlushSolutions[i + 1:]):

            SecSol = SecItem[1]

            # Remove all elements in CurrentSol that are in SecSol.
            if i == j:
                continue

            for Item in SecSol:

                if Item in CopySol:
                    CopySol.remove(Item)

        # If we have unique solutions left, use one of those? No. We can't do that.
        # We have to make sure that selecting this one still leaves us with options.
        # If we can't find one, then we have to hope later on that we have no duplicate solution sets.
        Found = False
        if CopySol:

            for Attempt in CopySol:

                Test = [x for x in CopySol if
                        x[GrapeType.RED] != Attempt[GrapeType.RED] and x[GrapeType.WHITE] != Attempt[
                            GrapeType.WHITE]]
                if Test:
                    Found = True
                    Choice = Attempt
                    break

        # If we can't find one that is unique, then pick one at random and hope for the best.
        if not CopySol:
            Choice = random.choice(CurrentSol)
        elif not Found:
            Choice = random.choice(CopySol)

        # Correct all other bottles.
        for j, SecItem in enumerate(BlushSolutions):

            SecSol = SecItem[1]

            # Set the current bottle's choice
            if i == j:
                BlushSolutions[j][1] = copy.deepcopy([Choice])
                continue

            # Otherwise, eliminate all other solutions that share anything with the choice
            # Only bother with the ones greater than myself. We've already solved the smaller ones.
            if j > i:
                BlushSolutions[j][1] = [x for x in SecSol if
                                        x[GrapeType.RED] != Choice[GrapeType.RED] and x[GrapeType.WHITE] != Choice[
                                            GrapeType.WHITE]]

def DetermineBestPath(Order, CPad, FieldMap, FullPath, CurrentBranch=0, Years=0, CurrentPath=list(), Initial=True):
    """
    Do a depth first search to exhaustively list all possible field harvestations until we can fulfill our order.
    """

    # Break condition
    # This is used to avoid stack overflows.
    if Years >= 10:
        return

    # Special case if initial entry
    if Initial:
        DetermineBestPath(Order, copy.deepcopy(CPad), FieldMap, FullPath, FieldType.MEDIUM, Years + 1,
                          copy.deepcopy(CurrentPath), False)
        DetermineBestPath(Order, copy.deepcopy(CPad), FieldMap, FullPath, FieldType.LARGE, Years + 1,
                          copy.deepcopy(CurrentPath), False)
        return

    # Harvest field and add to crush pad
    Grapes = FieldMap[CurrentBranch].HarvestField(True)
    CPad.AddGrapes(Grapes)
    CurrentPath.append(CurrentBranch)

    # Base condition:
    # Check if need is fulfilled based on crush pad
    if NeedIsFulfilled(Order, CPad, None):
        if CurrentPath not in FullPath:  # Only append if not in paths we already know.
            FullPath.append(CurrentPath)
        return

    # It is confusing, but we must check if the need is met BEFORE we age the wines. This provides a more accurate picture
    CPad.AgeCrushPad()

    # Recurse!
    DetermineBestPath(Order, copy.deepcopy(CPad), FieldMap, FullPath, FieldType.MEDIUM, Years + 1,
                      copy.deepcopy(CurrentPath), False)
    DetermineBestPath(Order, copy.deepcopy(CPad), FieldMap, FullPath, FieldType.LARGE, Years + 1,
                      copy.deepcopy(CurrentPath), False)

def RemoveSuboptimalPaths(HarvestPaths):

    # Find lengths of all items in harvest paths
    Lengths = [len(x) for x in HarvestPaths]
    MinPath = min(Lengths)
    return [x for x in HarvestPaths if len(x) == MinPath]

def DetermineCriticalHarvests(HarvestPaths, Order, FieldMap):

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
            CriticalHarvestsInYear.append(not NeedIsFulfilled(Order, CPad, None))

        Test = list(zip(copy.deepcopy(Path), CriticalHarvestsInYear))
        CriticalHarvests.append(Test)

    return CriticalHarvests

def DetermineNeededHarvests(HarvestPaths, Order, FieldMap, InitCrush = CrushPad()):

    NeededHarvests = []

    for Path in HarvestPaths:

        NeededHarvestsInPath = []
        OrderFilled = False

        TestPath = copy.deepcopy(Path)

        for i in range(1, len(Path)):

            NumSetToZero = len(Path) - i
            TestPath[i:] = [-1] * NumSetToZero

            # Imaginary crush pad
            CPad = copy.deepcopy(InitCrush)

            # Go through our entire path, skipping the -1 fields
            for Year in TestPath:

                if Year == -1:
                    CPad.AgeCrushPad()
                    continue

                # Harvest field, add grapes to crush pad, then age.
                Grapes = FieldMap[Year].HarvestField(True)
                CPad.AddGrapes(Grapes)
                CPad.AgeCrushPad()

            # If the need is fulfilled, the needed harvests are those that were harvested.
            if NeedIsFulfilled(Order, CPad, None):
                NeededHarvestsInPath = [x > -1 for x in TestPath]
                break

        # This clause executes unless we broke out of the for loop.
        # If we got here, it means we need all of the harvests in the path.
        else:
            NeededHarvestsInPath = [True for x in TestPath]

        # Zip up the path with the harvests needed and append it to the needed harvests list.
        Test = list(zip(copy.deepcopy(Path), NeededHarvestsInPath))
        NeededHarvests.append(Test)

    return NeededHarvests

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
    # The only other possibility is to favor large fields over smaller ones, but we'll leave it like this for now
    # Get a random one since it doesn't really matter at this point.
    Index = random.randint(1, len(FinalCandidates))

    return FinalCandidates[Index - 1]

def EstimateYears(Order, CPad, Cellar, FieldMap):

    NumNeeded = Order.GetNumRedWhiteGrapes()
    print(
        "Number of red grapes needed: {0:d}\nNumber of white grapes needed: {1:d}".format(NumNeeded[GrapeType.RED],
                                                                                          NumNeeded[
                                                                                              GrapeType.WHITE]))

    HarvestPaths = []
    DetermineBestPath(Order, CPad, FieldMap, HarvestPaths)
    HarvestPaths = RemoveSuboptimalPaths(HarvestPaths)
    CriticalHarvests = DetermineNeededHarvests(HarvestPaths, Order, FieldMap)
    CurrentPath = ChoosePath(CriticalHarvests)

    return CurrentPath

def GetPathForObjective(Order, CPad, Cellar, FieldMap):

    HarvestPaths = []

    CopyCPad = copy.deepcopy(CPad)
    CopyCellar = copy.deepcopy(Cellar)
    CopyField = copy.deepcopy(FieldMap)



    DetermineBestPath(Order, CopyCPad, CopyField, HarvestPaths)

    if not HarvestPaths:
        return []

    HarvestPaths = RemoveSuboptimalPaths(HarvestPaths)
    CriticalHarvests = DetermineNeededHarvests(HarvestPaths, Order, CopyField, CPad)
    CurrentPath = ChoosePath(CriticalHarvests)

    return CurrentPath

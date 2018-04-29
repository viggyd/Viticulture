from viticulture import WineType, GrapeType
from collections import defaultdict

class WineOrder:

    def __init__(self, Wines, VP=0, Residual=0):

        self.Wines = Wines
        self.WineMap = self.GenerateWineMap(self.Wines)
        self.VP = VP
        self.Residual = Residual


    def GetWines(self):
        """ Return list of wines in order"""
        return self.Wines

    def GetWineMap(self):
        return self.WineMap

    def GetVP(self):
        return self.VP

    def GetResidual(self):
        return self.Residual

    def GenerateWineMap(self, Wines):

        WineMap = defaultdict(list)
        for Wine in Wines:

            WineMap[Wine.Type].append(Wine.Grade)

        return WineMap

    def GetNumRedWhiteGrapes(Order):

        NumFillNeeds = {
            GrapeType.RED: 0,
            GrapeType.WHITE: 0
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

    def __repr__(self):
        return self.GetWines().__repr__()


    # Determine if the given set of wines can fulfill this wine order
    # Return true if the wines can fulfill it, false otherwise
    def CanFulfillOrder(self, Wines):

        FillMap = self.GenerateWineMap(Wines)

        # Iterate over the dictionary we are given.
        for OrderType, OrderGrades in self.WineMap.items():

            # If any of the types of the wine order do not match
            # What we are given, return false. We cannot fill the order.
            if not OrderType in FillMap:
                return False

            # We found a match!
            # Get the grades matching the type we want to fill
            AttemptGrades = FillMap[OrderType]

            # First check if we have enough in the things we are given
            # We cannot fulfill an order if we do not have enough of the type
            if len(AttemptGrades) < len(OrderGrades):
                return False

            # Finally, check quality
            # Here's the algorithm we're going to use...
            # 1. Sort from min -> max for both grade arrays
            # 2. Zip both arrays together (order, attempt)
            # 3. Iterate over zipped array
            # 4. If any lhs < rhs, return false

            # 1. Sort from min -> max for both grade arrays
            OrderGrades.sort()
            AttemptGrades.sort()

            # 2. Zip both arrays together (order, attempt)
            ZippedGrades = zip(OrderGrades, AttemptGrades)

            # 3. Iterate over zipped array
            for Order, Attempt in ZippedGrades:

                # 4. If any lhs > rhs, return false
                if Order > Attempt:
                    return False

        # If we've gotten here, then we must be okay!
        return True



    def PrintDictionary(self):

        return \
            {
                "Wines" : self.WineMap,
                "VP" : self.VP,
                "Residual" : self.Residual
            }
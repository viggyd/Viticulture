from ViticultureConstants import *
from Grape import Grape
import collections

class CrushPad:

    def __init__(self):

        self.RedCrush = [False for x in range(9)]
        self.WhiteCrush = self.RedCrush

        self.Crush = [[False for x in range(9)] for y in range(2)]



    def AddGrapes(self, GrapeArray):

        for Item in GrapeArray:
            self.AddGrape(Item.GetType(), Item.GetGrade())

    def AddGrape(self, Type, Grade):

        # Try to fill the maximum slot possible.
        # Start at the given grade, iterate down to 1.
        for i in range(Grade - 1, 0, -1):

            # If the slot we are trying to add to is not occupied, set to true and return
            if not self.Crush[Type][i]:
                self.Crush[Type][i] = True
                return i


    def AgeCrushPad(self):
        """Age all grapes in crush pad by 1

        """


        for i in range(2): # Iterate over both types of crush pads
            for j in range(8, -1, -1): # Go through each slot in reverse order

                # If the slot if not currently full, move the previous grade up by one.
                # We must check if it is full to ensure that they stop at the max grade.
                if not self.Crush[i][j] and j > 0:
                    self.Crush[i][j] = self.Crush[i][j - 1]
                    self.Crush[i][j - 1] = False


    def GetGrapes(self):

        GrapeArray = []
        for i in range(len(self.Crush)):
            for j in range(len(self.Crush[i])):

                if self.Crush[i][j]:
                    GrapeArray.append(Grape(i, j + 1))

        return GrapeArray



    def RemoveGrapes(self, GrapeArray):

        AllFound = True
        for Item in GrapeArray:

            if self.Crush[Item.GetType()][Item.GetGrade()-1]:
                self.Crush[Item.GetType()][Item.GetGrade()-1] = False
            else:
                AllFound = False

        return AllFound


    def RemoveLargestGrape(self, Type):

        GrapeArray = self.Crush[Type]

        for i in range(8, -1, -1):

            if GrapeArray[i]:
                GrapeArray[i] = False
                return Grape(Type, i + 1)

        return None



    def GrapeMapFromGrapes(self, Grapes):

        GrapeMap = collections.defaultdict(list)

        for Grp in Grapes:
            GrapeMap[Grp.GetType()].append(Grp.GetGrade())

        return GrapeMap

    def GetCrushMap(self):

        return self.GrapeMapFromGrapes(self.GetGrapes())



    def __repr__(self):

        CrushString = ""
        RemoveSome = False

        for i in range(2):

            if i == 0:
                CrushString += "Red: "
            else:
                CrushString += "White: "

            for j in range(9): # Iterate over both types of crush pads

                if self.Crush[i][j]:
                    CrushString = CrushString + str(j + 1) + ", "
                    RemoveSome = True

            if RemoveSome:
                CrushString = CrushString[:-2]
                RemoveSome = False

            CrushString += ". "

        return CrushString
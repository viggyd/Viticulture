from ViticultureConstants import *
from Wine import Wine

class WineCellar:
    """A player's wine cellar. Stores and ages wines.

    Attributes:
        cellar (list(list)): A 2-D list of the wine types along with the wines currently in the cellar.
        size (CellarType): Current size of the wine cellar (small, medium, large)

    """

    def __init__(self):
        """Example of docstring on the __init__ method.

            The __init__ method may be documented in either the class level
            docstring, or as a docstring on the __init__ method itself.
    
            Either form is acceptable, but the two should not be mixed. Choose one
            convention to document the __init__ method and be consistent with it.
    
            Note:
                Do not include the `self` parameter in the ``Args`` section.
    
            Args:

        """

        # Create the 2D array
        self.Cellar = [[False for x in range(9)] for y in range(4)]
        self.Size = CellarType.SMALL
        self.CurrMaxGrade = self.Size * 3 + 3

    def GetWines(self):

        AllWines = []
        for i, WType in enumerate(self.Cellar):
            for j, WGrade in enumerate(self.Cellar[i]):

                if WGrade:
                    AllWines.append(Wine(i, j))

        return AllWines

    # Make wine based on a specific set of given grapes.
    def MakeWine(self, DesiredType, Grapes):
        """Make wine based on list of grapes given

        Keyword arguments:
        DesiredType: The desired type of wine to make
        Grapes: Array of 1, 2, or 3 grapes used to make wine
        """

        Grapes = sorted(Grapes)

        if DesiredType == WineType.BLUSH:

            # Interlocks
            # If any of these conditions are true, exit.
            if len(Grapes) != 2 \
                or (Grapes[0].Type != GrapeType.RED or Grapes[1].Type != GrapeType.WHITE) \
                or self.Size < CellarType.MEDIUM \
                or Grapes[0].Grade + Grapes[1].Grade < 4:
                return False

            BlushRow = self.Cellar[WineType.BLUSH]
            TempGrade = Grapes[0].Grade + Grapes[1].Grade
            TempGrade = min(TempGrade-1, self.CurrMaxGrade-1)


            for temp in range(TempGrade, 2, -1):

                if not BlushRow[temp]:
                    self.Cellar[WineType.BLUSH][temp] = True
                    return True


        elif DesiredType == WineType.SPARKLING:

            if len(Grapes) != 3 \
                or (Grapes[0].Type != GrapeType.RED or Grapes[1].Type != GrapeType.RED or Grapes[2].Type != GrapeType.WHITE) \
                or self.Size < CellarType.LARGE \
                or Grapes[0].Grade + Grapes[1].Grade + Grapes[2].Grade < 7:
                return False

            BlushRow = self.Cellar[WineType.SPARKLING]
            TempGrade = Grapes[0].Grade + Grapes[1].Grade + Grapes[2].Grade
            TempGrade = min(TempGrade-1, self.CurrMaxGrade-1)

            for temp in range(TempGrade, 5, -1):

                if not BlushRow[temp]:
                    self.Cellar[WineType.SPARKLING][temp] = True
                    return True



        else:

            Grade = min(Grapes[0].Grade-1, self.CurrMaxGrade-1)

            for temp in range(Grade, -1, -1):

                if not self.Cellar[DesiredType][temp]:
                    self.Cellar[DesiredType][temp] = True
                    return True

        return False


    def UpgradeCellar(self):

        if self.Size == CellarType.SMALL:
            self.Size = CellarType.MEDIUM

        elif self.Size == CellarType.MEDIUM:
            self.Size = CellarType.LARGE

        self.CurrMaxGrade = self.Size * 3 + 3

    def AgeCellar(self):
        """Age all grapes in crush pad by 1

        """

        for i in range(4):  # Iterate over both types of crush pads
            for j in range(8, -1, -1):  # Go through each slot in reverse order

                # If the slot if not currently full, move the previous grade up by one.
                # We must check if it is full to ensure that they stop at the max grade.
                if not self.Cellar[i][j] and j > 0:
                    self.Cellar[i][j] = self.Cellar[i][j - 1]
                    self.Cellar[i][j - 1] = False
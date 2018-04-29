from viticulture import Grape, GrapeType

class Field:


    def __init__(self, MaxGrade):

        self.RedGrade = 0
        self.WhiteGrade = 0
        self.MaxGrade = MaxGrade
        self.Harvested = False

    def GetRedGrade(self):
        return self.RedGrade

    def GetWhiteGrade(self):
        return self.WhiteGrade

    def GetTotalGrade(self):
        return (self.RedGrade, self.WhiteGrade)


    def SetField(self, RedGrade, WhiteGrade):
        # Set field and destroy all other values.

        if RedGrade + WhiteGrade > self.MaxGrade:
            return False

        self.RedGrade = RedGrade
        self.WhiteGrade = WhiteGrade

        return True


    def PlantVine(self, Type, Grade):

        if self.RedGrade + self.WhiteGrade + Grade > self.MaxGrade:
            return False

        if Type == GrapeType.RED:
            self.RedGrade += Grade
        else:
            self.WhiteGrade += Grade

        return True

    def UprootVine(self, Type, Grade):

        if Type == GrapeType.RED:
            self.RedGrade -= Grade
        else:
            self.WhiteGrade -= Grade

    def HarvestField(self, Estimate=False):

        Grapes = []
        if self.RedGrade:
            Grapes.append(Grape(GrapeType.RED, self.RedGrade))

        if self.WhiteGrade:
            Grapes.append(Grape(GrapeType.WHITE, self.WhiteGrade))

        self.Harvested = not Estimate
        return Grapes

    def GetLayout(self):

        return \
            {
                "Capacity" : self.RedGrade + self.WhiteGrade,
                "Layout" : self.RedGrade - self.WhiteGrade
            }


    def __repr__(self):

        return "Red Grade: {self.RedGrade}. White Grade: {self.WhiteGrade}".format(self=self)
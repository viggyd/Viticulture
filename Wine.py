# Defines the wine card
from ViticultureConstants import *

class Wine:

    def __init__(self, Type, Grade=1):

        self.Grade = Grade
        self.Type = Type

    def Age(self, Cellar):

        # The maximum grade is based on the current cellar
        CurrentMaxGrade = Cellar * 3 + 3
        self.Grade = min(CurrentMaxGrade, self.Grade + 1)

    def GetGrade(self):
        return self.Grade

    def GetType(self):
        return self.Type

    def __repr__(self):

        if self.Type == WineType.RED:
            return "Red {self.Grade}".format(self=self)
        elif self.Type == WineType.WHITE:
            return "White {self.Grade}".format(self=self)
        elif self.Type == WineType.BLUSH:
            return "Blush {self.Grade}".format(self=self)
        elif self.Type == WineType.SPARKLING:
            return "Sparkling {self.Grade}".format(self=self)
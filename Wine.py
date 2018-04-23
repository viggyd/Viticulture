# Defines the wine card
from ViticultureConstants import *

class Wine:

    def __init__(self, Type, Grade=1):

        self.Grade = Grade
        self.Type = Type


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


    def __hash__(self):
        return hash((self.Type, self.Grade))


    def __eq__(self, other):

        return (self.Type, self.Grade) == (other.Type, other.Grade)

    def __lt__(self, other):

        if self.Type < other.Type:
            return True
        elif self.Type > other.Type:
            return False
        else:
            return self.Grade < other.Grade

    def __gt__(self, other):

        if self.Type > other.Type:
            return True
        elif self.Type < other.Type:
            return False
        else:
            return self.Grade > other.Grade
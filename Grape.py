from ViticultureConstants import *

class Grape:

    def __init__(self, Type, Grade):

        self.Type = Type
        self.Grade = Grade

    def GetType(self):
        return self.Type

    def GetTypeName(self):
        return self.Type.Name

    def GetGrade(self):
        return self.Grade

    def MeetsGrade(self, Type, Grade):

        if self.Type == Type and self.Grade >= Grade:
            return True

        return False

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

    def __eq__(self, other):

        return self.Type == other.Type \
            and self.Grade == other.Grade

    def __repr__(self):

        if self.Type == GrapeType.RED:
            return "Red {self.Grade}".format(self=self)
        elif self.Type == GrapeType.WHITE:
            return "White {self.Grade}".format(self=self)

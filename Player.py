from ViticultureConstants import *
from Cellar import WineCellar
from CrushPad import CrushPad
from WineOrderDeck import WineOrderDeck
from WineOrder import WineOrder
from Grape import Grape
from Field import Field
from Wine import Wine
import copy
import pprint
import random
import csv
import Solver

# Hello!
# You will note that there is a lot of list comprehension going on here.
# I am as of yet unsure of how this will affect the final simulations.
# But it's always better to optimize later as needed.


class Player:

    def __init__(self):

        # Set up the fields
        self.SField = Field(5)
        self.MField = Field(6)
        self.LField = Field(7)

        # Set up the crush pad and wine cellar
        self.CrushPad = CrushPad()
        self.Cellar = WineCellar()

        self.CurrentVP = 0

        self.FieldMap = {
            FieldType.SMALL  : self.SField,
            FieldType.MEDIUM : self.MField,
            FieldType.LARGE  : self.LField
        }

        self.Objectives = []


    def GetVP(self):
        return self.CurrentVP


    def Age(self):
        self.CrushPad.AgeCrushPad()
        # self.Cellar.AgeCellar()


    def SetField(self, Type, RedGrade=0, WhiteGrade=0):

        self.FieldMap[Type].PlantVine(GrapeType.RED, RedGrade)
        self.FieldMap[Type].PlantVine(GrapeType.WHITE, WhiteGrade)

    def SetFieldMap(self, FieldMap):

        self.FieldMap = copy.deepcopy(FieldMap)


    def HarvestField(self, Type):

        Grapes = self.FieldMap[Type].HarvestField()
        self.CrushPad.AddGrapes(Grapes)


    def AddVP(self, Update):
        self.CurrentVP += Update


    def AddObjective(self, Objective):
        self.Objectives.append(Objective)

    def GetCrushPad(self):
        return self.CrushPad

    def RemoveGrapesFromCrushPad(self, Grapes):
        self.CrushPad.RemoveGrapes(Grapes)

    def GetFieldMap(self):
        return self.FieldMap

    def GetCellar(self):
        return self.Cellar


    def GetAPathForCurrentObjective(self):

        if not self.Objectives:
            return []

        return Solver.GetPathForObjective(self.Objectives[0], self.CrushPad, self.Cellar, self.FieldMap)







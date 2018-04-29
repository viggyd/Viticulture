from viticulture import Wine, WineType, WineOrder
import csv
import random
import copy



class WineOrderDeck:

    def __init__(self, FilePath):

        self.Deck = self.ConstructWineDeck(FilePath)
        self.MasterCopy = copy.deepcopy(self.Deck)


    def DrawCard(self):

        Card = random.choice(self.Deck)
        self.Deck.remove(Card)

        if len(self.Deck) == 0:
            self.ReshuffleDeck()

        return Card

    def ReshuffleDeck(self):
        self.Deck = copy.deepcopy(self.MasterCopy)


    def ConstructWineDeck(self, FilePath):
        WineDeck = []

        with open(FilePath, 'r') as f:

            WineReader = csv.DictReader(f, delimiter=',')

            for row in WineReader:

                Wines = self.WineListFromTextFile(row['wines'])
                WineDeck.append(WineOrder(Wines, int(row['vp']), int(row['residual'])))

        return WineDeck

    @staticmethod
    def WineListFromTextFile(WineListStr):

        # Remove the []
        TempStr = WineListStr[1:-1]

        WineArray = TempStr.split()

        Wines = []
        for Item in WineArray:

            Grade = int(Item[0])
            Type = Item[1]
            WType = WineType.RED

            if Type.lower() == "r":
                WType = WineType.RED
            elif Type.lower() == "w":
                WType = WineType.WHITE
            elif Type.lower() == "b":
                WType = WineType.BLUSH
            elif Type.lower() == "s":
                WType = WineType.SPARKLING

            Wines.append(Wine(WType, Grade))

        return Wines
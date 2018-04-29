import unittest

from simulation import Solver
from viticulture import *


class TestWineOrderFulfill(unittest.TestCase):

    def setUp(self):
        self.OrderComplex = WineOrder([Wine(WineType.RED, 2), Wine(WineType.WHITE, 2), Wine(WineType.BLUSH, 5)])
        self.OrderDups = WineOrder([Wine(WineType.RED, 4), Wine(WineType.RED, 3), Wine(WineType.RED, 2)])


    def test_duplicates(self):

        self.assertTrue(
            self.OrderDups.CanFulfillOrder([Wine(WineType.RED, 4), Wine(WineType.RED, 3), Wine(WineType.RED, 2)]))
        self.assertTrue(
            self.OrderDups.CanFulfillOrder([Wine(WineType.RED, 5), Wine(WineType.RED, 3), Wine(WineType.RED, 2)]))
        self.assertTrue(
            self.OrderDups.CanFulfillOrder([Wine(WineType.RED, 5), Wine(WineType.RED, 4), Wine(WineType.RED, 2)]))
        self.assertTrue(
            self.OrderDups.CanFulfillOrder([Wine(WineType.RED, 5), Wine(WineType.RED, 4), Wine(WineType.RED, 3)]))


        self.assertFalse(
            self.OrderDups.CanFulfillOrder([Wine(WineType.RED, 4), Wine(WineType.RED, 3)]))
        self.assertFalse(
            self.OrderDups.CanFulfillOrder([Wine(WineType.WHITE, 4), Wine(WineType.BLUSH, 3), Wine(WineType.SPARKLING, 2)]))
        self.assertFalse(
            self.OrderDups.CanFulfillOrder([Wine(WineType.RED, 4), Wine(WineType.RED, 3), Wine(WineType.RED, 1)]))


    def test_complex(self):
        self.assertTrue(
            self.OrderComplex.CanFulfillOrder([Wine(WineType.RED, 2), Wine(WineType.WHITE, 2), Wine(WineType.BLUSH, 5)]))
        self.assertTrue(
            self.OrderComplex.CanFulfillOrder(
                [Wine(WineType.RED, 2), Wine(WineType.WHITE, 2), Wine(WineType.BLUSH, 5)]))
        self.assertTrue(
            self.OrderComplex.CanFulfillOrder(
                [Wine(WineType.RED, 2), Wine(WineType.WHITE, 2), Wine(WineType.BLUSH, 5)]))
        self.assertTrue(
            self.OrderComplex.CanFulfillOrder(
                [Wine(WineType.RED, 2), Wine(WineType.WHITE, 2), Wine(WineType.BLUSH, 5)]))

        self.assertFalse(
            self.OrderComplex.CanFulfillOrder(
                [Wine(WineType.RED, 1), Wine(WineType.WHITE, 2), Wine(WineType.BLUSH, 5)]))
        self.assertFalse(
            self.OrderComplex.CanFulfillOrder(
                [Wine(WineType.RED, 2), Wine(WineType.WHITE, 1), Wine(WineType.BLUSH, 5)]))
        self.assertFalse(
            self.OrderComplex.CanFulfillOrder(
                [Wine(WineType.RED, 2), Wine(WineType.WHITE, 2), Wine(WineType.BLUSH, 4)]))
        self.assertFalse(
            self.OrderComplex.CanFulfillOrder(
                [Wine(WineType.RED, 1), Wine(WineType.WHITE, 1), Wine(WineType.BLUSH, 4)]))
        self.assertFalse(
            self.OrderComplex.CanFulfillOrder(
                [Wine(WineType.RED, 1), Wine(WineType.RED, 2), Wine(WineType.RED, 3), Wine(WineType.WHITE, 1), Wine(WineType.BLUSH, 5)]))



class TestGrapeSorting(unittest.TestCase):

    def test_grapesorting(self):

        Grapes = [Grape(GrapeType.RED, 5),
                  Grape(GrapeType.RED, 3),
                  Grape(GrapeType.RED, 2),
                  Grape(GrapeType.WHITE, 1),
                  Grape(GrapeType.WHITE, 2),
                  Grape(GrapeType.WHITE, 3)
                  ]

        SortedGrapes = [
            Grape(GrapeType.RED, 2),
            Grape(GrapeType.RED, 3),
            Grape(GrapeType.RED, 5),
            Grape(GrapeType.WHITE, 1),
            Grape(GrapeType.WHITE, 2),
            Grape(GrapeType.WHITE, 3)
                  ]

        Grapes = sorted(Grapes)

        self.assertEqual(Grapes, SortedGrapes)


class TestCellarSuite(unittest.TestCase):

    def test_smallcellar(self):

        TCell = WineCellar()

        TCell.MakeWine(WineType.RED, [Grape(GrapeType.RED, 6)])
        self.assertTrue(TCell.Cellar[WineType.RED][2])

        TCell.MakeWine(WineType.RED, [Grape(GrapeType.RED, 5)])
        self.assertTrue(TCell.Cellar[WineType.RED][1])

        TCell.MakeWine(WineType.BLUSH, [Grape(GrapeType.RED, 5), Grape(GrapeType.WHITE, 3)])
        self.assertFalse(all(TCell.Cellar[WineType.BLUSH]))

    def test_medcellar(self):

        TCell = WineCellar()
        TCell.UpgradeCellar()


        TCell.MakeWine(WineType.BLUSH, [Grape(GrapeType.RED, 5), Grape(GrapeType.WHITE, 3)])
        self.assertTrue(TCell.Cellar[WineType.BLUSH][5])

        TCell.MakeWine(WineType.BLUSH, [Grape(GrapeType.RED, 1), Grape(GrapeType.WHITE, 1)])
        self.assertFalse(TCell.Cellar[WineType.BLUSH][1])

        TCell.MakeWine(WineType.BLUSH, [Grape(GrapeType.RED, 3), Grape(GrapeType.WHITE, 1)])
        self.assertTrue(TCell.Cellar[WineType.BLUSH][3])

class TestCrushPadSuite(unittest.TestCase):

    def test_crush(self):

        CPad = CrushPad()

        CPad.AddGrape(GrapeType.RED, 2)
        CPad.AddGrape(GrapeType.RED, 3)
        CPad.AddGrape(GrapeType.RED, 9)

        CPad.AgeCrushPad()

        BlankSlate = [False for x in range(9)]

        TestPad = BlankSlate
        TestPad[2] = True
        TestPad[3] = True
        TestPad[8] = True

        self.assertEqual(TestPad, CPad.Crush[0])


class TestBlushGenerateSolutions(unittest.TestCase):

    def test_generate_sols(self):

        Crush = CrushPad()

        Crush.AddGrape(GrapeType.RED, 2)
        Crush.AddGrape(GrapeType.RED, 3)
        Crush.AddGrape(GrapeType.WHITE, 3)
        Crush.AddGrape(GrapeType.WHITE, 4)

        CrushMap = Crush.GetCrushMap()
        WineBottle = Wine(WineType.BLUSH, 5)

        Sols = Solver.GenerateBlushSolutions(WineBottle, CrushMap)

        ExpSols = [
            {GrapeType.RED: 2, GrapeType.WHITE: 3},
            {GrapeType.RED: 2, GrapeType.WHITE: 4},
            {GrapeType.RED: 3, GrapeType.WHITE: 3},
            {GrapeType.RED: 3, GrapeType.WHITE: 4}
        ]

        self.assertEqual(Sols, ExpSols)

        WineBottle = Wine(WineType.BLUSH, 6)

        Sols = Solver.GenerateBlushSolutions(WineBottle, CrushMap)

        ExpSols = [
            {GrapeType.RED: 2, GrapeType.WHITE: 4},
            {GrapeType.RED: 3, GrapeType.WHITE: 3},
            {GrapeType.RED: 3, GrapeType.WHITE: 4}
        ]

        self.assertEqual(Sols, ExpSols)


    def test_multiple_in_order(self):

        Crush = CrushPad()

        Crush.AddGrape(GrapeType.RED, 2)
        Crush.AddGrape(GrapeType.RED, 3)
        Crush.AddGrape(GrapeType.WHITE, 3)
        Crush.AddGrape(GrapeType.WHITE, 4)

        CrushMap = Crush.GetCrushMap()
        Order = WineOrder([Wine(WineType.BLUSH, 5), Wine(WineType.BLUSH, 6)], 5, 2)
        BlushWines = [Wine(WineType.BLUSH, 5), Wine(WineType.BLUSH, 6)]



        BlushSolutions = []
        for Bottle in BlushWines:
            BlushSolutions.append([Bottle, Solver.GenerateBlushSolutions(Bottle, CrushMap)])

            Solver.SolveBlushWines(BlushSolutions)
        print("done")



if __name__ == '__main__':


    suite = unittest.TestSuite()

    suite.addTests(unittest.TestLoader().loadTestsFromTestCase((TestBlushGenerateSolutions)))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestWineOrderFulfill))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase((TestGrapeSorting)))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase((TestCellarSuite)))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase((TestCrushPadSuite)))


    unittest.TextTestRunner(verbosity=3).run(suite)




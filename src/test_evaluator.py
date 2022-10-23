import unittest

from src.evaluator import Evaluator, DEFAULT_EMPTY_ANS


class EvaluatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.e = Evaluator(evaluator_name="testing")

    def test_something(self):
        self.assertEqual(self.e.evaluate(gold="12 ducks", stud="12 duckies")["is_correct"], True)
        self.assertEqual(self.e.evaluate(gold="a. 37th, b. 42nd, c. 39, d. 40", stud="a. 37th floor, b. 42nd floor, c. 39th floor, d. 40th floor")["stud"], 37423940)
        self.assertEqual(self.e.evaluate(gold="25 ducks", stud="answer is 25 ducklings")["stud"], 25)
        self.assertEqual(self.e.evaluate(gold="4 c1", stud="4 c.1")["is_correct"], True)
        self.assertEqual(self.e.evaluate(gold="45", stud="abcd efgh. ij")["stud"], DEFAULT_EMPTY_ANS)
        self.assertEqual(self.e.evaluate(gold="5 {blue}. ", stud="5")["gold"], [51])
        self.assertEqual(self.e.evaluate(gold="5 {blue}. __OR__ 6 {brown}",stud="5 blue")["gold"], [51, 62])



if __name__ == '__main__':
    unittest.main()

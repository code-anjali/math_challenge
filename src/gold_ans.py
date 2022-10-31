from dataclasses import dataclass
from typing import List

from src.math_challenge import MathChallenge


class GoldAns:

    def __init__(self, math_challenge: MathChallenge):
        self.math_challenge: MathChallenge = math_challenge
        self.list_of_gold_answers: List[str] = ["-TBD-"]*18
        self.list_of_display_gold_answers: List[str] = ["-TBD-"]*18

    def set_gold_answers(self, gold_answers):
        self.list_of_gold_answers = gold_answers

    def set_display_answers(self, display_gold_answers):
        self.list_of_display_gold_answers = display_gold_answers
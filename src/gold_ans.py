from dataclasses import dataclass
from typing import List

from src.math_challenge import MathChallenge


@dataclass
class GoldAns:
    math_challenge: MathChallenge
    list_of_gold_answers: List[str]
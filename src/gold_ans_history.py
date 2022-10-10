from dataclasses import dataclass
from typing import Dict

from src.gold_ans import GoldAns
from src.math_challenge import MathChallenge


@dataclass
class GoldAnsHistory:
    dict_of_mc_gold_answers: Dict[MathChallenge,GoldAns]



from dataclasses import dataclass
from typing import List

@dataclass
class MathChallenge:
    mc_name : str
    questions: List[str]

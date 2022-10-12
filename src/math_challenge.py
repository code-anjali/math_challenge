from dataclasses import dataclass
from typing import List

@dataclass
class MathChallenge:
    mc_name : str
    # questions: List[str]

    def __hash__(self):
        return hash(self.mc_name)

    def __eq__(self, other):
        return self.mc_name == other.mc_name

    def __repr__(self):
        return self.mc_name


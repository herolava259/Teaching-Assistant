from dataclasses import dataclass
from enum import IntEnum

class ERating(IntEnum):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5

@dataclass(frozen=True)
class Feedback:
    rating: ERating
    content: str

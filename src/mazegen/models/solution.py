from typing import List, Tuple
from .direction import Direction

class Solution:

    def __init__(self, path_cells: List[Tuple[int, int]], directions: List[Direction]) -> None:

        self.path_cells = path_cells

        self.directions = directions

    def to_string(self) -> str:
        return "".join([d.name[0] for d in self.directions])
from typing import Tuple


class STNode:
    def __init__(self, max: int, seg: Tuple[int, int]):
        self.max = max
        self.seg = seg
        self.left = None
        self.right = None

    def __repr__(self):
        return f"STNode({self.max})"
    
class ST:
    def __init__(self, arr: 'list[int]'):
        self.root = None

    def _build(self, arr: 'list[int]'):
        if len(arr) == 1:
            self.root = arr[0]
            return
        
        self.root = (0, len(arr))
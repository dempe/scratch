from collections import deque
from typing import Optional

class BSTNode:
  """Binary search tree node"""

  def __init__(self, val: int,
               left: Optional['BSTNode'] = None,
               right: Optional['BSTNode'] = None):
    self.val = val
    self.left = left
    self.right = right


  def __str__(self):
    return f"{self.val}"


class BST:
  """Basic binary search tree"""
  def __init__(self, val: Optional[int] = None):
    self.root = BSTNode(val) if val else None


  def insert_helper(self, node: BSTNode, val: int):
    if val <= node.val:
      if not node.left: node.left = BSTNode(val)
      else:             self.insert_helper(node.left, val)
    else:
      if not node.right: node.right = BSTNode(val)
      else:              self.insert_helper(node.right, val)


  def insert(self, val: int):
    if not self.root: self.root = BSTNode(val)
    else: self.insert_helper(self.root, val)

  def __str__(self) -> str:
    return self.pin()
  

  def pin(self) -> str:
    def inorder(node: Optional[BSTNode]) -> 'list[str]':
      return inorder(node.left) + [str(node)] + inorder(node.right) if node else []
    return " ".join(inorder(self.root))


  def plo(self) -> str:
    """Print nodes in level order (like on LC)"""
    q = deque([self.root])
    strs = []

    while q:
      node = q.popleft()
      if node:
        strs.append(str(node.val))
        q.append(node.left)
        q.append(node.right)
      else: strs.append('null')

    # Remove trailing nulls
    while strs and strs[-1] == 'null': strs.pop()

    return ",".join(strs)


bt = BST()

while True:
  try:
    command = input("Insert value (or 'p'): ").strip()
  
    if command.lower() == 'p': print(bt.plo())
    else: bt.insert(int(command))
  except ValueError:
    print("Invalid input. Please enter an integer or a command.")
  except KeyboardInterrupt:
    print("\nExiting.")
    break

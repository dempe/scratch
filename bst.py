from collections import deque

class BSTNode:
  """Binary search tree node"""

  def __init__(self, val: int, left: 'BTNode' = None, right: 'BTNode' = None):
    self.val = val
    self.left = left
    self.right = right
       

  def __str__(self):
    return f"{self.val}"


class BT:
  """Basic binary search tree"""

  def __init__(self, val: int = None):
    self.root = BTNode(val) if val else None


  def insert_helper(self, node: BTNode, val: int):
    if val <= node.val:
      if not node.left: node.left = BTNode(val)
      else:             self.insert_helper(node.left, val)
    else:
      if not node.right: node.right = BTNode(val)
      else:              self.insert_helper(node.right, val)


  def insert(self, val: int):
    if not self.root: self.root = BTNode(val)
    else: self.insert_helper(self.root, val) 


  def __str__(self) -> str:
    def inorder(node: BTNode) -> [str]:
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


bt = BT()
        
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

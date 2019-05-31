from BSTClass import BST
class AVL(BST):
    def __init__(self, initialNode=None):
        self.leftChild = None
        self.rightChild = None
        self.balance = 0
        if initialNode == None:
            self.nodeValue = None
            self.emptyTree = True

        else:
            self.nodeValue = initialNode
            self.emptyTree = False



    def search(self, value):
        BST.search(value)

    def insert(self, newValue, currentNode):
        """Given a new value, add a node to the tree somewhere to add the new value. This performs the typical AVL insertion algorithm."""
        if self.isEmpty():
            self.emptyTree = False
            self.nodeValue = newValue
            self.leftChild = None
            self.rightChild = None
            return "heightIncrease"

        elif newValue < currentNode.nodeValue:
            if currentNode.hasLeftChild():
                res = self.insert(newValue, currentNode.leftChild)
            else:
                node = AVL(newValue)
                currentNode.leftChild = node
                res = "heightIncrease"

            if res == "heightIncrease":
                currentNode.balance -= 1
                if currentNode.balance == 0:
                    return "heightBalanced"
                elif currentNode.balance == -1:
                    return "heightIncrease"
                else:
                    if currentNode.leftChild.balance == -1:
                        self.singleRrotation(currentNode)
                    else:
                        self.doubleLRrotation(currentNode)
            else:
                return "heightBalanced"

        elif newValue >= currentNode.nodeValue:
            if currentNode.hasRightChild():
                res = self.insert(newValue, currentNode.rightChild)
            else:
                node = AVL(newValue)
                currentNode.setRightChild(node)
                res = "heightIncrease"

            if res == "heightIncrease":
                currentNode.balance += 1

                if currentNode.balance == 0:
                    return "heightBalanced"
                elif currentNode.balance == 1:
                    return "heightIncrease"
                else:
                    if currentNode.rightChild.balance == 1:
                        self.singleLrotation(currentNode)
                    else:
                        self.doubleRLrotation(currentNode)
            else:
                return "heightBalanced"

    def singleLrotation(self, rotation_root):
        print("Single Left Rotation")

        x = AVL()
        y = AVL()
        z = AVL()

        # newLeftTree = rotation_root.rightChild

        x = rotation_root.leftChild
        if rotation_root.rightChild.hasLeftChild():
            y = rotation_root.rightChild.leftChild
        if rotation_root.rightChild.hasRightChild():
            z = rotation_root.rightChild.rightChild

        # swap root and right child values
        newRootVal = rotation_root.rightChild.nodeValue
        rotation_root.rightChild.nodeValue = rotation_root.nodeValue
        rotation_root.nodeValue = newRootVal

        # new left tree

        rotation_root.leftChild = rotation_root.rightChild

        rotation_root.leftChild.leftChild = x
        rotation_root.leftChild.rightChild = y
        rotation_root.rightChild = z

        rotation_root.balance = 0
        rotation_root.leftChild.balance = 0

    def singleRrotation(self, rotation_root):
        print("Single Right Rotation")


        x = AVL()
        y = AVL()
        z = AVL()


        x = rotation_root.rightChild
        if rotation_root.leftChild.hasRightChild():
            y = rotation_root.leftChild.rightChild
        if rotation_root.leftChild.hasLeftChild():
            z = rotation_root.leftChild.leftChild

        # swap root and right child values
        newRootVal = rotation_root.leftChild.nodeValue
        rotation_root.leftChild.nodeValue = rotation_root.nodeValue
        rotation_root.nodeValue = newRootVal

        # new left tree

        rotation_root.rightChild = rotation_root.leftChild

        rotation_root.rightChild.rightChild = x
        rotation_root.rightChild.leftChild = y
        rotation_root.leftChild = z

        rotation_root.balance = 0
        rotation_root.rightChild.balance = 0


    def doubleRLrotation(self, rotation_root):
        print("Double Right Left Rotation")

        self.singleRrotation(rotation_root.rightChild)
        self.singleLrotation(rotation_root)

    def doubleLRrotation(self, rotation_root):
        print("Double Left Right Rotation")
        self.singleLrotation(rotation_root.leftChild)
        self.singleRrotation(rotation_root)





    def printTree(self):
        """Takes in a tree and prints it, printing first left subtree and then right,
        and using indentation to indicate the level in the tree."""
        if self.isEmpty():
            print("Tree is empty")
        else:
            self._printRecurDepth(0)

    def _printRecurDepth(self, depth):
        """prints the tree, using depth to track the levels"""
        indent = " " * depth
        indentPlus = ' ' * (depth + 5)
        if self.isLeaf():
            print(indent + "Leaf: " + str(self.nodeValue), "BF:", self.balance)
        else:
            print(indent + "Node: " + str(self.nodeValue), "BF:", self.balance)
            if self.hasLeftChild():
                print(indentPlus + "LEFT:")
                self.leftChild._printRecurDepth(depth + 5)
            else:
                print(indentPlus + "LEFT:  no left child")

            if self.hasRightChild():
                print(indentPlus + "RIGHT:")
                self.rightChild._printRecurDepth(depth + 5)
            else:
                print(indentPlus + "RIGHT:  no right child")

if __name__ == '__main__':
    tree = AVL(initialNode=40)
    tree.insert(40, tree)
    tree.insert(40, tree)



    print("-------------------------")
    tree.printTree()
    print("-------------------------")



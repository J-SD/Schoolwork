""" ==============================================================
Defines a decision tree class that builds and uses a decision tree.
It has a hole in it: no definition of ID3 or anything fancier.
The overall decision tree is a wrapper of sorts that handles the
whole-tree operations, and lets the basic stuff be handled by
the treeNode class
    ==============================================================
"""

from corpus import *
import math 

class DecisionTree:
    """Represents a decision tree, and various utilities for accessing
    its data. Missing an implementation of ID3."""
    
    
    def __init__(self, dataset):
        """Given a Dataset object, it sets up all the internal information
        so that it is ready to build the tree."""
        self.treeNode = None
        self.dataset = dataset
        self.instances = dataset.getInstances()
        self.attributes = dataset.getAttributes()
        self.attributeMap = dataset.getAttributeMap()
        self.categoryValues = dataset.getCategoryValues()
        self.category = dataset.getCategory()



    def searchTree(self, newInstance):
        """Once the tree is built, this will take a new Instance object
        and will determine the tree's classification of that instance.
        Returns False if no tree exists yet."""
        currTree = self.treeNode
        while currTree != None:
            if currTree.isLeaf():
                return currTree.getNodeValue()
            currFeat = currTree.getNodeValue()
            currTree = currTree.getChild(newInstance.getFeatureValue(currFeat)) 
        return False



    def buildTree(self):
        """Takes in no inputs, and uses ID3 to build the tree."""
        attribs = self.attributes.copy()
        self.doID3(attribs, self.instances, self.modeOfCategory(self.instances))


    def doID3(self, attributes, instances, defaultValue):
        """Recursive function that implements the ID3 algorithm."""
        # TODO: This is for you to implement.
        # if examples is empty then
        if not instances:
            # return a leaf node with defaultValue in it
            print("default value")
            return TreeNode(defaultValue)
        # else if all examples have the same value then
        elif self.areConsistent(instances):
            # return a leaf node with that value
            print("all consistent")
            return TreeNode(instances[0].getCatValue())
        # else if attributes is empty then
        elif not attributes:
            # return a leaf node with majority rules or unknown value
            print("no attributes")
            return TreeNode(self.modeOfCategory(instances))
        else:
            # set best = the best attribute in attributes
            best = attributes[0]
            for i in range(1, len(attributes)-1):
                gain = self.gain(attributes[i], instances)
                best_gain = self.gain(best, instances)
                if gain > best_gain:
                    best = attributes[i]
            # set qNode = a new question node containing best
            qNode = TreeNode(best)
            # set maj = majority value of examples
            maj = self.modeOfCategory(instances)
            # for each value vi that best can take on do
            for val in self.dataset.getAttributeValues(best):
                # set newExamp = the examples from examples with value vi
                newExamp = self.getSamplesWithValue(best, val, instances)
                # set newAttr = attributes minus best
                newAttr = attributes[:]
                del newAttr[newAttr.index(best)]
                # set subtree = ID3(newExamp, newAttr, maj)
                subtree = self.doID3(newAttr, newExamp, maj)
                # add a branch to qNode with label vi and child subtree
                qNode.addChild(val, subtree)
                qNode.printTree()
            # return qNode
            return qNode

    def modeOfCategory(self, examples):
        """Given a list of examples, it counts how many have each of the category values, and reports which
        value is most common."""
        countDict = dict()
        for cv in self.categoryValues:
            countDict[cv] = 0
        for inst in examples:
            instCatVal = inst.getCatValue()
            countDict[instCatVal] += 1
        maxCount = 0
        maxVal = None
        for cv in countDict:
            if countDict[cv] > maxCount:
                maxCount = countDict[cv]
                maxVal = cv
        return maxVal

    def getSamplesWithValue(self, attribute, attrValue, dataset):
        """This function takes a string that is an attribute, a specific value
        for that attribute, and a list of instances and it returns those instances
        that have the given value for that attribute"""
        samples = []
        for sample in dataset:
            if sample.getFeatureValue(attribute) == attrValue:
                samples.append(sample)
        return samples
    


    def areConsistent(self, dataset):
        """This takes in a dataset and returns True if all instances have the
    same value for the category we want to learn"""
        if dataset == []:
            return True
        cat = dataset[0].getCatValue()
        for inst in dataset:
            if not (inst.getCatValue() == cat):
                return False
        return True
    

    # ----------------------------------------------
    def gain(self, attribute, instances):
        """Give this a string which is an attribute and a dataset of instances we are
        asking about (which is a list of dictionaries), this will calculate and return
        the gain associated with choosing this particular attribute for the root of
        the current tree"""
        entropyProbs = self.genEntropyProbs(instances)
        wholeEntropy = self.entropy(entropyProbs)
        remain = self.remainder(attribute, instances)
        return wholeEntropy - remain



    def genEntropyProbs(self, dataset):
        """A helper for gain, this calculates a list of entropy probabilities"""
        entropyProbs = []
        for cat in self.categoryValues:
            catset = self.getSamplesWithValue(self.category, cat, dataset)
            entropyProbs.append(len(catset) / len(dataset))
        return entropyProbs


      
    def entropy(self, probList):
        """Given a list of probabilities, compute the entropy value for them"""
        sum = 0
        for prob in probList:
            if prob != 0:
                sum += -1 * prob * math.log(prob, 2)
        return sum


    def remainder(self, attribute, dataset):
        """A helper for gain... computes the remainder for a given attribute"""
        total = 0
        for attrVal in self.attributeMap[attribute]:
            sampleset = self.getSamplesWithValue(attribute, attrVal, dataset)
            if len(sampleset) > 0:
                term1 = len(sampleset) / len(dataset)
                entropyProbs = self.genEntropyProbs(sampleset)
                total += term1 * self.entropy(entropyProbs)
        return total
    
    
    
# end class decisionTree


class TreeNode:
    """Here a tree has a value, which should be a string and represents
    a feature type -- the question, or the ultimate category answer 
    if the tree is a leaf.  It also contains a dictionary organized by 
    the feature values that are assigned to that feature type.  The
    value associated with each feature value is another decision tree node."""

    def __init__(self, featName, featValues = []):
        """takes in the name of the feature and a list of values, and it initializes
        any answers for this node"""
        self.nodeValue = featName
        self.featureValues = featValues[:]
        self.answers = {} # dictionary built from featValues
        for fv in featValues:
            self.answers[fv] = None

    def getNodeValue(self):
        """Access the node's value"""
        return self.nodeValue


    def getAnswerValues(self):
        """Returns a list of the answer values"""
        return self.featureValues

    def getChild(self, featValue):
        """Returns a specific subtree given the feature value for it"""
        return self.answers[featValue]

    def addChild(self, featValue, newKid):
        """Adds a new subtree for a given feature value"""
        if featValue != self.featureValues:
            self.featureValues.append(featValue)
        self.answers[featValue] = newKid

    def isLeaf(self):
        """A node is a leaf if there are no answers/feature values associated with it"""
        return self.answers == {}

    # ----------------------------------------
    def printTree(self):
        self.doPrintTree(0)
 
    def doPrintTree(self, indentSize):
        indent = ' ' * indentSize
        if self.isLeaf():
            print(indent, 'Answer:', self.getNodeValue())
        else:
            print (indent, "Question:", self.getNodeValue(), list(self.answers.keys()))
            for a in self.answers:
                print (indent, "-----Value:",  a)
                subtree = self.getChild(a)
                subtree.doPrintTree(indentSize + 5)

         
# end class treeNode

    
if __name__ == '__main__':
    newTree = DecisionTree(Corpus("PythonDatasets/dog2.dat"))
    newTree.buildTree()
           

    
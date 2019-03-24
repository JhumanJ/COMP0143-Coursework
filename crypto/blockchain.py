from crypto.transaction import Transaction

"""
Represents a block of the blockchain
"""

class BlockChain(object):

    def __init__(self,blocks,transactionDict,inputDict,outputDict,tagsDict):
        self.blocks = blocks

        # Set dict on blockchain for efficient lookups
        self.transactionDict = transactionDict
        self.inputDict = inputDict
        self.outputDict = outputDict
        self.tagsDict = tagsDict

    def __str__(self):
        return "Whole blockahin containing {} blocks.".format(len(self.blocks))

    """
    Returns a specific transaction given an id
    """
    def getTransactionById(self,id):
        return self.transactionDict[id]

    """
    Returns a specific input given an id
    """

    def getInputById(self, id):
        return self.inputDict[id]

    """
    Returns a specific ouput given an id
    """

    def getOutputById(self, id):
        return self.outputDict[id]

    """
    Returns a specific tag given an id
    """

    def getTagById(self, id):
        return self.tagsDict[id]
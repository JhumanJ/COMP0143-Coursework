from crypto.transaction import Transaction

"""
Represents a block of the blockchain
"""

class Block(object):

    def __init__(self,id,transactions):
        self.id = id
        self.transactions = transactions

    def addTransaction(self,transaction: Transaction):
        self.transactions.append(transaction)

    def __str__(self):
        return "Block id: {} \nTransactions: {}".format(self.id,"".join(str(transaction) for transaction in self.transactions))
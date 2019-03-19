"""
Represents a public key with its attributes
"""

class PublicKey(object):
    
    def __init__(self,id,service,type):
        self.id = id
        self.service = service
        self.type = type

    def __str__(self):
        return "\n\t\t\tPublic Key id: {}\n\t\t\tService: {}\n\t\t\tType: {}".format(self.id,self.service,self.type)

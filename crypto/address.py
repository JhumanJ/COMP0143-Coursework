from crypto.public_key import PublicKey
from typing import Optional

"""
Represents a default address in a block
"""

class Address(object):

    def __init__(self,id,public_key: Optional[PublicKey]):
        self.id = id
        self.public_key = public_key

    def __str__(self):

        string =  "\n\t\t----------------\n\t\tAddress id: {}".format(self.id)
        if not self.public_key is None:
            string += "\n\t\tPublic Key: {}".format(self.public_key)

        return string

"""
Input Class
"""
class Input(Address):

    def __init__(self,id,public_key,output_id):
        Address.__init__(self,id,public_key)
        self.output_id = output_id

    def __str__(self):
        string = Address.__str__(self)

        return string + "\n\t\tOutput id: {}".format(self.output_id)

"""
Input Class
"""
class Output(Address):

    def __init__(self,id,public_key,value):
        Address.__init__(self,id,public_key)
        self.value = value

    def __str__(self):
        string = Address.__str__(self)

        return string + "\n\t\tValue: {}".format(self.value)
"""
Represents a transaction in a block
"""

class Transaction(object):

    def __init__(self,id,inputs,outputs):
        self.id = id
        self.inputs = inputs
        self.outputs = outputs

    def __str__(self):
        inputs = "".join([str(input)for input in self.inputs])
        outputs = "".join([str(output)for output in self.outputs])

        return "\n\t----------------\n\tTransaction id: {} \n\tInputs: {} \n\tOutputs: {}\n".format(self.id,inputs,outputs)
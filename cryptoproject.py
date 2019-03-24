import csv
from collections import Counter
import operator
from itertools import chain
from crypto.public_key import PublicKey
from crypto.address import *
from crypto.transaction import *
from crypto.block import *
from crypto.blockchain import BlockChain


transactions = csv.reader(open('./data/transactions.csv', 'rt'),delimiter=',')
inputs = csv.reader(open('./data/inputs.csv', 'rt'),delimiter=',')
outputs  = csv.reader(open('./data/outputs.csv', 'rt'),delimiter=',')
tags  = csv.reader(open('./data/tags.csv', 'rt'),delimiter=',')

"""
Returns a list of blocks which is the blockchain.
"""
def buildBlockChain():
    global transactions, inputs, outputs, tags

    # Build public keys objects
    tagsDict = {}
    for tag in tags:
        tagsDict[tag[2]] = PublicKey(tag[2],tag[0],tag[1])

    # Now build inputs and outputs dictionary. Key is the transaction ID for both
    inputDict = {}
    outputDict = {}
    for input in inputs:
        pk = None
        # Find know public key (with tags) if exists
        if not input[2] in ['0','-1','-10']:
            if input[2] in tagsDict:
                pk = tagsDict[input[2]]
            else:
                pk = PublicKey(input[2])

        if not input[1] in inputDict:
            inputDict[input[1]] = []
        inputDict[input[1]].append(Input(input[0],pk,input[3]))

    for output in outputs:
        pk = None

        # Find know public key (with tags) if exists
        if not output[2] in ['0','-1','-10']:
            if output[2] in tagsDict:
                pk = tagsDict[output[2]]
            else:
                pk = PublicKey(output[2])
        else:
            pk = output[2]

        if not output[1] in outputDict:
            outputDict[output[1]] = []
        outputDict[output[1]].append(Output(output[0],pk,output[3]))

    # Now build transaction dictionnary (block id is key)
    transactionDict = {}
    for transaction in transactions:
        if not transaction[1] in transactionDict:
            transactionDict[transaction[1]] = []

        transactionDict[transaction[1]].append(
            Transaction(
                transaction[0],
                inputDict[transaction[0]],
                outputDict[transaction[0]]
            )
        )

    # Finally create blockchain and blocks
    blockchain = []
    for key in transactionDict:
        blockchain.append(Block(key,transactionDict[key]))

    return BlockChain(blockchain,transactionDict,inputDict,outputDict,tagsDict)


blockchain = buildBlockChain()

def q1_1():
    global blockchain

    count = 0
    count1in2out = 0
    count1in1out = 0

    for block in blockchain.blocks:
        for transaction in block.transactions:
            count += 1
            if len(transaction.inputs) == 1:
                if len(transaction.outputs) == 2:
                    count1in2out +=1
                if len(transaction.outputs) == 1:
                    count1in1out +=1

    print("Total: {}, 1 in 2 out: {}, 1 in one out: {}".format(count,count1in2out,count1in1out))

    '''
    there are 216626 transactions in total
    there are 44898 transactions with one input and two outputs
    there are 160780 transactions with one input and one outputs
    '''


def q1_2():

    #todo: check that 0,-1 and,-10 are still added

    global blockchain

    utxos = {}

    # Build utxos
    for block in blockchain.blocks:
        for transaction in block.transactions:
            for output in transaction.outputs:
                if isinstance(output.public_key,PublicKey):
                    utxos[output.id] = int(output.value)

            for input in transaction.inputs:
                if isinstance(input.public_key,PublicKey):
                    if input.output_id != "-1":
                        if not input.output_id in utxos:
                            print("Error: {} output id not existing or already spent.".format(input.output_id))
                        else:
                            del utxos[input.output_id]

    print("Final number of utxos: {}".format(len(utxos.keys())))
    print("Max utxo value: {}".format(sorted(utxos.items(), key=lambda kv: kv[1],reverse=True)[0]))

    """
    Final number of utxos: 71904
    Max utxo value: 9000000000000
    """

def q1_3():
    global blockchain

    publicDict = {}

    for block in blockchain.blocks:
        for transaction in block.transactions:
            for input in transaction.inputs:
                if isinstance(input.public_key,PublicKey) and not input.public_key.id in publicDict:
                    publicDict[input.public_key.id] = (0,0)

            for output in transaction.outputs:
                if isinstance(output.public_key,PublicKey):
                    if not output.public_key.id in publicDict:
                        publicDict[output.public_key.id] = (0,0)

                    (value, count) = publicDict[output.public_key.id]
                    if output.public_key.id == '148105':
                        print(value,output.value)
                    publicDict[output.public_key.id] = (value + int(output.value), count+1)

    print("Total number of public keys: {}".format(len(publicDict.keys())))
    print("Public key which received the most: {}".format(sorted(publicDict.items(), key=lambda kv: kv[1][0],reverse=True)[0]))
    print("Public key which received most times: {}".format(sorted(publicDict.items(), key=lambda kv: kv[1][1],reverse=True)[0]))

    '''
    there are 174701 distinct public keys used across all the blocks
    the public key that received the most bitcoin is pk=148105, it received 27375023000000 satoshis
    the public key 148105 acted as an output the most number of times: 5498 times
    '''

def q1_4():
    """
    We already found weird attempts to use utxos in q2. Let's find their transaction id.
    """

    global blockchain

    utxos = {}
    weirdUtxos = []

    # Build utxos to find the one spent more thhan once
    for block in blockchain.blocks:
        for transaction in block.transactions:
            for output in transaction.outputs:
                if isinstance(output.public_key, PublicKey):
                    utxos[output.id] = 0

            for input in transaction.inputs:
                if isinstance(input.public_key, PublicKey):
                    if input.output_id != "-1":
                        if not input.output_id in utxos:
                            weirdUtxos.append(input.output_id)
                            print("Error: {} output id not existing.".format(input.output_id))
                        else:
                            utxos[input.output_id] +=1

    for key in utxos:
        if utxos[key] > 1:
            weirdUtxos.append(key)
            print("Error: utxo id {} was spent {} times.".format(key,utxos[key]))

    print(weirdUtxos)

    """
    Two transactions used output id of transactions that were not done yet, or not existing?
    utxos: 265834, 249860
    And 3 were doing double spending:
    utxos: 7998, 21928, 65403
    """

    #TODO check above and retrieve transactions ids

    '''
    There are transactions which used the same utxo twice, i.e double spending / UTXO='249860': 2, '7998': 2, '21928': 2, '65403': 2
    The transactions ids that were invalid because of double spending are: '207365', '204751', '12152', '30446', '61843', '61845'
    '''

def clustering():

    def clusterize(clusters,candidateCluster):
        """
        Helper to create clusters
        """
        toMerge = []
        for idx, cluster in enumerate(clusters):
            if len( cluster.copy().intersection(candidateCluster) ):
                toMerge.append(idx)

        if len(toMerge) == 0:
            clusters.append(candidateCluster)
        elif len(toMerge) == 1:
            clusters[toMerge[0]] = clusters[toMerge[0]].union(candidateCluster)
        else:
            for idx in toMerge:
                current = clusters[idx].copy()
                candidateCluster = candidateCluster.union(current)

            deleted = 0
            for idx in toMerge:
                del clusters[idx-deleted]
                deleted+=1
            clusters.append(candidateCluster)

        return clusters

    global blockchain

    clusters = []

    # Find multi inputs transactions
    for block in blockchain.blocks:
        for transaction in block.transactions:
            if len(transaction.inputs) > 1:
                candidateCluster = set([input.public_key.id for input in transaction.inputs])
                clusters = clusterize(clusters,candidateCluster)

    # Check clustering to make sure no public key is in two different clusters
    check = {}
    for cluster in clusters:
        for item in cluster:
            if not item in check:
                check[item] = 0
            check[item] += 1

    for key in check:
        if check[key] > 1:
            print("{} appears in {} clusters.".format(key,check[key]))

    print("Clustering done: {} clusters created".format(len(clusters)))
    return clusters

"""
Returns a dict mapping public key to cluster id
"""
def buildClusterDict(clusters):

    clusterDict = {}
    for idx, cluster in enumerate(clusters):
        for key in cluster:
            clusterDict[key] = idx
    return clusterDict

clusters = clustering()
clusterDict = buildClusterDict(clusters)

def q2_1():
    global clusters, clusterDict

    cluster = clusters[clusterDict['41442']]
    cluster = [int(val) for val in cluster]
    print("Length of the cluster: {}, max public key: {}, min: {}".format(len(cluster),max(cluster),min(cluster)))
    return

def q2_2():
    global clusters
    lenClusters = [len(cluster) for cluster in clusters]

    cluster = clusters[lenClusters.index(max(lenClusters))]
    cluster = [int(val) for val in cluster]

    print("Biggest cluster: {}, max public key: {}, min: {}".format(len(cluster),max(cluster),min(cluster)))

def q2_3():
    global clusters, clusterDict




q2_3()
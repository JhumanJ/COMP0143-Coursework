import csv
from collections import Counter
import operator
from itertools import chain
from crypto.public_key import PublicKey
from crypto.address import *
from crypto.transaction import *
from crypto.block import *


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

    # Now build inputs and outputs dictionnary. Key is the transaction ID for both
    inputDict = {}
    outputDict = {}
    for input in inputs:
        pk = None
        # Find know public key (with tags) if exists
        if not input[2] in ['0','-1']:
            if input[2] in tagsDict:
                pk = tagsDict[input[2]]

        if not input[1] in inputDict:
            inputDict[input[1]] = []
        inputDict[input[1]].append(Input(input[0],pk,input[3]))

    for output in outputs:
        pk = None
        # Find know public key (with tags) if exists
        if not output[2] in ['0','-1']:
            if output[2] in tagsDict:
                pk = tagsDict[output[2]]

        if not output[1] in outputDict:
            outputDict[output[1]] = []
        outputDict[output[1]].append(Input(output[0],pk,output[3]))

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

    return blockchain


blockchain = buildBlockChain()


def q1():
    # How many transactions were there in total? Of these, how many transactions had one input and two outputs?
    # How many transactions had one input and one output?
    s=set()
    inputs_list=[]
    outputs_list=[]
    count_inputs={}
    count_outputs={}
    for i in transactions:
        # i[0] is the tx_id
        s.add(i[0])
    total_tx = len(s)
    # one input two output: count number of tx with 2 output, add the tx id to a list / count number of tx with 1 input add tx id to list / use set intersection?
    for i in inputs:
        inputs_list.append(i[1])
    # number of inputs per transactions
    count_inputs=Counter(inputs_list)
    for i in outputs:
        outputs_list.append(i[1])
    count_outputs=Counter(outputs_list)
    tx_1_input = [key  for (key, value) in count_inputs.items() if value == 1]
    tx_2_output = [key  for (key, value) in count_outputs.items() if value == 2]
    tx_1_output = [key  for (key, value) in count_outputs.items() if value == 1]
    one_input_two_outputs = set(tx_1_input) & set (tx_2_output)
    one_input_one_outputs = set(tx_1_input) & set (tx_1_output)
    print (len(one_input_two_outputs))
    print (len(one_input_one_outputs))
    '''
    there are 44898 transactions with one input and two outputs
    there are 160780 transactions with one input and one outputs

    '''
def q2():
    # How many UTXOs exist, as of the last block of the dataset? Which UTXO has the highest associated value?
    tx_id = []
    utxo=[]
    for i in transactions:
        # the last block is block 100017
        if i[1]=='100017':
            # transactions included in the last block
            tx_id.append(i[0])
    for i in inputs:
        if i[1] in tx_id:
            utxo.append(i[3])
    print(len(utxo))

def q3():
    pk=set()
    pk_list=[]
    pk_dict={}
    values=[]
    max_btc=0
    for i in outputs:
        if i[2] != (-1):
            pk_dict[i[2]]=i[3]
            pk.add(i[2])
            pk_list.append(i[2])
    print(len(pk_list))
    print(len(pk_dict))
    max_btc=max(zip(pk_dict.values(), pk_dict.keys()))
    print(max_btc)
    counter=Counter(pk_list)
    max_pk=max(zip(counter.values(), counter.keys()))
    print(max_pk)
    print (counter)
    '''
    there are 174702 distinct public keys used across all the blocks
    the public key that received the most bitcoin is pk=98038, it received 9999971000 satoshis
    the public key 148105 acted as an output the most number of times: 5498 times
    '''

def q4():
    utxo=[]
    sig_id=[]
    dict_input={}
    tx_id=[]
    for i in inputs:
        utxo.append(i[3])
        sig_id.append(i[2])
        dict_input[i[1]]=i[3]
    double_spent = [key  for (key, value) in Counter(utxo).items() if value>1 and key!='-1']
    for i in double_spent:
        tx_id.append([key  for (key, value) in dict_input.items() if value == i])
    print(tx_id)
    '''
    There are transactions which used the same utxo twice, i.e double spending / UTXO='249860': 2, '7998': 2, '21928': 2, '65403': 2
    The transactions ids that were invalid because of double spending are: '207365', '204751', '12152', '30446', '61843', '61845'
    '''

def clustering():
        global inputs
        global outputs
        s=set()
        inputs_list=[]
        outputs_list=[]
        dict_cluster={}
        for i in inputs:
            inputs_list.append(i[1])
        count_inputs=Counter(inputs_list)
        for i in outputs:
            outputs_list.append(i[1])
        count_outputs=Counter(outputs_list)
        tx_multi_input = [key  for (key, value) in count_inputs.items() if value>1]
        tx_1_output = [key  for (key, value) in count_outputs.items() if value == 1]
        multi_input_two_outputs = set(tx_multi_input) & set (tx_1_output)

        # build dict of transactions
        transactions = {}
        for elem in csv.reader(open('./data/inputs.csv', 'rt'),delimiter=','):
            if not elem[1] in transactions:
                transactions[elem[1]] = set()
            transactions[elem[1]].add(elem[0])

        print ("len multi_input_two_outputs:" + str(len(multi_input_two_outputs)))
        

        clusters = []  # list of sets
        for tx in multi_input_two_outputs:
            clustersIndex = []
            inputs = transactions[tx]
            for input in inputs:
                for idx, cluster in enumerate(clusters):
                    if input in cluster:
                        # here we found that one of the input is in the current cluste set
                        clustersIndex.append(idx)

            # if no clusters found creaate a new one
            if len(clustersIndex) == 0:
                clusters.append(set(inputs))
            # if 1 cluster found add all iinputs to that cluster
            elif len(clustersIndex) == 1:
                for input in inputs:
                    clusters[clustersIndex[0]].add(input)
            # if more than 1, merge the clusters and add inputs to the resulting cluster
            elif len(clustersIndex) > 1:
                mergedSet = set()
                # Create a merged set
                for index in clustersIndex:
                    mergedSet.union(clusters[index].copy())
                # Now delete sets that were merged
                for index in clustersIndex:
                    clusters.remove(index)

                for input in inputs:
                    clusters[clustersIndex[0]].add(input)

                # Finally add new resulting clusters

                clusters.append(mergedSet)

        print(clusters)


        # cluster = 0
        # for elem in csv.reader(open('/Users/macbook/desktop/ucl/CS- year 4/Cryptocurrencies/data/inputs.csv', 'rt'),delimiter=','):
        #     if elem[1] in multi_input_two_outputs:
        #         if bool([key  for (key, value) in dict_cluster.items() if value==elem[0]]):
        #             index = [key  for (key, value) in dict_cluster.items() if value==elem[0]]
        #             min_index=min(index)
        #             for i in index:
        #                 dict_cluster[min_index].append(elem[0])
        #                 dict_cluster[min_index].append(i.keys())
        #                 del dict_cluster[i]
        #             print('appended')
        #         else:
        #             dict_cluster[cluster]=elem[0]
        #             cluster+=1
        #             print('created')

        # print(dict_cluster)
        # transactions with multi-inputs and one output
        # print (len(multi_input_two_outputs))

# clustering()

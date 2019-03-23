import csv
from collections import Counter
import operator
from itertools import chain
from crypto.public_key import PublicKey
from crypto.address import *
from crypto.transaction import *
from crypto.block import *

"""
Returns a list of blocks which is the blockchain.
"""
def buildBlockChain():
    transactions = csv.reader(open('./data/transactions.csv', 'rt'),delimiter=',')
    inputs = csv.reader(open('./data/inputs.csv', 'rt'),delimiter=',')
    outputs  = csv.reader(open('./data/outputs.csv', 'rt'),delimiter=',')
    tags  = csv.reader(open('./data/tags.csv', 'rt'),delimiter=',')

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


def q1_1():
    global blockchain

    count = 0
    count1in2out = 0
    count1in1out = 0

    for block in blockchain:
        for transaction in block.transactions:
            count += 1
            if len(transaction.inputs) == 1:
                if len(transaction.outputs) == 2:
                    count1in2out +=1
                if len(transaction.outputs) == 1:
                    count1in1out +=1

    print(count,count1in2out,count1in1out)

    '''
    there are 216626 transactions in total
    there are 44898 transactions with one input and two outputs
    there are 160780 transactions with one input and one output
    '''

def q1_2():
    # How many UTXOs exist, as of the last block of the dataset? Which UTXO has the highest associated value?
    transactions = csv.reader(open('./data/transactions.csv', 'rt'),delimiter=',')
    inputs = csv.reader(open('./data/inputs.csv', 'rt'),delimiter=',')
    outputs  = csv.reader(open('./data/outputs.csv', 'rt'),delimiter=',')
    tags  = csv.reader(open('./data/tags.csv', 'rt'),delimiter=',')

    utxo_spent = set()
    output_pk = set()
    dict_utxo = {}
    for i in inputs:
        utxo_spent.add(i[3])
    for i in outputs:
        if i[2] in dict_utxo.keys():
            float(dict_utxo[i[2]]) +float(i[3])
        else:
            dict_utxo[i[2]] = float(i[3])
        output_pk.add(i[2])
    unspent = output_pk - utxo_spent
    max_value=0
    pk = ''
    for utxo in unspent:
        if dict_utxo[utxo] > max_value:
            max_value=dict_utxo[utxo]
            pk = utxo
    print(utxo)
    print(max_value)
    print(len(unspent))

    return dict_utxo
    '''
    there are 60794 unspent utxo, the pk that received the most bitcoins is 2952 it received 4000000000000.0BTC in total
    '''

def q1_3():
    transactions = csv.reader(open('./data/transactions.csv', 'rt'),delimiter=',')
    inputs = csv.reader(open('./data/inputs.csv', 'rt'),delimiter=',')
    outputs  = csv.reader(open('./data/outputs.csv', 'rt'),delimiter=',')
    tags  = csv.reader(open('./data/tags.csv', 'rt'),delimiter=',')

    pk=set()
    pk_list=[]
    pk_dict={}
    values=[]
    max_btc=0
    for i in outputs:
        if i[2] != (-1) and i[2] != (0) and i[2] != (-10):
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

def q1_4():
    transactions = csv.reader(open('./data/transactions.csv', 'rt'),delimiter=',')
    inputs = csv.reader(open('./data/inputs.csv', 'rt'),delimiter=',')
    outputs  = csv.reader(open('./data/outputs.csv', 'rt'),delimiter=',')
    tags  = csv.reader(open('./data/tags.csv', 'rt'),delimiter=',')

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
def union(s,v,clusters):
    bool = (s!=v)
    s.update(s.union(v))
    if bool == True:
        clusters.remove(v)

def clustering():
    transactions = csv.reader(open('./data/transactions.csv', 'rt'),delimiter=',')
    inputs = csv.reader(open('./data/inputs.csv', 'rt'),delimiter=',')
    outputs  = csv.reader(open('./data/outputs.csv', 'rt'),delimiter=',')
    tags  = csv.reader(open('./data/tags.csv', 'rt'),delimiter=',')

    s=set()
    inputs_list=[]
    outputs_list=[]
    dict_cluster={}
    for i in inputs:
        inputs_list.append(i[1])
    count_inputs=Counter(inputs_list)
    # for i in outputs:
    #     outputs_list.append(i[1])
    count_outputs=Counter(outputs_list)
    tx_multi_input = [key  for (key, value) in count_inputs.items() if value>1]
    # tx_1_output = [key  for (key, value) in count_outputs.items() if value == 1]
    # multi_input_two_outputs = set(tx_multi_input) & set (tx_1_output)
    multi_input_two_outputs = set(tx_multi_input)

    # build dict of transactions
    transactions = {}
    for elem in csv.reader(open('./data/inputs.csv', 'rt'),delimiter=','):
        if not elem[1] in transactions:
            transactions[elem[1]] = set()
        transactions[elem[1]].add(elem[2])

    print ("len multi_input_two_outputs:" + str(len(multi_input_two_outputs)))

    clusters=[]
    for elem in transactions.keys():
        if elem in multi_input_two_outputs:
            clusters.append(set(transactions[elem]))
    for i in clusters:
        for j in clusters:
            if bool(i&j):
                union(i,j,clusters)
    print(clusters)

    return clusters


def q2_1():
    clusters=clustering()
    for i in clusters:
        if '41442' in i:
            print(len(i))
            convert_int = [int(j) for j in i]
            print(min(convert_int))
            print(max(convert_int))

    '''
    The size of the cluster is 50, minimum pk=40284, maximum pk=41911
    '''

def q2_2():
    clusters=clustering()
    max_len = 0
    cluster = set()
    for i in clusters:
        temp = len(i)
        if temp > max_len:
            max_len = temp
            cluster = i
    biggest_cluster=clusters.index(cluster)
    convert_int = [int(i) for i in clusters[biggest_cluster]]
    min_pk = min(convert_int)
    max_pk = max(convert_int)
    print(cluster)
    print(max_len)
    print(min_pk)
    print(max_pk)

    '''
    the length of the biggest cluster is 93023 the minimum pk is 29823 and the maximum pk is 173091
    '''

def q2_3():
    clusters=clustering()
    dict_utxo=q1_2()
    max_unspent = 0
    id = 0
    for i in clusters:
        received_btc =0
        for j in i:
            if j in dict_utxo.keys():
                received_btc += dict_utxo[j]
        if received_btc > max_unspent:
            max_unspent = received_btc
            id = clusters.index(i)
    convert_int = [int(i) for i in clusters[clusters.index(i)]]
    max_pk = max(convert_int)
    min_pk = min(convert_int)
    print(max_unspent)
    print(min_pk)
    print(max_pk)

    '''
    The richest cluster has 12541643427529.0 BTC, it contains the minimum pk 173528 and the maximum pk 173943
    '''

q2_3()

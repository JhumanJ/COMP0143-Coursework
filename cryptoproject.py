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
    dict_highest_associated_value={}
    for i in inputs:
        utxo_spent.add(i[3])
    for i in outputs:
        # if i[2] not in dict_utxo.keys():
        #     dict_utxo[i[2]]=0
        # dict_utxo[i[2]]+=float(i[3])

        if i[2] not in dict_highest_associated_value.keys():
            dict_highest_associated_value[i[2]]=0
        if dict_highest_associated_value[i[2]] < float(i[3]):
            dict_highest_associated_value[i[2]] = float(i[3])

        output_pk.add(i[2])

    unspent = output_pk - utxo_spent

    for i in csv.reader(open('./data/outputs.csv', 'rt'),delimiter=','):
        if i[2] not in dict_utxo.keys():
            dict_utxo[i[2]]=0
        if i[2] in unspent:
            dict_utxo[i[2]]+=float(i[3])

    # highest cumulative value received by a pk
    max_value=0
    pk = ''
    for utxo in unspent:
        if dict_utxo[utxo] > max_value:
            max_value=dict_utxo[utxo]
            # public key that received the most bitcoins
            pk = utxo
    highest_value = max(dict_highest_associated_value.values())
    richest_utxo = [key  for (key, value) in dict_highest_associated_value.items() if value==highest_value]
    print('there are '+str(len(unspent))+' unspent UTXOs '+'the utxo with the highest associated value is '+str(richest_utxo)+ ' it received '+str(highest_value))
    print (dict_utxo)
    return dict_utxo
    '''
    there are 60794 unspent UTXOs
    the public key 124231 received the most bitcoins, it received 10970000000000.0 satoshis

    there are 60794 unspent UTXOs the utxo with the highest associated value is ['138871', '138895'] it received 9000000000000.0
    '''

def q1_3():
    transactions = csv.reader(open('./data/transactions.csv', 'rt'),delimiter=',')
    inputs = csv.reader(open('./data/inputs.csv', 'rt'),delimiter=',')
    outputs  = csv.reader(open('./data/outputs.csv', 'rt'),delimiter=',')
    tags  = csv.reader(open('./data/tags.csv', 'rt'),delimiter=',')

    received={}
    pk =set()
    output_pks=[]
    for i in inputs:
        pk.add(i[2])
    for i in outputs:
        pk.add(i[2])
        if i[2] not in received.keys():
            received[i[2]]=0.0
        received[i[2]]+=float(i[3])
        output_pks.append(i[2])
    if '-1' in pk:
        pk.remove('-1')
        print('removed -1')
    if '0' in pk:
        pk.remove('0')
        print('removed 0')
    if '-10' in pk:
        pk.remove('-10')
        print('removed -10')
    count_outputs=Counter(output_pks)
    # max number of times a pk appeared as an output
    max_count = max(count_outputs.values())
    # pk that appeared the most as an output
    output_max=[key  for (key, value) in count_outputs.items() if value==max_count]
    max_received=max(list(received.values()))
    pk_max=[key  for (key, value) in received.items() if value==max_received]
    print('there are ' + str(len(pk)) + ' distinct public keys used across all the blocks, the public key that received the most bitcoin is pk=' + str(pk_max)
    + 'it received '+str(max_received) + ' satoshis, the public key ' + str(output_max) + ' acted as an output the most number of times: ' + str(max_count)+ ' times')

    '''
        there are 174701 distinct public keys used across all the blocks,
        the public key that received the most bitcoin is pk=['148105']it received 27375023000000.0 satoshis,
        the public key ['148105'] acted as an output the most number of times: 5498 times
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

# union of two sets
def union(s,v,clusters):
    # check that s and v are two different sets
    bool = (s!=v)
    s.update(s.union(v))
    if bool == True:
        # remove the set v --> subset of s
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
    count_outputs=Counter(outputs_list)
    tx_multi_input = [key  for (key, value) in count_inputs.items() if value>1]
    # set containing transaction id of multi input transactions
    multi_input_two_outputs = set(tx_multi_input)

    # build dict of transactions, contains transactions id as keys and input pk as values
    transactions = {}
    for elem in csv.reader(open('./data/inputs.csv', 'rt'),delimiter=','):
        if not elem[1] in transactions:
            transactions[elem[1]] = set()
        if elem[2] != -1 and elem[2]!= 0:
            transactions[elem[1]].add(elem[2])

    clusters=[]
    for elem in transactions.keys():
        # if transaction is multi input transaction
        if elem in multi_input_two_outputs:
            # append transaction to the list "clusters"
            clusters.append(set(transactions[elem]))
    for i in clusters:
        for j in clusters:
            # union of every set i and j
            if bool(i&j):
                union(i,j,clusters)
    print('there are '+ str(len(clusters)) + ' clusters')
    print(len(set.union(*list(clusters))))
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
    # print(cluster)
    print(max_len)
    print(min_pk)
    print(max_pk)

    '''
    the length of the biggest cluster is 921 the minimum pk is 29823 and the maximum pk is 173091
    '''

def get_value(input,output):
    transactions = csv.reader(open('./data/transactions.csv', 'rt'),delimiter=',')
    inputs = csv.reader(open('./data/inputs.csv', 'rt'),delimiter=',')
    outputs  = csv.reader(open('./data/outputs.csv', 'rt'),delimiter=',')
    tags  = csv.reader(open('./data/tags.csv', 'rt'),delimiter=',')
    tx = []
    value = 0
    for i in inputs:
        if i[2]==input and i[3]==output:
            tx.append(i[1])
    for i in outputs:
        for t in tx:
            if i[2]==output and i[1]==t:
                value = float(i[3])
    return value

def sender(cluster):
    transactions = csv.reader(open('./data/transactions.csv', 'rt'),delimiter=',')
    inputs = csv.reader(open('./data/inputs.csv', 'rt'),delimiter=',')
    outputs  = csv.reader(open('./data/outputs.csv', 'rt'),delimiter=',')
    tags  = csv.reader(open('./data/tags.csv', 'rt'),delimiter=',')
    # list of all the pk that sent money to a cluster
    dict_senders={}
    for i in inputs:
        # for every pk in the cluster
        for pk in cluster:
            if i[3]==pk and i[2]==pk:
                if i[2] not in dict_senders.keys():
                    dict_senders[i[2]]=0
                dict_senders[i[2]]+=get_value(i[2],i[3])
    print(dict_senders)
    return dict_senders


def q2_3():
    clusters=clustering()
    dict_utxo=q1_2()
    max_unspent = 0
    id = 0
    for i in clusters:
        received_satoshis =0
        for j in i:
            if j in dict_utxo.keys():
                received_satoshis += dict_utxo[j]
        if received_satoshis > max_unspent:
            max_unspent = received_satoshis
            id = clusters.index(i)
    convert_int = [int(i) for i in clusters[clusters.index(i)]]
    max_pk = max(convert_int)
    min_pk = min(convert_int)
    print(max_unspent)
    print(min_pk)
    print(max_pk)
    print(clusters[clusters.index(i)])
    dict_senders = sender(clusters[clusters.index(i)])
    max_value = max(list(dict_senders.values()))
    sender_pk = [key  for (key, value) in dict_senders.items() if value==max_value]

    print(max_value)
    print(sender_pk)
    '''
    The richest cluster has 12541643427529.0 satoshis, it contains the minimum pk 173528 and the maximum pk 173943
    '''

q2_3()

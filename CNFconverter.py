__author__ = 'TianXiang Tan'

import string
from copy import deepcopy

def eliminate_biconditional(sentence):
    if not isinstance(sentence, list):
        return sentence

    result = list()
    if sentence[0] == 'iff':
        result.append('and')
        p = eliminate_biconditional(sentence[1])
        q = eliminate_biconditional(sentence[2])
        result1 = ['implies', p, q]
        result2 = ['implies', q, p]
        result.append(result1)
        result.append(result2)
    else:
        result.append(sentence[0])
        for token in sentence:
            if token != sentence[0]:
                token = eliminate_biconditional(token)
                result.append(token)

    return result


def eliminate_implies(sentence):
    if not isinstance(sentence, list):
        return sentence

    result = list()
    if sentence[0] == 'implies':
        result.append('or')
        p = eliminate_implies(sentence[1])
        q = eliminate_implies(sentence[2])
        list_p = ['not', p]
        result.append(list_p)
        result.append(q)
    else:
        result.append(sentence[0])
        for token in sentence:
            if token != sentence[0]:
                token = eliminate_implies(token)
                result.append(token)

    return result


def push_or(sentence):
    if not isinstance(sentence, list):
        return sentence

    result = list()
    to_reduce = False
    if sentence[0] == 'or':
        for token in sentence:
            if token == sentence[0]:
                continue
            if isinstance(token, list) and token[0] == 'and':
                to_reduce = True
                distributed_token = token
                break
        if to_reduce:
            other_list = ['or']
            for token in sentence:
                if token != sentence[0] and token != distributed_token:
                    other_list.append(token)
            result = ['and']
            for token in distributed_token:
                if token != distributed_token[0]:
                    temp_list = deepcopy(other_list)
                    temp_list.append(token)
                    temp_list = push_or(temp_list)
                    result.append(temp_list)
            return result

    result = [sentence[0]]
    for token in sentence:
        if token != sentence[0]:
            result.append(push_or(token))
    return result


def push_not(sentence):
    if not isinstance(sentence, list):
        return sentence

    if sentence[0] == 'not':
        if isinstance(sentence[1], list):
            if sentence[1][0] == 'not':
                return push_not(sentence[1][1])
            elif sentence[1][0] == 'and':
                result = ['or']
            elif sentence[1][0] == 'or':
                result = ['and']
            for token in sentence[1]:
                if token != sentence[1][0]:
                    result.append(push_not(['not', token]))
            return result
        else:
            return sentence
    else:
        result = [sentence[0]]
        for token in sentence:
            if token != sentence[0]:
                result.append(push_not(token))
        return result


def eliminate_duplicate_not(sentence):
    if not isinstance(sentence, list):
        return sentence

    result = list()
    if sentence[0] == 'not':
        if isinstance(sentence[1], list) and sentence[1][0] == 'not':
            return eliminate_duplicate_not(sentence[1][1])
        else:
            result.append('not')
            result.append(eliminate_duplicate_not(sentence[1]))
    else:
        result.append(sentence[0])
        for component in sentence:
            if component != sentence[0]:
                result.append(eliminate_duplicate_not(component))

    return result


def reduce_duplicate_operand(sentence):
    if not isinstance(sentence, list):
        return sentence
    
    if sentence[0] == 'not':
        return ['not', reduce_duplicate_operand(sentence[1])]
    
    result = [sentence[0]]
    for token in sentence:
        if token != sentence[0]:
            if not isinstance(token, list):
                result.append(token)
            else:
                token = reduce_duplicate_operand(token)
                if token[0] == sentence[0]:
                    for temp in token:
                        if temp != token[0]:
                            result.append(temp)
                else:
                    result.append(token)
    return result
                

def reduce_duplicate_component(sentence):
    if not isinstance(sentence, list):
        return sentence
    
    result = [sentence[0]]
    if sentence[0] != 'not':
        for token in sentence:
            if token != sentence[0]:
                token = reduce_duplicate_component(token)
                in_result = False
                for temp in result:
                    if temp == token:
                        in_result = True
                        break
                if not in_result:
                    result.append(token)
    else:
        result.append(reduce_duplicate_component(sentence[1]))
    return result


def convert_to_cnf(sentence):
    # Eliminate the implication and the biconditional condition
    sentence = eliminate_biconditional(sentence)
    print '-biconditional:   {s}.'.format(s=sentence)
    sentence = eliminate_implies(sentence)
    print '-implies:         {s}.'.format(s=sentence)
    # Push the 'not' downward
    sentence = push_not(sentence)
    print '-not:             {s}.'.format(s=sentence)
    # Push or
    sentence = push_or(sentence)
    print '-or:              {s}.'.format(s=sentence)
    # Eliminate the duplicate nots
    #sentence = eliminate_duplicate_not(sentence)
    # Reduce duplicate operand
    sentence = reduce_duplicate_operand(sentence)
    print '-operand:         {s}.'.format(s=sentence)
    # Reduce duplicate component
    sentence = reduce_duplicate_component(sentence)
    print '-component:       {s}.'.format(s=sentence)
    return sentence


if __name__ == '__main__':
    input_file_name = 'sentences.txt'
    output_file_name = ''
    inputFile = open('sentences.txt')
    sentencesNum = string.atoi(inputFile.readline())

    while sentencesNum > 0:
        sentence = eval(inputFile.readline())
        print 'original:         {s}.'.format(s=sentence)
        sentence = convert_to_cnf(sentence)
        print 'converted:        {sentence}\n'.format(sentence=sentence)
        sentencesNum -= 1
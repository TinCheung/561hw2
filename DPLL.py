__author__ = 'TianXiang Tan'
import string


def findUnit(clauses, symbols):
    for c in clauses:
        if c in symbols:
            continue
        if not isinstance(c, list):
            return (c, True)
        elif c[0] == 'not':
            return (c[1], False)
    return (-1, False)


def findPure(clauses):
    for c in clauses:
        


def DPLL(clauses, symbols, assignment):
    pass

def getClauses(sentence):
    clauses = list()
    if sentence[0] == 'and':
        clauses = sentence[1:]
    else:
        clauses = sentence
    return clauses

def getSymbols(sentence):
    if not isinstance(sentence, list):
        return sentence
    
    result = []
    for token in sentence:
        if not isinstance(token, list):
            if len(token) == 1 and token not in result:
                result.append(token)
        else:
            sym_list = getSymbols(token)
            for sym in sym_list:
                if len(sym) == 1 and sym not in result:
                    result.append(sym)
    return result


if __name__ == '__main__':
    input_file_name = 'CNF_sentences.txt'
    output_file_name = ''
    inputFile = open(input_file_name)
    sentencesNum = string.atoi(inputFile.readline())

    while sentencesNum > 0:
        sentence = eval(inputFile.readline())
        print 'original:         {s}.'.format(s=sentence)
        symbols = getSymbols(sentence)
        clauses = getClauses(sentence)
        assignment = {}
        DPLL(clauses, symbols, assignment)
        sentencesNum -= 1
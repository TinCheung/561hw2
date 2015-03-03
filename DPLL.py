__author__ = 'TianXiang Tan'
import string
from copy import deepcopy


def findUnit(clauses, symbols):
    for clause in clauses:
        if not isinstance(clause, list) and clause in symbols:
            return (clause, True)
        # Consider the not variable
        elif isinstance(clause, list) and clause[0] == 'not' and clause[1] in symbols:
            return (clause, False)
    return ('', False)


def findPure(clauses, symbols):
    # Use two list to record the appearance of a variable and its negative one
    sym_list = list()
    not_sym_list = list()
    for clause in clauses:
        # Check the ['not', 'X'] and ['or', 'x', ...]
        if isinstance(clause, list):
            # If it is ['not', 'X']
            if clause[0] == 'not' and clause[1] in symbols and clause[1] not in not_sym_list:
                not_sym_list.append(clause[1])
            # If it is ['or', 'x', ...]
            elif clause[0] == 'or':
                for part in clause:
                    if part != clause[0]:
                        # If it is ['not', 'X']
                        if isinstance(part, list) and part[0] == 'not':
                            if part[1] in symbols and part[1] not in not_sym_list:
                                not_sym_list.append(part[1])
                        # If it is 'X'
                        elif len(part) == 1:
                            if part in symbols and part not in sym_list:
                                sym_list.append(part)
        # Check 'X', though it is checked in findUnit, we add it here for completeness.
        else:
            if clause not in sym_list and clause in symbols:
                sym_list.append(clause)
    # Find the symbol which only appear in sym_list or not_sym_list
    # Check sym_list first.
    for sym in sym_list:
        isUnique = True
        for nsym in not_sym_list:
            if nsym == sym:
                isUnique = False
                break
        if isUnique:
            return (sym, True)
    #Check the not_sym_list.
    for nsym in not_sym_list:
        isUnique = True
        for sym in sym_list:
            if sym == nsym:
                isUnique = False
                break
        if isUnique:
            return (nsym, False)
    # If can't find a pure symbol, then return ('', false)
    return ('', False)


def evaluateClause(clause, assignment):
    satisfied = False
    # If clause is a var like 'A'
    if not isinstance(clause, list) and clause in assignment.keys():
        satisfied = assignment[clause] and True
    # If it is the ['not', 'X'] and ['or', 'x', ...]
    else:
        # ['not', 'X']
        if clause[0] == 'not' and clause[1] in assignment.keys():
            satisfied = (not assignment[clause[1]]) and True
        # ['or', 'x', ...]
        else:
            orResult = False
            for part in clause:
                if part != clause[0]:
                    # if it is var like 'A':
                    if not isinstance(part, list) and part in assignment.keys():
                        orResult = assignment[part] or orResult
                    # if it is ['not', 'x']
                    elif isinstance(part, list) and part[1] in assignment.keys():
                        orResult = (not assignment[part[1]]) or orResult
            satisfied = True and orResult
    return satisfied


def removeTrueClauses(clauses, assignment):
    result = deepcopy(clauses)
    isDeleted = True
    while isDeleted:
        isDeleted = False
        for clause in result:
            if evaluateClause(clause, assignment):
                result.remove(clause)
                isDeleted = True
    return result


def checkSatisfied(clauses, assignment):
    satisfied = True
    for clause in clauses:
        satisfied = satisfied and evaluateClause(clause, assignment)
        if not satisfied:
            return False
    return True


def DPLL(clauses, symbols, assignment):
    if 0 == len(symbols):
        if checkSatisfied(clauses, assignment):
            return (True, assignment)
        else:
            return (False, assignment)
    else:
        pureSymbol = findPure(clauses, symbols)
        if pureSymbol[0] != '':
            symbols.remove(pureSymbol[0])
            assignment[pureSymbol[0]] = pureSymbol[1]
            return DPLL(removeTrueClauses(clauses, assignment), symbols, assignment)
        unitSymbol = findUnit(clauses, symbols)
        if unitSymbol[0] != '':
            symbols.remove(unitSymbol[0])
            assignment[unitSymbol[0]] = unitSymbol[1]
            return DPLL(removeTrueClauses(clauses, assignment), symbols, assignment)
        first_symbol = symbols[0]
        symbols.remove(first_symbol)
        assignment[first_symbol] = True
        result = DPLL(removeTrueClauses(clauses, assignment), symbols, assignment)
        if result[0] == True:
            return result
        else:
            assignment[first_symbol] = False
            result = DPLL(removeTrueClauses(clauses, assignment), symbols, assignment)
            return result

def getClauses(sentence):
    clauses = list()
    if sentence[0] == 'and':
        clauses = sentence[1:]
    else:
        clauses = [sentence]
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


def printResult(result):
    if result[0] == False:
        print '["false"]'
    else:
        print '["true"',
        assignment = result[1]
        for var in assignment:
            print ', "{v}={a}"'.format(v=var, a=assignment[var]),
        print ']'
    

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
        print 'symbols:          {s}.'.format(s=symbols)
        print 'clauses:          {s}.'.format(s=clauses)
        assignment = {}
        result = DPLL(clauses, symbols, assignment)
        printResult(result)
        print ""
        sentencesNum -= 1
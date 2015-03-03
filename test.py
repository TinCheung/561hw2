'''
Created on Mar 2, 2015

@author: TAN
'''

def changeList(a):
    for b in a:
        b = b + 1
        
a = [1,3,5]
changeList(a)
print a
b = a
b.append(6)
b.remove(1)
print b
print a

dic = {'a': True}
print dic
print len(dic)
l = 'a'
print dic[l] and (not False)
c = ('a', True)
print c[0]
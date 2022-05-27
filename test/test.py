# def compareIP(i1, i2):
#     i1 = i1.split(".")
#     i2 = i2.split(".")
#     for i in range(4):
#         if i1[i] != i2[i]:
#             return [i1,i2][i1[i] < i2[i]]
#     return i1

def ipPad(i):
    i = i.split(".")
    for index,value in enumerate(i):
        i[inex] = '0'*(3 - len(value)) + value
    ret = ''
    for ii in i:
        ret += i
    return ret


def ipSort(l):
     return sorted(l,key=ipPad)

l = sorted(["127.0.0.1","0.0.0.11",'1.2.3.4'])
print(l)
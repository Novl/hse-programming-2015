import time
import sys
import xml.dom.minidom

MAX_SIZE = float('+INF')

s_in = sys.argv[1]
s_out = sys.argv[2]

f = open(s_in, 'r')
f1 = open(s_out, 'w')

doc = xml.dom.minidom.parse(f)

elements_nets = doc.getElementsByTagName('net')

long = elements_nets.length
i = 0
A = []
while i < long:
    A.append([])
    j = 0
    while j < long:
        A[i].append(MAX_SIZE)
        j = j+1
    i = i+1

i = 0
while i < long:
    A[i][i] = 0
    i = i+1

resistors = doc.getElementsByTagName('resistor')

for t in resistors:
    be = int(t.getAttribute('net_from'))-1
    en = int(t.getAttribute("net_to"))-1
    size = float(t.getAttribute('resistance'))
    A[be][en] = A[en][be] = 1/(1/A[be][en]+1/size)

capactors = doc.getElementsByTagName('capactor')

for t in capactors:
    be = int(t.getAttribute('net_from'))-1
    en = int(t.getAttribute("net_to"))-1
    size = float(t.getAttribute('resistance'))
    A[be][en] = A[en][be] = 1/(1/A[be][en]+1/size)

diodes = doc.getElementsByTagName('diode')

for t in diodes:
    be = int(t.getAttribute('net_from'))-1
    en = int(t.getAttribute("net_to"))-1
    size = float(t.getAttribute('resistance'))
    A[be][en] = 1/(1/A[be][en]+1/size)
    size = float(t.getAttribute('reverse_resistance'))
    A[en][be] = 1/(1/A[en][be]+1/size)

k = 0
while k < long:
    i = 0
    while i < long:
        j = 0
        while j < long:
            if (i != j):
                if ((A[i][k]+A[k][j]) != 0):
                    if ((1/A[i][j]+1/(A[i][k]+A[k][j])) != 0):
                        A[i][j] = 1/(1/A[i][j]+1/(A[i][k]+A[k][j]))
            j = j+1
        i = i+1
    k = k+1

for row in A:
    for col in row:

        f1.write("{0:f},".format(col))
    f1.write("\n")

f.close()
f1.close()
print(' Time(ms) : ', (time.process_time()*1000))

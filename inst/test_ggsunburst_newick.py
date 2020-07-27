import sys
from ggsunburst3 import *

nw = sys.argv[1]
try:
    node_attr = sys.argv[2]
except:
    node_attr = ''
r,l,n,s,na = py_sunburst_data(nw, node_attributes=node_attr)
print (r)
print (l)
print (n)
print (s)

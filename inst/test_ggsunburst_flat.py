import sys
from ggsunburst import *

input = sys.argv[1]
type = sys.argv[2]
sep = sys.argv[3]
try:
    node_attr = sys.argv[4]
except:
    node_attr = ''
r,l,n,s,na = sunburst_data(input, type=type, sep=sep, node_attributes=node_attr)
print r
print l
print n
print s
print na

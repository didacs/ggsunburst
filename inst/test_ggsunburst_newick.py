import sys
from ggsunburst import *

nw = sys.argv[1]
try:
    node_attr = sys.argv[2]
except:
    node_attr = ''
r,l,n,s,na = sunburst_data(nw, node_attributes=node_attr)
print r
print l
print n
print s

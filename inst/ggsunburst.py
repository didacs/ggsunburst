import sys, os
from math import cos, sin, pi
from ete2.parser.newick import *
from ete2.coretype.tree import *


# Additional methods for class Tree
# they are set later in this same script

def initializator(self):
    """ """
    xpos = 1
    self.rects = {}
    self.labels = {}
    self.segments = {}
    for node in self.get_descendants('postorder'):
        node.rects = {}
        node.labels = {}
        node.segments = {}
        if node.is_leaf():
            node.x = xpos
            xpos += 1

def coordinates(self, topology_only=True, xlim=360, rot=0, type='sunburst'):
    """
rects: xmin, xmax, ymin, ymax
segments: rx, ry, px, pxend, ryend
text: x, y, label, rangle, pangle, hjust, hpjust 
"""
    xpos = 1
    for l in self.get_leaves():
        l.x = xpos
        l.xmin = l.x - 0.5
        l.xmax = l.x + 0.5
        l.rx = l.x
        l.px = 'NA'
        l.pxend = 'NA'
        xpos += 1

    for n in self.get_descendants('postorder'):
        n.ymax = n.ryend = n.get_distance(self, topology_only=topology_only)
        if topology_only:
            n.ymin = n.ry = n.ymax - 1
        else:
            n.ymin = n.ry = n.ymax - n.dist

        angle = (n.x - 0.5)*( -xlim / float(len(self) )) + 90 - rot
        n.rangle = self.rangle(angle)
        n.pangle = self.pangle(angle)
        n.hjust  = self.hjust(angle)
        n.hpjust = self.hjust_ptext(angle)

        if not n.is_leaf():
            leaves = n.get_leaves()
            n.xmin, n.xmax = leaves[0].xmin, leaves[-1].xmax
            n.x = n.xmin + (n.xmax - n.xmin)/2.
            n.y = n.ymin + (n.ymax - n.ymin)/2.

            children = n.get_children()
            min, max = children[0].x, children[-1].x
            n.rx = min + (max - min)/2.
            n.px = children[0].rx
            n.pxend = children[-1].rx
        else:
            if type == 'sunburst':
                n.y = n.ymin + (n.ymax - n.ymin)/2.
            elif type == 'tree':
                n.y = n.ymax
    

def _rects(self, topology_only=True):
    """populate .rects attribute"""
    self.rects.update( {'xmin':0.5, 'xmax':len(self)+0.5, 'ymin':0, 'ymax':1} )
    for n in self.get_descendants('postorder'):
        n.rects[ 'ymax' ] = n.get_distance(self, topology_only=topology_only)
        if not 'NoName' in n.name:
            n.rects[ 'name' ] = n.name
        else:
            n.rects[ 'name' ] = 'NA'
        if topology_only:
            n.rects[ 'ymin' ] = n.rects[ 'ymax' ] - 1
        else:
            n.rects[ 'ymin' ] = n.rects[ 'ymax' ] - n.dist
        if n.is_leaf():
            n.rects[ 'leaf' ] = 'TRUE'
            n.rects.update({'xmin':n.x-0.5, 'xmax':n.x+0.5, 'x':n.x})
        else:
            n.rects[ 'leaf' ] = 'FALSE'
            leaves = n.get_leaves()
            min, max = leaves[0].rects[ 'xmin' ], leaves[-1].rects[ 'xmax' ]
            n.rects[ 'xmin' ] = min
            n.rects[ 'xmax' ] = max
            n.x = min + (max - min)/2.
            n.rects['x'] = n.x

def _labels(self, xlim, rot, topology_only=True):
    """populate .labels dict with keys: label,angle,rangle,pangle,hrjust,hpjust,x"""
    for n in self.get_descendants('postorder'):
#        if not n.is_leaf():
#            leaves = n.get_leaves()
#            min, max = leaves[0].rects[ 'xmin' ], leaves[-1].rects[ 'xmax' ]
#            n.rects[ 'xmin' ] = min
#            n.rects[ 'xmax' ] = max
#            n.x = min + (max - min)/2.

        if hasattr(n,'x'):
            angle = (n.x - 0.5)*( -xlim / float(len(self) )) + 90 - rot
            n.labels[ 'label'  ] = n.name
            n.labels[ 'angle'  ] = angle                           # angle bisector of arc (angle for text label)
            n.labels[ 'rangle' ] = self.rangle(angle)              # radial text angle
            n.labels[ 'pangle' ] = self.pangle(angle)              # perpendicular text angle
            n.labels[ 'phjust' ] = self.hjust_ptext(angle)
            n.labels[ 'pvjust' ] = self.vjust_ptext(angle)
            n.labels[ 'rhjust' ] = self.hjust_rtext(angle)
            n.labels[ 'rvjust' ] = self.vjust_rtext(angle)
            n.labels[ 'x' ] = n.x
            n.labels[ 'delta_angle' ] = len(n) * ( xlim / float(len(self) )) # size of node in angles
            n.labels[ 'xfraction' ] = len(n) / float(len(self)) # fraction of x occupied by this node 

            max = n.get_distance(self, topology_only=topology_only)
            if topology_only:
                min = max -1
            else:
                min = max - n.dist
            
            if n.is_leaf():
                n.labels[ 'y_out' ] = max
                n.labels[ 'y' ] = min + (max - min)/2.
            else:
                n.labels[ 'y' ] = min + (max - min)/2.
                
        else:
            raise Exception, 'Node has no attribute "x"'

def _segments(self, topology_only=True):
    """populate node.segments
ry, ryend
rx, px, pxend
"""
    for n in self.get_descendants('postorder'):
        n.segments['ryend'] = n.get_distance(self, topology_only=topology_only)
        if topology_only:
            n.segments['ry'] = n.segments[ 'ryend' ] - 1
        else:
            n.segments['ry'] = n.segments[ 'ryend' ] - n.dist

        if n.is_leaf():
            n.segments['rx'] = n.x
            n.segments['px'] = 'NA'
            n.segments['pxend'] = 'NA'
        else:
            children = n.get_children()
            min, max = children[0].x, children[-1].x
            n.x = min + (max - min)/2.
            n.segments['rx'] = n.x
            n.segments['px'] = children[0].x
            n.segments['pxend'] = children[-1].x

# the following functions take an angle from 90 to -270 (0 is the horizontal)
# we can identify which quadrant each label falls by computing sin or cos of angle*pi/180
#     sin cos
#   I +   +
#  II -   +
# III -   -
#  VI +   -
# this R code will clarify this idea
# a=seq(90,-270, by=-10)
# cbind(angle=a, cos=cos(a * pi/180), sin=sin(a * pi/180))

def rangle(self, angle):
    if cos(angle*pi/180.) < 0:
        return angle + 180
    else:
        return angle

def pangle(self, angle):
    if sin(angle*pi/180.) < 0:
        return angle + 90
    else:
        return angle - 90

def hjust_ptext(self, angle):
    return .5

def vjust_ptext(self, angle): 
    if sin(angle*pi/180.) < 0: return 0 # II and III 
    else:                      return 1 # I and IV
        
def hjust_rtext(self, angle):
    if cos(angle*pi/180.) < 0: return 1 # III and IV
    else:                      return 0 # I and II

def vjust_rtext(self, angle):
    return 0.5

# Setting the methods to Tree class
setattr(Tree, "initializator", initializator)
setattr(Tree, "coordinates", coordinates)
setattr(Tree, "_rects", _rects)
setattr(Tree, "_labels", _labels)
setattr(Tree, "_segments", _segments)
setattr(Tree, "rangle", rangle)
setattr(Tree, "pangle", pangle)
setattr(Tree, "hjust_ptext", hjust_ptext)
setattr(Tree, "vjust_ptext", vjust_ptext)
setattr(Tree, "hjust_rtext", hjust_rtext)
setattr(Tree, "vjust_rtext", vjust_rtext)

# Functions to be loaded into R
def sunburst_data2(newick, ladderize=False, ultrametric=False, type='sunburst',
                  xlim=360, rot=0):
    t = Tree(newick)
    if ladderize:
        if not ladderize in ['L','LEFT','left','Left']:
            t.ladderize()
        else:
            t.ladderize(1)
    if not ultrametric in ['T','TRUE', True]:
        t.coordinates()
    else:
        t.convert_to_ultrametric(t.get_farthest_node()[1])
        t.coordinates(topology_only=False)

    nodes = ["xmin","xmax","ymin","ymax",
             "rx", "ry", "px", "pxend", "ryend",
             "x","y","label","rangle","hjust","pangle","hpjust"]
    nodes_str = '\t'.join(nodes) + '\n'
    leaves  = ["x","y","label","rangle","hjust"]
    leaves_str = '\t'.join(leaves) + '\n'
    print t
    for n in t.get_descendants():
        for x in nodes:
            print getattr(n, x)

        nodes_str += '\t'.join( map(str,[ getattr(n, x) for x in nodes ])) + '\n'
        if n.is_leaf():
            leaves_str += '\t'.join( map(str,[ getattr(n, x) for x in leaves ])) + '\n'
    return [nodes_str, leaves_str]

def sunburst_data(newick, ladderize=False, ultrametric=False,
                  xlim=360, rot=0, node_attributes=''):
    if node_attributes and not isinstance(node_attributes, list):
        node_attributes = [node_attributes]
    
    t = Tree(newick)
    if ladderize:
        if not ladderize in ['L','LEFT','left','Left']:
            t.ladderize()
        else:
            t.ladderize(1)
    t.initializator() # initialize required node dicts
    if not ultrametric in ['T','TRUE', True]:
        t._rects(topology_only=True)
        t._labels(xlim=xlim, rot=rot, topology_only=True)
    else:
        t.convert_to_ultrametric(t.get_farthest_node()[1])
        t._rects(topology_only=False)
        t._labels(xlim=xlim, rot=rot, topology_only=False)

    rects   = ["xmin","xmax","ymin","ymax","x","name","leaf"] 
    rect_str = '\t'.join(rects + map(str, node_attributes)) + '\n'

    node_labels  = ["x","y","label","rangle","rhjust","pangle","pvjust","delta_angle","xfraction"]
    node_labels_str = '\t'.join(node_labels + map(str, node_attributes)) + '\n'

    leaf_labels  = ["x","y","y_out","label","rangle","rhjust"]
    leaf_labels_str = '\t'.join(leaf_labels + map(str, node_attributes)).replace('rangle','angle').replace('rhjust','hjust') + '\n'

    for n in t.get_descendants():
        if not node_attributes:
            rect_str += '\t'.join( map(str,[n.rects[x] for x in rects])) + '\n'
        else:
            rect_str += '\t'.join( map(str,[n.rects[x] for x in rects])) + '\t'
            for x in map(str, node_attributes):
                if not hasattr(n,x):
                    sys.stderr.write('WARNING: attribute "%s" not set for node "%s", setting its value to "NA"\n' % (x,n.name))
                    setattr(n,x,'NA')
            rect_str += '\t'.join( map(str,[getattr(n,x) for x in map(str, node_attributes)]))+'\n'
            
        if n.is_leaf():
            if not node_attributes:
                leaf_labels_str += '\t'.join( map(str,[n.labels[x] for x in leaf_labels]))+'\n'
            else:
                leaf_labels_str += '\t'.join( map(str,[n.labels[x] for x in leaf_labels])) + '\t'
                for x in map(str, node_attributes):
                    if not hasattr(n,x):
                        sys.stderr.write('WARNING: attribute "%s" not set for node "%s", setting its value to "NA"\n' % (x,n.name))
                        setattr(n,x,'NA')
                leaf_labels_str += '\t'.join( map(str,[getattr(n,x) for x in map(str, node_attributes)]))+'\n'

        else:
            if not node_attributes:
                node_labels_str += '\t'.join( map(str,[n.labels[x] for x in node_labels]))+'\n'
            else:
                node_labels_str += '\t'.join( map(str,[n.labels[x] for x in node_labels])) + '\t'
                for x in map(str, node_attributes):
                    if not hasattr(n,x):
                        sys.stderr.write('WARNING: attribute "%s" not set for node "%s", setting its value to "NA"\n' % (x,n.name))
                        setattr(n,x,'NA')
                node_labels_str += '\t'.join( map(str,[getattr(n,x) for x in map(str, node_attributes)]))+'\n'
                
    return [rect_str, leaf_labels_str, node_labels_str]

def tree_data(newick, ladderize=False, ultrametric=False, xlim=360, type='tree',
              rot=0):
    t = Tree(newick)
    if ladderize:
        if not ladderize in ['L','LEFT','left','Left']:
            t.ladderize()
        else:
            t.ladderize(1)
    t.initializator() # initialize required node dicts
    if not ultrametric in ['T','TRUE', True]:
        t._segments(topology_only=True)
#        t._labels(xlim=xlim, rot=rot, topology_only=True, type=type)
    else:
        t.convert_to_ultrametric(t.get_farthest_node()[1])
        t._segments(topology_only=False)
#        t._labels(xlim=xlim, rot=rot, topology_only=False, type=type)

    segments = ["rx","ry","ryend","px","pxend"]
#    labels   = ["x","y","label","rangle","hjust"]
    segments_str = '\t'.join(segments)+'\n'
#    labels_str = '\t'.join(labels).replace('rangle','angle')+'\n'
    for n in t.get_descendants():
        segments_str += '\t'.join( map(str,[n.segments[x] for x in segments]))+'\n'
#        if n.is_leaf():
#            labels_str += '\t'.join( map(str,[n.labels[x] for x in labels]))+'\n'

    return [segments_str] #, labels_str]

def nw_print(newick, ladderize=False, ultrametric=False):
    t = Tree(newick)
    if ladderize:
        if not ladderize in ['L','LEFT','left','Left']:
            t.ladderize()
        else:
            t.ladderize(1)

    if ultrametric:
        t.convert_to_ultrametric(t.get_farthest_node()[1])

    return str(t)+'\n'

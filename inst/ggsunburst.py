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



def parse_node_parent(infile, sep=','):
    t = Tree()
    fh = open(infile)
    keys = [x.strip('"\'') for x in fh.readline().rstrip().split(sep)]
    if not all([x in map(lambda x:x.lower(), keys) for x in ['node','parent']]):
        raise Exception, 'ERROR first line must contain node and parent'

    for i in fh.readlines():
        values = [x.strip('"\'') for x in i.rstrip().split(sep)]
        if len(values) != len(keys):
            raise Exception, 'ERROR different number of fields in line:\n%s\n%s' % (keys,values)

        d = dict(zip(keys, values))
        
        parent = d['parent']
        del(d['parent'])
        node = d['node']
        del(d['node'])

        if parent in [x.name for x in t.get_descendants()]:
            p = t&parent
            n = p.add_child(name=node)
        elif parent:
            p = t.add_child(name=parent)
            n = p.add_child(name=node)
        else:
            p = t
            n = p.add_child(name=node)

        if d:
            n.add_features(**d)

#    print t.get_ascii(attributes=['name'])
    return t

def build_tree_from_tab(infile, sep="\t"):
    t = Tree()
    for line in open(infile):
        lineage = [x.strip('"\'') for x in line.rstrip().split(sep)]
        parent = t
        for name in lineage:
            if '->' in name:
                name,attributes = name.split('->')
                name = name.strip()
                leaf = parent.add_child(name=name)
                attributes = attributes.split(';')
                for attr in attributes:
                    k,v = attr.split(':')
                    leaf.add_feature(k,v)
            else:
                name = name.strip()
                children = [x.name for x in parent.get_children()]
                if not name in children:
                    parent = parent.add_child(name=name)
                else:
                    parent = [x for x in parent.get_children() if x.name == name][0]
    
    return t

def coordinates(self, topology_only=True, node_size=False, xlim=360, rot=0 ):
    """
rects: xmin, xmax, ymin, ymax
segments: rx, ry, px, pxend, ryend
text: x, y, label, rangle, pangle, hjust, hpjust
"""
    node2leaves = self.get_cached_content()
    # max value in x axis
    # the x axis increases by 1 fo each leaf
    # although it can increase also by the x.size attribute, if defined in the leaves
    try:
        xmax_global = sum([float(x.size) for x in node2leaves[ self ]])
    except:
        xmax_global = float(len(self))
    xmin_global = .5

    # y offset
    farthest,y_offset = self.get_farthest_node(topology_only=topology_only)

    for node in self.traverse('postorder'):
        # dictionaries for storing coordinates
        node.add_feature('rects', {})
        node.add_feature('labels', {})
        node.add_feature('segments', {})

        # y coordinates
        ymax = node.get_distance(self, topology_only=topology_only)
        ymax -= y_offset
        if topology_only:
            dist = 1.
        else:
            dist = node.dist
        ymin = ymax - dist


        ########### rects
        node.rects.update({'ymin':ymin, 'ymax':ymax})
        if not 'NoName' in node.name:
            node.rects[ 'name' ] = node.name
        else:
            node.rects[ 'name' ] = 'NA'

        # x coordinates for leaves (internal nodes require the leaves to have x coords to compute them)
        if node.is_leaf():
            try:
                node.size = float(node.size)
            except:
                node.size = 1.
                
            xmax = xmin_global + node.size
            x = xmin_global + (xmax-xmin_global)/2
            node.rects.update({'xmin':xmin_global, 'xmax':xmax, 'x':x, 'leaf':'TRUE'})
            node.x = x
            xmin_global += node.size

        else:
            leaves = node.get_leaves()
            xmin, xmax = leaves[0].rects[ 'xmin' ], leaves[-1].rects[ 'xmax' ]
            x = xmin + (xmax-xmin)/2
            node.rects.update({'xmin':xmin, 'xmax':xmax, 'x':x, 'leaf':'FALSE'})
            node.x = x


        ########### labels
        angle = ( node.x - 0.5 ) * ( -xlim / xmax_global ) + 90 - rot
        node.labels[ 'label'  ] = node.name
        node.labels[ 'angle'  ] = angle                           # angle bisector of arc (angle for text label)
        node.labels[ 'rangle' ] = self.rangle(angle)              # radial text angle
        node.labels[ 'pangle' ] = self.pangle(angle)              # perpendicular text angle
        node.labels[ 'phjust' ] = self.hjust_ptext(angle)
        node.labels[ 'pvjust' ] = self.vjust_ptext(angle)
        node.labels[ 'rhjust' ] = self.hjust_rtext(angle)
        node.labels[ 'rvjust' ] = self.vjust_rtext(angle)
        node.labels[ 'x' ] = node.x
        this_node_size_sum = sum([ float(x.size) for x in node2leaves[ node ] ])
        node.labels[ 'delta_angle' ] = this_node_size_sum * ( xlim / xmax_global ) # size of node in angles
        node.labels[ 'xfraction' ] = this_node_size_sum / xmax_global # fraction of x occupied by this node
        node.labels[ 'y' ] = ymin + (ymax - ymin)/2.
        if node.is_leaf():
            node.labels[ 'y_out' ] = ymax

        ########### segments
        ry = ymax - node.dist
        node.segments.update({'ryend':ymax, 'ry':ry})

        if node.is_leaf():
            node.segments.update({'px':'NA', 'pxend':'NA', 'rx':node.x})
        else:
            children = node.get_children()
            px, pxend = children[0].segments['rx'], children[-1].segments['rx']
            x = px + (pxend - px)/2.
            node.segments.update({'px':px, 'pxend':pxend, 'rx':x})


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
            minim, maxim = leaves[0].rects[ 'xmin' ], leaves[-1].rects[ 'xmax' ]
            n.rects[ 'xmin' ] = minim
            n.rects[ 'xmax' ] = maxim
            n.x = minim + (maxim - minim)/2.
            n.rects['x'] = n.x


def _labels(self, xlim, rot, topology_only=True):
    """populate .labels dict with keys: label,angle,rangle,pangle,hrjust,hpjust,x"""
    for n in self.get_descendants('postorder'):
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

            maxim = n.get_distance(self, topology_only=topology_only)
            if topology_only:
                minim = maxim -1
            else:
                minim = maxim - n.dist

            if n.is_leaf():
                n.labels[ 'y_out' ] = maxim
                n.labels[ 'y' ] = minim + (maxim - minim)/2.
            else:
                n.labels[ 'y' ] = minim + (maxim - minim)/2.

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
            minim, maxim = children[0].x, children[-1].x
            n.x = minim + (maxim - minim)/2.
            n.segments['rx'] = n.x
            n.segments['px'] = children[0].x
            n.segments['pxend'] = children[-1].x

# the following functions take an angle from 90 to -270 (0 is the horizontal)
# and identifies which quadrant each label falls by computing sin or cos of angle*pi/180
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
#setattr(Tree, "initializator", initializator)
setattr(Tree, "coordinates", coordinates)
#setattr(Tree, "_rects", _rects)
#setattr(Tree, "_labels", _labels)
#setattr(Tree, "_segments", _segments)
setattr(Tree, "rangle", rangle)
setattr(Tree, "pangle", pangle)
setattr(Tree, "hjust_ptext", hjust_ptext)
setattr(Tree, "vjust_ptext", vjust_ptext)
setattr(Tree, "hjust_rtext", hjust_rtext)
setattr(Tree, "vjust_rtext", vjust_rtext)

# Functions to be loaded into R
def py_sunburst_data(input, type="newick", sep="\t", ladderize=False, ultrametric=False,
                  xlim=360, rot=0, node_attributes=''):

    if node_attributes and not isinstance(node_attributes, list):
        node_attributes = [node_attributes]

    # load input file into a ete tree object
    t = ''
    if type == "newick":
        t = Tree(input)
    elif type == "lineage":
        t = build_tree_from_tab(input, sep=sep)
    elif type == "node_parent":
        t = parse_node_parent(input, sep=sep)

    for n in t.get_descendants():
        if not hasattr(n,'size'):
            n.size = 1.
            
#    print t.get_ascii(attributes=['name','size'])

    if not t:
        raise Exception, 'ERROR: input %s could not be loaded. make sure it is in newick or flat tabulated format' % input

    # the tree was succesfully loaded
    if not node_attributes and hasattr(t.get_children()[0],'node_attributes'):
        node_attributes = t.get_children()[0].node_attributes.split('%')

    if ladderize:
        if not ladderize in ['L','LEFT','left','Left']:
            t.ladderize()
        else:
            t.ladderize(1)

    if ultrametric in ['T','TRUE', True]:
        t.convert_to_ultrametric(t.get_farthest_node()[1])

    # compute coords for rects,node_labels,leaf_labels and segments
    t.coordinates(topology_only=False, node_size=True, xlim=xlim, rot=rot)

#    t.initializator() # initialize required node dicts
#    if not ultrametric in ['T','TRUE', True]:
#        t._rects(topology_only=False)
#        t._labels(xlim=xlim, rot=rot, topology_only=False)
#    else:
#        t.convert_to_ultrametric(t.get_farthest_node()[1])
#        t._rects(topology_only=False)
#        t._labels(xlim=xlim, rot=rot, topology_only=False)

    rects   = ["xmin","xmax","ymin","ymax","x","name","leaf"]
    rect_str = '\t'.join(rects + map(str, node_attributes)) + '\n'

    node_labels  = ["x","y","label","rangle","rhjust","pangle","pvjust","delta_angle","xfraction"]
    node_labels_str = '\t'.join(node_labels + map(str, node_attributes)) + '\n'

    leaf_labels  = ["x","y","y_out","label","rangle","pangle","rhjust"]
    leaf_labels_str = '\t'.join(leaf_labels + map(str, node_attributes)).replace('rangle','angle').replace('rhjust','hjust') + '\n'

    segments = ["rx","ry","ryend","px","pxend"]
    segments_str = '\t'.join(segments)+'\n'

    for n in t.get_descendants():
        if not node_attributes:
            rect_str += '\t'.join( map(str,[n.rects[x] for x in rects])) + '\n'
        else:
            rect_str += '\t'.join( map(str,[n.rects[x] for x in rects])) + '\t'
            for x in map(str, node_attributes):
                if not hasattr(n,x):
#                    sys.stderr.write('WARNING: attribute "%s" not set for node "%s", setting its value to "NA"\n' % (x,n.name))
                    setattr(n,x,'NA')
            rect_str += '\t'.join( map(str,[getattr(n,x) for x in map(str, node_attributes)]))+'\n'

        if n.is_leaf():
            if not node_attributes:
                leaf_labels_str += '\t'.join( map(str,[n.labels[x] for x in leaf_labels]))+'\n'
            else:
                leaf_labels_str += '\t'.join( map(str,[n.labels[x] for x in leaf_labels])) + '\t'
                for x in map(str, node_attributes):
                    if not hasattr(n,x):
#                        sys.stderr.write('WARNING: attribute "%s" not set for node "%s", setting its value to "NA"\n' % (x,n.name))
                        setattr(n,x,'NA')
                leaf_labels_str += '\t'.join( map(str,[getattr(n,x) for x in map(str, node_attributes)]))+'\n'

        else:
            if not node_attributes:
                node_labels_str += '\t'.join( map(str,[n.labels[x] for x in node_labels]))+'\n'
            else:
                node_labels_str += '\t'.join( map(str,[n.labels[x] for x in node_labels])) + '\t'
                for x in map(str, node_attributes):
                    if not hasattr(n,x):
#                        sys.stderr.write('WARNING: attribute "%s" not set for node "%s", setting its value to "NA"\n' % (x,n.name))
                        setattr(n,x,'NA')
                node_labels_str += '\t'.join( map(str,[getattr(n,x) for x in map(str, node_attributes)]))+'\n'
        segments_str += '\t'.join( map(str,[n.segments[x] for x in segments]))+'\n'

    return [rect_str, leaf_labels_str, node_labels_str, segments_str, ','.join(node_attributes)]

def tree_data(input, type="newick", sep="\t", ladderize=False, ultrametric=False, xlim=360,
              rot=0):
#    # try to load the input, it will fail if it is not in newick format
#    t = ''
#    try:
#        t = Tree(newick)
#    except:
#        not_newick = newick
#        t = build_tree_from_tab(not_newick)


    # load input file into a ete tree object
    t = ''
    if type == "newick":
        t = Tree(input)
    elif type == "lineage":
        t = build_tree_from_tab(input, sep=sep)
    elif type == "node_parent":
        t = parse_node_parent(input, sep=sep)

    if not t:
        raise Exception, 'ERROR: input %s could not be loaded. make sure it is in newick or tabulated format' % newick
    if ladderize:
        if not ladderize in ['L','LEFT','left','Left']:
            t.ladderize()
        else:
            t.ladderize(1)
    t.initializator() # initialize required node dicts
    if not ultrametric in ['T','TRUE', True]:
        t._segments(topology_only=False)
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

    return segments_str #, labels_str]

def py_nw_print(newick, format=8, ladderize=False, ultrametric=False):
    t = Tree(newick, format = format )
    if ladderize:
        if not ladderize in ['L','LEFT','left','Left']:
            t.ladderize()
        else:
            t.ladderize(1)

    if ultrametric:
        t.convert_to_ultrametric(t.get_farthest_node()[1])

    return str(t.get_ascii())+'\n'

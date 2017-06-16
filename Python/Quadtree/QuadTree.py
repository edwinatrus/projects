# A quadtree can be created by recursively calling subdivide from the root using BFS

class QuadTree(object):

    def __init__(self, rect):
        self.Root = Node(None, rect, None)

    def mesh(self, criteria):
        '''
        check if meshed already, if not:
        start meshing using BFS, criteria (Node -> Bool) is the function to decide if a node needs subdivision
        during BFS + smoothing, adjacent leaves depth difference <= 1, the one ready to subdivide always has smaller depth
        '''
        if self.Root.children == [None, None, None, None]:
            self.Root.subdivide()
            currentDepth = self.Root.children

            while currentDepth:
                nextDepth = []

                for currentNode in currentDepth:
                    if currentNode.type == Branch:
                        nextDepth += currentNode.children
                    else:
                        if (criteria(currentNode)):
                            currentNode.subdivide()
                            nextDepth += currentNode.children
                
                thislevel = nextDepth
        else:
            print("Already meshed")


    # inner class Node represent one node, its properties is subject to BFS
    class Node(object):
        
        def __init__(self, parent, rect, location):
            '''
            initialize a node in a quadtree with the following property:
            rect: coordinate of four corners
            location = 1, 2, 3, 4 indicatin topleft, topright, bottomright, bottomleft, None if is root

            following properties must be set after __init__ called:
                neighbour: [[], [], [], []]: top, right, bottom, left, each contains either one or two leaf reference
            '''

            self.parent = parent
            self.children = [None, None, None, None]
            self.location = location

            if parent == None:
                self.depth = 0
            else:
                self.depth = parent.depth + 1
            self.rect = rect

            if self.parent == None:
                self.type = "Root"
            else:
                self.type = "Leaf"

            # configure its neighbour and nodenum for root only
            if self.type = "Root":
                self.neighbour = [None, None, None, None]

        def subdivide(self):
            self.type = "Branch"

            # subdivide adjacents to enforce 2 to 1 ratio (called smoothing), required if neighbour has smaller depth
            for n in xrange(4):
                if self.neighbour[n].depth == self.depth - 1:
                    self.neighbour[n].subdivide()

            # actual subdivide the Node

            x0, z0, x1, z1 = self.rect
            h = (x1 - x0) / 2

            rects = []
            rects.append((x0, z0, x0 + h, z0 + h))
            rects.append((x0, z0 + h, x0 + h, z1))
            rects.append((x0 + h, z0 + h, x1, z1))
            rects.append((x0 + h, z0, x1, z0 + h))

            for n in xrange(4):
                self.children[n] = Node(self, rects[n], n + 1)

            # change neighbours' neighbour (point to self) to self.children
            if self.neighbour[0]:
                if len(self.neighbour[0].neighbour[2] == 1):
                    self.neighbour[0].neighbour[2] = [self.children[0]]
                else:
                    pass

            if self.neighbour[1]:
                if len(self.neighbour[1].neighbour[3] == 1):
                    pass
                else:
                    pass

            if self.neighbour[2]:
                if len(self.neighbour[2].neighbour[0] == 1):
                    pass
                else:
                    pass

            if self.neighbour[3]:
                if len(self.neighbour[3].neighbour[1] == 1):
                    pass
                else:
                    pass

            # assign children's neighbour
            for n in xrange(4):
                self.children[n].setNeighbour()

        def setNeighbour(self):
            '''
            this must be called after all four sub node is created
            '''

            # neighbour property:
            self.neighbour = []  # initialization

            if self.location == 1:
                pass

            elif self.location == 2:
                pass

            elif self.location == 3:
                pass

            else:
                pass
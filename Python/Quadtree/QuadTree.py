# A quadtree can be created by recursively calling subdivide from the root using BFS

class QuadTree(object):

    def __init__(self, rect):
        self.Root = Node(None, rect, None)

    def mesh(self, criteria):
        '''
        check if meshed already, if not:
        start meshing using BFS, criteria (Node -> Bool) is the function to decide if a node needs subdivision
        during BFS + smoothing, adjacent leaves depth difference <= 1, the one ready to subdivide always has smaller (or equal) depth

        later we can use DFS to assign node number
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
            rect: corner of rectangle to decide the location of the Node
            location = 1, 2, 3, 4 indicatin topleft, topright, bottomright, bottomleft, None if is root

            following properties must be set after __init__ called:
                neighbour: [up, right, bottom, left] neighbours in each direction, can either be None or [Node] or [Node, Node]
            '''

            self.parent = parent
            self.rect = rect     
            self.location = location
            self.children = [None, None, None, None]  # initial children list, actual children is decided by calling subdivide (only branch and root have children)

            if parent == None:
                self.type = "Root"
                self.depth = 0
                self.neighbour = [None, None, None, None]  # configure its neighbour for root only
            else:
                self.type = "Leaf"
                self.depth = parent.depth + 1
                

        def subdivide(self):
            self.type = "Branch"

            # subdivide adjacents to enforce 2 to 1 ratio (called smoothing), required if neighbour has smaller depth
            for n in xrange(4):
                if self.neighbour[n].depth == self.depth - 1:
                    self.neighbour[n].subdivide()

            # actual code to subdivide the Node
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
            for idx, val in enumerate(self.neighbour):
                if idx == 0:  # top
                    if val:
                        if len(val) == 1:
                            self.neighbour[idx][0].neighbour[2] = [self.children[1], self.children[0]]
                        else:
                            self.neighbour[idx][0].neighbour[2] = [self.children[0]]
                            self.neighbour[idx][1].neighbour[2] = [self.children[1]]
                elif idx == 1:  # right
                    if val:
                        if len(val) == 1:
                            self.neighbour[idx][0].neighbour[3] = [self.children[2], self.children[1]]
                        else:
                            self.neighbour[idx][0].neighbour[3] = [self.children[1]]
                            self.neighbour[idx][1].neighbour[3] = [self.children[2]]
                elif idx == 2:  # bottom
                    if val:
                        if len(val) == 1:
                            self.neighbour[idx][0].neighbour[0] = [self.children[3], self.children[2]]
                        else:
                            self.neighbour[idx][0].neighbour[0] = [self.children[2]]
                            self.neighbour[idx][1].neighbour[0] = [self.children[3]]
                else:  # left
                    if val:
                        if len(val) == 1:
                            self.neighbour[idx][0].neighbour[1] = [self.children[0], self.children[3]]
                        else:
                            self.neighbour[idx][0].neighbour[1] = [self.children[3]]
                            self.neighbour[idx][1].neighbour[1] = [self.children[0]]

            # assign children's neighbour
            for n in xrange(4):
                self.children[n].setNeighbour()

        def setNeighbour(self):
            '''
            this must be called after all four sub node is created
            '''

            # neighbour property:
            self.neighbour = [[], [], [], []]  # initialization

            if self.location == 1:
                self.neighbour[0] = self.parent.neighbour[0][0] if self.parent.neighbour[0] else None
                self.neighbour[1] = self.parent.children[1]
                self.neighbour[2] = self.parent.children[3]
                self.neighbour[3] = self.parent.neighbour[3][-1] if self.parent.neighbour[3] else None

            elif self.location == 2:
                self.neighbour[0] = self.parent.neighbour[0][-1] if self.parent.neighbour[0] else None
                self.neighbour[1] = self.parent.neighbour[1][0] if self.parent.neighbour[1] else None
                self.neighbour[2] = self.parent.children[2]
                self.neighbour[3] = self.parent.children[0]

            elif self.location == 3:
                self.neighbour[0] = self.parent.children[1]
                self.neighbour[1] = self.parent.neighbour[1][-1] if self.parent.neighbour[1] else None
                self.neighbour[2] = self.parent.neighbour[2][1] if self.parent.neighbour[2] else None
                self.neighbour[3] = self.parent.children[3]

            else:
                self.neighbour[0] = self.parent.children[0]
                self.neighbour[1] = self.parent.children[2]
                self.neighbour[2] = self.parent.neighbour[2][-1] if self.parent.neighbour[2] else None
                self.neighbour[3] = self.parent.neighbour[3][1] if self.parent.neighbour[3] else None
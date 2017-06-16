class QuadTree(object):
    def __init__(self, rect):
        self.Root = Node(None, rect, None)

    def mesh(self, criteria):
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

    class Node(object):
        def __init__(self, parent, rect, location):
            self.parent = parent
            self.rect = rect         
            self.location = location
            self.children = [None, None, None, None]

            if parent == None:
                self.depth = 0
                self.type = "Root"
                self.neighbour = [None, None, None, None]
            else:
                self.depth = parent.depth + 1
                self.type = "Leaf"

        def subdivide(self):
            self.type = "Branch"

            for n in xrange(4):
                if self.neighbour[n].depth == self.depth - 1:
                    self.neighbour[n].subdivide()

            x0, z0, x1, z1 = self.rect
            h = (x1 - x0) / 2

            rects = []
            rects.append((x0, z0, x0 + h, z0 + h))
            rects.append((x0, z0 + h, x0 + h, z1))
            rects.append((x0 + h, z0 + h, x1, z1))
            rects.append((x0 + h, z0, x1, z0 + h))

            for n in xrange(4):
                self.children[n] = Node(self, rects[n], n + 1)

            for idx, val in enumerate(self.neighbour):
                if idx == 0:  
                    if val:
                        if len(val) == 1:
                            self.neighbour[idx][0].neighbour[2] = [self.children[1], self.children[0]]
                        else:
                            self.neighbour[idx][0].neighbour[2] = [self.children[0]]
                            self.neighbour[idx][1].neighbour[2] = [self.children[1]]
                elif idx == 1:  
                    if val:
                        if len(val) == 1:
                            self.neighbour[idx][0].neighbour[3] = [self.children[2], self.children[1]]
                        else:
                            self.neighbour[idx][0].neighbour[3] = [self.children[1]]
                            self.neighbour[idx][1].neighbour[3] = [self.children[2]]
                elif idx == 2:  
                    if val:
                        if len(val) == 1:
                            self.neighbour[idx][0].neighbour[0] = [self.children[3], self.children[2]]
                        else:
                            self.neighbour[idx][0].neighbour[0] = [self.children[2]]
                            self.neighbour[idx][1].neighbour[0] = [self.children[3]]
                else:  
                    if val:
                        if len(val) == 1:
                            self.neighbour[idx][0].neighbour[1] = [self.children[0], self.children[3]]
                        else:
                            self.neighbour[idx][0].neighbour[1] = [self.children[3]]
                            self.neighbour[idx][1].neighbour[1] = [self.children[0]]

            for n in xrange(4):
                self.children[n].setNeighbour()

        def setNeighbour(self):
            self.neighbour = [[], [], [], []]

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
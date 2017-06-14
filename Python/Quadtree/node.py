class Node():
    
    def __init__(self, parent=None, rect):
        self.parent = parent
        self.children = [None, None, None, None]

        if parent == None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1
        self.rect = rect
        x0, z0, x1, z1 = rect

        if self.parent == None:
            self.type = "Root"
        else:
            self.type = "Leaf"
    
    def subdivide(self):
        self.type = "Branch"

        x0, z0, x1, z1 = self.rect
        h = (x1 - x0)/2

        rects = []
        rects.append((x0, z0, x0 + h, z0 + h))
        rects.append((x0, z0 + h, x0 + h, z1))
        rects.append((x0 + h, z0 + h, x1, z1))
        rects.append((x0 + h, z0, x1, z0 + h))
        
        for n in xrange(len(rects)):
            self.children[n] = Node(self, rects[n])


